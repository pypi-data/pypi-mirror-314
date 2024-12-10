"""
MySQL 相关工具类
"""

import dataclasses
from typing import Any, Dict, Generator, List, Optional, Tuple

import pymysql
import pymysql.cursors

import metasequoia_sql as ms_sql
from metasequoia_connector.connector import MysqlConnector
from metasequoia_connector.manager.connect_manager import ConnectManager
from metasequoia_connector.node import MysqlInstance, SshTunnel
from metasequoia_connector.utils.sql_format import to_quote_str_none_as_null


# ---------------------------------------- 查询方法 ----------------------------------------


def conn_select_all_as_dict(conn: pymysql.Connection, sql: str) -> Tuple[Dict[str, Any], ...]:
    """【查询】以字典列表格式返回所有结果"""
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute(sql)
        return cursor.fetchall()


def select_all_as_dict(manager: ConnectManager, mysql_name: str, db_name: str, sql: str):
    """【查询】以字典列表格式返回所有结果"""
    with manager.mysql_connect(mysql_name, db_name) as mysql_conn:
        return conn_select_all_as_dict(conn=mysql_conn, sql=sql)


def conn_select_one_as_dict(conn: pymysql.Connection, sql: str) -> Dict[str, Any]:
    """【查询】以字典格式返回一条结果"""
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute(sql)
        return cursor.fetchone()


def select_one_as_dict(manager: ConnectManager, mysql_name: str, db_name: str, sql: str):
    """【查询】以字典格式返回一条结果"""
    with manager.mysql_connect(mysql_name, db_name) as mysql_conn:
        return conn_select_one_as_dict(conn=mysql_conn, sql=sql)


def conn_execute_and_commit(conn: pymysql.Connection, sql: str) -> int:
    """【执行】执行 SQL 语句并提交，返回影响行数"""
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        result = cursor.execute(sql)
    conn.commit()
    return result


def execute_and_commit(manager: ConnectManager, mysql_name: str, db_name: str, sql: str) -> int:
    """【执行】执行 SQL 语句并提交，返回影响行数"""
    with manager.mysql_connect(mysql_name, db_name) as mysql_conn:
        return conn_execute_and_commit(conn=mysql_conn, sql=sql)


def conn_execute_and_commit_with_args(conn: pymysql.Connection, sql: str, *args) -> int:
    with conn.cursor() as cursor:
        result = cursor.execute(sql, args)
    conn.commit()
    return result


def show_databases(rds_instance: MysqlInstance):
    """执行：SHOW DATABASES"""
    with MysqlConnector(mysql_instance=rds_instance) as conn:
        return conn_show_databases(conn)


def show_tables(rds_instance: MysqlInstance, schema: str):
    """执行：SHOW TABLES"""
    with MysqlConnector(mysql_instance=rds_instance, schema=schema) as conn:
        return conn_show_tables(conn)


def show_create_table(rds_instance: MysqlInstance, schema: str, table: str,
                      ssh_tunnel: Optional[SshTunnel] = None):
    """执行：SHOW CREATE TABLE"""
    with MysqlConnector(mysql_instance=rds_instance, schema=schema) as conn:
        return conn_show_create_table(conn, table)


def conn_use(conn: pymysql.Connection, schema: str) -> None:
    with conn.cursor() as cursor:
        cursor.execute(f"USE `{schema}`")


def conn_select_all(conn: pymysql.Connection, sql: str) -> Tuple[Tuple[Any, ...], ...]:
    with conn.cursor() as cursor:
        cursor.execute(sql)
        return cursor.fetchall()


def select_iter_as_dict(manager: ConnectManager, mysql_name: str, db_name: str, sql: str,
                        primary_key: str, batch_size: int = 1000) -> Generator[Dict[str, Any], None, None]:
    """【执行】执行 SQL 语句并提交，返回影响行数"""
    with manager.mysql_connect(mysql_name, db_name) as mysql_conn:
        yield from conn_select_iter_as_dict(conn=mysql_conn, sql=sql, primary_key=primary_key, batch_size=batch_size)


