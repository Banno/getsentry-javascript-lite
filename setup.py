#!/usr/bin/env python
"""
sentry-kafka
==============

An extension for Sentry which integrates with Apache Kafka. It will forward
events to a Kafka instance for logging.
"""
from setuptools import setup, find_packages

install_requires = [
    'kafka-python>=0.9.2',
    'sentry>=7.4.0',
]

setup(
    name='sentry-banno-javascript',
    version='1.0',
    author='Chad Killingsworth - Jack Henry and Associates, Inc.',
    author_email='chad.killingsworth@banno.com',
    url='http://github.com/banno/getsentry-banno-javascript',
    description='A Sentry extension to expand raw js stacktraces.',
    long_description=__doc__,
    packages=find_packages(),
    zip_safe=False,
    install_requires=install_requires,
    include_package_data=True,
    entry_points={
        'sentry.apps': [
            'sentry_banno_javascript = sentry_banno_javascript ',
        ],
        'sentry.plugins': [
            'banno_javascript = sentry_banno_javascript.plugin:BannoJavascriptPlugin',
         ],
    },
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
