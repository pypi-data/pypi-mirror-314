import copy
import logging
from enum import Enum
from logging import getLogger
import cz_ossfs
import s3fs
from google.oauth2.credentials import Credentials
from pyarrow import fs
import string
import gcsfs

from clickzetta.bulkload import cz_table
from clickzetta.proto.generated import ingestion_pb2, file_format_type_pb2

MAX_NUM_ROWS_PER_FILE = 64 << 20
MAX_FILE_SIZE_IN_BYTES_PER_FILE = 256 << 20


class FileFormatType(Enum):
    TEXT = 'text'
    PARQUET = 'parquet'
    ORC = 'orc'
    AVRO = 'avro'
    CSV = 'csv'
    ARROW = 'arrow'
    HIVE_RESULT = 'hive_result'
    DUMMY = 'dummy'
    MEMORY = 'memory'
    ICEBERG = 'iceberg'


class CZOSSFileSystem(cz_ossfs.OSSFileSystem):
    def __init__(self, endpoint: string, secret: string, token: string, key: string, cz_feature: string = None):
        super(CZOSSFileSystem, self).__init__(endpoint=endpoint, secret=secret, token=token, key=key)
        self.cz_feature = cz_feature

    def exists(self, path, **kwargs):
        if self.cz_feature == 'bulkload':
            bucket_name, obj_name = super().split_path(path)

            connect_timeout = kwargs.get("connect_timeout", None)
            if not obj_name:
                return True

            if super()._call_oss(
                    "object_exists",
                    obj_name,
                    bucket=bucket_name,
                    timeout=connect_timeout,
            ):
                return True

            return False
        else:
            return super().exists(path, **kwargs)


class StagingConfig:
    def __init__(self, path: string, id: string, secret: string, token: string, endpoint: string, type: None):
        self.path = path
        self.id = id
        self.secret = secret
        self.token = token
        self.endpoint = endpoint
        self.type = type

    def create_file_io(self):
        if self.type == 'oss':
            return CZOSSFileSystem(endpoint=self.endpoint, secret=self.secret, token=self.token, key=self.id,
                                   cz_feature='bulkload')
        elif self.type == 's3':
            client_kwargs = {'region_name': self.endpoint}
            return s3fs.S3FileSystem(key=self.id, secret=self.secret, token=self.token, client_kwargs=client_kwargs)
        elif self.type == 'gcs':
            credentials = Credentials(token=self.token)
            return gcsfs.GCSFileSystem(project='clickzetta-connector', token=credentials)
        elif self.type == 'tos':
            raise NotImplementedError('TOS is not supported bulkload yet')
            # TODO wait for volces to support s3fs. Currently, it got an error as below:
            # TypeError: _create_client() got an unexpected keyword argument 's3'
            # import s3fs
            # client_kwargs = {'s3': {'addressing_style': 'virtual'}}
            # return s3fs.S3FileSystem(key=self.id, secret=self.secret, token=self.token,
            #                          endpoint_url='https://tos-s3-cn-guangzhou.volces.com', client_kwargs=client_kwargs)
        else:
            return fs.LocalFileSystem()


class BulkLoadConfig:
    def __init__(self, config: ingestion_pb2.BulkLoadStreamWriterConfig):
        self.config = config

    def get_staging_config(self, prefer_internal_endpoint=False):
        staging_path = self.config.staging_path
        staging_config = None
        if staging_path.oss_path.path != '':
            oss_path = staging_path.oss_path
            endpoint = oss_path.oss_endpoint
            if prefer_internal_endpoint:
                endpoint = oss_path.oss_internal_endpoint
            staging_config = StagingConfig(oss_path.path, oss_path.sts_ak_id, oss_path.sts_ak_secret,
                                           oss_path.sts_token, endpoint, 'oss')
        elif staging_path.cos_path.path != '':
            cos_path = staging_path.cos_path
            staging_config = StagingConfig(cos_path.path, cos_path.sts_ak_id, cos_path.sts_ak_secret,
                                           cos_path.sts_token,
                                           cos_path.cos_region, 'cos')
        elif staging_path.s3_path.path != '':
            s3_path = staging_path.s3_path
            staging_config = StagingConfig(s3_path.path, s3_path.sts_ak_id, s3_path.sts_ak_secret,
                                           s3_path.sts_token,
                                           s3_path.s3_region, 's3')
        elif staging_path.gcs_path.path != '':
            gcs_path = staging_path.gcs_path
            staging_config = StagingConfig(gcs_path.path, gcs_path.sts_ak_id, gcs_path.sts_ak_secret,
                                           gcs_path.sts_token,
                                           gcs_path.gcs_region, 'gcs')
        elif staging_path.tos_path.path != '':
            tos_path = staging_path.tos_path
            # replace the tos:// to https://tos-s3-cn-guangzhou.volces.com
            tos_path.path = tos_path.path.replace('tos://', 's3://')
            staging_config = StagingConfig(tos_path.path, tos_path.sts_ak_id, tos_path.sts_ak_secret,
                                           tos_path.sts_token,
                                           tos_path.tos_endpoint, 'tos')
        else:
            raise ValueError('Staging path is not set, please check the configuration')
        return staging_config

    def get_file_format(self):
        file_format = self.config.file_format
        if file_format == file_format_type_pb2.FileFormatType.TEXT:
            return FileFormatType.TEXT
        elif file_format == file_format_type_pb2.FileFormatType.PARQUET:
            return FileFormatType.PARQUET
        elif file_format == file_format_type_pb2.FileFormatType.ORC:
            return FileFormatType.ORC
        elif file_format == file_format_type_pb2.FileFormatType.AVRO:
            return FileFormatType.AVRO
        elif file_format == file_format_type_pb2.FileFormatType.CSV:
            return FileFormatType.CSV
        elif file_format == file_format_type_pb2.FileFormatType.ARROW:
            return FileFormatType.ARROW
        elif file_format == file_format_type_pb2.FileFormatType.HIVE_RESULT:
            return FileFormatType.HIVE_RESULT
        elif file_format == file_format_type_pb2.FileFormatType.DUMMY:
            return FileFormatType.DUMMY
        elif file_format == file_format_type_pb2.FileFormatType.MEMORY:
            return FileFormatType.MEMORY
        elif file_format == file_format_type_pb2.FileFormatType.ICEBERG:
            return FileFormatType.ICEBERG

    def get_max_rows_per_file(self):
        if self.config.max_num_rows_per_file > 0:
            return self.config.max_num_rows_per_file
        return MAX_NUM_ROWS_PER_FILE

    def get_max_file_size_per_file(self):
        if self.config.max_size_in_bytes_per_file > 0:
            return self.config.max_size_in_bytes_per_file
        return MAX_FILE_SIZE_IN_BYTES_PER_FILE


