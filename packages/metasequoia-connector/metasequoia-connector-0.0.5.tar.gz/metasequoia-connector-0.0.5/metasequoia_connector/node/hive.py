"""
Hive 连接器节点
"""

import dataclasses
from typing import List, Optional

from metasequoia_connector.node.ssh_tunnel import SshTunnel

__all__ = ["HiveInstance", "HiveTable"]


@dataclasses.dataclass(slots=True)
class HiveInstance:
    """Hive 实例"""

    hosts: List[str] = dataclasses.field(kw_only=True)
    port: int = dataclasses.field(kw_only=True)
    username: Optional[str] = dataclasses.field(kw_only=True, default=None)
    ssh_tunnel: Optional[SshTunnel] = dataclasses.field(kw_only=True, default=None)

    def set_hive_username(self, username: str) -> None:
        self.username = username


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class HiveTable:
    """Hive 表"""

    instance: HiveInstance = dataclasses.field(kw_only=True)
    schema: str = dataclasses.field(kw_only=True)
    table: str = dataclasses.field(kw_only=True)
