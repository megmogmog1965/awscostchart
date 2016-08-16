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
    return & store estimated charge.
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def awsDataTransfer(self, aws_access_key_id):
        return self._get_all(u'AWSDataTransfer', aws_access_key_id)
    
    def putAwsDataTransfer(self, aws_access_key_id, value, timestamp):
        '''
        :param value: any value.
        :param datetime.datetime timestamp: timestamp.
        '''
        return self._put_daily_data(u'AWSDataTransfer', aws_access_key_id, value, timestamp)
    
    def awsQueueService(self, aws_access_key_id):
        return self._get_all(u'AWSQueueService', aws_access_key_id)
    
    def putAwsQueueService(self, aws_access_key_id, value, timestamp):
        '''
        :param value: any value.
        :param datetime.datetime timestamp: timestamp.
        '''
        return self._put_daily_data(u'AWSQueueService', aws_access_key_id, value, timestamp)
    
    def amazonEC2(self, aws_access_key_id):
        return self._get_all(u'AmazonEC2', aws_access_key_id)
    
    def putAmazonEC2(self, aws_access_key_id, value, timestamp):
        '''
        :param value: any value.
        :param datetime.datetime timestamp: timestamp.
        '''
        return self._put_daily_data(u'AmazonEC2', aws_access_key_id, value, timestamp)
    
    def amazonES(self, aws_access_key_id):
        return self._get_all(u'AmazonES', aws_access_key_id)
    
    def putAmazonES(self, aws_access_key_id, value, timestamp):
        '''
        :param value: any value.
        :param datetime.datetime timestamp: timestamp.
        '''
        return self._put_daily_data(u'AmazonES', aws_access_key_id, value, timestamp)
    
    def amazonElastiCache(self, aws_access_key_id):
        return self._get_all(u'AmazonElastiCache', aws_access_key_id)
    
    def putAmazonElastiCache(self, aws_access_key_id, value, timestamp):
        '''
        :param value: any value.
        :param datetime.datetime timestamp: timestamp.
        '''
        return self._put_daily_data(u'AmazonElastiCache', aws_access_key_id, value, timestamp)
    
    def amazonRDS(self, aws_access_key_id):
        return self._get_all(u'AmazonRDS', aws_access_key_id)
    
    def putAmazonRDS(self, aws_access_key_id, value, timestamp):
        '''
        :param value: any value.
        :param datetime.datetime timestamp: timestamp.
        '''
        return self._put_daily_data(u'AmazonRDS', aws_access_key_id, value, timestamp)
    
    def amazonRoute53(self, aws_access_key_id):
        return self._get_all(u'AmazonRoute53', aws_access_key_id)
    
    def putAmazonRoute53(self, aws_access_key_id, value, timestamp):
        '''
        :param value: any value.
        :param datetime.datetime timestamp: timestamp.
        '''
        return self._put_daily_data(u'AmazonRoute53', aws_access_key_id, value, timestamp)
    
    def amazonS3(self, aws_access_key_id):
        return self._get_all(u'AmazonS3', aws_access_key_id)
    
    def putAmazonS3(self, aws_access_key_id, value, timestamp):
        '''
        :param value: any value.
        :param datetime.datetime timestamp: timestamp.
        '''
        return self._put_daily_data(u'AmazonS3', aws_access_key_id, value, timestamp)
    
    def amazonSNS(self, aws_access_key_id):
        return self._get_all(u'AmazonSNS', aws_access_key_id)
    
    def putAmazonSNS(self, aws_access_key_id, value, timestamp):
        '''
        :param value: any value.
        :param datetime.datetime timestamp: timestamp.
        '''
        return self._put_daily_data(u'AmazonSNS', aws_access_key_id, value, timestamp)
    
    def awskms(self, aws_access_key_id):
        return self._get_all(u'awskms', aws_access_key_id)
    
    def putAwskms(self, aws_access_key_id, value, timestamp):
        '''
        :param value: any value.
        :param datetime.datetime timestamp: timestamp.
        '''
        return self._put_daily_data(u'awskms', aws_access_key_id, value, timestamp)
    
    
    def _get_all(self, table_name, aws_access_key_id):
        Cost = Query()
        raw = _db.table(table_name).search(Cost.aws_access_key_id == aws_access_key_id)
        return map(lambda d: dict(d, timestamp=datetime.datetime.utcfromtimestamp(d[u'timestamp'])), raw)
    
    def _put_daily_data(self, table_name, aws_access_key_id, value, timestamp):
#         :todo: aws_access_key_id
        unixtime = calendar.timegm(timestamp.utctimetuple())
        return _db.table(table_name).insert({ u'aws_access_key_id': aws_access_key_id, u'value': value, u'timestamp': unixtime })


class MonthlyCostStore(object):
    '''
    return costs for each month.
    '''
    
    def __init__(self, inner):
        '''
        Constructor
        '''
        assert isinstance(inner, CostStore)
        self._inner = inner
    
    def awsDataTransfer(self, *args, **kwargs):
        return self._filter_monthly( self._inner.awsDataTransfer(*args, **kwargs) )
    
    def awsQueueService(self, *args, **kwargs):
        return self._filter_monthly( self._inner.awsQueueService(*args, **kwargs) )
    
    def amazonEC2(self, *args, **kwargs):
        return self._filter_monthly( self._inner.amazonEC2(*args, **kwargs) )
    
    def amazonES(self, *args, **kwargs):
        return self._filter_monthly( self._inner.amazonES(*args, **kwargs) )
    
    def amazonElastiCache(self, *args, **kwargs):
        return self._filter_monthly( self._inner.amazonElastiCache(*args, **kwargs) )
    
    def amazonRDS(self, *args, **kwargs):
        return self._filter_monthly( self._inner.amazonRDS(*args, **kwargs) )
    
    def amazonRoute53(self, *args, **kwargs):
        return self._filter_monthly( self._inner.amazonRoute53(*args, **kwargs) )
    
    def amazonS3(self, *args, **kwargs):
        return self._filter_monthly( self._inner.amazonS3(*args, **kwargs) )
    
    def amazonSNS(self, *args, **kwargs):
        return self._filter_monthly( self._inner.amazonSNS(*args, **kwargs) )
    
    def awskms(self, *args, **kwargs):
        return self._filter_monthly( self._inner.awskms(*args, **kwargs) )
    
    
    def _filter_monthly(self, data):
        mid = sorted(data, reverse=True, key=lambda e: e[u'timestamp'])
        
        def _gen(seq):
            prev = datetime.datetime(1970, 1, 1, 0, 0, 0)
            for e in seq:
                dt = e[u'timestamp']
                if dt.year == prev.year and dt.month == prev.month:
                    continue
                prev = dt
                
                yield e
        
        mid = list(_gen(mid))
        mid.reverse()
        
        return mid