class BulkLoadOperation(Enum):
    APPEND = 1
    UPSERT = 2
    OVERWRITE = 3


class BulkLoadState(Enum):
    CREATED = 1
    SEALED = 2
    COMMIT_SUBMITTED = 3
    COMMIT_SUCCESS = 4
    COMMIT_FAILED = 5
    ABORTED = 6


class BulkLoadOptions:
    def __init__(self, operation: BulkLoadOperation, partition_specs: str, record_keys: list,
                 prefer_internal_endpoint=False) -> None:
        self.operation = operation
        self.partition_specs = partition_specs
        self.record_keys = record_keys
        self.prefer_internal_endpoint = prefer_internal_endpoint
        self._properties = {'operation': operation, 'partition_specs': partition_specs, 'record_keys': record_keys,
                            'prefer_internal_endpoint': prefer_internal_endpoint}


    def to_api_repr(self) -> dict:
        return copy.deepcopy(self._properties)


class BulkLoadMetaData:
    def __init__(self, instance_id: int, info: ingestion_pb2.BulkLoadStreamInfo):
        self.instance_id = instance_id
        self.info = info
        self.table = cz_table.CZTable(info.stream_schema, info.identifier.schema_name, info.identifier.table_name)

    def get_instance_id(self):
        return self.instance_id

    def get_workspace(self):
        return self.info.identifier.workspace

    def get_schema_name(self):
        return self.info.identifier.schema_name

    def get_table_name(self):
        return self.info.identifier.table_name

    def get_stream_id(self):
        return self.info.stream_id

    def get_table(self):
        return self.table

    def get_prefer_internal_endpoint(self):
        return self.info.prefer_internal_endpoint

    def get_operation(self):
        if self.info.operation == ingestion_pb2.BulkLoadStreamOperation.BL_APPEND:
            return BulkLoadOperation.APPEND
        elif self.info.operation == ingestion_pb2.BulkLoadStreamOperation.BL_OVERWRITE:
            return BulkLoadOperation.OVERWRITE
        elif self.info.operation == ingestion_pb2.BulkLoadStreamOperation.BL_UPSERT:
            return BulkLoadOperation.UPSERT

    def get_state(self):
        if self.info.stream_state == ingestion_pb2.BulkLoadStreamState.BL_CREATED:
            return BulkLoadState.CREATED
        elif self.info.stream_state == ingestion_pb2.BulkLoadStreamState.BL_SEALED:
            return BulkLoadState.SEALED
        elif self.info.stream_state == ingestion_pb2.BulkLoadStreamState.BL_COMMIT_SUBMITTED:
            return BulkLoadState.COMMIT_SUBMITTED
        elif self.info.stream_state == ingestion_pb2.BulkLoadStreamState.BL_COMMIT_SUCCESS:
            return BulkLoadState.COMMIT_SUCCESS
        elif self.info.stream_state == ingestion_pb2.BulkLoadStreamState.BL_COMMIT_FAILED:
            return BulkLoadState.COMMIT_FAILED
        elif self.info.stream_state == ingestion_pb2.BulkLoadStreamState.BL_ABORTED:
            return BulkLoadState.ABORTED

    def get_sql_error_msg(self):
        return self.info.sql_error_msg

    def get_partition_specs(self):
        return self.info.partition_spec

    def get_record_keys(self):
        record_keys = []
        for key in self.info.record_keys:
            record_keys.append(key)

        return record_keys


class BulkLoadCommitOptions:
    def __init__(self, workspace: string, vc: string):
        self.workspace = workspace
        self.vc = vc


class BulkLoadCommitMode(Enum):
    COMMIT_STREAM = 1
    ABORT_STREAM = 2
