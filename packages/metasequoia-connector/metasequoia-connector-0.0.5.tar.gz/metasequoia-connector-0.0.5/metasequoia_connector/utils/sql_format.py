"""
通用工具类
"""

import enum
from typing import Any, List, Optional

__all__ = [
    "to_quote_str_none_as_null",
    "to_quote_str_none_as_zero_str",
    "to_quote_str_none_as_empty_str"
]


class NoneAs(enum.Enum):
    """处理 None 的方法"""

    ASSERT = None  # 不允许为空
    IGNORE = None  # 跳过 None 值
    NULL = "null"  # 将 None 视作 null
    EMPTY_STR = "''"  # 将 None 视作空字符串
    ZERO_STR = "'0'"  # 将 None 视作包含 0 的字符串

    @property
    def is_visible(self) -> bool:
        """如果当前配置下 None 值是否可以转化为字面值则返回 True，否则返回 False"""
        return self.value is not None


def to_quote_str(text: Optional[Any], none_as: NoneAs) -> str:
    """将 text 转化为 sql 的单引号字符串

    Parameters
    ----------
    text : Optional[str]
        需要转化为 sql 的单引号字符串的值
    none_as : NoneAs
        处理 None 值的方法

    Returns
    -------
    str
        sql 的单引号字符串
    """
    if text is None:
        if not none_as.is_visible:
            raise KeyError(f"none_as={none_as} 时 None 值无法被直接转化为 SQL 字面值")
        return none_as.value
    if isinstance(text, str):
        text = text.replace("\\", "\\\\").replace("'", "\\'")
    return f"'{text}'"


def to_quote_str_none_as_null(text: Optional[Any]) -> str:
    """将 text 转化为 sql 的单引号字符串并将 None 值处理为 null"""
    return to_quote_str(text, none_as=NoneAs.NULL)


def to_quote_str_none_as_empty_str(text: Optional[Any]) -> str:
    """将 text 转化为 sql 的单引号字符串并将 None 值处理为空字符串"""
    return to_quote_str(text, none_as=NoneAs.EMPTY_STR)


def to_quote_str_none_as_zero_str(text: Optional[Any]) -> str:
    """将 text 转化为 sql 的单引号字符串并将 None 值处理为 '0' 字符串"""
    return to_quote_str(text, none_as=NoneAs.ZERO_STR)


def to_quote_str_list(text_list: List[Optional[Any]], none_as: NoneAs) -> str:
    """将 text_list 转化用括号包含的单引号字符串的列表"""
    if none_as == NoneAs.IGNORE:
        quote_str_list = [to_quote_str(text, none_as=NoneAs.ASSERT) for text in text_list if text is not None]
    else:
        quote_str_list = [to_quote_str(text, none_as=none_as) for text in text_list]
    return "(" + ",".join(quote_str_list) + ")"


def to_quote_str_list_none_as_ignore(text_list: List[Optional[Any]]) -> str:
    """将 text_list 转化用括号包含的单引号字符串的列表，并将 None 值忽略"""
    return to_quote_str_list(text_list, none_as=NoneAs.IGNORE)


def to_quote_str_list_none_as_null(text_list: List[Optional[Any]]) -> str:
    """将 text_list 转化用括号包含的单引号字符串的列表，并将 None 值则置为 null"""
    return to_quote_str_list(text_list, none_as=NoneAs.NULL)
