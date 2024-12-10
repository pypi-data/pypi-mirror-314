#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from os.path import join as path_join, dirname as path_dirname

from setuptools import setup, find_packages

try:
    # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:
    # for pip <= 9.0.3
    from pip.req import parse_requirements

'''
try:
    requirements = [str(ir.req) for ir in parse_requirements("requirements.txt", session=False)]
except AttributeError:
    requirements = [str(ir.requirement) for ir in parse_requirements("requirements.txt", session=False)]
'''

def get_version():
    scope = {}
    with open(path_join(path_dirname(__file__), "dbfactor_analyzer", "version.py")) as fp:
        exec(fp.read(), scope)
    return scope.get('__version__', '1.1')


setup_args = dict(
    name='dbfactor_analyzer',
    version=get_version(),
    packages=find_packages(exclude=("tests", "tests.*")),
    author='DBZQ',
    author_email='xxli1017@foxmail.com',
    maintainer="",
    maintainer_email="",
    description='DBZQ single factor analyzer',
    zip_safe=False,
    platforms=["all"],
    license='Apache License v2',
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    #install_requires=requirements,
    include_package_data=True,
)


def main():
    setup(**setup_args)


if __name__ == "__main__":
    main()