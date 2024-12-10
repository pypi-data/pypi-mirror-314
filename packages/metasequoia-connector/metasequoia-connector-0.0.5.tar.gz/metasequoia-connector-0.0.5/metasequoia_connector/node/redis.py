"""
Redis 节点
"""

import dataclasses
from typing import Optional

from metasequoia_connector.node.ssh_tunnel import SshTunnel

__all__ = ["RedisInstance", "RedisDatabase"]


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class RedisInstance:
    """Redis 实例"""

    host: str = dataclasses.field(kw_only=True)
    passwd: str = dataclasses.field(kw_only=True)
    port: int = dataclasses.field(kw_only=True)
    ssh_tunnel: Optional[SshTunnel] = dataclasses.field(kw_only=True, default=None)


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class RedisDatabase:
    """Redis 数据库"""

    instance: RedisInstance = dataclasses.field(kw_only=True)
    db: int = dataclasses.field(kw_only=True)
