"""Cursor for ClickZetta DB-API."""
import abc

import collections
import logging
import contextlib
import re
from collections.abc import Mapping
from decimal import Decimal
from typing import Sequence, Union, Any, Optional, Dict, Tuple

from clickzetta.enums import JobID, FetchMode

from clickzetta.query_result import QueryResult

_LOGGER = logging.getLogger(__name__)

Column = collections.namedtuple(
    "Column",
    [
        "name",
        "type_code",
        "display_size",
        "internal_size",
        "precision",
        "scale",
        "null_ok",
    ],
)
SQL_COMMENT = r"\/\*.*?\*\/"

RE_SQL_INSERT_STMT = re.compile(
    rf"({SQL_COMMENT}|\s)*INSERT({SQL_COMMENT}|\s)"
    r"*(?:IGNORE\s+)?INTO\s+[`'\"]?.+[`'\"]?(?:\.[`'\"]?.+[`'\"]?)"
    r"{0,2}\s+VALUES\s*(\(.+\)).*",
    re.I | re.M | re.S,
    )

RE_SQL_ON_DUPLICATE = re.compile(
    r"""\s*ON\s+DUPLICATE\s+KEY(?:[^"'`]*["'`][^"'`]*["'`])*[^"'`]*$""",
    re.I | re.M | re.S,
    )

RE_SQL_COMMENT = re.compile(
    rf"""({SQL_COMMENT})|(["'`][^"'`]*?({SQL_COMMENT})[^"'`]*?["'`])""",
    re.I | re.M | re.S,
    )

RE_SQL_INSERT_VALUES = re.compile(r".*VALUES\s*(\(.+\)).*", re.I | re.M | re.S)

RE_PY_MAPPING_PARAM = re.compile(
    rb"""
    %
    \((?P<mapping_key>[^)]+)\)
    (?P<conversion_type>[diouxXeEfFgGcrs%])
    """,
    re.X,
)

class _ParamSubstitutor:
    """
    Substitutes parameters into SQL statement.
    """

    def __init__(self, params: Sequence[bytes]) -> None:
        self.params: Sequence[bytes] = params
        self.index: int = 0

    def __call__(self, matchobj: re.Match) -> bytes:
        index = self.index
        self.index += 1
        try:
            return bytes(self.params[index])
        except IndexError:
            raise Exception(
                "Not enough parameters for the SQL statement"
            ) from None

    @property
    def remaining(self) -> int:
        """Returns number of parameters remaining to be substituted"""
        return len(self.params) - self.index


class Cursor(object):
    def __init__(self, connection):
        self.connection = connection
        self.description = None
        self.arraysize = 100
        self.rowcount = -1
        self._query_result = None
        self._query_data = None
        self._closed = False
        self.job_id = None
        self._rows = None
        self.row_number = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self._closed = True

    def check_rows(self, fetch_mode=FetchMode.FETCH_ALL, size=0):
        if self._rows is None or self.row_number >= len(self._rows):
            self._rows = self._query_data.read(fetch_mode, size)
            self.row_number = 0

    def _set_rowcount(self, query_result):

        self.rowcount = query_result.total_row_count

    def _set_description(self, query_result: QueryResult):
        if query_result.schema is None:
            self.description = None
            return

        self.description = tuple(
            Column(
                name=field.name,
                type_code=field.field_type,
                display_size=None,
                internal_size=field.length,
                precision=field.precision,
                scale=field.scale,
                null_ok=field.nullable,
            )
            for field in query_result.schema
        )

    def execute(self, operation: str, parameters=None):

        self._execute(operation, parameters)

    def execute_with_job_id(self, operation: str, job_id=None, parameters=None):
        self._execute(operation, parameters, job_id)

    def _execute(
            self, operation: str, parameters, job_id=None
    ):
        if operation is None:
            raise ValueError("sql is empty")
        else:
            operation = operation.strip()
            if operation == "":
                raise ValueError("sql is empty")
        self._query_data = None
        self._query_job = None
        client = self.connection._client
        operation = operation + ";" if not operation.endswith(";") else operation

        self.job_id = client._format_job_id() if job_id is None or job_id == '' else job_id
        self.query = operation

        job_id = JobID(self.job_id, client.workspace, 100)

        self._query_result = client.submit_sql_job(token=client.token, sql=operation, job_id=job_id,
                                                   parameters=parameters)
        self._set_rowcount(self._query_result)
        self._query_data = self._query_result.data
        self._set_description(self._query_result)

    def executemany(self, operation: str):
        raise NotImplementedError

    def fetchone(self):
        self.check_rows(fetch_mode=FetchMode.FETCH_ONE)
        if self._rows is None or self.row_number >= len(self._rows):
            return None
        else:
            row = self._rows[self.row_number]
            self.row_number += 1
            return row

    def fetchmany(self, size=None):
        self.check_rows(fetch_mode=FetchMode.FETCH_MANY, size=size)
        if self._rows is None or self.row_number >= len(self._rows):
            return []
        else:
            end = self.row_number + (size or self.arraysize)
            rows = self._rows[self.row_number:end]
            self.row_number = min(end, len(self._rows))
            return rows

    def fetchall(self):
        self.check_rows(fetch_mode=FetchMode.FETCH_ALL)
        if self._rows is None or self.row_number >= len(self._rows):
            return []
        else:
            rows = self._rows[self.row_number:]
            self.row_number = len(self._rows)
            return rows

    def fetch_panda_all(self):
        return self._query_result.panda_data

    def get_job_id(self):
        return self.job_id

    def setinputsizes(self, sizes):
        """No-op, but for consistency raise an error if cursor is closed."""

    def setoutputsize(self, size, column=None):
        """No-op, but for consistency raise an error if cursor is closed."""

    def __iter__(self):
        return iter(self._query_data)