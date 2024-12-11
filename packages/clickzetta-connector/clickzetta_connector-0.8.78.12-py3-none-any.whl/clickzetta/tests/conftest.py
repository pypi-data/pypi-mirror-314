import logging
from pathlib import Path, PurePath
from typing import Dict, Generator

import pytest
import tomli

from clickzetta import connect
from clickzetta.dbapi.connection import Connection
from clickzetta.tests import ConnectParams

_it_config_path = PurePath(__file__).parent.joinpath("integration_test.toml")
_it_config_existed = Path(_it_config_path).exists()


def pytest_configure(config):
    config.addinivalue_line("markers", "integration_test")


def pytest_runtest_setup(item):
    if item.get_closest_marker("integration_test") and not _it_config_existed:
        pytest.skip("skipping integration test because config file not found")


@pytest.fixture(scope="session")
def it_config() -> Dict:
    with open(_it_config_path, "rb") as f:
        config = tomli.load(f)
        return config


@pytest.fixture(scope="session")
def it_connect_params(it_config: Dict) -> ConnectParams:
    return ConnectParams(**it_config["connection"])


@pytest.fixture(scope="session")
def it_conn_url(it_connect_params: ConnectParams):
    p = it_connect_params
    return (
        f"clickzetta://{p.username}:{p.password}@"
        f"{p.instance}.{p.service}/{p.workspace}"
        f"?virtualcluster={p.vcluster}"
    )


@pytest.fixture
def it_conn(it_config: Dict) -> Generator[Connection, None, None]:
    conn = connect(**it_config["connection"])
    yield conn
    try:
        conn.close()
    except Exception:
        pass
