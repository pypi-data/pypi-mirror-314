import pytest
from numpy.ma.testutils import assert_equal
from sqlalchemy import create_engine, text

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


@pytest.mark.integration_test
def test_url_protocol(it_conn_url):
    protocol = "http"
    engine = create_engine(
        f"{it_conn_url}&protocol={protocol}"
    )
    assert_equal(engine.dialect.protocol, protocol)

    with engine.connect() as conn:
        conn: Connection = conn.connection.connection
        assert_equal(conn._client.protocol, protocol)


@pytest.mark.integration_test
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


if __name__ == '__main__':
    pytest.main(['-vv', 'test_sqlalchemy.py'])
