import os.path

import io
import string
import base64
from time import sleep

import oss2
import pyarrow as pa
import logging
import enum
from clickzetta.enums import FetchMode
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED

from qcloud_cos import CosConfig, CosS3Client

from clickzetta.object_storage_client import ObjectStorageClient, ObjectStorageType

logger = logging.getLogger(__name__)


class QueryDataType(enum.Enum):
    Memory = 0
    File = 1


class QueryData(object):
    def __init__(self, data: list, data_type: QueryDataType, file_list: list = None,
                 object_storage_client:ObjectStorageClient = None):
        self.data = data
        self.data_type = data_type
        self.file_list = file_list
        self.object_storage_client = object_storage_client
        self.current_file_index = 0
        self.memory_read = False

    def read(self, fetch_mode=FetchMode.FETCH_ALL, size=0):
        if self.data_type == QueryDataType.Memory:
            if self.memory_read:
                return None
            self.memory_read = True
            return self.data
        elif self.data_type == QueryDataType.File:
            assert self.file_list is not None
            try:
                final_result = []
                if fetch_mode == FetchMode.FETCH_ONE:
                    file = self.file_list[0]
                    return self.read_object_file(file)
                elif fetch_mode == FetchMode.FETCH_MANY:
                    for file in self.file_list:
                        final_result.extend(self.read_object_file(file))
                        if len(final_result) >= size:
                            break
                else:
                    for file in self.file_list:
                        final_result.extend(self.read_object_file(file))
                return final_result
            except Exception as e:
                logger.error(f'Error while converting from arrow to result: {e}')
                raise Exception(f'Error while converting from arrow to result: {e}')

    def read_object_file(self, file):
        file_info = file.split('/', 3)
        result = []
        stream = self.object_storage_client.get_stream(file_info[2], file_info[3])
        with pa.ipc.RecordBatchStreamReader(stream) as reader:
            for index, row in reader.read_pandas().iterrows():
                result.append(tuple(row.to_list()))
            return result


class Field(object):
    def __init__(self):
        self.name = None
        self.field_type = None
        self.precision = None
        self.scale = None
        self.length = None
        self.nullable = None

    def set_name(self, name):
        self.name = name

    def set_type(self, type):
        self.field_type = type

    def set_precision(self, precision):
        self.precision = precision

    def set_scale(self, scale):
        self.scale = scale

    def set_length(self, length):
        self.length = length

    def set_nullable(self, nullable):
        self.nullable = nullable


