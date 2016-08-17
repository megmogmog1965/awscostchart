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
import codecs
import sqlite3
import tempfile
import datetime

# installed modules.
from flask import request

# my modules.
from http_error import make_httperror


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

def resource_dir():
    return os.path.join(root_dir(), u'resources')

def data_dir():
    dirpath = os.path.join(root_dir(), u'data')
    if not os.path.isdir(dirpath):
        os.mkdir(dirpath)
    return dirpath

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

def json_params(*keys, **default_values):
    '''
    :param key: 
    :param default_value: 
    :return: 
    :raise http_error._HttpError: 
    '''
    params = request.json
    
    missing_keys = filter(lambda k: not k in params, keys)
    if missing_keys:
        raise make_httperror(404, u'missing query params: %s' % (missing_keys))
    
    part1 = map(lambda k: params[k], keys)
    part2 = map(lambda k: params[k] if k in params else default_values[k], default_values)
    
    return part1 + part2

def connect_db():
    '''
    DB(現状はSQLite3)に接続します。DB Objectを返す
    (無かったら、Schemaから勝手に初期化・生成します)

    @return: DB.
    '''
    global _schema
    db_path = os.path.join(data_dir(), u'sqlite.db')

    # あれば読む. 無ければ勝手に作られる.
    db = sqlite3.connect(db_path)

    # 新しいテーブルがあるかもなので、毎回schema実施.
    if not _schema:
        schema_path = os.path.join(resource_dir(), u'schema.sql')
        with codecs.open(schema_path, 'r', 'utf-8') as f:
            _schema = f.read()
    db.cursor().executescript(_schema)

    return db
_schema = None

def __convert_oldjsondb_into_sqlitedb():
    '''
    convert old json.db (tinydb) to sqlite3.
    '''
    with codecs.open(os.path.join(root_dir(), u'db.json'), 'r', 'utf-8') as f:
        import json
        json_data = json.load(f)
    
    # awskeys.
    awskeys = [ json_data[u'awskeys'][key] for key in sorted(json_data[u'awskeys'].keys()) ]
    print awskeys
    
    # service costs.
    service_costs = []
    for service_name in [ u'AmazonES', u'AmazonRoute53', u'AmazonEC2', u'AWSDataTransfer', u'awskms', u'AmazonElastiCache', u'AmazonRDS', u'AmazonSNS', u'AmazonS3', u'AWSQueueService' ]:
        part = [ json_data[service_name][key] for key in sorted(json_data[service_name].keys()) ]
        part = map(lambda e: dict(e, service_name=service_name), part)
        service_costs.extend(part)
    service_costs = sorted(service_costs, key=lambda e: e[u'timestamp'])
    print service_costs
    
    # write into db.
    with connect_db() as db:
        for obj in awskeys:
            aws_access_key_id = obj[u'aws_access_key_id']
            aws_secret_access_key = obj[u'aws_secret_access_key']
            name = obj[u'name']
            db.execute(u'insert into awskeys values (?, ?, ?)', (aws_access_key_id, aws_secret_access_key, name, ))
        
        for obj in service_costs:
            service_name = obj[u'service_name']
            aws_access_key_id = obj[u'aws_access_key_id']
            timestamp = obj[u'timestamp']
            value = obj[u'value']
            db.execute(u'insert into service_costs values (null, ?, ?, ?, ?)', (service_name, aws_access_key_id, timestamp, value, ))
        
        db.commit()

