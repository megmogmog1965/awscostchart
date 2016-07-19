#!/usr/bin/env python
# encoding: utf-8

'''
Created on Jul 18, 2016

:author: Yusuke Kawatsu
'''

# built-in modules.
import os
import copy
import time
import shutil
import codecs
import sqlite3
import tempfile
import datetime

# installed modules.


# my modules.
from flaskserver.constants import _REPO_URL, _DATA_DIR, _SCHEMA_PATH


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

def replace_key(curkey, newkey, node):
    '''
    :param curkey: current key.
    :param newkey: new key.
    :param node: a node of tree.
    '''
    target = node
    
    if isinstance(node, (list, tuple, )):
        target = [ replace_key(curkey, newkey, child) for child in node ]
    
    elif isinstance(node, dict):
        target = { k: replace_key(curkey, newkey, v) for k, v in node.items() }
        if curkey in target:
            val = target.pop(curkey)
            target[newkey] = val
    
    return target

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

def connect_db():
    '''
    DB(現状はSQLite3)に接続します。DB Objectを返す
    (無かったら、Schemaから勝手に初期化・生成します)

    @return: DB.
    '''
    global _schema
    db_dir = os.path.join(_DATA_DIR)
    db_path = os.path.join(db_dir, u'sqlite.db')

    # あれば読む. 無ければ勝手に作られる.
    db = sqlite3.connect(db_path)

    # 新しいテーブルがあるかもなので、毎回schema実施.
    if not _schema:
        with codecs.open(_SCHEMA_PATH, 'r', 'utf-8') as f:
            _schema = f.read()
    db.cursor().executescript(_schema)

    return db
_schema = None

