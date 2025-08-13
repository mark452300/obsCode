#!/usr/bin/env python3
"""
OBS SDK 安装脚本

用于将 obs_sdk 安装为可导入的 Python 包。
"""

from setuptools import setup, find_packages
import os

# 读取 README 文件
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), "docs", "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return "OBS SDK - 模块化的 OBS 控制库"

setup(
    name="obs-sdk",
    version="1.0.0",
    description="模块化的 OBS Studio 控制库",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="OBS SDK Team",
    author_email="",
    url="https://github.com/your-repo/obs-sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Video",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "obs-websocket-py>=1.0",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "black",
            "flake8",
        ],
    },
    entry_points={
        "console_scripts": [
            "obs-sdk-test=tests.test_scene_creation:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
