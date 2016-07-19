#!/usr/bin/env python
# encoding: utf-8

'''
Created on Jul 18, 2016

@author: Yusuke Kawatsu
'''


class _HttpError(Exception):
    '''
    :see: http://flask.pocoo.org/docs/0.10/patterns/apierrors/
    '''
    def __init__(self, message=None, status_code=500, payload=None):
        Exception.__init__(self, message)
        self._message = message
        self._status_code = status_code
        self._payload = payload
    
    @property
    def message(self):
        return self._message
    
    @property
    def status_code(self):
        return self._status_code
    
    def to_dict(self):
        rv = dict(self._payload or ())
        rv['message'] = self.message
        return rv


def make_httperror(status_code, message):
    '''
    :rtype: :class:`flaskserver.utils.http_error._HttpError`
    '''
    return _HttpError(message=message, status_code=status_code)
