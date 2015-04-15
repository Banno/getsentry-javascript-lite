"""
sentry_javascript_lite.plugin
~~~~~~~~~~~~~~~~~~~~~
"""

import re

from django.conf import settings
from sentry.lang.javascript.plugin import JavascriptPlugin
from sentry.lang.javascript.processor import SourceProcessor
from sentry.interfaces.stacktrace import (Frame, Stacktrace)
from sentry_javascript_lite import VERSION

def javascript_lite_preprocess_event(data):
    if data.get('platform') != 'javascript':
        return

    processor = JavascriptLiteSourceProcessor()
    return processor.process(data)

class JavascriptPlugin(JavascriptPlugin):
    author = 'Chad Killingsworth, Jack Henry and Associates'
    author_url = 'https://github.com/Banno/getsentry-javascript-lite'
    version = VERSION
    description = "Preprocess Raw Javascript Stacktraces"
    resource_links = [
            ('Bug Tracker', 'https://github.com/Banno/getsentry-javascript-lite/issues'),
            ('Source', 'https://github.com/Banno/getsentry-javascript-lite'),
        ]
    slug = 'javascript-lite'
    title = 'Javascript-lite Event Preprocessor'
    conf_title = title
    conf_key = 'javascript-lite'

    def get_event_preprocessors(self, **kwargs):
        if not settings.SENTRY_SCRAPE_JAVASCRIPT_CONTEXT:
            return []
        return [javascript_lite_preprocess_event]


class JavascriptLiteSourceProcessor(SourceProcessor):
    chrome_ie_stacktrace_expr = re.compile(r'^\s*at (.*?) ?\(?((?:file|https?|chrome-extension):.*?):(\d+)(?::(\d+))?\)?\s*$',
        re.IGNORECASE)
    firefox_safari_stacktrace_expr = re.compile(r'^\s*(.*?)(?:\((.*?)\))?@((?:file|https?|chrome).*?):(\d+)(?::(\d+))?\s*$',
        re.IGNORECASE)
    whitespace_expr = re.compile(r'^\s+')
    location_parts_expr = re.compile(r'[\(\)\s]')

    def get_stacktraces(self, data):
        stacktraces = super(JavascriptLiteSourceProcessor, self).get_stacktraces(data);

        if (not stacktraces and 'extra' in data and
                isinstance(data['extra'], dict) and 'rawstack' in data['extra']):
            stacktraces = self.format_raw_stacktrace(data['extra']['rawstack'])
        if stacktraces:
            data['extra'].pop('rawstack', None)

        return stacktraces

    def format_raw_stacktrace(self, value):
        kwargs = {
            'frames': [],
            'frames_omitted': []
        }

        for frame in value.split('\n'):
            if JavascriptLiteSourceProcessor.chrome_ie_stacktrace_expr.search(frame):
                kwargs['frames'].append(self.format_chrome_ie_frame(frame))
            elif JavascriptLiteSourceProcessor.firefox_safari_stacktrace_expr.search(frame):
                kwargs['frames'].append(self.format_firefox_safari_frame(frame))

        if len(kwargs['frames']) > 0:
            return [Stacktrace(**kwargs)]

        return []

    def format_chrome_ie_frame(self, frame):
        tokens = JavascriptLiteSourceProcessor.chrome_ie_stacktrace_expr.findall(frame)[0]

        frame = {
            'filename': tokens[1],
            'function': tokens[0] or '?',
            'in_app': True,
        }

        try:
            frame['lineno'] = int(float(tokens[2]))
        except:
            pass

        try:
            frame['colno'] = int(float(tokens[3]))
        except:
            pass

        return Frame.to_python(frame)

    def format_firefox_safari_frame(self, frame):
        tokens = JavascriptLiteSourceProcessor.firefox_safari_stacktrace_expr.findall(frame)[0]

        frame = {
            'filename': tokens[2],
            'function': tokens[0] or '?',
            'in_app': True,
        }

        if tokens[1]:
            frame['args'] = tokens[1].split(',')

        try:
            frame['lineno'] = int(float(tokens[3]))
        except:
            pass

        try:
            frame['colno'] = int(float(tokens[4]))
        except:
            pass

        return Frame.to_python(frame)
