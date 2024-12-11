import datetime
import decimal
import logging
import string
import uuid

import os
import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.compute as pc
from logging import getLogger
from qcloud_cos import CosConfig, CosServiceError, CosClientError
from qcloud_cos import CosS3Client

from clickzetta.proto.generated import ingestion_pb2, data_type_pb2, file_format_type_pb2
from clickzetta.client import Client
from clickzetta.bulkload.bulkload_enums import BulkLoadMetaData, BulkLoadConfig, BulkLoadState, FileFormatType

_logger = getLogger(__name__)


class Row:
    def __init__(self, full_fields: dict, table_name: string):
        self.field_name_values = {}
        self.full_fields = full_fields
        self.table_name = table_name

    def set_value(self, field_name: string, field_value):
        if field_name in self.full_fields:
            self.field_name_values[field_name] = field_value
        else:
            raise RuntimeError('Field name:{} is not in table:{}'.format(field_name, self.table_name))


class BulkLoadWriter:
    def __init__(self, client: Client, meta_data: BulkLoadMetaData, config: BulkLoadConfig, partition_id: int):
        self.client = client
        self.meta_data = meta_data
        self.config = config
        self.partition_id = partition_id
        self.staging_config = config.get_staging_config(meta_data.get_prefer_internal_endpoint())
        self._process_staging_type()
        self.file_io = config.get_staging_config(meta_data.get_prefer_internal_endpoint()).create_file_io()
        self.file_format = config.get_file_format()
        self.max_file_records = config.get_max_rows_per_file()
        self.max_file_size = config.get_max_file_size_per_file()
        if meta_data.get_state() != BulkLoadState.CREATED:
            raise AssertionError("Failed to create BulkLoadStream due to invalid state:" + meta_data.get_state())
        self.partition_spec = self._parse_partition_spec(self.meta_data.table.schema,
                                                         self.meta_data.get_partition_specs())
        self.finished_files = []
        self.finished_file_sizes = []
        self.file_name_uuid = uuid.uuid4()
        self.file_id = 0
        self.closed = False
        self.current_total_rows = 0
        self.current_total_size = 0
        self.current_record_batch = {}
        self.current_batch_rows = 0
        # currently buffered size
        self.current_buffer_size = 0
        self.estimate_row_static_size = self._estimate_row_static_size()
        self.pyarrow_schema = self._generate_pyarrow_schema(self.meta_data.get_table().schema)
        self.writer = None

    def _process_staging_type(self):
        if self.staging_config.type == 'oss':
            self.location = self.staging_config.path
        elif self.staging_config.type == 'cos':
            self.location = '/tmp/' + self.staging_config.path
            cos_config = CosConfig(Region=self.staging_config.endpoint, SecretId=self.staging_config.id,
                                   SecretKey=self.staging_config.secret, Token=self.staging_config.token)
            self.cos_client = CosS3Client(cos_config)
        elif self.staging_config.type == 's3':
            self.location = self.staging_config.path
        elif self.staging_config.type == 'gcs':
            self.location = self.staging_config.path
        else:
            self.location = self.staging_config.path

    def get_stream_id(self):
        return self.meta_data.get_stream_id()

    def get_operation(self):
        return self.meta_data.get_operation()

    def get_schema(self):
        return self.meta_data.get_table().schema

    def get_table(self):
        return self.meta_data.get_table()

    def get_partition_id(self):
        return self.partition_id

    def create_row(self):
        return Row(self.meta_data.get_table().schema, self.meta_data.get_table_name())

    def write(self, row: Row):
        self._check_file_status()
        if not self.current_record_batch:
            self._construct_new_record_batch()

        for partition in self.partition_spec:
            row.field_name_values[partition] = self.partition_spec[partition]
        current_row_size = self.estimate_row_static_size
        for column in self.current_record_batch.keys():
            if column not in row.field_name_values:
                row.field_name_values[column] = None
        for filed_name in row.field_name_values:
            field_value = row.field_name_values[filed_name]
            self.current_record_batch[filed_name].append(field_value)
            if isinstance(field_value, str):
                current_row_size += len(field_value)
        self.current_buffer_size = self.current_buffer_size + current_row_size
        self.current_batch_rows = self.current_batch_rows + 1
        self.current_total_rows = self.current_total_rows + 1

        # batch rows set to 40000 or 16MB(in arrow), will get from session config later
        if self.current_batch_rows == 40000 or self.current_buffer_size >= 16 * 1024 * 1024:
            buffer_size = self._flush_record_batch()
            self.current_total_size = self.current_total_size + buffer_size
            self.current_buffer_size = 0

    def finish(self):
        if self.closed:
            raise AssertionError('BulkLoadWriter is already closed.')
        self._close_current_file()
        status = self.client.finish_bulkload_stream_writer(self.meta_data.get_instance_id(),
                                                           self.meta_data.get_workspace(),
                                                           self.meta_data.get_schema_name(),
                                                           self.meta_data.get_table_name(),
                                                           self.meta_data.get_stream_id(), self.partition_id,
                                                           self.finished_files, self.finished_file_sizes)
        if status.code != ingestion_pb2.Code.SUCCESS:
            msg = status.message
            raise RuntimeError(
                'Finish BulkLoadStreamWriter for instance:{}, workspace:{}, '
                'table:{}.{}, streamId:{}, partitionId:{} failed. Error message:{}'.format(
                    self.meta_data.get_instance_id(),
                    self.meta_data.get_workspace(), self.meta_data.get_schema_name(), self.meta_data.get_table_name(),
                    self.meta_data.get_stream_id(), self.partition_id, msg))
        _logger.info("Flush bulk load stream {} partitionId {} with {} files".format(self.meta_data.get_stream_id(),
                                                                                     self.partition_id,
                                                                                     len(self.finished_files)))
        self.finished_files.clear()
        self.finished_file_sizes.clear()
        self.closed = True

    def abort(self):
        self.writer.close()
        self.current_total_rows = 0
        self.current_total_size = 0
        self.current_batch_rows = 0
        self.current_record_batch = {}
        self.file_io.close()
        self.closed = True

    def close(self):
        if self.closed:
            return
        self.finish()

    def _flush_record_batch(self):
        if self.current_batch_rows == 0:
            return 0
        batch_data = []
        for item in self.current_record_batch:
            batch_data.append(self._convert_data_type(item, self.current_record_batch[item]))
        batch = pa.record_batch(batch_data, schema=self.pyarrow_schema)
        self.writer.write_batch(batch)
        self.current_batch_rows = 0
        self.current_record_batch.clear()
        return batch.get_total_buffer_size()

    def _estimate_type_size(self, data_type: data_type_pb2.DataType):
        if data_type.category == data_type_pb2.DataTypeCategory.INT8:
            return 1
        elif data_type.category == data_type_pb2.DataTypeCategory.INT16:
            return 2
        elif data_type.category == data_type_pb2.DataTypeCategory.INT32:
            return 4
        elif data_type.category == data_type_pb2.DataTypeCategory.INT64:
            return 8
        elif data_type.category == data_type_pb2.DataTypeCategory.FLOAT32:
            return 4
        elif data_type.category == data_type_pb2.DataTypeCategory.FLOAT64:
            return 8
        elif data_type.category == data_type_pb2.DataTypeCategory.DECIMAL:
            return 16
        elif data_type.category == data_type_pb2.DataTypeCategory.BOOLEAN:
            return 1
        elif data_type.category == data_type_pb2.DataTypeCategory.CHAR or \
                data_type.category == data_type_pb2.DataTypeCategory.VARCHAR or \
                data_type.category == data_type_pb2.DataTypeCategory.STRING:
            return 16
        elif data_type.category == data_type_pb2.DataTypeCategory.DATE:
            return 4
        elif data_type.category == data_type_pb2.DataTypeCategory.TIMESTAMP_LTZ:
            return 8
        # as default
        return 8

    def _estimate_row_static_size(self):
        schema = self.get_schema()
        row_size = 0
        for column_name, column_type in schema.items():
            row_size += self._estimate_type_size(column_type)
        return row_size

    def _convert_data_type(self, field_name: string, field_data: list):
        schema = self.meta_data.get_table().schema
        data_type = schema[field_name]
        if data_type.category == data_type_pb2.DataTypeCategory.INT8:
            return pc.cast(field_data, pa.int8())
        elif data_type.category == data_type_pb2.DataTypeCategory.INT16:
            return pc.cast(field_data, pa.int16())
        elif data_type.category == data_type_pb2.DataTypeCategory.INT32:
            return pc.cast(field_data, pa.int32())
        elif data_type.category == data_type_pb2.DataTypeCategory.INT64:
            return pc.cast(field_data, pa.int64())
        elif data_type.category == data_type_pb2.DataTypeCategory.FLOAT32:
            return pc.cast(field_data, pa.float32())
        elif data_type.category == data_type_pb2.DataTypeCategory.FLOAT64:
            return pc.cast(field_data, pa.float64())
        elif data_type.category == data_type_pb2.DataTypeCategory.DECIMAL:
            precision = data_type.decimalTypeInfo.precision
            scale = data_type.decimalTypeInfo.scale
            return pc.cast(field_data, pa.decimal128(precision, scale))
        elif data_type.category == data_type_pb2.DataTypeCategory.BOOLEAN:
            return pc.cast(field_data, pa.bool_())
        elif data_type.category == data_type_pb2.DataTypeCategory.CHAR or \
                data_type.category == data_type_pb2.DataTypeCategory.VARCHAR or \
                data_type.category == data_type_pb2.DataTypeCategory.STRING:
            return pc.cast(field_data, pa.string())
        elif data_type.category == data_type_pb2.DataTypeCategory.DATE:
            return pc.cast(field_data, pa.date32())
        elif data_type.category == data_type_pb2.DataTypeCategory.TIMESTAMP_LTZ:
            timestamp_unit = data_type.timestamp_info.tsUnit
            if timestamp_unit == data_type_pb2.TimestampUnit.SECONDS:
                return pc.cast(field_data, pa.timestamp('s', tz='UTC'))
            elif timestamp_unit == data_type_pb2.TimestampUnit.MILLISECONDS:
                return pc.cast(field_data, pa.timestamp('ms', tz='UTC'))
            elif timestamp_unit == data_type_pb2.TimestampUnit.MICROSECONDS:
                return pc.cast(field_data, pa.timestamp('us', tz='UTC'))
            elif timestamp_unit == data_type_pb2.TimestampUnit.NANOSECONDS:
                return pc.cast(field_data, pa.timestamp('ns', tz='UTC'))

    def _construct_new_record_batch(self):
        self.current_record_batch.clear()
        table_fields = self.meta_data.get_table().schema
        for filed in table_fields:
            self.current_record_batch[filed] = []
        self.current_batch_rows = 0

    def _generate_pyarrow_schema(self, schema: dict) -> pa.Schema:
        pyarrow_fields = []
        for field in schema:
            data_type = schema[field]
            if data_type.category == data_type_pb2.DataTypeCategory.INT8:
                pyarrow_fields.append(pa.field(field, pa.int8()))
            elif data_type.category == data_type_pb2.DataTypeCategory.INT16:
                pyarrow_fields.append(pa.field(field, pa.int16()))
            elif data_type.category == data_type_pb2.DataTypeCategory.INT32:
                pyarrow_fields.append(pa.field(field, pa.int32()))
            elif data_type.category == data_type_pb2.DataTypeCategory.INT64:
                pyarrow_fields.append(pa.field(field, pa.int64()))
            elif data_type.category == data_type_pb2.DataTypeCategory.FLOAT32:
                pyarrow_fields.append(pa.field(field, pa.float32()))
            elif data_type.category == data_type_pb2.DataTypeCategory.FLOAT64:
                pyarrow_fields.append(pa.field(field, pa.float64()))
            elif data_type.category == data_type_pb2.DataTypeCategory.DECIMAL:
                precision = data_type.decimalTypeInfo.precision
                scale = data_type.decimalTypeInfo.scale
                pyarrow_fields.append(pa.field(field, pa.decimal128(precision, scale)))
            elif data_type.category == data_type_pb2.DataTypeCategory.BOOLEAN:
                pyarrow_fields.append(pa.field(field, pa.bool_()))
            elif data_type.category == data_type_pb2.DataTypeCategory.CHAR or \
                    data_type.category == data_type_pb2.DataTypeCategory.VARCHAR or \
                    data_type.category == data_type_pb2.DataTypeCategory.STRING:
                pyarrow_fields.append(pa.field(field, pa.string()))
            elif data_type.category == data_type_pb2.DataTypeCategory.DATE:
                pyarrow_fields.append(pa.field(field, pa.date32()))
            elif data_type.category == data_type_pb2.DataTypeCategory.TIMESTAMP_LTZ:
                timestamp_unit = data_type.timestamp_info.tsUnit
                if timestamp_unit == data_type_pb2.TimestampUnit.SECONDS:
                    pyarrow_fields.append(pa.field(field, pa.timestamp('s', tz='UTC')))
                elif timestamp_unit == data_type_pb2.TimestampUnit.MILLISECONDS:
                    pyarrow_fields.append(pa.field(field, pa.timestamp('ms', tz='UTC')))
                elif timestamp_unit == data_type_pb2.TimestampUnit.MICROSECONDS:
                    pyarrow_fields.append(pa.field(field, pa.timestamp('us', tz='UTC')))
                elif timestamp_unit == data_type_pb2.TimestampUnit.NANOSECONDS:
                    pyarrow_fields.append(pa.field(field, pa.timestamp('ns', tz='UTC')))
        return pa.schema(pyarrow_fields)

    def _parse_partition_spec(self, schema: dict, partition_spec: string) -> dict:
        partition_value_dict = {}
        if partition_spec.strip() == '':
            return partition_value_dict
        partition_pairs = partition_spec.strip().split(',')
        for partition in partition_pairs:
            kv = partition.strip().split('=')
            partition_value_dict[kv[0].strip()] = kv[1].strip()
        for field in schema:
            if field in partition_value_dict:
                data_type = schema[field]
                if data_type.category == data_type_pb2.DataTypeCategory.INT8 or \
                        data_type.category == data_type_pb2.DataTypeCategory.INT16 or \
                        data_type.category == data_type_pb2.DataTypeCategory.INT32:
                    partition_value_dict[field] = int(partition_value_dict[field])
                elif data_type.category == data_type_pb2.DataTypeCategory.INT64:
                    partition_value_dict[field] = int(partition_value_dict[field])
                elif data_type.category == data_type_pb2.DataTypeCategory.FLOAT32 or \
                        data_type.category == data_type_pb2.DataTypeCategory.FLOAT64:
                    partition_value_dict[field] = float(partition_value_dict[field])
                elif data_type.category == data_type_pb2.DataTypeCategory.DECIMAL:
                    partition_value_dict[field] = decimal.Decimal(partition_value_dict[field])
                elif data_type.category == data_type_pb2.DataTypeCategory.BOOLEAN:
                    partition_value_dict[field] = bool(partition_value_dict[field])
                elif data_type.category == data_type_pb2.DataTypeCategory.DATE:
                    partition_value_dict[field] = (
                            datetime.strptime(partition_value_dict[field], '%Y-%m-%d') - datetime(1970, 1, 1)).days

        return partition_value_dict

    def _get_current_file_name(self):
        return '{}{}-{}.{}'.format(self.location, self.file_name_uuid, self.file_id, self.file_format.value)

    def _create_next_file_writer(self):
        file_name = self._get_current_file_name()
        if self.staging_config.type == 'cos':
            if not os.path.exists(os.path.dirname(file_name)):
                self.file_io.create_dir(os.path.dirname(file_name))
        if self.file_format == FileFormatType.PARQUET:
            return pq.ParquetWriter(file_name, self.pyarrow_schema, filesystem=self.file_io)
        else:
            raise NotImplementedError('File format:{} is not supported yet.'.format(self.file_format.value))

    def _close_current_file(self):
        if self.writer is not None:
            buffer_size = self._flush_record_batch()
            self.writer.close()
            file_name = self._upload_local_file()
            self.finished_files.append(file_name)
            self.finished_file_sizes.append(self.current_total_size + buffer_size)
            self.current_total_size = 0
            self.current_total_rows = 0
            self.current_batch_rows = 0
            self.current_record_batch.clear()
            self.file_id = self.file_id + 1
            self.writer = None

    def _upload_local_file(self):
        if self.staging_config.type == 'cos':
            try:
                file_name = self._get_current_file_name()[5:]
                path_infos = file_name.split('/', 3)
                bucket = path_infos[2]
                key = path_infos[3]
                response = self.cos_client.upload_file(Bucket=bucket, LocalFilePath=self._get_current_file_name(),
                                                       Key=key, MAXThread=8, EnableMD5=True, PartSize=100)
                _logger.info('Upload file {} to cos successfully.Etag is {}'.format(file_name, response['ETag']))
                self.file_io.delete_file(self._get_current_file_name())
                _logger.info('Delete local file {} successfully.'.format(self._get_current_file_name()))
                return file_name
            except CosServiceError as e:
                raise e
            except CosClientError as e:
                raise e
            except Exception as e:
                raise e
        elif self.staging_config.type == 'oss':
            return self._get_current_file_name()
        elif self.staging_config.type == 's3':
            return self._get_current_file_name()
        elif self.staging_config.type == 'gcs':
            return self._get_current_file_name()
        else:
            return self._get_current_file_name()

    def _check_file_status(self):
        if self.writer is not None:
            if self.current_total_rows >= self.max_file_records or self.current_total_size > self.max_file_size:
                self._close_current_file()

        if self.writer is None:
            self.writer = self._create_next_file_writer()
