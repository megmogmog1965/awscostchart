#!/usr/bin/env python
# encoding: utf-8

'''
Created on Aug 4, 2016

@author: Yusuke Kawatsu
'''

# my modules.
from server.util import connect_db


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
        with connect_db() as db:
            cursor = db.cursor()
            cursor.execute(u'select aws_access_key_id, aws_secret_access_key, name from awskeys order by aws_access_key_id')
            ret = [ {
                    u'aws_access_key_id': row[0],
                    u'aws_secret_access_key': row[1],
                    u'name': row[2]
                } for row in cursor.fetchall() ]
            
            return ret
    
    @classmethod
    def putKey(cls, name, aws_access_key_id, aws_secret_access_key):
        with connect_db() as db:
            db.execute(u'insert into awskeys values (?, ?, ?)', (aws_access_key_id, aws_secret_access_key, name, ))
            db.commit()
