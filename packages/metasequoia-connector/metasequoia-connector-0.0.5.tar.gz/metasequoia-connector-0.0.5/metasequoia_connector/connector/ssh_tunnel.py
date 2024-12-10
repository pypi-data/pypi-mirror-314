from typing import List, Optional, Tuple

import sshtunnel

from metasequoia_connector.node import SshTunnel

__all__ = ["create_ssh_tunnel"]


def create_ssh_tunnel(ssh_tunnel: SshTunnel,
                      remote_bind_address: Optional[Tuple[str, int]] = None,
                      remote_bind_addresses: Optional[List[Tuple[str, int]]] = None
                      ) -> sshtunnel.SSHTunnelForwarder:
    """使用 SshTunnel 隧道对象创建到 remote_host:remote_port 的 SSH 隧道

    TODO 待调整所有 SSH Tunnel 的调用逻辑，避免多个绑定地址报错

    关闭隧道时需要 close()
    建议使用 WITH ... AS ... 的语法调用这个函数

    Parameters
    ----------
    ssh_tunnel : SshTunnel
        SSH 隧道对象
    remote_bind_address : Optional[Tuple[str, int]], default = None
        远端服务器地址和端口的元组，用于连接到单个远端地址
    remote_bind_addresses: Optional[List[Tuple[str, int]]], default = None
        远端服务器地址和端口的元组的列表，用于连接到多个远端地址的列表
    """
    ssh_tunnel_forwarder = sshtunnel.SSHTunnelForwarder(
        ssh_address_or_host=(ssh_tunnel.host, ssh_tunnel.port),
        ssh_username=ssh_tunnel.username,
        ssh_password=ssh_tunnel.password,
        ssh_pkey=ssh_tunnel.pkey,
        remote_bind_address=remote_bind_address,
        remote_bind_addresses=remote_bind_addresses
    )
    ssh_tunnel_forwarder.start()
    return ssh_tunnel_forwarder
