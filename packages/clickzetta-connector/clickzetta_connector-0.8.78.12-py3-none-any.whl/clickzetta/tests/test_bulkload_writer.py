import random
from decimal import Decimal
from typing import Generator, NamedTuple

import pytest
from google.protobuf.json_format import MessageToDict, ParseDict

from clickzetta.bulkload.bulkload_enums import *
from clickzetta.session import Session
from clickzetta.tests import ConnectParams


class _TempTable(NamedTuple):
    name: str
    schema: str
    workspace: str
    vcluster: str


def _generate_temp_table(conn, conn_params, ddl_schema, partitioned_by: str = ""):
    table_name = "temp_" + "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(16)
    )
    conn.cursor().execute(f"create table {table_name} ({ddl_schema}) {partitioned_by}")
    yield _TempTable(
        table_name,
        conn_params.schema,
        conn_params.workspace,
        conn_params.vcluster,
    )
    conn.cursor().execute(f"drop table {table_name}")


@pytest.fixture
def temp_table(
    it_conn, it_connect_params: ConnectParams
) -> Generator[_TempTable, None, None]:
    yield from _generate_temp_table(
        it_conn,
        it_connect_params,
        "id int, month string, amount int, cost decimal(10,2)",
    )


@pytest.fixture
def temp_pt_table(
    it_conn, it_connect_params: ConnectParams
) -> Generator[_TempTable, None, None]:
    yield from _generate_temp_table(
        it_conn,
        it_connect_params,
        "id int, month string, amount int, cost decimal(10,2)",
        "partitioned by (pt string)",
    )


@pytest.mark.integration_test
class TestBulkLoad:
    def test_bulkload_config(self):
        writer_config = ingestion_pb2.BulkLoadStreamWriterConfig()
        writer_config.max_num_rows_per_file = 100
        writer_config.max_size_in_bytes_per_file = 200
        mgs_dict = MessageToDict(writer_config)
        protobuf_msg = ParseDict(mgs_dict, ingestion_pb2.BulkLoadStreamWriterConfig())
        print(protobuf_msg.max_num_rows_per_file)

    def test_bulkload_basic(self, it_conn, temp_table: _TempTable):
        bulkload_stream = it_conn.create_bulkload_stream(
            schema=temp_table.schema, table=temp_table.name
        )
        writer = bulkload_stream.open_writer(0)
        for index in range(10):
            row = writer.create_row()
            row.set_value("id", index)
            row.set_value("month", "January")
            row.set_value("amount", 45)
            row.set_value("cost", 113.56)
            writer.write(row)
        writer.close()
        bulkload_stream.commit()
        bulkload_stream.close()

        cursor = it_conn.cursor()
        cursor.execute(f"SELECT * FROM {temp_table.schema}.{temp_table.name};")
        result = cursor.fetchall()
        assert len(result) == 10
        for index, row in enumerate(cursor.fetchall()):
            assert row == (index, "January", 45, Decimal("113.56"))

    def test_get_bulkload_stream(self, it_conn, temp_table: _TempTable):
        stream1 = it_conn.create_bulkload_stream(
            schema=temp_table.schema,
            table=temp_table.name,
            operation=BulkLoadOperation.OVERWRITE,
        )
        stream2 = it_conn.get_bulkload_stream(
            schema=temp_table.schema,
            table=temp_table.name,
            stream_id=stream1.get_stream_id(),
        )
        assert stream1.get_stream_id() == stream2.get_stream_id()

        writer1 = stream1.open_writer(1)
        row = writer1.create_row()
        row.set_value("id", 1)
        row.set_value("month", "January")
        row.set_value("amount", 45)
        row.set_value("cost", 113.56)
        writer1.write(row)
        writer1.close()

        writer2 = stream2.open_writer(2)
        row = writer2.create_row()
        row.set_value("id", 2)
        row.set_value("month", "Feb")
        row.set_value("amount", 67)
        row.set_value("cost", 561.13)
        writer2.write(row)
        writer2.close()

        stream1.commit()
        cur = it_conn.cursor()
        cur.execute(
            "select id, month, amount, cost "
            f"from {temp_table.schema}.{temp_table.name} "
            "order by id asc;"
        )
        rs = cur.fetchall()
        cur.close()
        assert len(rs) == 2
        assert rs[0] == (1, "January", 45, Decimal("113.56"))
        assert rs[1] == (2, "Feb", 67, Decimal("561.13"))

    def test_bulkload_distributed_writer(self, it_conn_url, temp_table: _TempTable):
        config = {"url": it_conn_url}
        session = Session.builder.configs(config).create()
        bulkload_config = BulkLoadOptions(BulkLoadOperation.APPEND, None, None)
        driver_bulkload_stream = session.create_bulkload_stream(
            temp_table.schema, temp_table.name, bulkload_config
        )
        stream_id = driver_bulkload_stream.get_stream_id()
        executor_stream = session.create_bulkload_stream(
            temp_table.schema, temp_table.name, bulkload_config
        )
        writer_list = []
        for index in range(3):
            writer_list.append(executor_stream.open_writer(index))

        for writer in writer_list:
            row = writer.create_row()
            row.set_value("id", random.randint(1, 1000))
            row.set_value("month", "January")
            row.set_value("amount", 45)
            row.set_value("cost", 113.56)
            writer.write(row)

        for writer in writer_list:
            writer.close()
        commit_options = BulkLoadCommitOptions(
            temp_table.workspace, temp_table.vcluster
        )
        executor_stream.commit(commit_options)
        executor_stream.close()
        driver_bulkload_stream.commit(commit_options)
        driver_bulkload_stream.close()
        session.close()
