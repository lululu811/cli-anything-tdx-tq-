"""
TDX TQ SDK CLI Harness - setup.py

Package: cli-anything-tdx-tq
Namespace: cli_anything.tdx_tq
"""

from setuptools import setup, find_namespace_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8') if (this_directory / "README.md").exists() else ""

setup(
    name="cli-anything-tdx-tq",
    version="1.0.0",
    author="Jin",
    description="TDX TQ SDK CLI - 通达信量化接口命令行工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_namespace_packages(include=["cli_anything.*"]),
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "pandas>=1.3.0",
        "numpy>=1.20.0",
        "tdx-tq-sdk>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "cli-anything-tdx-tq=cli_anything.tdx_tq.tdx_tq_cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="tdx 通达信 量化 trading stock finance cli",
)
