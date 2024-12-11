from typing import Generator

import numpy
from numpy.ma.testutils import assert_equal

import pytest

from clickzetta.dbapi import Connection


@pytest.mark.skip("clickzetta-connector does not support timezone")
def test_timestamp_type(it_conn: Generator[Connection, None, None]):
    """Tests the timestamp type with different timezones.
    If the time zone changes due to changes in the it_conn configuration, just ignore this test.
    """
    it_conn._client._pure_arrow_decoding = True
    # Should be changed to {'hints': {}} if the timezone is return by the server
    my_param = {'hints': {'cz.sql.timezone': 'Asia/Shanghai'}}
    sql = """select timestamp "2024-09-05 03:07:58", timestamp_ntz "2024-09-05 03:07:58", timestamp_ltz"2024-09-05 03:07:58" """
    cursor = it_conn.cursor()
    cursor.execute(sql, parameters=my_param)
    result = cursor.fetchall()
    assert result[0][0].strftime("%Y-%m-%d %H:%M:%S") == "2024-09-05 03:07:58"
    # The timestamp_ntz is always in UTC. It will -8 hours from the timestamp_ltz 'Asia/Shanghai'
    assert result[0][1].strftime("%Y-%m-%d %H:%M:%S") == "2024-09-05 03:07:58"
    assert result[0][2].strftime("%Y-%m-%d %H:%M:%S") == "2024-09-05 03:07:58"


@pytest.mark.skip("clickzetta-connector does not support timezone")
def test_timestamp_type_with_file_hint(it_conn: Generator[Connection, None, None]):
    it_conn._client._pure_arrow_decoding = True
    # Should be changed to {'hints': {}} if the timezone is return by the server
    my_param = {'hints': {'cz.sql.timezone': 'Europe/Berlin'}}
    my_param['hints']['cz.sql.adhoc.result.type'] = 'file'
    sql = """select timestamp "2024-09-05 03:07:58", timestamp_ntz "2024-09-05 03:07:58", timestamp_ltz"2024-09-05 03:07:58" """
    cursor = it_conn.cursor()
    cursor.execute(sql, parameters=my_param)
    result = cursor.fetchall()
    assert result[0][0].strftime("%Y-%m-%d %H:%M:%S") == '2024-09-04 21:07:58'
    assert result[0][1].strftime("%Y-%m-%d %H:%M:%S") == '2024-09-05 03:07:58'
    assert result[0][2].strftime("%Y-%m-%d %H:%M:%S") == '2024-09-04 21:07:58'


@pytest.mark.integration_test
def test_float_double_type(it_conn: Generator[Connection, None, None]):
    with it_conn as conn:
        my_param = {'hints': {}}
        cursor = conn.cursor()
        cursor.execute("""select * from values 
            (float(1.0), float(1.0), float(1.2), float(0.1), float(0.1), float(0.0), float(0.0)),
            (double(1.0), double(1.0), double(1.2), double(0.1), double(0.1), double(0.0), double(0.0))
            """, parameters=my_param)
        result = cursor.fetchall()
        assert len(result) == 2
        excepted = [(1.0, 1.0, 1.2, 0.1, 0.1, 0.0, 0.0), (1.0, 1.0, 1.2, 0.1, 0.1, 0.0, 0.0)]
        for i in range(len(result)):
            for j in range(len(result[i])):
                assert str(numpy.float32(result[i][j])) == str(excepted[i][j])


