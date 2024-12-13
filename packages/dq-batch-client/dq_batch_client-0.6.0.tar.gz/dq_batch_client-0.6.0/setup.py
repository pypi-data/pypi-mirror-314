#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'requests >= 2.27.1'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='dq-batch-client',
    version='0.6.0',
    python_requires='>=3.6',
    description="Python library which allows to use http://dataquality.pl in easy way.",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
    author="Algolytics Technologies",
    author_email='info@algolytics.pl',
    url='https://github.com/Algolytics/dq_batch_client',
    packages=[
        'dq',
    ],
    package_dir={'dq': 'dq'},
    include_package_data=True,
    install_requires=requirements,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords=['dataquality', 'dq', 'dq-batch-client'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
