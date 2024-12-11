"""Client for interacting with the ClickZetta API."""

from __future__ import absolute_import
from __future__ import division

import re
import time
import shutil
from urllib.parse import urlparse, unquote

import clickzetta
from sqlalchemy.engine.url import make_url
import json
import random
import os
import requests.exceptions
import typing
from typing import (
    Any,
    Dict,
    IO,
    Iterable,
    Mapping,
    List,
    Optional,
    Sequence,
    Tuple,
    Union,
)
import uuid
import warnings
import logging
from google.protobuf.json_format import MessageToJson, Parse, ParseDict
from datetime import datetime

from clickzetta._helpers import _get_click_zetta_host, _DEFAULT_HOST

from clickzetta.enums import *
from clickzetta.table import Table
from clickzetta.query_result import QueryResult, QueryData, QueryDataType
from clickzetta.proto.generated import ingestion_pb2
from clickzetta.bulkload.bulkload_enums import BulkLoadOptions, BulkLoadMetaData, BulkLoadOperation, \
    BulkLoadCommitMode, BulkLoadConfig
from clickzetta.utils import split_sql
from clickzetta._volume import resolve_local_path

TIMEOUT_HEADER = "X-Server-Timeout"
TimeoutType = Union[float, None]
ResumableTimeoutType = Union[
    None, float, Tuple[float, float]
]

if typing.TYPE_CHECKING:
    PathType = Union[str, bytes, os.PathLike[str], os.PathLike[bytes]]
    import requests

_DEFAULT_CHUNKSIZE = 10 * 1024 * 1024  # 10 MB
_MAX_MULTIPART_SIZE = 5 * 1024 * 1024
_DEFAULT_NUM_RETRIES = 6
_GENERIC_CONTENT_TYPE = "*/*"

_MIN_GET_QUERY_RESULTS_TIMEOUT = 120
HTTP_PROTOCOL_DEFAULT_PORT = '80'
HTTPS_PROTOCOL_DEFAULT_PORT = '443'
HTTP_PROTOCOL_PREFIX = 'http://'
HTTPS_PROTOCOL_PREFIX = 'https://'

DEFAULT_TIMEOUT = None

FIRST_SQL_SUBMIT_TIMEOUT = 30
HYBRID_SQL_TIMEOUT = 120

HEADERS = {
    'Content-Type': 'application/json'
}

DEFAULT_INSTANCE_ID = 100

