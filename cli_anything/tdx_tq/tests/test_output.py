"""
输出格式化模块单元测试
"""

import pytest
import pandas as pd
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from cli_anything.tdx_tq.utils.output import to_json, format_table, format_output


class TestToJson:
    """测试 JSON 转换"""

    def test_to_json_dict(self):
        """测试字典转 JSON"""
        data = {'name': '测试', 'value': 100}
        result = to_json(data)
        parsed = json.loads(result)
        assert parsed['name'] == '测试'
        assert parsed['value'] == 100

    def test_to_json_dataframe(self):
        """测试 DataFrame 转 JSON"""
        df = pd.DataFrame({'A': [1, 2], 'B': ['a', 'b']})
        result = to_json(df)
        parsed = json.loads(result)
        assert len(parsed) == 2
        assert parsed[0]['A'] == 1
        assert parsed[0]['B'] == 'a'

    def test_to_json_custom_indent(self):
        """测试自定义缩进"""
        data = {'key': 'value'}
        result = to_json(data, indent=4)
        assert '    ' in result  # 4 空格缩进

    def test_to_json_ensure_ascii(self):
        """测试 ASCII 转义"""
        data = {'name': '测试'}
        result_ascii = to_json(data, ensure_ascii=True)
        result_utf8 = to_json(data, ensure_ascii=False)
        assert '\\u' in result_ascii
        assert '测试' in result_utf8


class TestFormatTable:
    """测试表格格式化"""

    def test_format_table_dataframe(self):
        """测试 DataFrame 表格化"""
        df = pd.DataFrame({'A': [1, 2], 'B': ['a', 'b']})
        result = format_table(df)
        assert 'A' in result
        assert 'B' in result
        assert '1' in result
        assert '2' in result

    def test_format_table_dict(self):
        """测试字典表格化"""
        data = {'key1': 'value1', 'key2': 'value2'}
        result = format_table(data)
        assert 'key1' in result
        assert 'value1' in result

    def test_format_table_list(self):
        """测试列表表格化"""
        data = ['item1', 'item2', 'item3']
        result = format_table(data)
        assert 'item1' in result
        assert 'item2' in result
        assert 'item3' in result


class TestFormatOutput:
    """测试格式输出"""

    def test_format_output_json(self):
        """测试 JSON 格式输出"""
        data = {'key': 'value'}
        result = format_output(data, output_format='json')
        parsed = json.loads(result)
        assert parsed['key'] == 'value'

    def test_format_output_text(self):
        """测试文本格式输出"""
        df = pd.DataFrame({'A': [1, 2]})
        result = format_output(df, output_format='text')
        assert 'A' in result


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
