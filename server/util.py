#!/usr/bin/env python
# encoding: utf-8

'''
Created on Aug 4, 2016

:author: Yusuke Kawatsu
'''

# built-in modules.
import os
import copy
import time
import shutil
import tempfile
import datetime

# installed modules.
pass

# my modules.
pass


class TempDir(object):
    '''
    temporaryのdirectoryを作って、確実に消す.
    '''

    @classmethod
    def parentDir(cls):
        return tempfile.gettempdir()

    @property
    def name(self):
        return self._name

    def __init__(self):
        self._name = tempfile.mkdtemp()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if os.path.isdir(self._name):
            shutil.rmtree(self._name)

    def __del__(self):
        if os.path.isdir(self._name):
            shutil.rmtree(self._name)

class Dot(object):
    def __init__(self, dic):
        self._dic = dic
    
    def __getattr__(self, attr):
        raw = self._dic[attr]
        return Dot(raw) if isinstance(raw, dict) else raw


def root_dir():
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return to_unicode(parent_dir)

def to_unicode(encodedStr):
    ''' an unicode-str. '''
    if isinstance(encodedStr, unicode):
        return encodedStr

    for charset in [u'cp932', u'utf-8', u'euc-jp', u'shift-jis', u'iso2022-jp']:
        try:
            return encodedStr.decode(charset)
        except:
            pass

def to_str(unicodeStr):
    ''' an unicode-str. '''
    if isinstance(unicodeStr, str):
        return unicodeStr
    
    for charset in [u'cp932', u'utf-8', u'euc-jp', u'shift-jis', u'iso2022-jp']:
        try:
            return unicodeStr.encode(charset)
        except:
            pass

def strtime(dtime=None):
    '''
    :param dtime: use datetime.datetime.utcnow() if dtime is none.
    :rtype: unicode
    '''
    target = dtime if dtime else datetime.datetime.utcnow()
    return to_unicode(target.strftime(u'%Y-%m-%dT%H:%M:%S.%fZ'))

def retry(func, times=3, cooldown=10):
    '''
    :param func: lambda式 (引数無し).
    :param times: 最大試行回数.
    :param cooldown: 待ち時間 (sec).
    '''
    for i in xrange(times - 1):
        i # for warning.
        try:
            return func()
        except:
            time.sleep(cooldown)

    return func()

def merge_json(dest, src):
    '''
    :param dest: dict
    :param src: dict
    '''
    dest = copy.deepcopy(dest)

    for key, val in src.items():
        if isinstance(val, dict) and key in dest and isinstance(dest[key], dict):
            # object.
            branch = merge_json(dest[key], val)
            dest[key] = branch
        else:
            # other.
            dest[key] = val

    return dest

def normalize(node):
    '''
    - datetime.datetime --> integer (milli-sec unixtime)
    '''
    if isinstance(node, list):
        for i, child in enumerate(node):
            new_child = normalize(child)
            node[i] = new_child
    
    elif isinstance(node, dict):
        for k, v in node.items():
            new_child = normalize(v)
            node[k] = new_child
    
    elif isinstance(node, datetime.datetime):
        timestamp = int(time.mktime(node.timetuple()) * 1000)
        return timestamp
    
    return node

