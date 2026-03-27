"""
配置管理模块

管理 CLI 配置和路径设置。
"""

import os
from pathlib import Path
from typing import Optional


class Config:
    """CLI 配置管理类"""

    # 默认通达信路径
    DEFAULT_TDX_PATH = r'D:\new_tdx64'

    # 默认插件路径
    DEFAULT_PYPLUGINS_PATH = r'D:\new_tdx64\PYPlugins'
    DEFAULT_SYS_PATH = r'D:\new_tdx64\PYPlugins\sys'

    def __init__(self):
        self._tdx_path: Optional[str] = None
        self._pyplugins_path: Optional[str] = None
        self._sys_path: Optional[str] = None

    @property
    def tdx_path(self) -> str:
        """获取通达信安装路径"""
        return self._tdx_path or os.environ.get('TDX_PATH', self.DEFAULT_TDX_PATH)

    @tdx_path.setter
    def tdx_path(self, value: str):
        self._tdx_path = value
        os.environ['TDX_PATH'] = value

    @property
    def pyplugins_path(self) -> str:
        """获取插件路径"""
        return self._pyplugins_path or self.DEFAULT_PYPLUGINS_PATH

    @property
    def sys_path(self) -> str:
        """获取系统插件路径"""
        return self._sys_path or self.DEFAULT_SYS_PATH

    def validate_paths(self) -> bool:
        """验证路径是否存在"""
        paths = [
            self.tdx_path,
            self.pyplugins_path,
            self.sys_path
        ]
        return all(os.path.exists(p) for p in paths)

    def get_status(self) -> dict:
        """获取配置状态"""
        return {
            'tdx_path': self.tdx_path,
            'tdx_exists': os.path.exists(self.tdx_path),
            'pyplugins_path': self.pyplugins_path,
            'pyplugins_exists': os.path.exists(self.pyplugins_path),
            'sys_path': self.sys_path,
            'sys_exists': os.path.exists(self.sys_path)
        }


# 全局配置实例
config = Config()
