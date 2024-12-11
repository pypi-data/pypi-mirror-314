from logging import getLogger
import time
from clickzetta.client import Client
from clickzetta.bulkload.bulkload_enums import BulkLoadMetaData, BulkLoadCommitOptions, BulkLoadState, BulkLoadCommitMode
from clickzetta.bulkload.bulkload_writer import BulkLoadWriter

_logger = getLogger(__name__)

class BulkLoadStream:
    def __init__(self, meta_data: BulkLoadMetaData, client: Client,
                 commit_options: BulkLoadCommitOptions=None):
        self.meta_data = meta_data
        self.client = client
        self.commit_options = commit_options
        self.closed = False

    def get_stream_id(self):
        return self.meta_data.get_stream_id()

    def get_operation(self):
        return self.meta_data.get_operation()

    def get_stream_state(self):
        return self.meta_data.get_state()

    def get_sql_error(self):
        return self.meta_data.get_sql_error_msg()

    def get_schema(self):
        return self.meta_data.get_schema_name()

    def get_table(self):
        return self.meta_data.get_table()

    def get_record_keys(self):
        return self.meta_data.get_record_keys()

    def get_partition_specs(self):
        return self.meta_data.get_partition_specs()

    def open_writer(self, partition_id: int):
        config = self.client.open_bulkload_stream_writer(self.meta_data.get_instance_id(),
                                                         self.meta_data.get_workspace(),
                                                         self.meta_data.get_schema_name(),
                                                         self.meta_data.get_table_name(),
                                                         self.meta_data.get_stream_id(), partition_id)

        return BulkLoadWriter(self.client, self.meta_data, config, partition_id)

    def commit(self, options: BulkLoadCommitOptions=None):
        if self.closed:
            return
        _logger.info("Committing BulkLoadStream:" + self.meta_data.get_stream_id())
        if options is None:
            options = self.commit_options
            if options is None:
                raise ValueError(f'No commit option specified')
        self.client.commit_bulkload_stream(self.meta_data.get_instance_id(), self.meta_data.get_workspace(),
                                           self.meta_data.get_schema_name(), self.meta_data.get_table_name(),
                                           self.meta_data.get_stream_id(), options.workspace, options.vc,
                                           BulkLoadCommitMode.COMMIT_STREAM)

        state = BulkLoadState.COMMIT_SUBMITTED
        sql_error_msg = ''
        # commit waiting max time is 5 hours.so try to get result every 10s for 1800 times.
        for try_time in range(1800):
            current_stream = BulkLoadStream(self.client.get_bulkload_stream(self.meta_data.get_schema_name(),
                                                                            self.meta_data.get_table_name(),
                                                                            self.meta_data.get_stream_id()),
                                            self.client)
            state = current_stream.get_stream_state()
            sql_error_msg = current_stream.get_sql_error()
            _logger.info(
                "Get BulkLoadStream:" + self.meta_data.get_stream_id() + ", state:" + state.name + ",time:" + str(
                    try_time))
            if state == BulkLoadState.COMMIT_SUCCESS or state == BulkLoadState.COMMIT_FAILED:
                break
            else:
                time.sleep(2)
        if state != BulkLoadState.COMMIT_SUCCESS:
            _logger.error(
                "BulkLoadStream:" + self.get_stream_id() + " sync commit failed or timeout with state:" + state.name
                + " with error:" + sql_error_msg)
            raise IOError(
                "BulkLoadStream:" + self.get_stream_id() + " sync commit failed or timeout with state:" + state.name
                + " with error:" + sql_error_msg)
        self.closed = True

    def abort(self):
        _logger.info("Aborting BulkLoadStream:" + self.meta_data.get_stream_id())
        ret = self.client.commit_bulkload_stream(self.meta_data.get_instance_id(), self.meta_data.get_workspace(),
                                                 self.meta_data.get_schema_name(), self.meta_data.get_table_name(),
                                                 self.meta_data.get_stream_id(), '', '',
                                                 BulkLoadCommitMode.ABORT_STREAM)
        if ret.get_state() != BulkLoadState.ABORTED:
            raise IOError(
                "BulkLoadStream:" + self.get_stream_id() + " abort failed ")
        self.closed = True

    def close(self):
        if self.closed:
            return
        else:
            self.commit()