class QueryResult(object):
    def __init__(self, total_msg):
        self.data = None
        self.state = None
        self.total_row_count = 0
        self.total_msg = total_msg
        self.schema = []
        self._parse_result_data()

    def _parse_field(self, field: str, schema_field: Field):
        schema_field.set_name(field['name'])
        if field['type'].__contains__('charTypeInfo'):
            schema_field.set_type(field['type']['category'])
            schema_field.set_nullable(str(field['type']['nullable']) != 'False')
            schema_field.set_length(field['type']['charTypeInfo']['length'])
        elif field['type'].__contains__('decimalTypeInfo'):
            schema_field.set_type(field['type']['category'])
            schema_field.set_nullable(str(field['type']['nullable']) == 'true')
            schema_field.set_precision(field['type']['decimalTypeInfo']['precision'])
            schema_field.set_scale(field['type']['decimalTypeInfo']['scale'])
        else:
            schema_field.set_type(field['type']['category'])
            schema_field.set_nullable(str(field['type']['nullable']) == 'true')

    def get_result_state(self) -> string:
        return self.total_msg['status']['state']

    def get_arrow_result(self, arrow_buffer):
        try:
            buffer = base64.b64decode(arrow_buffer)
            with pa.ipc.RecordBatchStreamReader(io.BytesIO(buffer)) as reader:
                table = reader.read_all()
                column_dict = {}
                for index, column_name in enumerate(table.column_names):
                    if column_name in column_dict:
                        column_dict[f'{column_name}_{index}'] = index
                    else:
                        column_dict[column_name] = index
                new_table = table.rename_columns(column_dict.keys())
                pandas_result = new_table.to_pandas()
                self.panda_data = pandas_result
                result = []
                for index, row in pandas_result.iterrows():
                    result.append(tuple(row.tolist()))
                ##########################################################
                # result = []
                # batches = [b for b in new_table.to_batches()]
                # for batch in batches:
                #     cols = [batch.column(i) for i in range(batch.num_columns)]
                #     for row_index in range(batch.num_rows):
                #         row_values = []
                #         for col in cols:
                #             value = col[row_index].as_py()
                #             if value is not None and isinstance(col[row_index], pa.lib.MapScalar):
                #                 d = dict()
                #                 for v in value:
                #                     d[str(v[0])] = v[1]
                #                 value = d
                #             row_values.append(value)
                #         result.append(tuple(row_values))
                ############################################################
                return result

        except Exception as e:
            logger.error(f'Error while converting from arrow to result: {e}')
            raise Exception(f'Error while converting from arrow to result: {e}')

    def get_result_schema(self):
        fields = self.total_msg['resultSet']['metadata']['fields']
        for field in fields:
            schema_field = Field()
            self._parse_field(field, schema_field)
            self.schema.append(schema_field)

    def get_object_storage_type(self, path: str) -> ObjectStorageType:
        if path.lower().startswith('oss://'):
            return ObjectStorageType.OSS
        elif path.lower().startswith('cos://'):
            return ObjectStorageType.COS
        elif path.lower().startswith('s3://'):
            return ObjectStorageType.S3
        elif path.lower().startswith('gs://'):
            return ObjectStorageType.GCS
        elif path.lower().startswith("tos://"):
            return ObjectStorageType.TOS

    def get_object_storage_file_list(self) -> list:
        object_storage_file_list = self.total_msg['resultSet']['location']['location']
        return object_storage_file_list

    def get_oss_bucket(self) -> oss2.Bucket:
        location_info = self.total_msg['resultSet']['location']
        id = location_info['stsAkId']
        secret = location_info['stsAkSecret']
        token = location_info['stsToken']
        endpoint = location_info['ossEndpoint']
        if len(location_info['location']) == 0:
            raise Exception('No file found in oss when get result from clickzetta')
        bucket_name = location_info['location'][0].split('/', 3)[2]
        auth = oss2.StsAuth(id, secret, token)
        bucket = oss2.Bucket(auth, endpoint, bucket_name)
        return bucket

    def get_cos_client(self) -> CosS3Client:
        location_info = self.total_msg['resultSet']['location']
        region = location_info['objectStorageRegion']
        id = location_info['stsAkId']
        secret = location_info['stsAkSecret']
        token = location_info['stsToken']
        cos_config = CosConfig(Region=region, SecretId=id, SecretKey=secret, Token=token)
        client = CosS3Client(cos_config)
        return client

    def _parse_result_data(self):
        if len(self.total_msg) == 0:
            return
        self.state = self.total_msg['status']['state']
        if self.state != 'FAILED' and self.state != 'CANCELLED':
            if 'data' not in self.total_msg['resultSet']:
                if 'location' in self.total_msg['resultSet']:
                    self.get_result_schema()
                    file_list = self.get_object_storage_file_list()
                    if len(file_list) == 0:
                        self.total_row_count = 0
                        self.data = QueryData(data=[], data_type=QueryDataType.Memory)
                        return
                    object_storage_type = self.get_object_storage_type(file_list[0])
                    location_info = self.total_msg['resultSet']['location']
                    ak_id = location_info['stsAkId']
                    ak_secret = location_info['stsAkSecret']
                    token = location_info['stsToken']
                    endpoint = None
                    bucket = None
                    if object_storage_type == ObjectStorageType.OSS:
                        endpoint = location_info['ossEndpoint']
                        bucket = location_info['location'][0].split('/', 3)[2]
                    elif object_storage_type == ObjectStorageType.COS:
                        endpoint = location_info['objectStorageRegion']
                    elif object_storage_type == ObjectStorageType.S3:
                        endpoint = location_info['objectStorageRegion']
                    else:
                        endpoint = location_info["objectStorageRegion"]
                    object_storage_client = ObjectStorageClient(object_storage_type, ak_id, ak_secret, token,
                                                                endpoint, bucket)
                    self.data = QueryData(data_type=QueryDataType.File, file_list=file_list, data=None,
                                          object_storage_client=object_storage_client)

                else:
                    field = Field()
                    field.set_name('RESULT_MESSAGE')
                    field.set_type("STRING")
                    self.schema.append(field)
                    self.total_row_count = 1
                    result_data = [['OPERATION SUCCEED']]
                    self.data = QueryData(data=result_data, data_type=QueryDataType.Memory)
            else:
                if not (len(self.total_msg['resultSet']['data']['data'])):
                    self.total_row_count = 0
                    fields = self.total_msg['resultSet']['metadata']['fields']
                    for field in fields:
                        schema_field = Field()
                        self._parse_field(field, schema_field)
                        self.schema.append(schema_field)
                    self.data = QueryData(data=[], data_type=QueryDataType.Memory)
                    return
                result_data = self.total_msg['resultSet']['data']['data']
                self.get_result_schema()
                query_result = []
                for row in result_data:
                    partial_result = self.get_arrow_result(row)
                    query_result.extend(entity for entity in partial_result)
                self.data = QueryData(data=query_result, data_type=QueryDataType.Memory)

        else:
            raise Exception('SQL job execute failed.Error:' + self.total_msg['status']['message'])
