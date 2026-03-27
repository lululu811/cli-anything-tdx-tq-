"""
CLI E2E 测试

测试完整的命令行接口流程。
"""

import pytest
import subprocess
import json
import os
from pathlib import Path


def _resolve_cli(cli_name: str) -> list:
    """
    解析 CLI 命令路径

    Args:
        cli_name: CLI 命令名称

    Returns:
        CLI 命令列表
    """
    # 始终使用已安装版本
    return [cli_name]


class TestCLIBase:
    """测试 CLI 基础命令"""

    def test_cli_version(self):
        """测试版本号"""
        cli = _resolve_cli("cli-anything-tdx-tq")
        result = subprocess.run(
            cli + ['--version'],
            capture_output=True,
            text=True,
            shell=True
        )
        assert result.returncode == 0
        assert '1.0.0' in result.stdout

    def test_cli_help(self):
        """测试帮助信息"""
        cli = _resolve_cli("cli-anything-tdx-tq")
        result = subprocess.run(
            cli + ['--help'],
            capture_output=True,
            text=True,
            shell=True
        )
        assert result.returncode == 0
        assert 'market' in result.stdout
        assert 'stock' in result.stdout
        assert 'sector' in result.stdout

    def test_cli_status(self):
        """测试状态查询"""
        cli = _resolve_cli("cli-anything-tdx-tq")
        result = subprocess.run(
            cli + ['status'],
            capture_output=True,
            text=True,
            shell=True
        )
        assert result.returncode == 0
        assert 'TDX TQ SDK' in result.stdout or '状态' in result.stdout


class TestCLIMarket:
    """测试行情数据命令"""

    def test_market_get_help(self):
        """测试获取行情帮助"""
        cli = _resolve_cli("cli-anything-tdx-tq")
        result = subprocess.run(
            cli + ['market', 'get', '--help'],
            capture_output=True,
            text=True,
            shell=True
        )
        assert result.returncode == 0
        assert '--stocks' in result.stdout
        assert '--period' in result.stdout

    def test_market_snapshot_help(self):
        """测试行情快照帮助"""
        cli = _resolve_cli("cli-anything-tdx-tq")
        result = subprocess.run(
            cli + ['market', 'snapshot', '--help'],
            capture_output=True,
            text=True,
            shell=True
        )
        assert result.returncode == 0


class TestCLIStock:
    """测试股票信息命令"""

    def test_stock_info_help(self):
        """测试股票信息帮助"""
        cli = _resolve_cli("cli-anything-tdx-tq")
        result = subprocess.run(
            cli + ['stock', 'info', '--help'],
            capture_output=True,
            text=True,
            shell=True
        )
        assert result.returncode == 0
        assert '--stock' in result.stdout


class TestCLISector:
    """测试板块数据命令"""

    def test_sector_list_help(self):
        """测试板块列表帮助"""
        cli = _resolve_cli("cli-anything-tdx-tq")
        result = subprocess.run(
            cli + ['sector', 'list', '--help'],
            capture_output=True,
            text=True,
            shell=True
        )
        assert result.returncode == 0
        assert '--type' in result.stdout


class TestCLISubprocess:
    """测试 CLI 子进程调用"""

    def test_cli_installed(self):
        """测试 CLI 已安装"""
        # 检查是否可以通过 subprocess 调用
        try:
            result = subprocess.run(
                ['cli-anything-tdx-tq', '--version'],
                capture_output=True,
                text=True,
                timeout=10,
                shell=True
            )
            # 如果安装成功，返回 0
            assert result.returncode == 0 or '1.0.0' in result.stdout
        except FileNotFoundError:
            # 如果未安装，跳过测试
            pytest.skip("CLI 未安装到 PATH")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
