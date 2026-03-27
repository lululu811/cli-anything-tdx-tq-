"""
数据导出模块单元测试
"""

import pytest
import pandas as pd
import os
import json
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from cli_anything.tdx_tq.core.export import export_dataframe, export_dict


class TestExportDataframe:
    """测试 DataFrame 导出"""

    def setup_method(self):
        """每个测试前的准备工作"""
        self.test_dir = tempfile.mkdtemp()
        self.df = pd.DataFrame({'A': [1, 2, 3], 'B': ['a', 'b', 'c']})

    def teardown_method(self):
        """每个测试后的清理工作"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_export_dataframe_csv(self):
        """测试导出为 CSV"""
        output_path = os.path.join(self.test_dir, 'test.csv')
        result = export_dataframe(self.df, output_path, format='csv')

        assert os.path.exists(result)
        # 验证内容
        df_read = pd.read_csv(result, index_col=0)
        assert len(df_read) == 3
        assert 'A' in df_read.columns
        assert 'B' in df_read.columns

    def test_export_dataframe_json(self):
        """测试导出为 JSON"""
        output_path = os.path.join(self.test_dir, 'test.json')
        result = export_dataframe(self.df, output_path, format='json')

        assert os.path.exists(result)
        # 验证内容
        with open(result, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert len(data) == 3

    def test_export_dataframe_invalid_format(self):
        """测试无效格式"""
        output_path = os.path.join(self.test_dir, 'test.invalid')
        with pytest.raises(ValueError, match="不支持的格式"):
            export_dataframe(self.df, output_path, format='invalid')


class TestExportDict:
    """测试字典数据导出"""

    def setup_method(self):
        """每个测试前的准备工作"""
        self.test_dir = tempfile.mkdtemp()
        self.data = {
            'stock1': pd.DataFrame({'A': [1, 2]}),
            'stock2': pd.DataFrame({'A': [3, 4]})
        }

    def teardown_method(self):
        """每个测试后的清理工作"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_export_dict_csv(self):
        """测试导出字典为 CSV"""
        result = export_dict(self.data, self.test_dir, format='csv')

        assert 'stock1' in result
        assert 'stock2' in result
        assert os.path.exists(result['stock1'])
        assert os.path.exists(result['stock2'])

    def test_export_dict_with_prefix(self):
        """测试带前缀导出"""
        result = export_dict(self.data, self.test_dir, format='csv', prefix='data_')

        # 验证文件名包含前缀
        assert 'data_stock1.csv' in result['stock1']
        assert 'data_stock2.csv' in result['stock2']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
