"""
MySQL 连接器
"""

import redis

from metasequoia_connector.connector.ssh_tunnel import create_ssh_tunnel
from metasequoia_connector.node import RedisDatabase

__all__ = [
    "RedisConnector",
    "RedisConnectionPool",
]


class RedisConnectionPool:
    """Redis 连接池"""

    def __init__(self, redis_database: RedisDatabase) -> None:
        """Redis 连接的构造方法

        Parameters
        ----------
        redis_database : MysqlInstance
            Redis 实例对象
        """
        self._ssh_tunnel_con = None
        self._is_close = False

        if redis_database.instance.ssh_tunnel is not None:
            # 启动 SSH 隧道
            self._ssh_tunnel_con = create_ssh_tunnel(
                redis_database.instance.ssh_tunnel,
                remote_bind_address=(redis_database.instance.host, redis_database.instance.port)
            )

            # 更新 Redis 连接信息，令 Redis 连接到 SSH 隧道
            host = "127.0.0.1"
            port = self._ssh_tunnel_con.local_bind_port
        else:
            host = redis_database.instance.host
            port = redis_database.instance.port

        # 启动 Redis 连接池
        self._connection_pool = redis.ConnectionPool(
            host=host,
            password=redis_database.instance.passwd,
            db=redis_database.db,
            port=port
        )

    def close(self, is_del: bool = False):
        if self._is_close is False:
            if self._connection_pool is not None:
                # noinspection PyBroadException
                try:
                    self._connection_pool.disconnect()
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
        return getattr(self._connection_pool, name)

    def __enter__(self):
        """在进入 WITH 语句时被调用（返回值作为 AS 后面的变量）"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """在离开 WITH 语句时被调用"""
        self.close()

    def __del__(self):
        """在对象被销毁时调用"""
        self.close(is_del=True)


class RedisConnector:
    def __init__(self, redis_database: RedisDatabase) -> None:
        """Redis 连接的构造方法

        Parameters
        ----------
        redis_database : MysqlInstance
            Redis 实例对象
        """
        self._ssh_tunnel_con = None
        self._is_close = False

        if redis_database.instance.ssh_tunnel is not None:
            # 启动 SSH 隧道
            self._ssh_tunnel_con = create_ssh_tunnel(
                redis_database.instance.ssh_tunnel,
                remote_bind_address=(redis_database.instance.host, redis_database.instance.port)
            )

            # 更新 Redis 连接信息，令 Redis 连接到 SSH 隧道
            host = "127.0.0.1"
            port = self._ssh_tunnel_con.local_bind_port
        else:
            host = redis_database.instance.host
            port = redis_database.instance.port

        # 启动 Redis 连接
        connection_pool = redis.ConnectionPool(
            host=host,
            password=redis_database.instance.passwd,
            db=redis_database.db,
            port=port
        )
        self._redis_con = redis.Redis(connection_pool=connection_pool)

    def close(self, is_del: bool = False):
        if self._is_close is False:
            if self._redis_con is not None:
                # noinspection PyBroadException
                try:
                    self._redis_con.close()
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
        return getattr(self._redis_con, name)

    def __enter__(self):
        """在进入 WITH 语句时被调用（返回值作为 AS 后面的变量）"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """在离开 WITH 语句时被调用"""
        self.close()

    def __del__(self):
        """在对象被销毁时调用"""
        self.close(is_del=True)
