"""
连接器节点
"""

import dataclasses
from typing import List, Optional

from metasequoia_connector.node.common import HostPort
from metasequoia_connector.node.ssh_tunnel import SshTunnel


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class KafkaServer:
    """Kafka 集群对象"""

    bootstrap_servers: List[str] = dataclasses.field(kw_only=True)
    ssh_tunnel: Optional[SshTunnel] = dataclasses.field(kw_only=True, default=None)

    def get_host_list(self) -> List[HostPort]:
        return [HostPort.create_by_url(server) for server in self.bootstrap_servers]

    def __hash__(self):
        return hash((tuple(self.bootstrap_servers), self.ssh_tunnel))


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class KafkaTopic:
    """Kafka TOPIC"""

    kafka_server: KafkaServer = dataclasses.field(kw_only=True)
    topic: str = dataclasses.field(kw_only=True)


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class KafkaGroup:
    """Kafka 消费者组"""

    kafka_server: KafkaServer = dataclasses.field(kw_only=True)
    group: str = dataclasses.field(kw_only=True)


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class KafkaTopicsGroup:
    """Kafka TOPIC 并指定消费者组"""

    kafka_server: KafkaServer = dataclasses.field(kw_only=True)
    topics: List[str] = dataclasses.field(kw_only=True)
    group_id: str = dataclasses.field(kw_only=True)
