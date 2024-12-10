"""
海豚元数据
"""

import dataclasses

from metasequoia_connector.node.mysql import MysqlInstance

__all__ = ["DSProcess", "DSTask", "DSProcessTask", "DSMetaInstance"]


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class DSProcess:
    """海豚工作流节点"""

    project_code: int = dataclasses.field(kw_only=True)
    process_code: int = dataclasses.field(kw_only=True)

    def get_process_url(self, domain: str):
        """获取工作流定义的 Url"""
        return f"{domain}/dolphinscheduler/ui/projects/{self.project_code}/workflow/definitions/{self.process_code}"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class DSTask:
    """海豚任务节点"""

    project_code: int = dataclasses.field(kw_only=True)
    task_code: int = dataclasses.field(kw_only=True)


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class DSProcessTask:
    """海豚工作流任务节点"""

    project_code: int = dataclasses.field(kw_only=True)
    process_code: int = dataclasses.field(kw_only=True)
    task_code: int = dataclasses.field(kw_only=True)

    def get_process_url(self, domain: str):
        """获取工作流定义的 Url"""
        return f"{domain}/dolphinscheduler/ui/projects/{self.project_code}/workflow/definitions/{self.process_code}"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class DSMetaInstance(MysqlInstance):
    """海豚调度元数据实例"""

    db: str = dataclasses.field(kw_only=True)