class Client(object):

    def __init__(self, username: str = None, password: str = None, instance: str = None, workspace: str = None,
                 vcluster: str = None, cz_url: str = None, service: str = None, schema: str = None,
                 magic_token: str = None, protocol: str = None, hints: {} = None):
        self.schema = None
        self.magic_token = None
        self.protocol = None
        self.hints = hints
        if cz_url is not None:
            self._parse_url(cz_url)
            self.instance_id = 0
        else:
            if service is None:
                raise ValueError('ClickZetta connection url `service` is required.')
            else:
                if protocol is None or protocol == 'https':
                    self.service = HTTPS_PROTOCOL_PREFIX + service if not service.startswith(
                        HTTPS_PROTOCOL_PREFIX) else service
                elif protocol == 'http':
                    self.service = HTTP_PROTOCOL_PREFIX + service if not service.startswith(
                        HTTP_PROTOCOL_PREFIX) else service
                else:
                    raise ValueError('protocol must be http or https. Other protocols are not supported yet.')
            self.token = None
            self.workspace = workspace
            self.instance = instance
            self.vcluster = vcluster
            self.session = None
            self.instance_id = 0
            self.username = username
            self.schema = schema
            self.password = password
            self.magic_token = magic_token
            self.protocol = protocol
        if self.magic_token is not None:
            self.token = self.magic_token
        else:
            self.token = self.log_in_cz(self.username, self.password, self.instance)

    def _parse_url(self, url: string):
        url = make_url(url)
        query = dict(url.query)
        port = url.port

        self.instance = url.host.split('.')[0]
        length = len(self.instance) + 1

        if 'protocol' in query:
            self.protocol = query.pop('protocol')
            if self.protocol == 'http':
                if not port:
                    self.service = HTTP_PROTOCOL_PREFIX + url.host[length:] + ':' + HTTP_PROTOCOL_DEFAULT_PORT
                else:
                    self.service = HTTP_PROTOCOL_PREFIX + url.host[length:] + ':' + str(port)
            else:
                raise ValueError('protocol parameter must be http. Other protocols are not supported yet.')
        else:
            self.protocol = 'https'
            if not port:
                self.service = HTTPS_PROTOCOL_PREFIX + url.host[length:] + ':' + HTTPS_PROTOCOL_DEFAULT_PORT
            else:
                self.service = HTTPS_PROTOCOL_PREFIX + url.host[length:] + ':' + str(port)

        self.workspace = url.database
        self.username = url.username
        self.password = url.password

        if 'virtualcluster' in query or 'virtualCluster' in query or 'vcluster' in query:
            if 'virtualcluster' in query:
                self.vcluster = query.pop('virtualcluster')
            elif 'virtualCluster' in query:
                self.vcluster = query.pop('virtualCluster')
            else:
                self.vcluster = query.pop('vcluster')
        else:
            raise ValueError('url must have `virtualcluster` or `virtualCluster` or `vcluster` parameter.')
        if 'schema' in query:
            self.schema = query.pop('schema')
        if 'magic_token' in query:
            self.magic_token = query.pop('magic_token')

    def log_in_cz(self, username: str, password: str, instance: str) -> str:
        path = "/clickzetta-portal/user/loginSingle"
        login_params = LoginParams(username, password, instance)
        api_repr = login_params.to_api_repr()
        data = json.dumps(api_repr)
        try:
            api_response = requests.post(self.service + path, data=data, headers=HEADERS, timeout=10)
            if api_response.status_code != 200:
                raise requests.exceptions.RequestException(
                    "user:" + login_params.username + " login to clickzetta failed, error:" + api_response.text)
            result = api_response.text
            result_dict = json.loads(result)
            if result_dict['code'] != 0:
                raise requests.exceptions.RequestException(
                    "user:" + login_params.username + " login to clickzetta failed, error:" + result_dict['message'])
            if result_dict['data']['token'] is None:
                raise requests.exceptions.RequestException(
                    "user:" + login_params.username + " login to clickzetta  failed, error: token is None")
            else:
                token = result_dict['data']['token']
                return token
        except requests.exceptions.RequestException:
            raise

    def create_bulkload_stream(self, schema_name: string, table_name: string,
                               options: BulkLoadOptions) -> BulkLoadMetaData:
        create_bulk_load_request = ingestion_pb2.CreateBulkLoadStreamRequest()
        account = ingestion_pb2.Account()
        user_ident = ingestion_pb2.UserIdentifier()
        user_ident.instance_id = self.instance_id
        user_ident.workspace = self.workspace
        user_ident.user_name = self.username
        account.user_ident.CopyFrom(user_ident)
        account.token = self.token
        create_bulk_load_request.account.CopyFrom(account)
        table_identifier = ingestion_pb2.TableIdentifier()
        table_identifier.instance_id = self.instance_id
        table_identifier.workspace = self.workspace
        table_identifier.schema_name = schema_name
        table_identifier.table_name = table_name
        create_bulk_load_request.identifier.CopyFrom(table_identifier)
        if options.operation == BulkLoadOperation.APPEND:
            create_bulk_load_request.operation = ingestion_pb2.BulkLoadStreamOperation.BL_APPEND
        elif options.operation == BulkLoadOperation.UPSERT:
            create_bulk_load_request.operation = ingestion_pb2.BulkLoadStreamOperation.BL_UPSERT
        elif options.operation == BulkLoadOperation.OVERWRITE:
            create_bulk_load_request.operation = ingestion_pb2.BulkLoadStreamOperation.BL_OVERWRITE
        if options.partition_specs is not None:
            create_bulk_load_request.partition_spec = options.partition_specs
        if options.record_keys is not None:
            keys = []
            for key in options.record_keys:
                keys.append(key)
            create_bulk_load_request.record_keys.extend(keys)
        create_bulk_load_request.prefer_internal_endpoint = options.prefer_internal_endpoint
        response = self._gate_way_call(create_bulk_load_request, ingestion_pb2.MethodEnum.CREATE_BULK_LOAD_STREAM_V2)
        response_pb = ParseDict(response, ingestion_pb2.CreateBulkLoadStreamResponse(), ignore_unknown_fields=True)
        self.instance_id = response_pb.info.identifier.instance_id
        bulkload_meta_data = BulkLoadMetaData(response_pb.info.identifier.instance_id, response_pb.info)

        return bulkload_meta_data

    def commit_bulkload_stream(self, instance_id: int, workspace: string, schema_name: string, table_name: string,
                               stream_id: string, execute_workspace: string, execute_vc: string,
                               commit_mode: BulkLoadCommitMode) -> BulkLoadMetaData:
        commit_bulkload_request = ingestion_pb2.CommitBulkLoadStreamRequest()
        account = ingestion_pb2.Account()
        user_ident = ingestion_pb2.UserIdentifier()
        user_ident.instance_id = instance_id
        user_ident.workspace = workspace
        user_ident.user_name = self.username
        account.user_ident.CopyFrom(user_ident)
        account.token = self.token
        commit_bulkload_request.account.CopyFrom(account)
        table_identifier = ingestion_pb2.TableIdentifier()
        table_identifier.instance_id = instance_id
        table_identifier.workspace = workspace
        table_identifier.schema_name = schema_name
        table_identifier.table_name = table_name
        commit_bulkload_request.identifier.CopyFrom(table_identifier)
        commit_bulkload_request.stream_id = stream_id
        commit_bulkload_request.execute_workspace = execute_workspace
        commit_bulkload_request.execute_vc_name = execute_vc
        if commit_mode == BulkLoadCommitMode.COMMIT_STREAM:
            commit_bulkload_request.commit_mode = ingestion_pb2.CommitBulkLoadStreamRequest.CommitMode.COMMIT_STREAM
        elif commit_mode == BulkLoadCommitMode.ABORT_STREAM:
            commit_bulkload_request.commit_mode = ingestion_pb2.CommitBulkLoadStreamRequest.CommitMode.ABORT_STREAM

        response = self._gate_way_call(commit_bulkload_request, ingestion_pb2.MethodEnum.COMMIT_BULK_LOAD_STREAM_V2)
        response_pb = ParseDict(response, ingestion_pb2.CommitBulkLoadStreamResponse(), ignore_unknown_fields=True)
        bulkload_meta_data = BulkLoadMetaData(self.instance_id, response_pb.info)
        return bulkload_meta_data

    def get_bulkload_stream(self, schema_name: string, table_name: string, stream_id: string) -> BulkLoadMetaData:
        get_bulkload_stream_request = ingestion_pb2.GetBulkLoadStreamRequest()
        account = ingestion_pb2.Account()
        user_ident = ingestion_pb2.UserIdentifier()
        user_ident.instance_id = self.instance_id
        user_ident.workspace = self.workspace
        user_ident.user_name = self.username
        account.user_ident.CopyFrom(user_ident)
        account.token = self.token
        get_bulkload_stream_request.account.CopyFrom(account)
        table_identifier = ingestion_pb2.TableIdentifier()
        table_identifier.instance_id = self.instance_id
        table_identifier.workspace = self.workspace
        table_identifier.schema_name = schema_name
        table_identifier.table_name = table_name
        get_bulkload_stream_request.identifier.CopyFrom(table_identifier)
        get_bulkload_stream_request.stream_id = stream_id
        get_bulkload_stream_request.need_table_meta = True
        response = self._gate_way_call(get_bulkload_stream_request, ingestion_pb2.MethodEnum.GET_BULK_LOAD_STREAM_V2)
        response_pb = ParseDict(response, ingestion_pb2.GetBulkLoadStreamResponse(), ignore_unknown_fields=True)
        bulkload_meta_data = BulkLoadMetaData(self.instance_id, response_pb.info)
        return bulkload_meta_data

    def open_bulkload_stream_writer(self, instance_id: int, workspace: string, schema_name: string, table_name: string,
                                    stream_id: string, partition_id: int) -> BulkLoadConfig:
        open_bulkload_stream_request = ingestion_pb2.OpenBulkLoadStreamWriterRequest()
        account = ingestion_pb2.Account()
        user_ident = ingestion_pb2.UserIdentifier()
        user_ident.instance_id = instance_id
        user_ident.workspace = workspace
        user_ident.user_name = self.username
        account.user_ident.CopyFrom(user_ident)
        account.token = self.token
        open_bulkload_stream_request.account.CopyFrom(account)
        table_identifier = ingestion_pb2.TableIdentifier()
        table_identifier.instance_id = instance_id
        table_identifier.workspace = workspace
        table_identifier.schema_name = schema_name
        table_identifier.table_name = table_name
        open_bulkload_stream_request.identifier.CopyFrom(table_identifier)
        open_bulkload_stream_request.stream_id = stream_id
        open_bulkload_stream_request.partition_id = partition_id
        response = self._gate_way_call(open_bulkload_stream_request,
                                       ingestion_pb2.MethodEnum.OPEN_BULK_LOAD_STREAM_WRITER_V2)
        response_pb = ParseDict(response, ingestion_pb2.OpenBulkLoadStreamWriterResponse(), ignore_unknown_fields=True)
        bulkload_config = response_pb.config
        return BulkLoadConfig(bulkload_config)

    def finish_bulkload_stream_writer(self, instance_id: int, workspace: string, schema_name: string,
                                      table_name: string,
                                      stream_id: string, partition_id: int, written_files: list,
                                      written_lengths: list) -> ingestion_pb2.ResponseStatus:
        finish_bulkload_stream_request = ingestion_pb2.FinishBulkLoadStreamWriterRequest()
        account = ingestion_pb2.Account()
        user_ident = ingestion_pb2.UserIdentifier()
        user_ident.instance_id = instance_id
        user_ident.workspace = workspace
        user_ident.user_name = self.username
        account.user_ident.CopyFrom(user_ident)
        account.token = self.token
        finish_bulkload_stream_request.account.CopyFrom(account)
        table_identifier = ingestion_pb2.TableIdentifier()
        table_identifier.instance_id = instance_id
        table_identifier.workspace = workspace
        table_identifier.schema_name = schema_name
        table_identifier.table_name = table_name
        finish_bulkload_stream_request.identifier.CopyFrom(table_identifier)
        finish_bulkload_stream_request.stream_id = stream_id
        finish_bulkload_stream_request.partition_id = partition_id
        finish_bulkload_stream_request.written_files.extend(written_files)
        finish_bulkload_stream_request.written_lengths.extend(written_lengths)
        response = self._gate_way_call(finish_bulkload_stream_request,
                                       ingestion_pb2.MethodEnum.FINISH_BULK_LOAD_STREAM_WRITER_V2)
        response_pb = ParseDict(response, ingestion_pb2.FinishBulkLoadStreamWriterResponse(), ignore_unknown_fields=True)
        return response_pb.status

    def _gate_way_call(self, request, method: ingestion_pb2.MethodEnum):
        path = '/igs/gatewayEndpoint'
        gate_way_request = ingestion_pb2.GatewayRequest()
        gate_way_request.methodEnumValue = method
        gate_way_request.message = MessageToJson(request)

        HEADERS['instanceName'] = self.instance
        HEADERS['X-ClickZetta-Token'] = self.token
        try:
            api_response = requests.post(self.service + path, data=MessageToJson(gate_way_request), headers=HEADERS)
            api_response.encoding = 'utf-8'
            result = api_response.text
            result_dict = json.loads(result)
            if api_response.status_code != 200:
                raise requests.exceptions.RequestException(
                    'gate_way_call return failed code.Error message:' + result_dict['message'])
            result_status = ParseDict(result_dict['status'], ingestion_pb2.GateWayResponseStatus)
            if result_status.code == ingestion_pb2.Code.SUCCESS:
                message_json = json.loads(result_dict['message'])
                internal_result_status = message_json['status']
                if internal_result_status["code"] == "SUCCESS":
                    return json.loads(result_dict['message'])
                else:
                    raise requests.exceptions.RequestException(
                        'gate_way_call return failed code.Error message:' + internal_result_status["error_message"])
            else:
                raise requests.exceptions.RequestException(
                    'gate_way_call return failed code.Error message:' + result_status.message)

        except requests.exceptions.RequestException as request_exception:
            logging.error('gate_way_request error:{}'.format(request_exception))
            raise requests.exceptions.RequestException(
                'gate_way_request error:{}'.format(request_exception))
        except Exception as e:
            logging.error('gate_way_request error:{}'.format(e))
            raise requests.exceptions.RequestException(
                'gate_way_request error:{}'.format(e))

    def pre_process_sql(self, sql):
        queries = split_sql(sql)
        if queries:
            if len(queries) == 1 and self.process_use_cmd(queries[0]):
                return None
            for query in queries[:-1]:
                self.process_use_cmd(query)
        return queries[-1] + "\n;"

    def process_use_cmd(self, sql: str):
        has_processed = True
        sql = re.sub(r'\s+', ' ', sql)
        if sql.lower().startswith("use vcluster "):
            self.vcluster = sql.lower().replace('use vcluster ', '').strip()
        elif sql.lower().startswith('use schema '):
            self.schema = sql.lower().replace('use schema ', '').strip()
        elif sql.lower().startswith("use "):
            self.schema = sql.lower().replace('use ', '').strip()
        else:
            has_processed = False
        return has_processed

    def submit_sql_job(self, token: str, sql: str, job_id: JobID, parameters=None, schema=None) -> QueryResult:
        sql = self.pre_process_sql(sql)
        path = "/lh/submitJob"
        if (not sql) or 'test plain returns' in sql or 'test unicode returns' in sql:
            res = QueryResult({})
            res.data = QueryData(data=[], data_type=QueryDataType.Memory)
            return res
        table = Table(self.workspace, '', self.instance, self.vcluster)
        vc = table.vcluster
        job_type = JobType.SQL_JOB
        logging.info(
            "clickzetta connector submitting job,  id:" + job_id.id)
        job_name = "SQL_JOB"
        user_id = 0
        reqeust_mode = JobRequestMode.HYBRID
        timeout = FIRST_SQL_SUBMIT_TIMEOUT
        job_config = {}
        sdk_job_timeout = 0
        sdk_job_priority = 15
        sql_job_set_prop = {'cz.sql.adhoc.result.type': 'embedded', 'cz.sql.adhoc.default.format': 'arrow'}
        job_timeout_ms = 0
        hints = self.hints if self.hints is not None else {}
        if parameters is not None and len(parameters) != 0:
            if 'hints' in parameters.keys():
                hints = parameters['hints']
            for key in parameters.keys():
                if "%(" + key + ")s" in sql:
                    sql = sql.replace("%(" + key + ")s", str(parameters[key]))
        if len(hints) > 0:
            for key in hints:
                if key == 'sdk.job.timeout':
                    sdk_job_timeout = int(hints[key])
                elif key == 'sdk.job.priority':
                    sdk_job_priority = int(hints[key])
                elif key == 'sdk.query.timeout.ms':
                    job_timeout_ms = int(hints[key])
                else:
                    sql_job_set_prop[key] = hints[key]
        timeout = sdk_job_timeout if 0 < sdk_job_timeout <= timeout else timeout
        sql_config = SQLJobConfig(0, "0", "0", sql_job_set_prop)
        schema_name = ''
        if self.schema is not None:
            schema_name = self.schema
        if schema is not None:
            schema_name = schema
        sql_job = SQLJob(sql_config, table.workspace, schema_name, [sql])
        user_agent = ""

        job_desc = JobDesc(vc, job_type, job_id, job_name, user_id, reqeust_mode, timeout, job_config, sql_job,
                           job_timeout_ms,
                           user_agent, sdk_job_priority)
        job_request = JobRequest(job_desc)
        data = json.dumps(job_request.to_api_repr())
        HEADERS['instanceName'] = table.instance
        HEADERS['X-ClickZetta-Token'] = token
        logging.debug('BEGIN TO SEND REQUEST:' + sql + ' TO CZ SERVER, TIME:' + str(datetime.now()))
        try:
            api_response = self.session.post(self.service + path, data=data, headers=HEADERS)
            if api_response.status_code != 200:
                raise requests.exceptions.RequestException(
                    "submit sql job failed:" + str(api_response.status_code) + api_response.text + ".sql:" + sql)
            api_response.encoding = 'utf-8'
            result = ""
            try:
                result = api_response.text
                result_dict = json.loads(result)
            except Exception as e:
                raise requests.exceptions.RequestException(
                    f"Parsing json data for job id [{job_id}] failed:{e}. raw result is: {result}")
            if int(result_dict['code']) != 200:
                raise requests.exceptions.RequestException(
                    "submit sql job failed:" + str(result_dict))
            get_job_result_dict = self.process_sql_response_with_timeout(sdk_job_timeout, result_dict, job_id,
                                                                         job_timeout_ms)
            logging.debug('GET RESPONSE FROM CZ SERVER FOR REQUEST:' + sql + ' TIME:' + str(datetime.now()))
            query_result = QueryResult(get_job_result_dict)
            if sql.lstrip().upper().startswith('PUT ') or sql.lstrip().upper().startswith('GET '):
                check_volume_result = self.process_volume_sql(token, sql, query_result)
                return check_volume_result
            return query_result
        except Exception as e:
            raise Exception("submit sql job failed:" + str(e))

    def process_volume_sql(self, token: str, sql: str, query_result: QueryResult) -> QueryResult:
        upper_sql = sql.strip().upper()
        outcome = query_result.data.read()
        if len(outcome) != 1:
            raise Exception(f"get volume sql failed, with result: {outcome}")
        outcome_obj = json.loads(outcome[0][0])
        if outcome_obj['status'] == 'FAILED':
            raise Exception(f"{outcome_obj['request']['command']} volume failed: {outcome_obj['error']}")
        if upper_sql.startswith('GET'):
            query_result = self.gen_volume_result(outcome_obj)
            if outcome_obj['status'] == 'CONTINUE' and outcome_obj['nextMarker'] != '':
                sql = 'set cz.sql.volume.file.transfer.next.marker=nextMarker;' + sql
                job_id = JobID(self._format_job_id(), self.workspace, DEFAULT_INSTANCE_ID)
                next_result = self.submit_sql_job(token=token, sql=sql, job_id=job_id)
                return self._merge_query_result(query_result, next_result)
            return query_result
        elif upper_sql.startswith("PUT"):
            if outcome_obj['status'] == 'CONTINUE':
                sql = self._gen_new_put_sql(outcome_obj)
                job_id = JobID(self._format_job_id(), self.workspace, DEFAULT_INSTANCE_ID)
                return self.submit_sql_job(token=token, sql=sql, job_id=job_id)
            else:
                return self.gen_volume_result(outcome_obj)

    def gen_volume_result(self, outcome: Any):
        result_list = []
        if outcome['request']['command'].upper() == 'GET':
            volume_files = self.get_volume_files(outcome)
            for i in range(len(volume_files)):
                response = requests.get(outcome['ticket']['presignedUrls'][i], stream=True)
                local_path = os.path.join(outcome['request']['localPaths'][0], volume_files[i])
                if not os.path.exists(os.path.dirname(local_path)):
                    os.makedirs(os.path.dirname(local_path))
                with open(local_path, 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                logging.info(f"get volume success, volume_path:{volume_files[i]}, local_path:{local_path}")
                res = [volume_files[i], local_path, os.path.getsize(local_path)]
                result_list.append(res)
        elif outcome['request']['command'].upper() == 'PUT':
            if outcome['status'] == 'SUCCESS':
                for i in range(len(outcome['ticket']['presignedUrls'])):
                    local_path = outcome['request']['localPaths'][i]
                    if not os.path.exists(local_path):
                        raise Exception(f"put volume failed, local_path:{local_path} not exists")
                    with open(local_path, 'rb') as f:
                        requests.put(outcome['ticket']['presignedUrls'][i], data=f.read(), headers={})
                    logging.info(f"put volume success, local_path:{local_path}")
                    volume_file = ''
                    if 'file' in outcome['request']:
                        volume_file = outcome['request']['file']
                    else:
                        if 'subdirectory' in outcome['request']:
                            path = outcome['request']['subdirectory']
                            path = path if path[-1] == '/' else path + '/'
                            volume_file = path + os.path.basename(local_path)
                        else:
                            volume_file = os.path.basename(local_path)
                    res = [local_path, volume_file, os.path.getsize(local_path)]
                    result_list.append(res)
        query_result = QueryResult({})
        query_result.data = QueryData(data=result_list, data_type=QueryDataType.Memory)
        return query_result

    def get_volume_files(self, outcome: Any):
        volume_files = []
        if 'file' in outcome['request']:
            volume_files.append(os.path.basename(os.path.abspath(outcome['request']['file'])))
        else:
            for url in outcome['ticket']['presignedUrls']:
                parsed_url = urlparse(unquote(url))
                path_parts = parsed_url.path.split('/')
                volume_files.append(path_parts[-1])
        return volume_files

    def process_sql_response_with_timeout(self, sdk_job_timeout, result_dict, job_id, job_timeout_ms):
        if ('status' in result_dict and 'errorCode' in result_dict['status'] and
                result_dict['status']['errorCode'] == 'CZLH-60010'):
            raise Exception("submit sql job:" + str(job_id.id) + " timeout after " + str(job_timeout_ms)
                            + " ms. killed by lakehouse")
        if 0 < sdk_job_timeout <= FIRST_SQL_SUBMIT_TIMEOUT:
            # check resultSet first, then check status
            if 'resultSet' in result_dict:
                if 'data' in result_dict['resultSet']:
                    if 'data' in result_dict['resultSet']['data']:
                        return result_dict
            if 'status' in result_dict:
                if 'state' in result_dict['status']:
                    status = result_dict['status']['state']
                    if status == "QUEUEING" or status == "SETUP" or status == "RUNNING":
                        raise Exception("submit sql job:" + str(job_id.id) + " timeout after " + str(
                            FIRST_SQL_SUBMIT_TIMEOUT) + " seconds. killed by sdk.")
                    else:
                        return result_dict
            else:
                raise Exception("submit sql job:" + str(job_id.id) + " failed, root: " + str(result_dict))

        elif sdk_job_timeout > FIRST_SQL_SUBMIT_TIMEOUT:
            return self.wait_job_finished(result_dict, job_id, HEADERS, sdk_job_timeout - FIRST_SQL_SUBMIT_TIMEOUT)
        else:
            return self.wait_job_finished(result_dict, job_id, HEADERS, HYBRID_SQL_TIMEOUT - FIRST_SQL_SUBMIT_TIMEOUT)

    def close(self):
        pass

    def cancel_job(self, job_id: JobID, headers):
        account = clickzetta.enums.ClickZettaAccount(0)
        cancel_job_request = clickzetta.enums.CancelJobRequest(account, job_id, '', False)
        path = '/lh/cancelJob'
        data = json.dumps(cancel_job_request.to_api_repr())
        try:
            self.session.post(self.service + path, data=data, headers=headers)
        except Exception as e:
            logging.error('clickzeta connector cancel job error:{}'.format(e))

    def check_if_job_timeout(self, sdk_job_timeout, sql_job_start_time, job_id, headers):
        if sdk_job_timeout > 0:
            if (datetime.now() - sql_job_start_time).seconds > sdk_job_timeout:
                self.cancel_job(job_id, headers)
                return True
        return False

    def get_job_profile(self, job_id: string):
        result_dict = self._get_job(job_id, clickzetta.enums.JobRequestType.PROFILE)
        return result_dict

    def get_job_result(self, job_id: string):
        result_dict = self._get_job(job_id, clickzetta.enums.JobRequestType.RESULT)
        return result_dict

    def get_job_progress(self, job_id: string):
        result_dict = self._get_job(job_id, clickzetta.enums.JobRequestType.PROGRESS)
        return result_dict

    def get_job_summary(self, job_id: string):
        result_dict = self._get_job(job_id, clickzetta.enums.JobRequestType.SUMMARY)
        return result_dict

    def get_job_plan(self, job_id: string):
        result_dict = self._get_job(job_id, clickzetta.enums.JobRequestType.PLAN)
        return result_dict

    def _get_job(self, job_id: string, type: string):
        HEADERS['instanceName'] = self.instance
        HEADERS['X-ClickZetta-Token'] = self.token
        id = JobID(job_id, self.workspace, DEFAULT_INSTANCE_ID)
        account = clickzetta.enums.ClickZettaAccount(0)
        get_job_request = clickzetta.enums.GetJobRequest(account, id, 0, '')
        path = '/lh/getJob'
        try:
            api_request = clickzetta.enums.APIGetJobRequest(get_job_request, '', type)
            data = json.dumps(api_request.to_api_repr())
            api_response = self.session.post(self.service + path, data=data, headers=HEADERS)
            result = api_response.text
            result_dict = json.loads(result)
            if int(result_dict['code']) != 200:
                raise requests.exceptions.RequestException(f"Get job:{id.id} {type} failed:{result_dict}")
            return result_dict
        except AttributeError as e:
            raise requests.exceptions.RequestException(f"Get job:{id.id} {type} failed:{e}, Only supports：result/progress/summary/plan/profile.")
        except Exception as e:
            raise Exception(f"Get job:{id.id} {type} failed:{e}")

    def is_job_finished(self, result_dict):
        if 'status' in result_dict:
            if 'state' in result_dict['status']:
                status = result_dict['status']['state']
                if status == "SUCCEED" or status == 'FAILED':
                    return True
                elif status == "QUEUEING" or status == "SETUP" or status == "RUNNING":
                    if 'resultSet' in result_dict:
                        if 'data' in result_dict['resultSet']:
                            if 'data' in result_dict['resultSet']['data']:
                                return True
                        elif 'location' in result_dict['resultSet']:
                            return True
        return False

    def wait_job_finished(self, result_dict, job_id: JobID, headers, sdk_job_timeout=0):
        if 'status' in result_dict:
            if 'state' in result_dict['status']:
                if not self.is_job_finished(result_dict):
                    account = clickzetta.enums.ClickZettaAccount(0)
                    get_job_result_request = clickzetta.enums.GetJobRequest(account, job_id, 0, '')
                    api_request = clickzetta.enums.APIGetJobRequest(get_job_result_request, '', clickzetta.enums.JobRequestType.RESULT)
                    path = '/lh/getJob'
                    data = json.dumps(api_request.to_api_repr())
                    sql_job_start_time = datetime.now()
                    while True:
                        if self.check_if_job_timeout(sdk_job_timeout, sql_job_start_time, job_id, headers):
                            logging.error("clickzetta sql job:" + str(job_id.id) + " timeout after " + str(
                                sdk_job_timeout) + " seconds. killed by sdk.")
                            raise Exception("clickzetta sql job:" + str(job_id.id) + " timeout after " + str(
                                sdk_job_timeout) + " seconds. killed by sdk.")
                        get_job_result_response = self.session.post(self.service + path, data=data, headers=headers)
                        result = get_job_result_response.text
                        get_job_result_dict = json.loads(result)
                        if int(get_job_result_dict['code']) != 200:
                            raise requests.exceptions.RequestException(
                                "Get async sql job:" + str(job_id.id) + " result failed:" + get_job_result_dict)
                        if 'status' in get_job_result_dict:
                            if 'state' in get_job_result_dict['status']:
                                if get_job_result_dict['status']['state'] == 'SUCCEED' or \
                                        get_job_result_dict['status']['state'] == 'FAILED' or \
                                        get_job_result_dict['status']['state'] == 'CANCELLED':
                                    logging.info(
                                        "Get async sql job:" + str(job_id.id) + " result successfully.")
                                    return get_job_result_dict
                                else:
                                    logging.info("Get async sql job:" + str(
                                        job_id.id) + " result pending, retry after 10 seconds.")
                                    time.sleep(3)
                            else:
                                raise Exception(
                                    "Get async sql job:" + str(
                                        job_id.id) + " result failed, http response job state is not exist.")
                        else:
                            raise Exception(
                                "Get async sql job:" + str(
                                    job_id.id) + " result failed, http response job status is not exist.")

                else:
                    return result_dict
            else:
                raise Exception("Execute sql job:" + str(job_id.id) + " failed, http response job state is not exist.")
        else:
            raise Exception("Execute sql job:" + str(job_id.id) + " failed, http response job status is not exist.")

    def _format_job_id(self):
        unique_id = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        format_unique_id = unique_id.replace('-', '').replace(':', '').replace('.', '').replace(' ', '') \
                           + str(random.randint(10000, 99999))
        return format_unique_id

    def generate_job_id(self):
        return self._format_job_id()

    def get_table_names(self, schema: str):
        job_id = JobID(self._format_job_id(), self.workspace, DEFAULT_INSTANCE_ID)
        query_result = self.submit_sql_job(token=self.token, sql='show tables;', schema=schema, job_id=job_id)
        query_data = query_result.data.read()
        table_names = []
        for entry in query_data:
            table_names.append(entry[1])

        return table_names

    def get_schemas(self):
        job_id = JobID(self._format_job_id(), self.workspace, DEFAULT_INSTANCE_ID)
        query_result = self.submit_sql_job(token=self.token, sql='show schemas;', job_id=job_id)
        query_data = query_result.data.read()
        schema_names = []
        for entry in query_data:
            schema_names.append(entry[0])

        return schema_names

    def get_columns(self, table_name: str, schema: str):
        job_id = JobID(self._format_job_id(), self.workspace, DEFAULT_INSTANCE_ID)
        if '.' in table_name:
            schema = table_name.split('.')[0]
            table_name = table_name.split('.')[1]
        query_result = self.submit_sql_job(token=self.token,
                                           sql='select * from ' + schema + '.' + table_name + ' limit 1;',
                                           job_id=job_id)
        schema = query_result.schema

        return schema

    def has_table(self, full_table_name: str):
        job_id = JobID(self._format_job_id(), self.workspace, DEFAULT_INSTANCE_ID)
        try:
            query_result = self.submit_sql_job(token=self.token, sql='show create table ' + full_table_name + ';',
                                               job_id=job_id)
        except Exception as e:
            return False
        if query_result.state != 'FAILED':
            return True
        else:
            return False

    def _merge_query_result(self, res1: QueryResult, res2: QueryResult):
        new_data = res1.data.data + res2.data.data
        res1.data = QueryData(data=new_data, data_type=QueryDataType.Memory)
        return res1

    def _gen_new_put_sql(self, outcome_obj):
        prefix = ''
        option_part = ''
        for option in outcome_obj['request']['options']:
            if option['name'].upper() == 'SOURCE_PREFIX':
                prefix = option['value']
            option_part += ' ' + option['name'] + ' = ' + option['value']
        requested_paths = outcome_obj['request']['localPaths']
        resolved_paths = []
        for p in requested_paths:
            resolved_paths += resolve_local_path(p)
        if len(resolved_paths) == 0:
            raise Exception('No local file to put into volume')
        sql = 'PUT '
        sql += ", ".join(f"'{p}'" for p in resolved_paths)
        sql += ' TO ' + outcome_obj['request']['volumeIdentifier']
        if 'subdirectory' in outcome_obj['request']:
            sql += " SUBDIRECTORY '" + outcome_obj['request']['subdirectory'] + "'"
        elif 'file' in outcome_obj['request']:
            sql += " FILE '" + outcome_obj['request']['file'] + "'"
        sql += option_part
        sql += ';'
        return sql


def _add_server_timeout_header(headers: Optional[Dict[str, str]], kwargs):
    timeout = kwargs.get("timeout")
    if timeout is not None:
        if headers is None:
            headers = {}
        headers[TIMEOUT_HEADER] = str(timeout)

    if headers:
        kwargs["headers"] = headers

    return kwargs