def conn_select_iter_as_dict(conn: pymysql.Connection, sql: str, primary_key: str, batch_size: int = 1000
                             ) -> Generator[Dict[str, Any], None, None]:
    """使用 sql 查询 conn 连接的 MySQL，并将结果作为 dict 的迭代器返回

    使用基于 primary_key 的深翻页方法，要求：

    - primary_key 字段为主键或为唯一键（有索引，且在 WHERE 条件后仍然有索引可用于排序）
    - 提供的 SQL 语句中不能包含 GROUP BY 子句、ORDER BY 子句和 LIMIT 子句
    - 提供的 SQL 语句中查询的字段需要包含主键字段

    Parameters
    ----------
    conn : pymysql.Connection
        Mysql 连接
    sql : str
        SQL 语句
    primary_key : str
        主键或唯一键
    batch_size : int, default = 1000
        每次翻页多少条记录

    Yields
    ------
    Dict[str, Any]
        查询结果记录
    """
    # 解析并检查 SQL 语句
    select_statement: ms_sql.ASTSingleSelectStatement = ms_sql.SQLParser.parse_single_select_statement(sql)
    if select_statement.group_by_clause is not None:
        raise KeyError(f"SQL 语句包含 ORDER BY 子句：{sql}")
    if select_statement.order_by_clause is not None:
        raise KeyError(f"SQL 语句包含 ORDER BY 子句：{sql}")
    if select_statement.limit_clause is not None:
        raise KeyError(f"SQL 语句包含 LIMIT 子句：{sql}")

    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        # 构造第一次请求的语句
        actual_sql = ms_sql.ASTSingleSelectStatement(
            with_clause=select_statement.with_clause,
            select_clause=select_statement.select_clause,
            from_clause=select_statement.from_clause,
            lateral_view_clauses=select_statement.lateral_view_clauses,
            join_clauses=select_statement.join_clauses,
            where_clause=select_statement.where_clause,
            group_by_clause=select_statement.group_by_clause,
            having_clause=select_statement.having_clause,
            order_by_clause=ms_sql.SQLParser.parse_order_by_clause(f"ORDER BY {primary_key}"),
            limit_clause=ms_sql.ASTLimitClause(limit=batch_size, offset=0)
        ).source(ms_sql.SQLType.MYSQL)

        max_primary_key = None
        while True:
            n_fetch = cursor.execute(actual_sql)

            for query_row in cursor.fetchall():
                max_primary_key = query_row[primary_key]  # 更新当前主键最大值（用于下一次请求）
                yield query_row

            if n_fetch < batch_size:
                break  # 如果当前页数量少于 LIMIT 数量，则说明已经是最后一页，跳出循环

            if select_statement.where_clause is None:
                # 初始原始 SQL 语句没有 WHERE 子句的情况
                actual_sql = ms_sql.ASTSingleSelectStatement(
                    with_clause=select_statement.with_clause,
                    select_clause=select_statement.select_clause,
                    from_clause=select_statement.from_clause,
                    lateral_view_clauses=select_statement.lateral_view_clauses,
                    join_clauses=select_statement.join_clauses,
                    where_clause=ms_sql.SQLParser.parse_where_clause(f"WHERE {primary_key} > '{max_primary_key}'"),
                    group_by_clause=select_statement.group_by_clause,
                    having_clause=select_statement.having_clause,
                    order_by_clause=ms_sql.SQLParser.parse_order_by_clause(f"ORDER BY {primary_key}"),
                    limit_clause=ms_sql.ASTLimitClause(limit=batch_size, offset=0)
                ).source(ms_sql.SQLType.MYSQL)
            else:
                # 初始原始 SQL 语句有 WHERE 子句的情况
                where_condition_str = select_statement.where_clause.condition.source(ms_sql.SQLType.MYSQL)
                actual_sql = ms_sql.ASTSingleSelectStatement(
                    with_clause=select_statement.with_clause,
                    select_clause=select_statement.select_clause,
                    from_clause=select_statement.from_clause,
                    lateral_view_clauses=select_statement.lateral_view_clauses,
                    join_clauses=select_statement.join_clauses,
                    where_clause=ms_sql.SQLParser.parse_where_clause(
                        f"WHERE ({where_condition_str}) AND {primary_key} > '{max_primary_key}'"),
                    group_by_clause=select_statement.group_by_clause,
                    having_clause=select_statement.having_clause,
                    order_by_clause=ms_sql.SQLParser.parse_order_by_clause(f"ORDER BY {primary_key}"),
                    limit_clause=ms_sql.ASTLimitClause(limit=batch_size, offset=0)
                ).source(ms_sql.SQLType.MYSQL)


def conn_execute_multi_and_commit(conn: pymysql.Connection, sql_list: List[str]) -> int:
    """在同一个事务中执行多个 SQL 语句，并 commit"""
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        for sql in sql_list:
            result = cursor.execute(sql)
        conn.commit()
        return result


def conn_show_databases(conn: pymysql.Connection) -> List[str]:
    """执行 SHOW DATABASES 语句，返回数据库名称的列表"""
    return [row["Database"] for row in conn_select_all_as_dict(conn, "SHOW DATABASES")]


