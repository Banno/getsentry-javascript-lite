# sentry-javascript-lite

An extension for [Sentry](https://github.com/getsentry/sentry) to expand raw javascript stack traces on the server, rather than the client. Allows for a lighter client.

## Install

Install the package via pip:

    pip install sentry-javascript-lite

This plugin includes all of the functionality of the builtin Javascript plugin. It is redundant to have both enabled.

## Usage

The plugin looks for an extra field `rawstack` in the event data. It then attempts to expand this field into a Sentry stacktrace. This allows clients to simply submit the stack property provided with a browser exception.

Example client usage:

```JavaScript
/** @param {Error} e */
function ExceptionLogger(e) {
  var data = {
    'project': 2,
    'logger': 'my-custom-logger',
    'platform': 'javascript',
    'level': 4,
    'request': {
      'url': '' + location.href,
      'headers': {
        'User-Agent': navigator.userAgent
      }
    },
    'exception': {
      'type': e.name,
      'value': e.message
    },
    'message': e.message,
    'extra': {
      'rawstack': e.stacktrace || e.stack
    }
  };

  if (e['cause']) {
    data['cause'] = e['cause'];
  }

  if (e['culprit']) {
    data['culprit'] = e['culprit'];
  }

  var dataString = JSON.stringify(data);
  var endpoint = endpointParsedFromDsn +
      '?sentry_version=4&sentry_client=' +
      encodeURIComponent(data['logger']) +
      '&sentry_key=' + apikey +
      '&sentry_data=' + encodeURIComponent(dataString);

  var xhr = new XMLHttpRequest();
  if ('withCredentials' in xhr) {
    xhr.open('GET', endpoint, true);
    xhr.send();
  } else {
    (new Image())['src'] = endpoint;
  }
)
```

*Note: The stack or stacktrace property on browser Error objects is only provided by modern browsers. For older browser support, use the official raven-js client.*
