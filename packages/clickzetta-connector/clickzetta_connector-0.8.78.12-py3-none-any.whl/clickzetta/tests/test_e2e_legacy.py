# tests extracted from test_bulkload_writer.py
import pytest
from numpy.ma.testutils import assert_equal
from sqlalchemy import create_engine, text

from clickzetta.bulkload.bulkload_enums import BulkLoadOptions, BulkLoadOperation, BulkLoadCommitOptions
from clickzetta.dbapi import Connection


@pytest.mark.integration_test
def test_query_with_magic_token(it_conn_url):
    magic_token = "eyJhbGciOiJIUzI1Ni.eyJhY2NvdW50SWQiOjExMTAxMSwidGVuYW50SWQiOjExMTAxMSwidXNlck5hbWUiOiJTRF9kZW1vIiwidXNlcklkIjoxMDA4MTQ5LCJpYXQiOjE2OTI4NjAyMDMsImV4cCI6MTY5MzExOTQwM30.HP7JN8QLyPOLF3gs_tmEmGQtmd0yTo77h2TIPEc0ZwA"
    engine = create_engine(
        f"{it_conn_url}&magic_token={magic_token}"
    )
    assert_equal(engine.dialect.magic_token, magic_token)

    with engine.connect() as conn:
        conn: Connection = conn.connection.connection
        assert_equal(conn._client.magic_token, magic_token)


def test_url_protocol(it_conn_url):
    protocol = "http"
    engine = create_engine(
        f"{it_conn_url}&protocol={protocol}"
    )
    assert_equal(engine.dialect.protocol, protocol)

    with engine.connect() as conn:
        conn: Connection = conn.connection.connection
        assert_equal(conn._client.protocol, protocol)


def test_repeat_column_names(it_conn_url):
    engine = create_engine(it_conn_url)

    sql = text(
        "SELECT DATE_FORMAT(NOW(),'HH:mm:ss'), DATE_FORMAT(NOW(),'HH:mm:ss'), DATE_FORMAT(NOW(),'HH:mm:ss');"
    )

    with engine.connect() as conn:
        cursor = conn.execute(sql)
        results = cursor.fetchall()
        row = results[0]
        assert row[0] == row[1] == row[2]



def test_fetchone(it_conn):
    with it_conn as conn:
        cursor = conn.cursor()
        sql = "select * from values('1', '1'), ('2', '2');"
        cursor.execute(sql)
        results = cursor.fetchone()
        for col in results:
            assert_equal('1', col)


def test_get_job_profile(it_conn):
    with it_conn as conn:
        cursor = conn.cursor()
        sql = "select * from values('1', '1'), ('2', '2');"
        cursor.execute(sql)
        results = cursor.fetchall()
        count = 0
        print(results)
        for r in results:
            count += 1
            print(count)
            print(r)
        print(conn.get_job_profile(cursor.job_id))
