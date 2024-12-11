import os
import unittest
from datetime import date, datetime
from decimal import Decimal

import numpy
import pyarrow as pa
import pytz
from pyarrow import timestamp


class TestArrowFileReading(unittest.TestCase):

    @staticmethod
    def create_arrow_table(file_path) -> pa.Table:
        with open(file_path, "rb") as f:
            stream = pa.py_buffer(f.read())
            with pa.ipc.RecordBatchStreamReader(stream) as reader:
                return reader.read_all()

    def check_column_metadata(self, table, expected_metadata):
        schema = table.schema
        for i, column_meta in enumerate(expected_metadata):
            self.assertEqual(column_meta['name'], schema[i].name)
            self.assertEqual(column_meta['type'], str(schema[i].type))

    def test_read_simple_file(self):
        expected_metadata = [
            {"name": "a", "type": "int32"},
            {"name": "b", "type": "string"}
        ]
        file_path = os.path.join(os.path.dirname(__file__), 'resources', 'int_string_uncompressed.arrow')
        print("file_path: ", str(file_path))
        table = self.create_arrow_table(file_path)
        self.check_column_metadata(table, expected_metadata)

        expected_a = [1, 2, 3]
        expected_b = ["a", "b", "c"]

        column_a = table.column("a").to_pylist()
        column_b = table.column("b").to_pylist()

        self.assertEqual(column_a, expected_a)
        self.assertEqual(column_b, expected_b)

    def test_read_primitive_type(self):
        expected_metadata = [
            {"name": "c1", "type": "int8"},
            {"name": "c2", "type": "int16"},
            {"name": "c3", "type": "int32"},
            {"name": "c4", "type": "int64"},
            {"name": "c5", "type": "float"},
            {"name": "c6", "type": "double"},
            {"name": "c7", "type": "bool"}
        ]
        file_path = os.path.join(os.path.dirname(__file__), 'resources', 'numeric.arrow')
        table = self.create_arrow_table(file_path)
        self.check_column_metadata(table, expected_metadata)

        expected_c1 = [0, 1, 2, 0, 1, 2]
        expected_c2 = [0, 1, 2, 0, 1, 2]
        expected_c3 = [0, 1, 2, 0, 1, 2]
        expected_c4 = [0, 1, 2, 0, 1, 2]
        expected_c5 = [0.0, 1.0, 2.0, 0.0, 1.0, 2.0]
        expected_c6 = [0.0, 1.0, 2.0, 0.0, 1.0, 2.0]
        expected_c7 = [True, False, True, True, False, True]

        column_c1 = table.column("c1").to_pylist()
        column_c2 = table.column("c2").to_pylist()
        column_c3 = table.column("c3").to_pylist()
        column_c4 = table.column("c4").to_pylist()
        column_c5 = table.column("c5").to_pylist()
        column_c6 = table.column("c6").to_pylist()
        column_c7 = table.column("c7").to_pylist()

        for i in range(6):
            self.assertEqual(column_c1[i], expected_c1[i])
            self.assertEqual(column_c2[i], expected_c2[i])
            self.assertEqual(column_c3[i], expected_c3[i])
            self.assertEqual(column_c4[i], expected_c4[i])
            self.assertAlmostEqual(column_c5[i], expected_c5[i], places=6)
            self.assertAlmostEqual(column_c6[i], expected_c6[i], places=7)
            self.assertEqual(column_c7[i], expected_c7[i])

            self.assertEqual(str(column_c1[i]), str(expected_c1[i]))
            self.assertEqual(str(column_c2[i]), str(expected_c2[i]))
            self.assertEqual(str(column_c3[i]), str(expected_c3[i]))
            self.assertEqual(str(column_c4[i]), str(expected_c4[i]))
            self.assertEqual(str(column_c5[i]), str(expected_c5[i]))
            self.assertEqual(str(column_c6[i]), str(expected_c6[i]))
            self.assertEqual(str(column_c7[i]), str(expected_c7[i]))

    def test_read_decimal_type(self):
        expected_metadata = [
            {"name": "c1", "type": "decimal128(4, 0)"},
            {"name": "c2", "type": "decimal128(12, 2)"},
            {"name": "c3", "type": "decimal128(20, 4)"}
        ]
        file_path = os.path.join(os.path.dirname(__file__), 'resources', 'decimal.arrow')
        table = self.create_arrow_table(file_path)
        self.check_column_metadata(table, expected_metadata)

        expected_c1 = [Decimal("0"), Decimal("1"), Decimal("2")]
        expected_c2 = [Decimal("0.00"), Decimal("1.01"), Decimal("2.02")]
        expected_c3 = [Decimal("0.0000"), Decimal("1.0101"), Decimal("2.0202")]

        column_c1 = table.column("c1").to_pylist()
        column_c2 = table.column("c2").to_pylist()
        column_c3 = table.column("c3").to_pylist()

        for i in range(3):
            self.assertEqual(column_c1[i], expected_c1[i])
            self.assertEqual(column_c2[i], expected_c2[i])
            self.assertEqual(column_c3[i], expected_c3[i])

            self.assertEqual(str(column_c1[i]), str(expected_c1[i]))
            self.assertEqual(str(column_c2[i]), str(expected_c2[i]))
            self.assertEqual(str(column_c3[i]), str(expected_c3[i]))

    def test_read_binary_type(self):
        expected_metadata = [
            {"name": "c1", "type": "string"},
            {"name": "c2", "type": "string"},
            {"name": "c3", "type": "string"},
            {"name": "c4", "type": "binary"}
        ]
        file_path = os.path.join(os.path.dirname(__file__), 'resources', 'string.arrow')
        table = self.create_arrow_table(file_path)
        self.check_column_metadata(table, expected_metadata)

        expected_c1 = ["char0", "char1", "char2"]
        expected_c2 = ["varchar0", "varchar1", "varchar2"]
        expected_c3 = ["string0", "string1", "string2"]
        expected_c4 = [b"binary0", b"binary1", b"binary2"]
        expected_c4_str = ["b'binary0'", "b'binary1'", "b'binary2'"]

        column_c1 = table.column("c1").to_pylist()
        column_c2 = table.column("c2").to_pylist()
        column_c3 = table.column("c3").to_pylist()
        column_c4 = table.column("c4").to_pylist()

        for i in range(3):
            self.assertEqual(column_c1[i], expected_c1[i])
            self.assertEqual(column_c2[i], expected_c2[i])
            self.assertEqual(column_c3[i], expected_c3[i])
            self.assertEqual(column_c4[i], expected_c4[i])

            self.assertEqual(column_c1[i], expected_c1[i])
            self.assertEqual(column_c2[i], expected_c2[i])
            self.assertEqual(column_c3[i], expected_c3[i])
            self.assertEqual(str(column_c4[i]), expected_c4_str[i])

    def test_read_temporal_type(self):
        expected_metadata = [
            {"name": "c1", "type": pa.date32()},
            {"name": "c2", "type": str(timestamp("us", "UTC"))},
            # TODO Maybe we should cast the type to string
            {"name": "c3", "type": "month_interval"},
            {"name": "c4", "type": "month_day_nano_interval"}
        ]
        file_path = os.path.join(os.path.dirname(__file__), 'resources', 'temporal.arrow')
        table = self.create_arrow_table(file_path)
        self.check_column_metadata(table, expected_metadata)

        utc = pytz.UTC
        expected_c1 = [date(1970, 1, 1), date(1980, 1, 10), date(1990, 1, 18)]
        expected_c2 = [datetime.fromtimestamp(0, tz=utc), datetime(1986, 12, 28, 0, 0, 0, 10001, tzinfo=utc),
                       datetime(2003, 12, 24, 0, 0, 0, 20002, tzinfo=utc)]
        expected_c3 = ["0-0", "1-1", "2-2"]
        expected_c4 = ["0 00:00:00.000000000", "0 01:00:01.000001000", "0 02:00:02.000002000"]

        column_c1 = table.column("c1").to_pylist()
        column_c2 = table.column("c2").to_pylist()
        # TODO got an error here: pyarrow/table.pxi:1312: in pyarrow.lib.ChunkedArray.to_pylist
        # column_c3 = table.column("c3").to_pylist()
        # column_c4 = table.column("c4").to_pylist()

        for i in range(3):
            print(f"column_c1[{i}]: ", column_c1[i])
            self.assertEqual(column_c1[i], expected_c1[i])
            print(f"column_c2[{i}]: ", column_c2[i])
            self.assertEqual(column_c2[i], expected_c2[i])
            # self.assertEqual(column_c3[i], expected_c3[i])
            # self.assertEqual(column_c4[i], expected_c4[i])

            self.assertEqual(str(column_c1[i]), str(expected_c1[i]))
            self.assertEqual(str(column_c2[i]), str(expected_c2[i]))
            # self.assertEqual(str(column_c3[i]), str(expected_c3[i]))
            # self.assertEqual(str(column_c4[i]), str(expected_c4[i]))

    def test_read_complex_type(self):
        expected_metadata = [
            {"name": "c1", "type": "struct<c11: int32, c12: struct<c121: int32>>"},
            {"name": "c2", "type": "map<int32, int32>"},
            {"name": "c3", "type": "list<element: int32>"},
            {"name": "c4", "type": "list<element: list<element: int32>>"}
        ]
        file_path = os.path.join(os.path.dirname(__file__), 'resources', 'complex.arrow')
        table = self.create_arrow_table(file_path)
        self.check_column_metadata(table, expected_metadata)

        expected_c1 = [
            "{'c11': None, 'c12': {'c121': -1}}",
            "{'c11': 2, 'c12': {'c121': None}}",
            "{'c11': 3, 'c12': None}"
        ]
        expected_c2 = ["[(1, 1), (2, None)]", '[]', None]
        expected_c3 = ['[1, None]', '[]', None]
        expected_c4 = ['[[1], [1, None]]', '[None, [], [None]]', '[[3], [3, 3]]']

        column_c1 = table.column("c1").to_pylist()
        column_c2 = table.column("c2").to_pylist()
        column_c3 = table.column("c3").to_pylist()
        column_c4 = table.column("c4").to_pylist()

        for i in range(3):
            self.assertEqual(str(column_c1[i]) if column_c1[i] is not None else None, expected_c1[i])
            # map<int32, int32> will return a list of tuples
            self.assertEqual(str(column_c2[i]) if column_c2[i] is not None else None, expected_c2[i])
            self.assertEqual(str(column_c3[i]) if column_c3[i] is not None else None, expected_c3[i])
            self.assertEqual(str(column_c4[i]) if column_c4[i] is not None else None, expected_c4[i])

    def test_read_nested_temporal_type(self):
        expected_metadata = [
            {"name": "a", "type": "timestamp[us, tz=UTC]"},
            {"name": "b", "type": "list<element: timestamp[us, tz=UTC] not null>"},
            {"name": "c", "type": "month_interval"},
            {"name": "d", "type": "list<element: month_interval not null>"}
        ]
        file_path = os.path.join(os.path.dirname(__file__), 'resources', 'nested_temporal.arrow')
        table = self.create_arrow_table(file_path)
        self.check_column_metadata(table, expected_metadata)

        self.assertTrue(table.num_rows > 0)

        utc = pytz.UTC
        expected_ts = datetime.fromtimestamp(691952411000 / 1000, utc)
        # 1991-12-05 17:00:11+00:00
        expected_ts_str = expected_ts.strftime("%Y-%m-%d %H:%M:%S")

        column_a = table.column("a").to_pylist()
        column_b = table.column("b").to_pylist()
        # Datatype not supported
        # column_c = table.column("c").to_pylist()
        # column_d = table.column("d").to_pylist()

        self.assertEqual(column_a[0], expected_ts)
        self.assertEqual(column_a[0].strftime("%Y-%m-%d %H:%M:%S"), expected_ts_str)
        self.assertEqual(column_b[0][0].strftime("%Y-%m-%d %H:%M:%S"), expected_ts_str)
        # Datatype not supported
        # self.assertEqual(column_c[0], "10-10")
        # self.assertEqual(str(column_d[0]), "[10-10]")

    def test_read_floating_number_from_ipc_file(self):
        expected_metadata = [
            {"name": "a", "type": "float"},
            {"name": "b", "type": "float"},
            {"name": "c", "type": "float"},
            {"name": "d", "type": "float"}
        ]
        file_path = os.path.join(os.path.dirname(__file__), 'resources', 'float.arrow')
        table = self.create_arrow_table(file_path)

        # Validate metadata
        table = table.rename_columns(["a", "b", "c", "d"])
        schema = table.schema
        for i, column_meta in enumerate(expected_metadata):
            self.assertEqual(column_meta['name'], schema[i].name)
            self.assertEqual(column_meta['type'], str(schema[i].type))

        expected_a = [1.0]
        expected_b = [1.2]
        expected_c = [0.1]
        expected_d = [0.1]

        column_a = table.column("a").to_pylist()
        column_b = table.column("b").to_pylist()
        column_c = table.column("c").to_pylist()
        column_d = table.column("d").to_pylist()

        self.assertEqual(str(column_a[0]), str(expected_a[0]))
        self.assertEqual(str(numpy.float32(column_b[0])), str(expected_b[0]))
        self.assertEqual(str(numpy.float32(column_c[0])), str(expected_c[0]))
        self.assertEqual(str(numpy.float32(column_d[0])), str(expected_d[0]))

        self.assertEqual(str(column_a[0]), "1.0")
        self.assertEqual(str(numpy.float32(column_b[0])), "1.2")
        self.assertEqual(str(numpy.float32(column_c[0])), "0.1")
        self.assertEqual(str(numpy.float32(column_d[0])), "0.1")

    def test_read_null_from_ipc_file(self):
        expected_metadata = [
            {"name": "a", "type": "month_day_nano_interval"}
        ]
        file_path = os.path.join(os.path.dirname(__file__), 'resources', 'null.arrow')
        table = self.create_arrow_table(file_path)
        table = table.rename_columns(["a"])

        # Validate metadata
        schema = table.schema
        for i, column_meta in enumerate(expected_metadata):
            self.assertEqual(column_meta['name'], schema[i].name)
            self.assertEqual(column_meta['type'], str(schema[i].type))

        column_a = table.column("a").to_pylist()

        self.assertTrue(len(column_a) > 0)
        self.assertIsNone(column_a[0])
        self.assertIsNone(column_a[0])
        self.assertIsNone(column_a[0])
        self.assertIsNone(column_a[0])

        self.assertEqual(len(column_a), 1)

    def test_read_json(self):
        expected_ids = [11, 22, 33, 44, 55]
        expected_contents = [
            '{"a":1,"b":{"c":1}}',
            '{"a":2,"b":{"c":2.2}}',
            '{"a":true,"b":{"c":false}}',
            '{"a":"aaa","b":{"c":"ccc"}}',
            '{"a":3,"b":{"c":3.3}}'
        ]

        file_path = os.path.join(os.path.dirname(__file__), 'resources', 'json.arrow')
        table = self.create_arrow_table(file_path)

        ids = table.column("id").to_pylist()
        contents = table.column("content").to_pylist()

        self.assertEqual(ids, expected_ids)
        self.assertEqual(contents, expected_contents)