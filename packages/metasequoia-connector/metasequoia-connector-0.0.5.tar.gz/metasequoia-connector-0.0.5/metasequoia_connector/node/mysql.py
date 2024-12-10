import dataclasses
from typing import Optional

from metasequoia_connector.node.ssh_tunnel import SshTunnel

__all__ = ["MysqlInstance", "MysqlTable"]


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class MysqlInstance:
    """MySQL 实例"""

    host: str = dataclasses.field(kw_only=True)
    port: int = dataclasses.field(kw_only=True)
    user: str = dataclasses.field(kw_only=True)
    passwd: str = dataclasses.field(kw_only=True)
    ssh_tunnel: Optional[SshTunnel] = dataclasses.field(kw_only=True, default=None)


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class MysqlTable:
    """MySQL 表"""

    instance: MysqlInstance = dataclasses.field(kw_only=True)
    schema: str = dataclasses.field(kw_only=True)
    table: str = dataclasses.field(kw_only=True)
