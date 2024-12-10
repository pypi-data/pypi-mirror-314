"""
连接器通用工具类
"""

__all__ = [
    "WrapConnector"
]


class WrapConnector:
    """嵌套连接器（以提供 with 开关的功能）"""

    def __init__(self, connection):
        self._mysql_con = connection
        self._is_close = False

    def close(self):
        if self._is_close is False:
            if self._mysql_con is not None:
                self._mysql_con.close()
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
        self.close()
