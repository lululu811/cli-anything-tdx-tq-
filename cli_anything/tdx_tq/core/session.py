"""
会话管理模块

管理 TdxTq 连接状态和生命周期。
"""

import sys
import os
from typing import Optional, Dict, Any
from pathlib import Path

# 添加通达信插件路径
tdx_dir = os.environ.get('TDX_PATH', r'D:\new_tdx64')
pyplugins_dir = os.path.join(tdx_dir, 'PYPlugins')
sys_dir = os.path.join(pyplugins_dir, 'sys')

if os.path.exists(pyplugins_dir) and pyplugins_dir not in sys.path:
    sys.path.insert(0, pyplugins_dir)
if os.path.exists(sys_dir) and sys_dir not in sys.path:
    sys.path.insert(0, sys_dir)

from tdx_tq.core import TdxTq, TdxError, TdxInitError, TdxDataError, TdxParamError


class Session:
    """CLI 会话管理类"""

    _instance: Optional['Session'] = None
    _tdx: Optional[TdxTq] = None
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._tdx is None:
            self._tdx = TdxTq()

    @property
    def tdx(self) -> TdxTq:
        """获取 TdxTq 实例"""
        return self._tdx

    @property
    def is_initialized(self) -> bool:
        """是否已初始化"""
        return self._initialized

    def initialize(self, script_path: Optional[str] = None) -> None:
        """
        初始化连接

        Args:
            script_path: 脚本路径，默认使用 __file__
        """
        if self._initialized:
            return

        if script_path is None:
            import inspect
            frame = inspect.currentframe()
            try:
                frame = inspect.stack()[1]
                script_path = frame.filename
            finally:
                del frame

        self._tdx.initialize(script_path)
        self._initialized = True

    def close(self) -> None:
        """关闭连接"""
        if self._initialized:
            self._tdx.close()
            self._initialized = False

    def ensure_initialized(self) -> None:
        """确保已初始化"""
        if not self._initialized:
            self.initialize()

    def __del__(self):
        if self._initialized:
            self.close()


# 全局会话实例
session = Session()