@pytest.mark.integration_test
def test_data_types(it_conn: Generator[Connection, None, None]):
    with it_conn as conn:
        my_param = {'hints': {}}
        cursor = conn.cursor()
        cursor.execute("""drop table if exists test_datatype_smoke;""", parameters=my_param)
        sql = """CREATE TABLE if not exists test_datatype_smoke (
            c_bigint BIGINT,
            c_boolean BOOLEAN,
            c_binary BINARY,
            c_char CHAR,
            c_date DATE,
            c_decimal DECIMAL(20, 6),
            c_double DOUBLE,
            c_float FLOAT,
            c_int INT,
            c_smallint SMALLINT,
            c_string STRING,
            c_timestamp TIMESTAMP,
            c_tinyint TINYINT,
            c_array ARRAY<STRUCT<a: INT, b: STRING>>,
            c_map MAP<STRING, STRING>,
            c_struct STRUCT<a: INT, b: STRING, c: DOUBLE>,
            c_varchar VARCHAR(1024),
            c_json JSON
        );"""
        cursor.execute(sql, parameters=my_param)
        cursor.execute(
            """insert into test_datatype_smoke values(1,false,x'1','1',date'2024-09-14',1bd,1d,1f,1,1,'1',
            timestamp '2024-09-19 12:16:55',1,array(struct(1,'a')),map(1,'2'),struct(1,'a',0.1d),'1',json'{\"a\":1,\"b\":\"a\"}');""",
            parameters=my_param)
        cursor.execute("""select * from test_datatype_smoke;""", parameters=my_param)
        result = cursor.fetchall()
        assert len(result) == 1
        assert result[0][0] == 1
        assert result[0][1] is False
        assert result[0][2] == b'\x01'
        assert result[0][3] == '1'
        assert result[0][4].strftime("%Y-%m-%d") == '2024-09-14'
        assert result[0][5] == 1.0
        assert result[0][6] == 1.0
        assert result[0][7] == 1.0
        assert result[0][8] == 1
        assert result[0][9] == 1
        assert result[0][10] == '1'
        # assert result[0][11].strftime("%Y-%m-%d %H:%M:%S") == '2024-09-19 12:16:55'
        assert result[0][11].strftime("%Y-%m-%d %H:%M:%S") == '2024-09-19 04:16:55'
        assert result[0][12] == 1
        assert result[0][13] == [{'a': 1, 'b': 'a'}]
        assert result[0][14] == [('1', '2')]
        assert result[0][15] == {'a': 1, 'b': 'a', 'c': 0.1}
        assert result[0][16] == '1'
        assert result[0][17] == '{"a":1,"b":"a"}'
        cursor.execute("""drop table if exists test_datatype_smoke;""", parameters=my_param)


@pytest.mark.skip("clickzetta-connector does not support _pure_arrow_decoding")
def test_none_and_nan_type(it_conn: Generator[Connection, None, None]):
    if not it_conn:
        pytest.skip("skipping integration test because config file not found")
    with it_conn as conn:
        conn._client._pure_arrow_decoding = True
        cursor = conn.cursor()
        cursor.execute(
            ' SELECT CASE WHEN a is NULL THEN CAST(5 AS INT) WHEN a = 1 THEN CAST(6 AS INT) ELSE NULL END AS `a` FROM '
            '( SELECT col1 AS `a` FROM VALUES (CAST(NULL AS INT)), (CAST(2 AS INT)), (CAST(1 AS INT)), (CAST(3 AS INT))'
            ', (CAST(NULL AS INT)))')
        result = cursor.fetchall()
        # _pure_arrow_decoding fixed the bug that None will return NaN
        assert_equal(str(result), "[(5,), (None,), (6,), (None,), (5,)]")

        cursor.execute("SELECT ACOSH(-1)")
        result = cursor.fetchall()
        assert_equal(str(result), '[(nan,)]')


@pytest.mark.integration_test
def test_interval_type(it_conn: Generator[Connection, None, None]):
    if not it_conn:
        pytest.skip("skipping integration test because config file not found")
    with it_conn as conn:
        conn._client._pure_arrow_decoding = True
        cursor = conn.cursor()
        try:
            cursor.execute(
                "select interval 7 year, interval 7 month, interval 7 day, interval 7 hour, interval 7 minute, "
                "interval 7 second, interval 7 week")
        except Exception as e:
            assert "Datatype not supported" in str(e)
        cursor.execute(
            "select interval 7 day, interval 7 hour, interval 7 minute, interval 7 second, interval 7 week")
        result = cursor.fetchall()
        assert_equal(str(result),
                     "[(MonthDayNano(months=0, days=7, nanoseconds=0), MonthDayNano(months=0, days=0, nanoseconds=25200000000000), MonthDayNano(months=0, days=0, nanoseconds=420000000000), MonthDayNano(months=0, days=0, nanoseconds=7000000000), MonthDayNano(months=0, days=49, nanoseconds=0))]")


@pytest.mark.skip("Wait for release to UAT")
def test_interval_type(it_conn: Generator[Connection, None, None]):
    if not it_conn:
        pytest.skip("skipping integration test because config file not found")
    with it_conn as conn:
        conn._client._pure_arrow_decoding = True
        cursor = conn.cursor()
        cursor.execute("SELECT vector(1, 2, 3)")
        result = cursor.fetchall()
        assert_equal(result[0][0], "[1,2,3]")
