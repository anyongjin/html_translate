#!/usr/bin/python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='html_translate',
    version='0.1.1',
    author='anyongjin',
    description='translate html text into another language',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pyyaml',
        'beautifulsoup4'
    ],
    # MANIFEST.in中包含需要打包的文件。这里指定需要安装的文件（安装所有）
    include_package_data=True
)

