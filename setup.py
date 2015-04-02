#!/usr/bin/env python
"""
sentry-banno-javascript
==============

An extension for Sentry which expands raw javascript stacktraces allowing
for lighter clients.
"""
from setuptools import setup, find_packages

install_requires = [
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
            'sentry_banno_javascript = sentry_banno_javascript.plugin:BannoJavascriptPlugin',
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
