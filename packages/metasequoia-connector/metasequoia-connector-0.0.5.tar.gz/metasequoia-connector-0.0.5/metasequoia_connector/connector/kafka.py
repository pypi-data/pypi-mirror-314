"""
Kafka 连接器：基于 kafka-python
"""

from typing import List, Optional

from kafka import KafkaConsumer, KafkaProducer
from kafka.admin import KafkaAdminClient

from metasequoia_connector.connector.ssh_tunnel import create_ssh_tunnel
from metasequoia_connector.node import KafkaServer, KafkaTopicsGroup

__all__ = ["ConnKafkaAdminClient", "ConnKafkaConsumer", "ConnKafkaProducer"]


class ConnKafkaAdminClient:
    """根据 KafkaServer 对象创建 kafka-python 的 KafkaAdminClient 对象"""

    def __init__(self, kafka_server: KafkaServer):
        self.kafka_server = kafka_server  # MySQl 实例的配置

        # 初始化 MySQL 连接和 SSH 隧道连接
        self.kafka_admin_client = None
        self.ssh_tunnel_conn = None

    def __enter__(self):
        """在进入 with as 语句的时候被 with 调用，返回值作为 as 后面的变量"""
        if self.kafka_server.ssh_tunnel is not None:
            # 计算远端的地址立列表
            remote_bind_addresses = [(host_port.host, host_port.port)
                                     for host_port in self.kafka_server.get_host_list()]

            # 启动 SSH 隧道
            self.ssh_tunnel_conn = create_ssh_tunnel(
                self.kafka_server.ssh_tunnel,
                remote_bind_addresses=remote_bind_addresses
            )

            # 更新 Kafka 集群连接信息，令 Kafka 集群连接到 SSH 隧道
            if len(remote_bind_addresses) > 1:
                addresses = [f"127.0.0.1:{local_bind_port}"
                             for local_bind_port in self.ssh_tunnel_conn.local_bind_ports]
            else:
                addresses = [f"127.0.0.1:{self.ssh_tunnel_conn.local_bind_port}"]
        else:
            addresses = [f"{host_port.host}:{host_port.port}" for host_port in self.kafka_server.get_host_list()]

        # 启动 Kafka 集群连接
        self.kafka_admin_client = KafkaAdminClient(bootstrap_servers=addresses)

        return self.kafka_admin_client

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.kafka_admin_client is not None:
            self.kafka_admin_client.close()
        if self.ssh_tunnel_conn is not None:
            self.ssh_tunnel_conn.close()


class ConnKafkaConsumer:
    """根据 KafkaServer 对象创建 kafka-python 的 KafkaConsumer 对象"""

    def __init__(self, kafka_server: KafkaServer,
                 topics: Optional[List[str]] = None,
                 group_id: Optional[str] = None):
        self.kafka_server = kafka_server  # MySQl 实例的配置
        self.topics = topics
        self.group_id = group_id

        # 初始化 MySQL 连接和 SSH 隧道连接
        self.kafka_consumer = None
        self.ssh_tunnel_conn = None

    @staticmethod
    def by_kafka_topic_group(kafka_topics_group: KafkaTopicsGroup):
        """根据 KafkaTopicGroup 对象构造 KafkaConsumer 对象"""
        return ConnKafkaConsumer(
            kafka_server=kafka_topics_group.kafka_server,
            topics=kafka_topics_group.topics,
            group_id=kafka_topics_group.group_id
        )

    def __enter__(self):
        """在进入 with as 语句的时候被 with 调用，返回值作为 as 后面的变量"""
        if self.kafka_server.ssh_tunnel is not None:
            # 计算远端的地址立列表
            remote_bind_addresses = [(host_port.host, host_port.port)
                                     for host_port in self.kafka_server.get_host_list()]

            # 启动 SSH 隧道
            self.ssh_tunnel_conn = create_ssh_tunnel(
                self.kafka_server.ssh_tunnel,
                remote_bind_addresses=remote_bind_addresses
            )

            # 更新 Kafka 集群连接信息，令 Kafka 集群连接到 SSH 隧道
            if len(remote_bind_addresses) > 1:
                addresses = [f"127.0.0.1:{local_bind_port}"
                             for local_bind_port in self.ssh_tunnel_conn.local_bind_ports]
            else:
                addresses = [f"127.0.0.1:{self.ssh_tunnel_conn.local_bind_port}"]
        else:
            addresses = [f"{host_port.host}:{host_port.port}" for host_port in self.kafka_server.get_host_list()]

        # 启动 Kafka 集群连接
        if self.topics is not None:
            self.kafka_consumer = KafkaConsumer(*self.topics,
                                                bootstrap_servers=addresses,
                                                group_id=self.group_id,
                                                auto_offset_reset="latest",
                                                api_version=(0, 11))
        else:
            self.kafka_consumer = KafkaConsumer(bootstrap_servers=addresses,
                                                group_id=self.group_id,
                                                auto_offset_reset="latest",
                                                api_version=(0, 11))

        return self.kafka_consumer

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.kafka_consumer is not None:
            self.kafka_consumer.close()
        if self.ssh_tunnel_conn is not None:
            self.ssh_tunnel_conn.close()


class ConnKafkaProducer:
    """根据 KafkaServer 对象创建 kafka-python 的 KafkaProducer 对象"""

    def __init__(self, kafka_server: KafkaServer):
        self.kafka_server = kafka_server  # MySQl 实例的配置

        # 初始化 MySQL 连接和 SSH 隧道连接
        self.kafka_producer = None
        self.ssh_tunnel_conn = None

    def __enter__(self):
        """在进入 with as 语句的时候被 with 调用，返回值作为 as 后面的变量"""
        if self.kafka_server.ssh_tunnel is not None:
            # 计算远端的地址立列表
            remote_bind_addresses = [(host_port.host, host_port.port)
                                     for host_port in self.kafka_server.get_host_list()]

            # 启动 SSH 隧道
            self.ssh_tunnel_conn = create_ssh_tunnel(
                self.kafka_server.ssh_tunnel,
                remote_bind_addresses=remote_bind_addresses
            )

            # 更新 Kafka 集群连接信息，令 Kafka 集群连接到 SSH 隧道
            if len(remote_bind_addresses) > 1:
                addresses = [f"127.0.0.1:{local_bind_port}"
                             for local_bind_port in self.ssh_tunnel_conn.local_bind_ports]
            else:
                addresses = [f"127.0.0.1:{self.ssh_tunnel_conn.local_bind_port}"]
        else:
            addresses = [f"{host_port.host}:{host_port.port}" for host_port in self.kafka_server.get_host_list()]

        # 启动 Kafka 集群连接
        self.kafka_producer = KafkaProducer(bootstrap_servers=addresses,
                                            batch_size=1048576,
                                            linger_ms=50)

        return self.kafka_producer

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.kafka_producer is not None:
            self.kafka_producer.close()
        if self.ssh_tunnel_conn is not None:
            self.ssh_tunnel_conn.close()
