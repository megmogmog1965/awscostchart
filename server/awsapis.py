#!/usr/bin/env python

'''
Created on Aug 4, 2016

@author: Yusuke Kawatsu
'''

# built-in modules.
import datetime

# installed modules.
from boto.ec2 import cloudwatch

# my modules.
pass


_SERVICES = [
    u'AWSDataTransfer',
    u'AWSQueueService',
    u'AmazonEC2',
    u'AmazonES',
    u'AmazonElastiCache',
    u'AmazonRDS',
    u'AmazonRoute53',
    u'AmazonS3',
    u'AmazonSNS',
    u'awskms'
]


def aws_billing(aws_access_key_id, aws_secret_access_key):
    '''
    :rtype: :class:`server.awsapis._AwsApis`
    '''
    return _AwsApis(aws_access_key_id, aws_secret_access_key)


class _AwsApis(object):
    
    _latest_data = {}
    
    def __init__(self, aws_access_key_id, aws_secret_access_key):
        self._aws_access_key_id = aws_access_key_id
        self._aws_secret_access_key = aws_secret_access_key
    
    def estimated_charge(self):
        '''
        :return: 
            {
                u'AmazonEC2': {
                    u'Maximum': 50.64,
                    u'Timestamp': datetime.datetime(2016, 8, 1, 19, 0),
                    u'Unit': u'None'
                },
                ...
            }
        '''
        return self._all_costs()
    
    def _all_costs(self):
        # :todo: check...?
        if _AwsApis._latest_data:
            return _AwsApis._latest_data
        
        # communicate.
        _AwsApis._latest_data = dict((name, self._service_cost_of_latest(name)) for name in _SERVICES)
        
        return _AwsApis._latest_data
    
    def _service_cost_of_latest(self, service_name):
        # connection.
        con = cloudwatch.connect_to_region(
            u'us-east-1',
            aws_access_key_id=self._aws_access_key_id,
            aws_secret_access_key=self._aws_secret_access_key)
        
        end_time = datetime.datetime.utcnow()
        start_time = end_time - datetime.timedelta(hours=4)
        
        mid = con.get_metric_statistics(
            60 * 60,
            #datetime.datetime(1970, 1, 1, 0, 0, 0),
            start_time,
            end_time,
            u'EstimatedCharges',
            u'AWS/Billing',
            u'Maximum',
            dimensions = { u'ServiceName': [ service_name ], u'Currency': [ u'USD' ] }
        )
        
        mid = sorted(mid, key=lambda e: e[u'Timestamp'])
        
        return mid[-1] if mid else None

