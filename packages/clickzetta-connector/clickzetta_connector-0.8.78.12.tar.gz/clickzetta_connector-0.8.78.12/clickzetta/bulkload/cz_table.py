import string
from clickzetta.proto.generated import metadata_entity_pb2, ingestion_pb2, table_meta_pb2


class CZTable:
    def __init__(self, table_meta: ingestion_pb2.StreamSchema, schema_name: string, table_name: string):
        self.schema_name = schema_name
        self.table_name = table_name
        self.table_meta = table_meta
        self.schema = {}
        fields = table_meta.data_fields
        for field in fields:
            self.schema[field.name] = field.type

