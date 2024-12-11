"""Connection for ClickZetta DB-API."""
import weakref
import logging
import time

import requests
from requests.adapters import HTTPAdapter
from clickzetta.client import Client
from clickzetta.dbapi import cursor
from clickzetta.dbapi import _helpers
from clickzetta.bulkload.bulkload_enums import BulkLoadOperation, BulkLoadOptions, BulkLoadCommitOptions
from clickzetta.bulkload.bulkload_stream import BulkLoadStream

is_token_init = False
current_token = None
token_init_time = 0
https_session = None
user_token_dict = {}
user_token_time_dict = {}
https_session_inited = False


@_helpers.raise_on_closed("Operating on a closed connection.")
class Connection(object):
    def __init__(self, client=None):
        if client is None:
            logging.error('Connection must has a LogParams to log in.')
            raise AssertionError('Connection must has a LogParams to log in.')
        else:
            self._owns_client = True

        self._client = client
        if self._client.magic_token is not None:
            self._client.token = self._client.magic_token
        else:
            self._update_token()

        if not globals()['https_session_inited']:
            session = requests.Session()
            session.mount(self._client.service, HTTPAdapter(pool_connections=20, pool_maxsize=100, max_retries=1000))
            globals()['https_session'] = session
            globals()['https_session_inited'] = True

        self._client.session = globals()['https_session']
        self._closed = False
        self._cursors_created = weakref.WeakSet()

    def _update_token(self):
        current_time = int(time.time())
        unique_key = self._client.username + "?" + self._client.instance
        if globals()['user_token_dict'].__contains__(unique_key):
            if current_time - globals()['user_token_time_dict'][unique_key] > 24 * 60 * 60 * 2:
                new_token = self._client.log_in_cz(self._client.username, self._client.password,
                                                   self._client.instance)
                globals()['user_token_dict'][unique_key] = new_token
                globals()['user_token_time_dict'][unique_key] = current_time
                self._client.token = new_token
            else:
                self._client.token = globals()['user_token_dict'][unique_key]
        else:
            new_token = self._client.log_in_cz(self._client.username, self._client.password, self._client.instance)
            globals()['user_token_dict'][unique_key] = new_token
            globals()['user_token_time_dict'][unique_key] = current_time
            self._client.token = new_token

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self._closed = True

        if self._owns_client:
            self._client.close()

        for cursor_ in self._cursors_created:
            if not cursor_._closed:
                cursor_.close()

    def commit(self):
        """No-op, but for consistency raise an error if connection is closed."""

    def cursor(self):
        """Return a new cursor object."""
        if self._client.username is not None and self._client.password is not None:
            self._update_token()
        new_cursor = cursor.Cursor(self)
        self._cursors_created.add(new_cursor)
        return new_cursor

    def create_bulkload_stream(self, **kwargs):
        schema = kwargs.get('schema', self._client.schema)
        table = kwargs.get('table')
        if schema is None:
            schema = self._client.schema
        if schema is None:
            raise ValueError(f'No schema specified')
        if table is None:
            raise ValueError(f'No table specified')

        operation = kwargs.get('operation', BulkLoadOperation.APPEND)
        workspace = kwargs.get('workspace', self._client.workspace)
        vcluster = kwargs.get('vcluster', self._client.vcluster)
        partition_spec = kwargs.get('partition_spec')
        record_keys = kwargs.get('record_keys')
        prefer_internal_endpoint = kwargs.get('prefer_internal_endpoint', False)

        bulkload_meta_data = self._client.create_bulkload_stream(
            schema, table, BulkLoadOptions(operation, partition_spec, record_keys, prefer_internal_endpoint))
        return BulkLoadStream(bulkload_meta_data, self._client,
                              BulkLoadCommitOptions(workspace, vcluster))

    def get_bulkload_stream(self, stream_id: str, schema: str = None, table: str = None):
        bulkload_meta_data = self._client.get_bulkload_stream(schema, table, stream_id)
        return BulkLoadStream(bulkload_meta_data, self._client,
                              BulkLoadCommitOptions(self._client.workspace, self._client.vcluster))

    def get_job_profile(self, job_id: str):
        return self._client.get_job_profile(job_id)

    def get_job_result(self, job_id: str):
        return self._client.get_job_result(job_id)

    def get_job_progress(self, job_id: str):
        return self._client.get_job_progress(job_id)

    def get_job_summary(self, job_id: str):
        return self._client.get_job_summary(job_id)

    def get_job_plan(self, job_id: str):
        return self._client.get_job_plan(job_id)


def connect(**kwargs) -> Connection:
    client = kwargs.get('client')
    if client is None:
        client = Client(cz_url=kwargs.get('cz_url'),  # setting client or cz_url will ignore following parameters
                        username=kwargs.get('username'), password=kwargs.get('password'),
                        instance=kwargs.get('instance'), service=kwargs.get('service'),
                        workspace=kwargs.get('workspace'), vcluster=kwargs.get('vcluster'),
                        schema=kwargs.get('schema', 'public'), magic_token=kwargs.get('magic_token'),
                        protocol=kwargs.get('protocol'), hints=kwargs.get('hints'))
    return Connection(client)
