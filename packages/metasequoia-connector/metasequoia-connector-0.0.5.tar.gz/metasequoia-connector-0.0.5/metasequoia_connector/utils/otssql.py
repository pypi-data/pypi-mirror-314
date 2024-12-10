"""
otssql 工具函数
"""

from typing import Any, Dict, Tuple

import otssql
from metasequoia_connector.manager.connect_manager import ConnectManager


def conn_select_all_as_dict(conn: otssql.Connection, sql: str) -> Tuple[Dict[str, Any], ...]:
    """使用 sql 查询 conn 连接的 MySQL，并将结果作为 dict 的列表返回"""
    with conn.cursor(otssql.cursor.DictCursor) as cursor:
        cursor.execute(sql)
        return cursor.fetchall()


def select_all_as_dict(manager: ConnectManager, ots_name: str, sql: str, **params):
    with manager.otssql_connect(ots_name, **params) as ots_conn:
        return conn_select_all_as_dict(conn=ots_conn, sql=sql)


def conn_select_one_as_dict(conn: otssql.Connection, sql: str) -> Dict[str, Any]:
    with conn.cursor(otssql.cursor.DictCursor) as cursor:
        cursor.execute(sql)
        return cursor.fetchone()


def select_one_as_dict(manager: ConnectManager, ots_name: str, sql: str):
    with manager.otssql_connect(ots_name) as ots_conn:
        return conn_select_one_as_dict(conn=ots_conn, sql=sql)


def conn_execute_and_commit(conn: otssql.Connection, sql: str) -> int:
    """执行 SQL 语句，并 commit"""
    with conn.cursor(otssql.cursor.DictCursor) as cursor:
        result = cursor.execute(sql)
    conn.commit()
    return result


def execute_and_commit(manager: ConnectManager, ots_name: str, sql: str) -> int:
    with manager.otssql_connect(ots_name) as ots_conn:
        return conn_execute_and_commit(conn=ots_conn, sql=sql)
