"""
海豚调度的工具方法
"""

import collections
import datetime
import json
from typing import List, Dict, Any, Tuple, Set, Union, Optional, Iterable

import pymysql

from metasequoia_connector.node import DSProcess, DSProcessTask, DSTask
from metasequoia_connector.utils import mysql, sql_format

GeneralTask = Union[DSProcessTask, DSTask]


def get_project_list(conn: pymysql.Connection) -> Tuple[Dict[str, Any], ...]:
    """获取海豚调度的项目列表"""
    return mysql.conn_select_all_as_dict(
        conn, "SELECT `code`, `name` "
              "FROM t_ds_project"
    )


def get_process_list_by_project(conn: pymysql.Connection, project_code: str) -> Tuple[Dict[str, Any], ...]:
    """获取海豚调度指定项目的工作流列表"""
    return mysql.conn_select_all_as_dict(
        conn, f"SELECT `code`, `name` "
              f"FROM t_ds_process_definition "
              f"WHERE `project_code` = '{project_code}'"
    )


def get_task_list_by_process(conn: pymysql.Connection,
                             project_code: str,
                             process_code: str
                             ) -> Tuple[Dict[str, Any], ...]:
    """获取海豚调度指定项目、工作流的任务列表"""
    return mysql.conn_select_all_as_dict(
        conn, f"SELECT DISTINCT `post_task_code` "
              f"FROM t_ds_process_task_relation "
              f"WHERE `project_code` = '{project_code}' "
              f"  AND `process_definition_code`= '{process_code}'"
    )


def get_down_process_by_process(conn: pymysql.Connection,
                                process: DSProcess
                                ) -> List[DSProcess]:
    """根据 DSProcess 工作流对象，查询依赖该任务的下游工作流对象的列表"""
    query_result = mysql.conn_select_all_as_dict(
        conn, f"SELECT t1.project_code, t1.process_definition_code "
              f"FROM t_ds_process_task_relation AS t1 "
              f"INNER JOIN ("
              f"    SELECT `project_code`, `code` "
              f"    FROM t_ds_task_definition "
              f"    WHERE task_type = 'DEPENDENT' AND task_params LIKE '%{process.project_code}%{process.process_code}%'"
              f") AS t2 ON t1.project_code = t2.project_code AND t1.post_task_code = t2.code;"
    )
    return [DSProcess(project_code=query_row["project_code"], process_code=query_row["process_definition_code"])
            for query_row in query_result]


def get_dependent_task_params_by_task_list(conn: pymysql.Connection,
                                           project_code: str,
                                           task_code_list: List[int]) -> Tuple[Dict[str, Any], ...]:
    """获取海豚指定任务列表中依赖的其他工作流任务的任务参数"""
    task_code_str = ", ".join(f"'{task_code}'" for task_code in task_code_list)
    return mysql.conn_select_all_as_dict(
        conn, f"SELECT `task_params` "
              f"FROM t_ds_task_definition "
              f"WHERE `project_code` = '{project_code}' "
              f"  AND `code` IN ({task_code_str}) "
              f"  AND `task_type` ='DEPENDENT'"
    )


def get_task_code_list_by_process_code_list(conn: pymysql.Connection, project_code: int,
                                            process_code_list: List[int]) -> List[int]:
    """获取 project_code 中的 process_code_list 对应的 task_code 的列表"""
    process_code_list_str = ",".join([f"'{process_code}'" for process_code in process_code_list])
    return [row["post_task_code"] for row in mysql.conn_select_all_as_dict(
        conn, f"SELECT DISTINCT `post_task_code` "
              f"FROM t_ds_process_task_relation "
              f"WHERE `project_code` = '{project_code}' "
              f"  AND `process_definition_code` IN ({process_code_list_str})"
    )]


def _grouped_process_by_project(process_list: List[DSProcess]) -> Dict[int, List[DSProcess]]:
    """按所属项目对工作流进行分组"""
    grouped_process_dict = collections.defaultdict(list)
    for process in process_list:
        grouped_process_dict[process.project_code].append(process)
    return grouped_process_dict


def get_task_list_by_process_list(conn: pymysql.Connection,
                                  process_list: List[DSProcess]
                                  ) -> List[DSProcessTask]:
    """根据工作流集合，获取工作流包含的工作流任务节点列表"""
    result = []
    grouped_process_dict = _grouped_process_by_project(process_list)
    for project_code, grouped_process_list in grouped_process_dict.items():
        grouped_process_list_str = ",".join(str(process.process_code) for process in grouped_process_list)
        query_data = mysql.conn_select_all_as_dict(
            conn, f"SELECT DISTINCT `process_definition_code`, `post_task_code` "
                  f"FROM t_ds_process_task_relation "
                  f"WHERE `project_code` = '{project_code}' "
                  f"  AND `process_definition_code` IN ({grouped_process_list_str})"
        )
        for query_row in query_data:
            process_code = query_row["process_definition_code"]
            task_code = query_row["post_task_code"]
            result.append(DSProcessTask(project_code=project_code, process_code=process_code, task_code=task_code))
    return result


