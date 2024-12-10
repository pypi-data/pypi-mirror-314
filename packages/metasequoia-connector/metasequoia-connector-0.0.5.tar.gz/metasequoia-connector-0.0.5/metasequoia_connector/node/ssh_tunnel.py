import dataclasses
from typing import Tuple

__all__ = ["SshTunnel"]


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class SshTunnel:
    """SSH 隧道"""

    host: str = dataclasses.field(kw_only=True)  # 对应 ssh_address_or_host 参数
    port: int = dataclasses.field(kw_only=True)  # 对应 ssh_address_or_host 参数
    username: str = dataclasses.field(kw_only=True)
    password: str = dataclasses.field(kw_only=True, default=None)
    pkey: str = dataclasses.field(kw_only=True, default=None)

    @property
    def address(self) -> Tuple[str, int]:
        return self.host, self.port
