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
                errors.append('Line %s: %s'
                    % (error['lineno'], error['error']))

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


def process_args():
    usage = 'Usage: minimizejs.py [filename]'
    parser = OptionParser(usage=usage)
    option, args = parser.parse_args()

    if len(args) < 1:
        return sys.stdin
    else:
        return args[0]


def main():
    js = process_args()
    try:
        data = minimize(js)
        print data
    except Exception, e:
        print >>sys.stderr, unicode(e)


if __name__ == '__main__':
    main()
