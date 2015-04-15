#!/usr/bin/env python
"""
sentry-javascript-lite
==============

An extension for Sentry which expands raw javascript stacktraces on the server
allowing for lighter clients.
"""
from setuptools import setup, find_packages

install_requires = [
    'sentry>=7.4.0',
]

setup(
    name='sentry-javascript-lite',
    version='1.0',
    download_url='https://github.com/banno/getsentry-javascript-lite/tarball/1.0',
    author='Chad Killingsworth - Jack Henry and Associates, Inc.',
    author_email='chad.killingsworth@banno.com',
    url='http://github.com/banno/getsentry-javascript-lite',
    description='A Sentry extension to expand raw js stacktraces.',
    long_description=__doc__,
    packages=find_packages(),
    zip_safe=False,
    install_requires=install_requires,
    include_package_data=True,
    license='Apache-2.0',
    entry_points={
        'sentry.apps': [
            'sentry_javascript_lite = sentry_javascript_lite ',
        ],
        'sentry.plugins': [
            'sentry_javascript_lite = sentry_javascript_lite.plugin:JavascriptPlugin',
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