def get_dependence_process_set(conn: pymysql.Connection, process_list: List[DSProcess]) -> Set[DSProcess]:
    """获取当前任务依赖的所有上游任务的集合"""

    # 原始工作流集合
    source_process_set = set(process_list)

    # 已经添加过的工作流集合
    visited = set(process_list)
    while process_list:
        # 按所属项目对工作流进行分组
        grouped_process_dict = _grouped_process_by_project(process_list)

        # 清空旧的 process_list
        process_list.clear()

        # 按组分析工作流
        for project_code, group_process_list in grouped_process_dict.items():
            # 获取当前项目的工作流中包含的 task_code 的列表
            process_code_list = [process.process_code for process in group_process_list]
            task_code_list = get_task_code_list_by_process_code_list(conn, project_code, process_code_list)

            # 获取当前项目的 task_code_list 的列表中，DEPENDENT 类型 task 的 task_params 字段
            task_code_list_str = ", ".join(f"'{task_code}'" for task_code in task_code_list)
            dependent_tasks_list = mysql.conn_select_all_as_dict(
                conn, f"SELECT `task_params` "
                      f"FROM t_ds_task_definition "
                      f"WHERE `project_code` = '{project_code}' "
                      f"  AND `code` IN ({task_code_list_str}) "
                      f"  AND `task_type` ='DEPENDENT'"
            )

            # 遍历所有 task_params 字段，并将其中依赖的上游任务添加到新队列中
            for dependent_task in dependent_tasks_list:
                for dependence_task in json.loads(dependent_task["task_params"])["dependence"]["dependTaskList"]:
                    for dependence_item in dependence_task["dependItemList"]:
                        dependence_process = DSProcess(project_code=dependence_item["projectCode"],  # 依赖的项目ID
                                                       process_code=dependence_item["definitionCode"])  # 依赖的工作流ID
                        if dependence_process not in visited:
                            visited.add(dependence_process)
                            process_list.append(dependence_process)

    return visited - source_process_set


def get_schedule_release_state_by_process_list(conn: pymysql.Connection, process_list: List[DSProcess]
                                               ) -> Dict[DSProcess, int]:
    """获取当前工作流集合的定时上线状态"""
    process_hash = {process.process_code: process for process in process_list}
    process_list_str = ",".join(str(process.process_code) for process in process_list)
    query_data = mysql.conn_select_all_as_dict(conn, f"SELECT `process_definition_code`, `release_state` "
                                                     f"FROM `t_ds_schedules` "
                                                     f"WHERE `process_definition_code` IN ({process_list_str})")
    return {process_hash[query_row["process_definition_code"]]: query_row["release_state"] for query_row in query_data}


def get_schedule_priority_state_by_process_list(conn: pymysql.Connection, process_list: List[DSProcess]
                                                ) -> Dict[DSProcess, int]:
    """获取当前工作流集合的定时优先级"""
    process_hash = {process.process_code: process for process in process_list}
    process_list_str = ",".join(str(process.process_code) for process in process_list)
    query_data = mysql.conn_select_all_as_dict(conn, f"SELECT `process_definition_code`, `process_instance_priority` "
                                                     f"FROM `t_ds_schedules` "
                                                     f"WHERE `process_definition_code` IN ({process_list_str})")
    return {process_hash[query_row["process_definition_code"]]: query_row["process_instance_priority"]
            for query_row in query_data}


def get_process_name_dict_by_process_list(conn: pymysql.Connection,
                                          task_list: List[DSProcess]):
    """根据 process_list 获取 process 对象到任务名称的映射关系"""
    process_hash = {task.process_code: task for task in task_list}
    process_code_list_str = ",".join([f"{task.process_code}" for task in task_list])
    query_data = mysql.conn_select_all_as_dict(
        conn, f"SELECT `code`, `name` "
              f"FROM t_ds_process_definition "
              f"WHERE `code` IN ({process_code_list_str})"
    )
    return {process_hash[query_row["code"]]: query_row["name"] for query_row in query_data}


def get_task_name_dict_by_task_list(conn: pymysql.Connection,
                                    task_list: List[GeneralTask]):
    """根据 task_list 获取 task 对象到任务名称的映射关系"""
    task_hash = {task.task_code: task for task in task_list}
    task_code_list_str = ",".join([f"{task.task_code}" for task in task_list])
    query_data = mysql.conn_select_all_as_dict(
        conn, f"SELECT `code`, `name` "
              f"FROM t_ds_task_definition "
              f"WHERE `code` IN ({task_code_list_str})"
    )
    return {task_hash[query_row["code"]]: query_row["name"] for query_row in query_data}


