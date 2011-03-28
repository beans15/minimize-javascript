#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import urllib
import urllib2

import simplejson

from optparse import OptionParser


def minimize(js):
    if isinstance(js, basestring):
        js = open(js)

    with js:
        code = js.read()
        post = [
            ('js_code', code),
            ('compilation_level', 'SIMPLE_OPTIMIZATIONS'),
            ('output_format', 'json'),
            ('output_info', 'compiled_code'),
            ('output_info', 'errors'),
        ]
        post_data = urllib.urlencode(post)

        request = \
            urllib2.Request('http://closure-compiler.appspot.com/compile')
        request.add_data(post_data)

        response = urllib2.urlopen(request)
        compiled_data = simplejson.load(response)

        if compiled_data.get('errors', None):
            errors = []
            for error in compiled_data['errors']:
                errors.append('Line %s: %s' % (error['lineno'], error['error']))

            error_message = "Syntax error:\n"
            error_message += "\n".join(errors)
            raise RuntimeError(error_message)
        elif compiled_data.get('serverErrors', None):
            errors = []
            for error in compiled_data['serverErrors']:
                errors.append(error['error'])

            error_message = "Server error:\n"
            error_message += "\n".join(errors)
            raise RuntimeError(error_message)

        return compiled_data['compiledCode']


if __name__ == '__main__':
    argv = sys.argv[1:]
    if len(argv) < 1:
        print >>sys.stderr, 'error: Specify javascript file.'
        sys.exit(-1)

    try:
        js = argv[0]
        minimized_data = minimize(js)
        print minimized_data
    except Exception, e:
        print >>sys.stderr, unicode(e)
        sys.exit(-1)
