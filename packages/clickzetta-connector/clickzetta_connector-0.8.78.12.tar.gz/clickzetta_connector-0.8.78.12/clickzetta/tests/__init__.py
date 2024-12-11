from typing import NamedTuple


class ConnectParams(NamedTuple):
    username: str
    password: str
    service: str
    instance: str
    workspace: str
    schema: str
    vcluster: str
