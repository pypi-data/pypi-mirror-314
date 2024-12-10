"""
OTS 连接器
"""

import ssl
from typing import Optional

import otssql
from metasequoia_connector.node import OTSInstance, SshTunnel

__all__ = ["OTSConnector"]


class OTSConnector:
    def __init__(self, ots_instance: OTSInstance, ssh_tunnel_info: Optional[SshTunnel] = None, **params) -> None:
        """OTS 连接的构造方法

        Parameters
        ----------
        ots_instance : OTSInstance
            OTS 实例的对象
        ssh_tunnel_info : Optional[SshTunnel]
            SSH 隧道的对象 TODO 暂未生效
        """
        self._ssh_tunnel_con = None
        self._is_close = False

        self._ots_con = otssql.connect(
            end_point=ots_instance.end_point,
            access_key_id=ots_instance.access_key_id,
            access_key_secret=ots_instance.access_key_secret,
            instance_name=ots_instance.instance_name,
            ssl_version=ssl.PROTOCOL_TLSv1_2,
            **params
        )

    def close(self, is_del: bool = False):
        if self._is_close is False:
            if self._ots_con is not None:
                # noinspection PyBroadException
                try:
                    self._ots_con.close()
                except Exception:
                    pass
            if self._ssh_tunnel_con is not None and is_del is False:
                # 如果是在对象销毁的过程中调用，则不销毁 SshTunnel 对象，因为该对象在销毁过程中调用 close 方法可能出现无法预料的报错或卡死
                # noinspection PyBroadException
                try:
                    self._ssh_tunnel_con.stop()
                except Exception:
                    pass

    def __getattr__(self, name):
        """代理嵌套连接类中的所有成员"""
        return getattr(self._ots_con, name)

    def __enter__(self):
        """在进入 WITH 语句时被调用（返回值作为 AS 后面的变量）"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """在离开 WITH 语句时被调用"""
        self.close()

    def __del__(self):
        """在对象被销毁时调用"""
        self.close(is_del=True)
