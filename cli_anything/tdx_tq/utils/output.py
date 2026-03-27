"""
输出格式化模块

处理 CLI 输出的 JSON 和文本格式。
"""

import json
import pandas as pd
from typing import Any, Dict, List, Optional


def to_json(data: Any, indent: int = 2, ensure_ascii: bool = False) -> str:
    """
    将数据转换为 JSON 字符串

    Args:
        data: 要转换的数据
        indent: 缩进空格数
        ensure_ascii: 是否转义非 ASCII 字符

    Returns:
        JSON 字符串
    """
    def convert(obj):
        if isinstance(obj, pd.DataFrame):
            return obj.to_dict('records')
        elif isinstance(obj, pd.Series):
            return obj.to_dict()
        elif hasattr(obj, 'to_dict'):
            return obj.to_dict()
        elif isinstance(obj, (pd.Timestamp, pd.DatetimeTZDtype)):
            return str(obj)
        return obj

    converted = convert(data)
    return json.dumps(converted, indent=indent, ensure_ascii=ensure_ascii, default=str)


def format_table(data: Any, show_index: bool = True) -> str:
    """
    将数据格式化为表格文本

    Args:
        data: 要格式化的数据
        show_index: 是否显示索引

    Returns:
        表格字符串
    """
    if isinstance(data, pd.DataFrame):
        return data.to_string(index=show_index)
    elif isinstance(data, dict):
        lines = []
        for k, v in data.items():
            lines.append(f"{k}: {v}")
        return '\n'.join(lines)
    elif isinstance(data, list):
        return '\n'.join(str(item) for item in data)
    return str(data)


def format_output(data: Any, output_format: str = 'text') -> str:
    """
    根据指定格式输出数据

    Args:
        data: 要输出的数据
        output_format: 输出格式 ('json' 或 'text')

    Returns:
        格式化后的字符串
    """
    if output_format == 'json':
        return to_json(data)
    else:
        return format_table(data)
