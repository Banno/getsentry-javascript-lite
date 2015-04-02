"""
sentry_banno_javascript.models
~~~~~~~~~~~~~~~~~~~~~
"""

import math
import re

from django.conf import settings
from sentry.lang.javascript.plugin import JavascriptPlugin
from sentry.lang.javascript.processor import SourceProcessor
from sentry.interfaces.stacktrace import (Frame, Stacktrace)
from sentry_banno_javascript import VERSION

def banno_preprocess_event(data):
    if data.get('platform') != 'javascript':
        return

    processor = BannoSourceProcessor()
    return processor.process(data)

class BannoJavascriptPlugin(JavascriptPlugin):
    author = 'Chad Killingsworth, Jack Henry and Associates'
    author_url = 'https://github.com/Banno/getsentry-banno-javascript'
    version = VERSION
    description = "Preprocess Javascript Events and Obtain Sourcemaps from S3"
    resource_links = [
        ('Bug Tracker', 'https://github.com/Banno/getsentry-banno-javascript/issues'),
        ('Source', 'https://github.com/Banno/getsentry-banno-javascript'),
        ]
    slug = 'banno-javascript'
    title = 'Banno Javascript Event Preprocessor'
    conf_title = title
    conf_key = 'banno-javascript'

    def get_event_preprocessors(self, **kwargs):
        if not settings.SENTRY_SCRAPE_JAVASCRIPT_CONTEXT:
            return []
        return [banno_preprocess_event]


class BannoSourceProcessor(SourceProcessor):
    chrome_ie_stacktrace_expr = re.compile(r'\s+at ')
    firefox_safari_stacktrace_expr = re.compile(r'\S+\:\d+')
    whitespace_expr = re.compile(r'^\s+')
    location_parts_expr = re.compile(r'[\(\)\s]')

    def get_stacktraces(self, data):
        stacktraces = super(BannoSourceProcessor, self).get_stacktraces(data);

        if (not stacktraces and 'extra' in data and
                isinstance(data['extra'], dict) and 'rawstack' in data['extra']):
            stacktraces = self.format_raw_stacktrace(data['extra']['rawstack'])
        if stacktraces:
            data['extra'].pop('rawstack', None)

        return stacktraces

    def process(self, data):
        return super(BannoSourceProcessor, self).process(data)

    def format_raw_stacktrace(self, value):
        try:
            if re.search(BannoSourceProcessor.chrome_ie_stacktrace_expr, value):
                return [self.format_chrome_ie_stacktrace(value)]
            if re.search(BannoSourceProcessor.firefox_safari_stacktrace_expr, value):
                return [self.format_firefox_safari_stacktrace(value)]
        except:
            return []

    def format_chrome_ie_stacktrace(self, value):
        kwargs = {
            'frames': [],
            'frames_omitted': []
        }

        for frame in value.split('\n'):
            if not BannoSourceProcessor.chrome_ie_stacktrace_expr.search(frame):
                continue
            tokens = re.split(r'\s+', re.sub(BannoSourceProcessor.whitespace_expr, '', frame))[1:]
            location = self.extract_location(re.sub(BannoSourceProcessor.location_parts_expr, '', tokens.pop()))
            functionName = tokens[0] if len(tokens) > 0 and tokens[0] != 'Anonymous' else None
            if functionName == 'new':
                functionName = (tokens[1] if len(tokens) > 2 and
                                tokens[1] != 'Anonymous' else None)

            kwargs['frames'].append(
                Frame.to_python({
                    'filename': location[0],
                    'lineno': location[1],
                    'colno': location[2],
                    'function': functionName,
                    'in_app': True,
                })
            )

        return Stacktrace(**kwargs)


    def format_firefox_safari_stacktrace(self, value):
        kwargs = {
            'frames': [],
            'frames_omitted': []
        }

        for frame in value.split('\n'):
            if not BannoSourceProcessor.firefox_safari_stacktrace_expr.search(frame):
                continue
            tokens = frame.split('@')
            location = self.extract_location(tokens.pop())
            functionName = None
            if len(tokens) > 0:
                functionName = tokens[0]
                tokens = tokens[1:]

            kwargs['frames'].append(
                Frame.to_python({
                    'filename': location[0],
                    'lineno': location[1],
                    'colno': location[2],
                    'function': functionName,
                    'in_app': True,
                })
            )

        return Stacktrace(**kwargs)

    def extract_location(self, value):
        locationParts = value.split(':')
        lastNumber = locationParts.pop()
        try:
            possibleNumber = float(locationParts[-1])
        except:
            possibleNumber = float('NaN')

        if not math.isnan(possibleNumber) and not math.isinf(possibleNumber):
            lineNumber = locationParts.pop()
            return (':'.join(locationParts), lineNumber, lastNumber)

        return (':'.join(locationParts), lastNumber, None)

