#!/usr/bin/env python
# encoding: utf-8

'''
Created on Aug 4, 2016

@author: Yusuke Kawatsu
'''

# built-in modules.
import calendar
import datetime

# my modules.
from server.store import _db

# installed modules.
from tinydb.queries import Query


class CostStore(object):
    '''
    classdocs
    '''
    
    def __init__(self, params):
        '''
        Constructor
        '''
        pass
    
    @classmethod
    def awsDataTransfer(cls, aws_access_key_id):
        return CostStore._get_all(u'AWSDataTransfer', aws_access_key_id)
    
    @classmethod
    def putAwsDataTransfer(cls, aws_access_key_id, value, timestamp):
        '''
        :param value: any value.
        :param datetime.datetime timestamp: timestamp.
        '''
        return CostStore._put_daily_data(u'AWSDataTransfer', aws_access_key_id, value, timestamp)
    
    @classmethod
    def awsQueueService(cls, aws_access_key_id):
        return CostStore._get_all(u'AWSQueueService', aws_access_key_id)
    
    @classmethod
    def putAwsQueueService(cls, aws_access_key_id, value, timestamp):
        '''
        :param value: any value.
        :param datetime.datetime timestamp: timestamp.
        '''
        return CostStore._put_daily_data(u'AWSQueueService', aws_access_key_id, value, timestamp)
    
    @classmethod
    def amazonEC2(cls, aws_access_key_id):
        return CostStore._get_all(u'AmazonEC2', aws_access_key_id)
    
    @classmethod
    def putAmazonEC2(cls, aws_access_key_id, value, timestamp):
        '''
        :param value: any value.
        :param datetime.datetime timestamp: timestamp.
        '''
        return CostStore._put_daily_data(u'AmazonEC2', aws_access_key_id, value, timestamp)
    
    @classmethod
    def amazonES(cls, aws_access_key_id):
        return CostStore._get_all(u'AmazonES', aws_access_key_id)
    
    @classmethod
    def putAmazonES(cls, aws_access_key_id, value, timestamp):
        '''
        :param value: any value.
        :param datetime.datetime timestamp: timestamp.
        '''
        return CostStore._put_daily_data(u'AmazonES', aws_access_key_id, value, timestamp)
    
    @classmethod
    def amazonElastiCache(cls, aws_access_key_id):
        return CostStore._get_all(u'AmazonElastiCache', aws_access_key_id)
    
    @classmethod
    def putAmazonElastiCache(cls, aws_access_key_id, value, timestamp):
        '''
        :param value: any value.
        :param datetime.datetime timestamp: timestamp.
        '''
        return CostStore._put_daily_data(u'AmazonElastiCache', aws_access_key_id, value, timestamp)
    
    @classmethod
    def amazonRDS(cls, aws_access_key_id):
        return CostStore._get_all(u'AmazonRDS', aws_access_key_id)
    
    @classmethod
    def putAmazonRDS(cls, aws_access_key_id, value, timestamp):
        '''
        :param value: any value.
        :param datetime.datetime timestamp: timestamp.
        '''
        return CostStore._put_daily_data(u'AmazonRDS', aws_access_key_id, value, timestamp)
    
    @classmethod
    def amazonRoute53(cls, aws_access_key_id):
        return CostStore._get_all(u'AmazonRoute53', aws_access_key_id)
    
    @classmethod
    def putAmazonRoute53(cls, aws_access_key_id, value, timestamp):
        '''
        :param value: any value.
        :param datetime.datetime timestamp: timestamp.
        '''
        return CostStore._put_daily_data(u'AmazonRoute53', aws_access_key_id, value, timestamp)
    
    @classmethod
    def amazonS3(cls, aws_access_key_id):
        return CostStore._get_all(u'AmazonS3', aws_access_key_id)
    
    @classmethod
    def putAmazonS3(cls, aws_access_key_id, value, timestamp):
        '''
        :param value: any value.
        :param datetime.datetime timestamp: timestamp.
        '''
        return CostStore._put_daily_data(u'AmazonS3', aws_access_key_id, value, timestamp)
    
    @classmethod
    def amazonSNS(cls, aws_access_key_id):
        return CostStore._get_all(u'AmazonSNS', aws_access_key_id)
    
    @classmethod
    def putAmazonSNS(cls, aws_access_key_id, value, timestamp):
        '''
        :param value: any value.
        :param datetime.datetime timestamp: timestamp.
        '''
        return CostStore._put_daily_data(u'AmazonSNS', aws_access_key_id, value, timestamp)
    
    @classmethod
    def awskms(cls, aws_access_key_id):
        return CostStore._get_all(u'awskms', aws_access_key_id)
    
    @classmethod
    def putAwskms(cls, aws_access_key_id, value, timestamp):
        '''
        :param value: any value.
        :param datetime.datetime timestamp: timestamp.
        '''
        return CostStore._put_daily_data(u'awskms', aws_access_key_id, value, timestamp)
    
    
    @classmethod
    def _get_all(cls, table_name, aws_access_key_id):
        Cost = Query()
        raw = _db.table(table_name).search(Cost.aws_access_key_id == aws_access_key_id)
        return map(lambda d: dict(d, timestamp=datetime.datetime.utcfromtimestamp(d[u'timestamp'])), raw)
    
    @classmethod
    def _put_daily_data(cls, table_name, aws_access_key_id, value, timestamp):
#         :todo: aws_access_key_id
        unixtime = calendar.timegm(timestamp.utctimetuple())
        return _db.table(table_name).insert({ u'aws_access_key_id': aws_access_key_id, u'value': value, u'timestamp': unixtime })


