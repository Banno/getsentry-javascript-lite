"""
sentry_javascript_lite
~~~~~~~~~~~~~~
"""

try:
    VERSION = __import__('pkg_resources') \
        .get_distribution('sentry_javascript_lite').version
except Exception, e:
    VERSION = 'unknown'