def filter_process_task_by_condition(conn: pymysql.Connection,
                                     task_list: List[GeneralTask],
                                     condition: str) -> List[GeneralTask]:
    """根据 condition 条件过滤 task_list 中的任务，返回新的列表"""
    task_code_list_str = ",".join([f"{task.task_code}" for task in task_list])
    query_data = mysql.conn_select_all_as_dict(
        conn, f"SELECT `code` "
              f"FROM t_ds_task_definition "
              f"WHERE `code` IN ({task_code_list_str}) "
              f"  AND {condition}"
    )
    task_code_set = {query_row["code"] for query_row in query_data}
    return [process_task for process_task in task_list if process_task.task_code in task_code_set]


def get_process_info_by_process(conn: pymysql.Connection, process: DSProcess) -> dict:
    """获取海豚调度指定工作流的名称"""
    return mysql.conn_select_one_as_dict(
        conn,
        f"SELECT * "
        f"FROM t_ds_process_definition "
        f"WHERE `project_code` = '{process.project_code}' AND `code` = '{process.process_code}'"
    )


def get_process_info_by_process_list(conn: pymysql.Connection,
                                     process_list: List[DSProcess],
                                     need_columns: Optional[List[str]] = None) -> Iterable[Dict[str, Any]]:
    """使用 DSProcess 对象的列表，查询工作流定义的详细信息"""
    # 检查并规范化参数：必须返回 project_code 和 code
    if need_columns is not None:
        if "project_code" not in need_columns:
            need_columns.append("project_code")
        if "code" not in need_columns:
            need_columns.append("code")

    # 构造查询 SQL 并执行查询
    select_column_str = ",".join([f"`{column}`" for column in need_columns]) if need_columns is not None else "*"
    process_list_str = sql_format.to_quote_str_list_none_as_ignore([process.process_code for process in process_list])
    query_result = mysql.conn_select_all_as_dict(
        conn=conn,
        sql=f"SELECT {select_column_str} FROM t_ds_process_definition WHERE `code` IN {process_list_str}"
    )

    # 根据 project_code 筛选查询结果
    final_result = []
    process_hash = {process.process_code: process.project_code for process in process_list}
    for query_row in query_result:
        process_code = query_row["code"]
        project_code = query_row["project_code"]
        if project_code == process_hash[process_code]:
            final_result.append(query_row)
    return final_result


def get_scheduler_info_by_process_list(conn: pymysql.Connection,
                                       process_list: List[DSProcess],
                                       need_columns: Optional[List[str]] = None) -> Iterable[Dict[str, Any]]:
    """使用 DSProcess 对象的列表，查询工作流的定时的上线状态"""
    select_column_str = ",".join([f"`{column}`" for column in need_columns]) if need_columns is not None else "*"
    process_list_str = sql_format.to_quote_str_list_none_as_ignore([process.process_code for process in process_list])
    return mysql.conn_select_all_as_dict(
        conn=conn,
        sql=f"SELECT {select_column_str} FROM t_ds_schedules WHERE process_definition_code IN {process_list_str}"
    )


def get_recent_state_history_by_process(conn: pymysql.Connection,
                                        process: DSProcess,
                                        limit: int = 30) -> List[str]:
    """获取 process 工作流最近 limit 次运行的 state_history 字段"""
    query_result = mysql.conn_select_all_as_dict(
        conn=conn,
        sql=f"SELECT state_history "
            f"FROM t_ds_process_instance "
            f"WHERE process_definition_code = '{process.process_code}' "
            f"ORDER BY id DESC LIMIT {limit}"
    )
    return [query_row["state_history"] for query_row in query_result]


def get_recent_start_time_and_success_time_by_process(
        conn: pymysql.Connection,
        process: DSProcess,
        limit: int = 30
) -> List[Dict[str, Optional[datetime.datetime]]]:
    """获取 process 工作流最近 limit 次运行的开始时间和结束时间"""
    result = []
    for state_history_source in get_recent_state_history_by_process(conn, process, limit):
        state_history = json.loads(state_history_source)
        row = {}
        for state_item in state_history:
            state_time = datetime.datetime.strptime(state_item["time"], "%Y-%m-%d %H:%M:%S")
            if (state_item["state"] == "RUNNING_EXECUTION"
                    and state_item["desc"] == "init running"):
                row["init_time"] = state_time  # 初始化时间
            if (state_item["state"] == "RUNNING_EXECUTION"
                    and state_item["desc"] == "start a new process from scheduler"):
                row["start_process_time"] = state_time  # 进程启动时间
            if state_item["state"] == "SUCCESS":
                row["success_time"] = state_time  # 成功时间
        result.append(row)
    return result
