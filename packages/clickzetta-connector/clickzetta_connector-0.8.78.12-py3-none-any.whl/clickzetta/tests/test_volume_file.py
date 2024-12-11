import logging
import re
from datetime import datetime
from typing import List, Dict, Generator, Tuple, Sequence
from abc import ABC, abstractmethod
from pathlib import Path

import pytest

from clickzetta.dbapi.connection import Connection
from clickzetta.dbapi.cursor import Cursor
from clickzetta import connect

_LOG = logging.getLogger(__name__)


def _random_str(length: int):
    import random
    import string

    chars = string.ascii_lowercase + string.digits
    return "".join(random.choice(chars) for i in range(length))


def _execute_and_fetch(cursor: Cursor, sql: str) -> List:
    _LOG.info(f"Executing sql: {sql}")
    cursor.execute(sql)
    return cursor.fetchall()


class _Executor(ABC):
    @abstractmethod
    def execute(self, sql: str) -> List:
        pass

    @abstractmethod
    def context_values(self) -> Dict[str, str]:
        pass

    @abstractmethod
    def close(self) -> None:
        pass


class _ExternalVolumeExecutor(_Executor):
    def __init__(
        self,
        volume_name: str,
        volume_location: str,
        volume_connection: str,
        db_connection: Connection,
    ) -> None:
        self._volume_name = volume_name
        self._volume_location = volume_location
        self._volume_connection = volume_connection
        self._conn = db_connection
        self._cursor = self._conn.cursor()

        self.execute(
            f"CREATE EXTERNAL VOLUME `{self._volume_name}` "
            f"LOCATION '{self._volume_location}' "
            f"USING connection {self._volume_connection} "
            "directory = (enable=true) recursive=true ;"
        )

    def execute(self, sql: str) -> List:
        return _execute_and_fetch(self._cursor, sql)

    def context_values(self) -> Dict[str, str]:
        return {
            "volume_name": self._volume_name,
            "volume_location": self._volume_location,
        }

    def close(self) -> None:
        self.execute(f"DELETE VOLUME `{self._volume_name}` SUBDIRECTORY '/' ;")
        self.execute(f"DROP VOLUME `{self._volume_name}` ;")
        if self._cursor:
            self._cursor.close()
        if self._conn:
            self._conn.close()


class _TableVolumeExecutor(_Executor):
    def __init__(self, table_name: str, db_connection: Connection) -> None:
        self._table_name = table_name
        self._conn = db_connection
        self._cursor = self._conn.cursor()

        self.execute(f"CREATE TABLE `{self._table_name}` (a int, b int) ;")

    def execute(self, sql: str) -> List:
        return _execute_and_fetch(self._cursor, sql)

    def context_values(self) -> Dict[str, str]:
        return {"table_name": self._table_name}

    def close(self) -> None:
        self.execute(f"DELETE TABLE VOLUME `{self._table_name}` SUBDIRECTORY '/' ;")
        self.execute(f"DROP TABLE IF EXISTS `{self._table_name}` ;")
        if self._cursor:
            self._cursor.close()
        if self._conn:
            self._conn.close()


class _UserVolumeExecutor(_Executor):
    def __init__(self, subdir: str, db_connection: Connection) -> None:
        self._subdir = subdir
        self._conn = db_connection
        self._cursor = self._conn.cursor()

    def execute(self, sql: str) -> List:
        return _execute_and_fetch(self._cursor, sql)

    def context_values(self) -> Dict[str, str]:
        return {"subdir": self._subdir}

    def close(self) -> None:
        self.execute(f"DELETE USER VOLUME SUBDIRECTORY '{self._subdir}' ;")
        if self._cursor:
            self._cursor.close()
        if self._conn:
            self._conn.close()


@pytest.fixture
def ext_vol_executor(it_config: Dict):
    volume_config = it_config.get("volume_file", None)
    assert volume_config is not None
    volume_connection = volume_config["volume_connection"]
    location_base = volume_config["volume_location_base"]
    if location_base.endswith("/"):
        location_base = location_base[:-1]
    date = datetime.now().strftime("%Y%m%d")
    volume_name = f"vol_{date}_{_random_str(12)}"
    volume_location = f"{location_base}/{date}/{volume_name}"

    connection_config = it_config["connection"]
    assert connection_config is not None
    db_connection = connect(**connection_config)

    tester = _ExternalVolumeExecutor(
        volume_name, volume_location, volume_connection, db_connection
    )
    yield tester
    tester.close()


@pytest.fixture
def table_vol_executor(it_config: Dict):
    date = datetime.now().strftime("%Y%m%d")
    table_name = f"tbl_{date}_{_random_str(12)}"
    connection_config = it_config["connection"]
    db_connection = connect(**connection_config)
    tester = _TableVolumeExecutor(table_name, db_connection)
    yield tester
    tester.close()


@pytest.fixture
def user_vol_executor(it_config: Dict):
    date = datetime.now().strftime("%Y%m%d")
    subdir = f"{date}/{_random_str(12)}"
    connection_config = it_config["connection"]
    db_connection = connect(**connection_config)
    tester = _UserVolumeExecutor(subdir, db_connection)
    yield tester
    tester.close()


def _collect_sql_files(prefix: str) -> List[Path]:
    res_dir = Path(__file__).parent / "res"
    return sorted([file for file in res_dir.glob(f"{prefix}*.sql")])


def _path_name(val: Path) -> str:
    return val.name


