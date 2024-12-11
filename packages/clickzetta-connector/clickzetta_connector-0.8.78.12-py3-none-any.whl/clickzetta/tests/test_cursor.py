from random import choice
import random
import string
from typing import Generator
import pytest
import datetime
from decimal import Decimal
from clickzetta.dbapi import Connection

TEMP_OBJECT_NAME_PREFIX = "clickzetta_temp_"


def random_name_for_temp_object() -> str:
    return f"{TEMP_OBJECT_NAME_PREFIX}table_{generate_random_alphanumeric().lower()}"


ALPHANUMERIC = string.digits + string.ascii_lowercase


def generate_random_alphanumeric(length: int = 10) -> str:
    return "".join(choice(ALPHANUMERIC) for _ in range(length))


def random_alphanumeric_str(n: int):
    return "".join(
        random.choice(
            string.ascii_uppercase + string.ascii_lowercase + string.digits
        )
        for _ in range(n)
    )


@pytest.mark.skip("clickzetta-connector does not support bind parameters")
def test_batch_insert(it_conn: Generator[Connection, None, None]):
    """Tests columnless bulk insert into a new table from a collected result of 'SELECT *'"""
    if not it_conn:
        pytest.skip("skipping integration test because config file not found")
    with it_conn as conn:
        cursor = conn.cursor()
        table = random_name_for_temp_object()
        cursor.execute(f'create table {table}(`a` string, `b` string)')
        data = [
            [random_alphanumeric_str(230), random_alphanumeric_str(230)]
        ]
        cursor.executemany(f'INSERT INTO {table}(`a`, `b`) VALUES (?, ?)', data)
        cursor.execute(f'SELECT * FROM {table}')
        result = cursor.fetchall()
        print("count:" + str(len(result)))
        assert len(result) == 1
        assert result[0][0] == data[0][0]
        assert result[0][1] == data[0][1]
        cursor.execute(f'drop table {table}')


@pytest.mark.skip("clickzetta-connector does not support bind parameters")
def test_prepare_statement(it_conn: Generator[Connection, None, None]):
    """Tests columnless bulk insert into a new table from a collected result of 'SELECT *'"""
    if not it_conn:
        pytest.skip("skipping integration test because config file not found")
    with it_conn as conn:
        cursor = conn.cursor()
        table = random_name_for_temp_object()
        cursor.execute(f'create table {table}(`a` string, `b` string)')
        data = [random_alphanumeric_str(230), random_alphanumeric_str(230)]
        cursor.execute(f'INSERT INTO {table}(`a`, `b`) VALUES (?, ?)', binding_params=data)
        cursor.execute(f'SELECT * FROM {table}')
        result = cursor.fetchall()
        print("count:" + str(len(result)))
        assert len(result) == 1
        assert result[0][0] == data[0]
        assert result[0][1] == data[1]
        cursor.execute(f'drop table {table}')

@pytest.mark.skip("clickzetta-connector does not support bind parameters")
def test_batch_insert_complex_type(it_conn: Generator[Connection, None, None]):
    """Tests bulk insert into a new table with all Clickzetta supported data types"""
    if not it_conn:
        pytest.skip("skipping integration test because config file not found")

    with it_conn as conn:
        conn._client._pure_arrow_decoding = True
        cursor = conn.cursor()
        table = random_name_for_temp_object()
        cursor.execute(f'''
            CREATE TABLE {table} (
                c_bigint BIGINT,
                c_boolean BOOLEAN,
                c_binary BINARY,
                c_char CHAR,
                c_date DATE,
                c_decimal DECIMAL(20, 6),
                c_double DOUBLE,
                c_float FLOAT,
                c_int INT,
                c_interval INTERVAL DAY,
                c_smallint SMALLINT,
                c_string STRING,
                c_timestamp TIMESTAMP,
                c_tinyint TINYINT,
                c_array ARRAY<STRUCT<a: INT, b: STRING>>,
                c_map MAP<STRING, STRING>,
                c_struct STRUCT<a: INT, b: STRING, c: DOUBLE>,
                c_varchar VARCHAR(1024),
                c_json JSON
            )
        ''')

        data = [
            (
                1,
                True,
                b'\x01',
                'a',
                datetime.date(2022, 2, 1),
                1000.123456,
                2.0,
                1.5,
                42,
                'INTERVAL 1 DAY',
                103,
                'test string 1',
                datetime.datetime.now(),
                11,
                [(1, 'A')],
                {'key1': 'value1'},
                (1, 'A', 2.0),
                'varchar example 1',
                ("JSON '" + '{"id": 2, "value": "100", "comment": "JSON Sample data"}' + "'")
            ),
            (
                2,
                False,
                b'\x02',
                'b',
                datetime.date(2022, 2, 2),
                2000.234567,
                4.0,
                2.5,
                84,
                'INTERVAL 2 DAY',
                104,
                'test string 2',
                datetime.datetime.now(),
                12,
                [(2, 'B')],  # array<struct>
                {'key2': 'value2'},  # dict
                (2, 'B', 4.0),  # struct
                'varchar example 2',
                ("JSON '" + '{"id": 2, "value": "100", "comment": "JSON Sample data"}' + "'")  # json
            )
        ]
        sql = f'''
            INSERT INTO {table} (
                c_bigint, c_boolean, c_binary, c_char, c_date, c_decimal, c_double, 
                c_float, c_int, c_interval, c_smallint, c_string, c_timestamp, 
                c_tinyint, c_array, c_map, c_struct, c_varchar, c_json
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
        '''

        print("data:\n" + str(data))
        print("sql:\n" + sql)
        cursor.executemany(sql, data)

        cursor.execute(f'SELECT * FROM {table}')
        result = cursor.fetchall()
        print("count:" + str(len(result)))
        # c_bigint, c_boolean, c_binary, c_char, c_date, c_decimal, c_double,
        # c_float, c_int, c_interval, c_smallint, c_string, c_timestamp,
        # c_tinyint, c_array, c_map, c_struct, c_varchar, c_json
        try:
            assert len(result) == 2
            assert result[0][0] == 1
            assert result[0][1] is True
            assert result[0][2] == b'\x01'
            assert result[0][3] == 'a'
            assert result[0][4] == datetime.date(2022, 2, 1)
            assert result[0][5] == Decimal('1000.123456')
            assert result[0][6] == 2.0
            assert result[0][7] == 1.5
            assert result[0][8] == 42
            assert str(result[0][9]) == 'MonthDayNano(months=0, days=1, nanoseconds=0)'
            assert result[0][10] == 103
            assert result[0][11] == 'test string 1'
            assert isinstance(result[0][12], datetime.datetime)
            assert result[0][13] == 11
            assert result[0][14] == [{'a': 1, 'b': 'A'}]
            assert result[0][15] == [('key1', 'value1')]
            assert result[0][16] == {'a': 1, 'b': 'A', 'c': 2.0}
            assert result[0][17] == 'varchar example 1'
            assert result[0][18] == '{"comment":"JSON Sample data","id":2,"value":"100"}'
        finally:
            cursor.execute(f'drop table {table}')