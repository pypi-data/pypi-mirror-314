from typing import Optional

from metasequoia_connector.connector import *
from metasequoia_connector.manager import ConnectManager
from metasequoia_connector.node import *
from metasequoia_connector.utils import dolphin, hive, kafka, mysql, otssql, sql_format


def from_environment(environ_name: Optional[str] = None, mode: str = "dev") -> ConnectManager:
    """从环境变量中读取配置文件路径，并加载配置文件"""
    return ConnectManager.from_environment(environ_name, mode=mode)


# 定义连接器的别名
connect_dolphin_meta = DSMetaConnector  # 定义海豚元数据连接器的别名
connect_hive = HiveConnector  # 定义 Hive 连接器的别名
connect_kafka_admin_client = ConnKafkaAdminClient  # 定义 Kafka 管理客户端连接器的别名
connect_kafka_consumer = ConnKafkaConsumer  # 定义 Kafka 消费者连接器的别名
connect_kafka_consumer_by_kafka_topics_group = ConnKafkaConsumer.by_kafka_topic_group  # 使用 KafkaTopicsGroup 构造 KafkaConsumer
connect_kafka_producer = ConnKafkaProducer  # 定义 Kafka 生产者连接器的别名
connect_mysql = MysqlConnector  # 定义 MySQL 连接器的别名
connect_ots = OTSConnector  # 定义 OTS 连接器的别名
create_ssh_tunnel = create_ssh_tunnel  # 定义 SSH 隧道连接器的别名

del Optional
