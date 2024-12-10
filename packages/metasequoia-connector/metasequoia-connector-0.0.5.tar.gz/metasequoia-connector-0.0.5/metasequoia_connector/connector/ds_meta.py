from metasequoia_connector.connector.mysql import MysqlConnector
from metasequoia_connector.node import DSMetaInstance

__all__ = ["DSMetaConnector"]


class DSMetaConnector(MysqlConnector):
    """海豚调度元数据连接器"""

    def __init__(self, dolphin_scheduler_meta_info: DSMetaInstance):
        super().__init__(dolphin_scheduler_meta_info,
                         schema=dolphin_scheduler_meta_info.db)
        self._dolphin_scheduler_meta_info = dolphin_scheduler_meta_info
