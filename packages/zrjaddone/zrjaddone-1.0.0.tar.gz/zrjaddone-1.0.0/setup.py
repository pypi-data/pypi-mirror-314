#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 14:09:14 2024

@author: xiaoxiami
"""

from setuptools import setup, find_packages

setup(
    name="zrjaddone",  # 包名，发布后可用 pip 安装
    version="1.0.0",  # 版本号
    description="A simple package to add 1 to a given number",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="zrj",
    author_email="",
    url="",  # 你的项目地址
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "addone=addone.main:add_one",  # 将 `addone` 命令行映射到 `add_one` 函数
        ],
    },
)