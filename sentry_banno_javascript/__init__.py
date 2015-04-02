"""
sentry_banno_javascript
~~~~~~~~~~~~~~
"""

try:
    VERSION = __import__('pkg_resources') \
        .get_distribution('sentry_banno_javascript').version
except Exception, e:
    VERSION = 'unknown'

from sentry.plugins import register

from .plugin import BannoJavascriptPlugin

register(BannoJavascriptPlugin)
