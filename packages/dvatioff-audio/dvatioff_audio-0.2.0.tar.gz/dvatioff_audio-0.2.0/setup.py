# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="dvatioff-audio",  # 包名，在 PyPI 上必须唯一
    version="0.2.0",  # 版本号
    author="dvatiOFF",
    author_email="dvatioff@gmail.com",
    description="Personal audio utils package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dvatiOFF/python-audio-utils",  # 可选
    packages=find_packages(),  # 自动查找需要打包的模块
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',  # 指定最低 Python 版本
)
