#!/usr/bin/env python3

# for this setup.py, we have scripts/ which should be installed to /usr/bin
# the library is in encdec/

from setuptools import setup, find_packages
import os

setup(
    name='encdec',
    version='0.1',
    description='encoding and decoding tools',
    author='Aaron Esau',
    maintainer='Aaron Esau',
    packages=['encdec'],
    scripts=['scripts/'+x for x in os.listdir('scripts/')],
)
