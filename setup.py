#!/usr/bin/env python

from setuptools import setup

setup(
    name='sslib',
    version='0.1.0',
    author='Jonathan Queiroz',
    author_email='dev@johnjq.com',
    url='https://github.com/jqueiroz/python-sslib',
    description='A Python3 library for sharing secrets.',
    license='MIT',
    packages=['sslib', 'sslib.shamir'],
    python_requires='>=3',
)
