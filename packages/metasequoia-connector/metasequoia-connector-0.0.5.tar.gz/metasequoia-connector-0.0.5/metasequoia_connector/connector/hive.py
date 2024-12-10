"""
Hive 连接器
"""

import random
from typing import Optional

from pyhive import hive

from metasequoia_connector.connector.ssh_tunnel import create_ssh_tunnel
from metasequoia_connector.node import HiveInstance

__all__ = ["HiveConnector"]


class HiveConnector:
    def __init__(self,
                 hive_instance: HiveInstance,
                 schema: Optional[str] = None) -> None:
        """MySQL 连接的构造方法

        Parameters
        ----------
        hive_instance : RdsInstance
            MySQL 实例的配置
        schema : Optional[str], default = None
            数据库名称
        """
        self.hive_instance_info = hive_instance  # MySQl 实例的配置
        self.schema = schema  # 数据库

        # 初始化 Hive 连接和 SSH 隧道连接
        self.hive_conn = None
        self.ssh_tunnel_conn = None

    def __enter__(self):
        """在进入 with as 语句的时候被 with 调用，返回值作为 as 后面的变量

        因为 pyhive 不支持连接多个 Hive Client 的集群，因此在其中随机选择
        """

        choose_host = random.choice(self.hive_instance_info.hosts)

        ssh_tunnel_info = self.hive_instance_info.ssh_tunnel

        if ssh_tunnel_info is not None:
            # 启动 SSH 隧道
            self.ssh_tunnel_conn = create_ssh_tunnel(
                ssh_tunnel_info,
                remote_bind_address=(choose_host, self.hive_instance_info.port)
            )

            # 更新 MySQL 连接信息，令 MySQL 连接到 SSH 隧道
            host = "127.0.0.1"
            port = self.ssh_tunnel_conn.local_bind_port
        else:
            host = choose_host
            port = self.hive_instance_info.port

        self.hive_conn = hive.Connection(host=host, port=port, username=self.hive_instance_info.username)

        return self.hive_conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.hive_conn is not None:
            self.hive_conn.close()
        if self.ssh_tunnel_conn is not None:
            self.ssh_tunnel_conn.close()
