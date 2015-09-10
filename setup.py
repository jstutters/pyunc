#!/usr/bin/env python

"""
Setup file for PyUNC
"""

from setuptools import setup


setup(
    name='PyUNC',
    description='Classes for reading UNC format MRI files',
    url='https://github.com/jstutters/PyUNC',
    version='0.0.1',
    author='Jon Stutters',
    author_email='j.stutters@ucl.ac.uk',
    packages=['pyunc'],
    install_requires=[
        "numpy",
    ]
)
