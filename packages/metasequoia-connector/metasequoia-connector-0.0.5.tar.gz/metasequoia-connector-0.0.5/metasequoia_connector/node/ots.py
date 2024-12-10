"""
OTS 节点
"""

import dataclasses

__all__ = ["OTSInstance", "OTSTable", "OTSIndex"]


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class OTSInstance:
    """OTS 实例"""

    end_point: str = dataclasses.field(kw_only=True)
    access_key_id: str = dataclasses.field(kw_only=True)
    access_key_secret: str = dataclasses.field(kw_only=True)
    instance_name: str = dataclasses.field(kw_only=True)


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class OTSTable:
    """OTS 表"""

    ots_instance: OTSInstance = dataclasses.field(kw_only=True)
    table_name: str = dataclasses.field(kw_only=True)

    def get_ots_index(self, index_name: str):
        """获取当前表中名为 index_name 的多元索引对象"""
        return OTSIndex(ots_instance=self.ots_instance, table_name=self.table_name, index_name=index_name)


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class OTSIndex:
    """OTS 多元索引"""

    ots_instance: OTSInstance = dataclasses.field(kw_only=True)
    table_name: str = dataclasses.field(kw_only=True)
    index_name: str = dataclasses.field(kw_only=True)
