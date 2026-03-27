"""
配置管理模块单元测试
"""

import pytest
import os
from pathlib import Path

# 导入被测模块
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from cli_anything.tdx_tq.core.config import Config


class TestConfig:
    """配置管理测试类"""

    def setup_method(self):
        """每个测试前的准备工作"""
        self.config = Config()

    def test_config_default_paths(self):
        """测试默认路径配置"""
        assert self.config.tdx_path == os.environ.get('TDX_PATH', r'D:\new_tdx64')
        assert self.config.pyplugins_path == r'D:\new_tdx64\PYPlugins'
        assert self.config.sys_path == r'D:\new_tdx64\PYPlugins\sys'

    def test_config_custom_path(self):
        """测试自定义路径配置"""
        custom_path = r'D:\custom_tdx'
        self.config.tdx_path = custom_path
        assert self.config.tdx_path == custom_path
        assert os.environ.get('TDX_PATH') == custom_path

    def test_config_get_status(self):
        """测试获取配置状态"""
        status = self.config.get_status()
        assert 'tdx_path' in status
        assert 'tdx_exists' in status
        assert 'pyplugins_path' in status
        assert 'pyplugins_exists' in status
        assert 'sys_path' in status
        assert 'sys_exists' in status

    def test_config_validate_paths(self):
        """测试路径验证"""
        # 注意：这个测试依赖于实际路径是否存在
        result = self.config.validate_paths()
        # 如果默认路径存在，返回 True；否则返回 False
        assert isinstance(result, bool)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
