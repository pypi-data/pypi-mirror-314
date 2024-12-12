#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re

import setuptools

with open('ptools_base/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ptools_base",
    version=version,
    author="JasonZhang",
    author_email="qwertjkl9090@163.com",
    description="P Test Platform Tools Base Lib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    install_requires=[
        'pydantic==2.10.3',
    ],
    packages=setuptools.find_packages(exclude=['tests']),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
    ]
)
