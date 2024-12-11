import string
from typing import Any, Dict, List, Literal, Optional, Set, Tuple, Union

from clickzetta.client import Client
from clickzetta.bulkload.bulkload_stream import BulkLoadStream
from clickzetta.bulkload.bulkload_enums import *


class Session:
    class SessionBuilder:
        def __init__(self) -> None:
            self._options = {}

        def _remove_config(self, key: str) -> "Session.SessionBuilder":
            self._options.pop(key, None)
            return self

        def config(self, key: str, value: Union[int, str]) -> "Session.SessionBuilder":
            self._options[key] = value
            return self

        def configs(
                self, options: Dict[str, Union[int, str]]
        ) -> "Session.SessionBuilder":
            self._options = {**self._options, **options}
            return self

        def create(self) -> "Session":
            session = self._create_internal(self._options.get("url"))
            return session

        def _create_internal(
                self, conn: string = None
        ) -> "Session":
            new_session = Session(
                conn,
                self._options,
            )
            return new_session

        def __get__(self, obj, objtype=None):
            return Session.SessionBuilder()

    builder: SessionBuilder = SessionBuilder()

    def __init__(self, conn: string, options: Optional[Dict[str, Any]] = None) -> None:
        self._client = Client(cz_url=conn)

    def create_bulkload_stream(self, schema_name: string, table_name: string,
                               options: BulkLoadOptions) -> BulkLoadStream:
        return self._create_bulkload_stream_internal(schema_name, table_name, options)

    def _create_bulkload_stream_internal(self, schema_name: string, table_name: string,
                                         options: BulkLoadOptions) -> BulkLoadStream:
        bulkload_meta_data = self._client.create_bulkload_stream(schema_name, table_name, options)
        return BulkLoadStream(bulkload_meta_data, self._client)

    def commit_bulkload_stream(self, instance_id: int, workspace: string, schema_name: string, table_name: string,
                               stream_id: string, execute_workspace: string, execute_vc: string,
                               commit_mode: BulkLoadCommitMode) -> BulkLoadMetaData:
        return self._commit_bulkload_stream(instance_id, workspace, schema_name, table_name, stream_id,
                                            execute_workspace, execute_vc, commit_mode)

    def _commit_bulkload_stream(self, instance_id: int, workspace: string, schema_name: string, table_name: string,
                                stream_id: string, execute_workspace: string, execute_vc: string,
                                commit_mode: BulkLoadCommitMode) -> BulkLoadMetaData:
        return self._client.commit_bulkload_stream(instance_id, workspace, schema_name, table_name, stream_id,
                                                   execute_workspace, execute_vc, commit_mode)

    def get_bulkload_stream(self, schema_name: string, table_name: string, stream_id: string) -> BulkLoadStream:
        return self._get_bulkload_stream(schema_name, table_name, stream_id)

    def _get_bulkload_stream(self, schema_name: string, table_name: string, stream_id: string) -> BulkLoadStream:
        bulkload_meta_data = self._client.get_bulkload_stream(schema_name, table_name, stream_id)
        return BulkLoadStream(bulkload_meta_data, self._client)

    def close(self):
        return
