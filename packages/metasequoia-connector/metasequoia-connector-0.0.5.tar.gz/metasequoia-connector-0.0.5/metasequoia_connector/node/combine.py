"""
组合节点
"""

from metasequoia_connector.node.kafka import KafkaTopic
from metasequoia_connector.node.mysql import MysqlTable

__all__ = ["MysqlTableWithKafkaTopic"]


class MysqlTableWithKafkaTopic:
    """有 Kafka TOPIC 监听的 RDS 表"""

    def __init__(self, rds_table: MysqlTable, kafka_topic: KafkaTopic):
        self._rds_table = rds_table
        self._kafka_topic = kafka_topic

    @property
    def rds_table(self) -> MysqlTable:
        return self._rds_table

    @property
    def kafka_topic(self) -> KafkaTopic:
        return self._kafka_topic
