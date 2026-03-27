"""
数据导出模块

导出数据到各种格式（CSV, JSON, Excel）。
"""

import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional, Union


def export_dataframe(
    df: pd.DataFrame,
    output_path: str,
    format: str = 'csv',
    **kwargs
) -> str:
    """
    导出 DataFrame 到文件

    Args:
        df: 要导出的 DataFrame
        output_path: 输出文件路径
        format: 输出格式 ('csv', 'json', 'excel')

    Returns:
        输出文件路径
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if format == 'csv':
        df.to_csv(path, index=True, encoding='utf-8-sig')
    elif format == 'json':
        df.to_json(path, orient='records', force_ascii=False, indent=2)
    elif format == 'excel':
        df.to_excel(path, index=True, engine='openpyxl')
    else:
        raise ValueError(f"不支持的格式：{format}")

    return str(path)


def export_dict(
    data: Dict[str, Any],
    output_dir: str,
    format: str = 'csv',
    prefix: str = ''
) -> Dict[str, str]:
    """
    导出字典数据到文件

    Args:
        data: 数据字典，键为文件名前缀，值为 DataFrame
        output_dir: 输出目录
        format: 输出格式
        prefix: 文件名前缀

    Returns:
        输出文件路径字典
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    exported_files = {}

    for key, df in data.items():
        if isinstance(df, pd.DataFrame):
            filename = f"{prefix}{key}.{format}"
            filepath = output_path / filename
            export_dataframe(df, str(filepath), format=format)
            exported_files[key] = str(filepath)

    return exported_files


def create_export_parser():
    """创建导出参数解析器"""
    import argparse
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-o', '--output', required=True, help='输出文件路径')
    parser.add_argument('-f', '--format', choices=['csv', 'json', 'excel'], default='csv',
                       help='输出格式')
    return parser