def conn_show_tables(conn: pymysql.Connection) -> List[str]:
    """执行 SHOW TABLES 语句，返回表名的列表"""
    return [row[0] for row in conn_select_all(conn, "SHOW TABLES")]


def conn_show_create_table(conn: pymysql.Connection, table: str) -> Optional[str]:
    """执行 SHOW CREATE TABLE 语句

    无法获取时返回 None，在以下场景下无法获取：
    1. 账号没有权限
    2. 表名不存在

    实现说明：
    1. 为使名称完全为数字的表执行正常，所以在表名外添加了引号
    """
    result = conn_select_all_as_dict(conn, f"SHOW CREATE TABLE `{table}`")[0]
    if "Create Table" in result:
        return result["Create Table"]
    else:  # 当表名不存在或没有权限时，没有 Create Table 列，只有 Error 列
        return None


def conn_insert_into_by_dict_list(conn: pymysql.Connection,
                                  table_name: str,
                                  write_list: List[dict],
                                  batch_size: int = 1000,
                                  debug: bool = False) -> int:
    """将 data 中的 dataclass 格式数据写入到 table_name 中

    Parameters
    ----------
    conn : pymysql.Connection
        MySQL 连接
    table_name : str
        表名，可以是 table_name 或 schema_name.table_name
    write_list : List[dataclasses.dataclass]
        记录的列表，要求每条记录拥有相同的结构（将根据第 1 条记录获取数据结构）
    batch_size : int, default = 1000
        每一批的数量
    debug : bool, default = False
        是否开启调试模式（开启时打印进度日志）

    Returns
    -------
    int
        影响的记录数
    """
    if len(write_list) == 0:
        return 0  # 如果没有要写入记录则返回 0

    # 获取所有列的清单（遍历所有记录获取全集）
    column_set = set()
    for item in write_list:
        column_set |= set(item.keys())
    column_list = list(column_set)
    column_list_str = ",".join(column_list)

    # 获取每条记录的值的列表
    result = 0
    value_list = []
    for i, write_data in enumerate(write_list):
        # 获取当前记录中每个字段的格式化后的值的列表
        cell_list = [to_quote_str_none_as_null(write_data.get(column)) for column in column_list]
        value_str = ",".join(cell_list)
        value_list.append(f"({value_str})")
        if len(value_list) >= batch_size:
            value_list_str = ",".join(value_list)
            sql = f"INSERT INTO `{table_name}` ({column_list_str}) VALUES {value_list_str}"
            result += conn_execute_and_commit(conn, sql)
            value_list = []
            if debug is True:
                print(f"already write {i} / {len(write_list)}")
    if value_list:
        value_list_str = ",".join(value_list)
        sql = f"INSERT INTO `{table_name}` ({column_list_str}) VALUES {value_list_str}"
        result += conn_execute_and_commit(conn, sql)
    return result


def conn_insert_dataclass_list(conn: pymysql.Connection,
                               table_name: str,
                               write_list: List[dataclasses.dataclass]) -> int:
    """将 data 中的 dataclass 格式数据写入到 table_name 中

    Parameters
    ----------
    conn : pymysql.Connection
        MySQL 连接
    table_name : str
        表名，可以是 table_name 或 schema_name.table_name
    write_list : List[dataclasses.dataclass]
        记录的列表，要求每条记录拥有相同的结构（将根据第 1 条记录获取数据结构）

    Returns
    -------
    int
        影响的记录数
    """
    if len(write_list) == 0:
        return 0  # 如果没有要写入记录则返回 0

    # 获取所有列的清单（按第 1 条记录）
    column_list = [field.name for field in dataclasses.fields(write_list[0])]
    column_list_str = ",".join(f"`{column_name}`" for column_name in column_list)

    # 获取每条记录的值的列表
    value_list = []
    for write_data in write_list:
        # 获取当前记录中每个字段的格式化后的值的列表
        cell_list = [to_quote_str_none_as_null(getattr(write_data, column))
                     for column in column_list]
        value_str = ",".join(cell_list)
        value_list.append(f"({value_str})")
    value_list_str = ",".join(value_list)
    sql = f"INSERT INTO `{table_name}` ({column_list_str}) VALUES {value_list_str}"
    return conn_execute_and_commit(conn, sql)


def insert_dataclass_list(manager: ConnectManager, mysql_name: str, db_name: str,
                          table_name: str,
                          write_list: List[dataclasses.dataclass]) -> int:
    """【执行】执行 SQL 语句并提交，返回影响行数"""
    with manager.mysql_connect(mysql_name, db_name) as mysql_conn:
        return conn_insert_dataclass_list(conn=mysql_conn, table_name=table_name, write_list=write_list)


