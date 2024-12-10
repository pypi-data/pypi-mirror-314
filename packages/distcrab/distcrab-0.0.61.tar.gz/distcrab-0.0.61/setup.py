#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from setuptools import setup, find_packages

setup(
    name='distcrab',
    version='0.0.61',
    long_description=(Path(__file__).parent / 'readme.md').read_text(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'asyncssh',
        'aiodav',
        'aiofile',
        'aiostream',
        'humanize',
        'dnspython',
        'GitPython',
        'httpx',
        'pyOpenSSL',
    ]
)
