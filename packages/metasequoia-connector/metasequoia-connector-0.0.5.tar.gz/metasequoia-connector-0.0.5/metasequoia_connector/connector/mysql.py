"""
MySQL 连接器
"""

from typing import Optional

import dbutils
import pymysql
import pymysql.cursors

from metasequoia_connector.connector.ssh_tunnel import create_ssh_tunnel
from metasequoia_connector.node import MysqlInstance

__all__ = [
    "MysqlConnectionPool",
    "MysqlConnector",
]


class MysqlConnectionPool:
    """MySQL 连接池"""

    def __init__(self,
                 mysql_instance: MysqlInstance,
                 schema: Optional[str] = None,
                 connect_timeout: int = 5,
                 read_timeout: int = 10) -> None:
        """MySQL 连接的构造方法

        Parameters
        ----------
        mysql_instance : MysqlInstance
            MySQL 实例对象
        schema : Optional[str], default = None
            数据库名称
        connect_timeout : int, default = 10
            连接超时时间
        read_timeout : int, default = 30
            读取超时时间
        """
        self._ssh_tunnel_con = None
        self._is_close = False

        # 初始化 MySQL 连接和 SSH 隧道连接
        if mysql_instance.ssh_tunnel is not None:
            # 启动 SSH 隧道
            self._ssh_tunnel_con = create_ssh_tunnel(
                mysql_instance.ssh_tunnel,
                remote_bind_address=(mysql_instance.host, mysql_instance.port)
            )

            # 更新 MySQL 连接信息，令 MySQL 连接到 SSH 隧道
            host = "127.0.0.1"
            port = self._ssh_tunnel_con.local_bind_port
        else:
            host = mysql_instance.host
            port = mysql_instance.port

        # 启动 MySQL 连接
        self._mysql_pool = dbutils.pooled_db.PooledDB(
            creator=pymysql,
            host=host,
            port=port,
            user=mysql_instance.user,
            passwd=mysql_instance.passwd,
            db=schema,
            connect_timeout=connect_timeout,
            read_timeout=read_timeout
        )

    def close(self, is_del: bool = False):
        if self._is_close is False:
            if self._mysql_pool is not None:
                # noinspection PyBroadException
                try:
                    self._mysql_pool.close()
                except Exception:
                    pass
            if self._ssh_tunnel_con is not None and is_del is False:
                # 如果是在对象销毁的过程中调用，则不销毁 SshTunnel 对象，因为该对象在销毁过程中调用 close 方法可能出现无法预料的报错或卡死
                # noinspection PyBroadException
                try:
                    self._ssh_tunnel_con.stop()
                except Exception:
                    pass
            self._is_close = True

    def __getattr__(self, name):
        """代理嵌套连接类中的所有成员"""
        return getattr(self._mysql_pool, name)

    def __enter__(self):
        """在进入 WITH 语句时被调用（返回值作为 AS 后面的变量）"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """在离开 WITH 语句时被调用"""
        self.close()

    def __del__(self):
        """在对象被销毁时调用"""
        self.close(is_del=True)


class MysqlConnector:
    def __init__(self,
                 mysql_instance: MysqlInstance,
                 schema: Optional[str] = None,
                 connect_timeout: int = 5,
                 read_timeout: int = 10) -> None:
        """MySQL 连接的构造方法

        Parameters
        ----------
        mysql_instance : MysqlInstance
            MySQL 实例对象
        schema : Optional[str], default = None
            数据库名称
        connect_timeout : int, default = 10
            连接超时时间
        read_timeout : int, default = 30
            读取超时时间
        """
        self._ssh_tunnel_con = None
        self._is_close = False

        # 初始化 MySQL 连接和 SSH 隧道连接
        if mysql_instance.ssh_tunnel is not None:
            # 启动 SSH 隧道
            self._ssh_tunnel_con = create_ssh_tunnel(
                mysql_instance.ssh_tunnel,
                remote_bind_address=(mysql_instance.host, mysql_instance.port)
            )

            # 更新 MySQL 连接信息，令 MySQL 连接到 SSH 隧道
            host = "127.0.0.1"
            port = self._ssh_tunnel_con.local_bind_port
        else:
            host = mysql_instance.host
            port = mysql_instance.port

        # 启动 MySQL 连接
        self._mysql_con = pymysql.connect(
            host=host,
            port=port,
            user=mysql_instance.user,
            passwd=mysql_instance.passwd,
            db=schema,
            connect_timeout=connect_timeout,
            read_timeout=read_timeout
        )

    def close(self, is_del: bool = False):
        if self._is_close is False:
            if self._mysql_con is not None:
                # noinspection PyBroadException
                try:
                    self._mysql_con.close()
                except Exception:
                    pass
            if self._ssh_tunnel_con is not None and is_del is False:
                # 如果是在对象销毁的过程中调用，则不销毁 SshTunnel 对象，因为该对象在销毁过程中调用 close 方法可能出现无法预料的报错或卡死
                # noinspection PyBroadException
                try:
                    self._ssh_tunnel_con.stop()
                except Exception:
                    pass
            self._is_close = True

    def __getattr__(self, name):
        """代理嵌套连接类中的所有成员"""
        return getattr(self._mysql_con, name)

    def __enter__(self):
        """在进入 WITH 语句时被调用（返回值作为 AS 后面的变量）"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """在离开 WITH 语句时被调用"""
        self.close()

    def __del__(self):
        """在对象被销毁时调用"""
        self.close(is_del=True)