class _SqlFileTester:
    def __init__(self, sql_file: Path, executor: _Executor, tmp_path: Path) -> None:
        self._sql_file = sql_file
        self._executor = executor
        self._tmp_path = tmp_path
        self._context_values = executor.context_values()
        self._context_values["path_prefix"] = str(tmp_path.relative_to(Path.cwd()))
        self._context_values["abs_path_prefix"] = str(tmp_path)

    def run(self):
        _LOG.info(f"Testing on {self._sql_file}")
        for line_no, block in self._iter_blocks():
            first_line = block[0]
            if first_line.startswith("--!! "):
                self._run_cmd_block(line_no, block)
            elif first_line.startswith("--"):
                continue  # comment block
            else:
                self._run_query_block(line_no, block)

    def _iter_blocks(self) -> Generator[Tuple[int, List[str]], None, None]:
        with open(self._sql_file, "r") as file:
            block = []
            line_no = 0
            for line in file:
                line_no += 1
                if line == "" or line.strip() == "":
                    if len(block) > 0:
                        yield (line_no - len(block) + 1, block)
                        block.clear()
                else:
                    block.append(line)
        if len(block) > 0:
            yield (line_no - len(block) + 1, block)

    def _run_cmd_block(self, line_no: int, block: List[str]):
        _LOG.debug(f"Executing command block @{line_no}")
        for line in block:
            tokens = line.split()
            if tokens[0] != "--!!":
                raise ValueError(f"invalid command {line} in block@{line_no}")
            cmd = tokens[1]
            if cmd == "tmp_file":
                self._cmd_tmp_file(tokens[2:])
            elif cmd == "compare_file":
                self._cmd_compare_file(tokens[2:])
            else:
                raise ValueError(f"invalid command {cmd} in block@{line_no}")

    def _run_query_block(self, line_no: int, block: List[str]):
        _LOG.debug(f"Executing command block@{line_no}")
        is_output = lambda line: line.startswith("-->> ")
        div = next((i for i, l in enumerate(block) if is_output(l)), len(block))
        if div == 0:
            raise ValueError(f"no query for query block@{line_no}")
        query = "".join(block[:div])
        query = self._sub_text(query)
        query_output = self._executor.execute(query)
        if div < len(block):
            query_output.sort()
            expected_output = [l[5:].rstrip() for l in block[div:]]
            self._check_output(expected_output, query_output)

    def _sub_text(self, text: str) -> str:
        pattern = re.compile(r"\{(\w+)\}")

        def _repl(match):
            key = match.group(1)
            if key not in self._context_values:
                raise ValueError(f"unknown context value: {key}")
            return self._context_values[key]

        return pattern.sub(_repl, text)

    def _check_output(self, expected_output: List[str], actual_output: List[List]):
        assert len(expected_output) == len(actual_output)
        for row_no in range(len(expected_output)):
            expected_line = self._sub_text(expected_output[row_no])
            expected_row = expected_line.split(",")
            actual_row = actual_output[row_no]
            assert len(expected_row) <= len(actual_row)
            if self._compare_row(row_no, expected_row, actual_row):
                assert len(expected_row) == len(actual_row)

    def _compare_row(self, row_no, expected_row: List[str], actual_row: Sequence):
        for col_no in range(len(expected_row)):
            expected_value = expected_row[col_no]
            if expected_value == "...":
                return False
            elif expected_value.startswith("**"):
                assert str(actual_row[col_no]).endswith(
                    expected_value[2:]
                ), f"value not matched at row#{row_no}:{col_no}"
            else:
                assert (
                    str(actual_row[col_no]) == expected_value
                ), f"value not matched at row#{row_no}:{col_no}"
        return True

    def _cmd_tmp_file(self, args: List[str]):
        if len(args) != 2:
            raise ValueError(f"invalid tmp_file args: {args}")
        filename = args[0]
        filesize = int(args[1])
        path = self._tmp_path / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        content = _random_str(filesize).encode("utf-8")
        path.write_bytes(content)

    def _cmd_compare_file(self, args: List[str]):
        if len(args) != 2:
            raise ValueError(f"invalid compare_file args: {args}")
        base_file = self._tmp_path / args[0]
        ref_file = self._tmp_path / args[1]
        if not base_file.exists():
            raise ValueError(f"base file not found: {base_file}")
        if not ref_file.exists():
            raise ValueError(f"ref file not found: {ref_file}")
        if base_file.read_bytes() != ref_file.read_bytes():
            raise ValueError(f"file content not equals: {base_file} vs {ref_file}")


@pytest.mark.integration_test
class TestExternalVolume:
    @pytest.mark.parametrize(
        "sql_file", _collect_sql_files("external_volume_"), ids=_path_name
    )
    def test_sql_file(self, sql_file, ext_vol_executor, tmp_path):
        _SqlFileTester(sql_file, ext_vol_executor, tmp_path).run()


@pytest.mark.integration_test
class TestTableVolume:
    @pytest.mark.parametrize(
        "sql_file", _collect_sql_files("table_volume_"), ids=_path_name
    )
    def test_sql_file(self, sql_file, table_vol_executor, tmp_path):
        _SqlFileTester(sql_file, table_vol_executor, tmp_path).run()


@pytest.mark.integration_test
class TestUserVolume:
    @pytest.mark.parametrize(
        "sql_file", _collect_sql_files("user_volume_"), ids=_path_name
    )
    def test_sql_file(self, sql_file, user_vol_executor, tmp_path):
        _SqlFileTester(sql_file, user_vol_executor, tmp_path).run()
