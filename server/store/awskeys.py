#!/usr/bin/env python
# encoding: utf-8

'''
Created on Aug 4, 2016

@author: Yusuke Kawatsu
'''

from server.store import _db


class AwsKeyStore(object):
    '''
    classdocs
    '''
    
    def __init__(self, params):
        '''
        Constructor
        '''
        pass
    
    @classmethod
    def keys(cls):
        return _db.table(u'awskeys').all()
    
    @classmethod
    def putKey(cls, name, aws_access_key_id, aws_secret_access_key):
        return _db.table(u'awskeys').insert({
            u'name': name,
            u'aws_access_key_id': aws_access_key_id,
            u'aws_secret_access_key': aws_secret_access_key
        })