def conn_insert_or_update_dataclass(conn: pymysql.Connection,
                                    table_name: str,
                                    write_data: dataclasses.dataclass) -> int:
    """将 dataclass 对象写入到 table_name 中

    Parameters
    ----------
    conn : pymysql.Connection
        MySQL 连接
    table_name : str
        表名，可以是 table_name 或 schema_name.table_name
    write_data : dataclasses.dataclass
        dataclasses 对象

    Returns
    -------
    int
        影响的记录数
    """
    # 获取 dataclasses 对象中的所有列
    column_name_list = [field.name for field in dataclasses.fields(write_data)]

    # 生成所有列的清单
    column_name_list_str = ",".join(f"`{column_name}`" for column_name in column_name_list)

    # 生成每个字段格式化后的值的列表
    value_list = [to_quote_str_none_as_null(getattr(write_data, column_name)) for column_name in column_name_list]
    value_list_str = ",".join(value_list)

    # 生成 ON DUPLICATE KEY UPDATE 语句
    update_list = [f"`{column_name}` = VALUES(`{column_name}`)" for column_name in column_name_list]
    update_list_str = ",".join(update_list)

    sql = (f"INSERT INTO `{table_name}` ({column_name_list_str}) "
           f"VALUES ({value_list_str}) "
           f"ON DUPLICATE KEY UPDATE {update_list_str}")

    return conn_execute_and_commit(conn, sql)


def insert_or_update_dataclass(manager: ConnectManager, mysql_name: str, db_name: str,
                               table_name: str,
                               write_data: dataclasses.dataclass) -> int:
    """【执行】执行 SQL 语句并提交，返回影响行数"""
    with manager.mysql_connect(mysql_name, db_name) as mysql_conn:
        return conn_insert_or_update_dataclass(conn=mysql_conn, table_name=table_name, write_data=write_data)


def conn_insert_into_or_update_by_dataclass_list(conn: pymysql.Connection,
                                                 table_name: str,
                                                 unique_key: List[str],
                                                 write_list: List[dataclasses.dataclass]) -> int:
    """将 data 中的 dataclass 格式数据写入到 table_name 中，如果有重复值，则更新除 unique_key 之外的字段

    语句逻辑：
    INSERT INTO ... ON DUPLICATE KEY UPDATE

    Parameters
    ----------
    conn : pymysql.Connection
        MySQL 连接
    table_name : str
        表名，可以是 table_name 或 schema_name.table_name
    unique_key : List[str]
        表唯一键，在 ON DUPLICATE KEY UPDATE 时不更新这些字段
    write_list : List[dataclasses.dataclass]
        记录的列表，要求每条记录拥有相同的结构（将根据第 1 条记录获取数据结构）

    Returns
    -------
    int
        影响的记录数
    """
    if len(write_list) == 0:
        return 0  # 如果没有要写入记录则返回 0

    # 获取所有列的清单（按第 1 条记录）
    column_list = [field.name for field in dataclasses.fields(write_list[0])]
    column_list_str = ",".join(column_list)

    # 计算所有需要更新的字段
    update_column_list = [f"`{field}`=VALUES(`{field}`)" for field in column_list if field not in unique_key]
    update_column_list_str = ",".join(update_column_list)

    # 获取每条记录的值的列表
    value_list = []
    for write_data in write_list:
        # 获取当前记录中每个字段的格式化后的值的列表
        cell_list = [to_quote_str_none_as_null(getattr(write_data, column))
                     for column in column_list]
        value_str = ",".join(cell_list)
        value_list.append(f"({value_str})")
    value_list_str = ",".join(value_list)
    sql = (f"INSERT INTO `{table_name}` ({column_list_str}) VALUES {value_list_str} "
           f"ON DUPLICATE KEY UPDATE {update_column_list_str}")
    return conn_execute_and_commit(conn, sql)


def insert_or_update_dataclass_list(manager: ConnectManager, mysql_name: str, db_name: str,
                                    unique_key: List[str],
                                    table_name: str,
                                    write_list: List[dataclasses.dataclass]) -> int:
    """【执行】执行 SQL 语句并提交，返回影响行数"""
    with manager.mysql_connect(mysql_name, db_name) as mysql_conn:
        return conn_insert_into_or_update_by_dataclass_list(conn=mysql_conn, table_name=table_name,
                                                            unique_key=unique_key, write_list=write_list)
