#!/usr/bin/env python
# encoding: utf-8

'''
Created on Aug 4, 2016

@author: Yusuke Kawatsu.
'''

# built-in modules.
import datetime
import threading

# installed modules.
from flask import Flask
from flask import jsonify
from flask_autodoc.autodoc import Autodoc

# my modules.
from server.awsapis import aws_billing
from server.http_error import _HttpError
from server.store.costs import CostStore
from server.store.costs import MonthlyCostStore
from server.store.awskeys import AwsKeyStore
from server.util import Dot
from server.util import normalize
from server.util import json_params
from server.logger import logger


# flask app.
app = Flask(__name__, static_path=u'/static', static_folder=u'./static')
app.debug = True
auto = Autodoc(app)

# register error handler.
@app.errorhandler(_HttpError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@auto.doc()
@app.route('/', methods=['GET'])
def index():
    '''
    index page.
    '''
    # index.htmlを返す. Jinja2でrenderingはしない.
    return app.send_static_file(u'html/index.html')

@auto.doc()
@app.route('/apis', methods=['GET'])
def apidocs():
    '''
    api documentation.
    '''
    return auto.html()

@auto.doc()
@app.route('/apis/estimated_charge', methods=['GET'])
def get_estimated_charge():
    '''
    get estimated charge.
    '''
    ret = {}
    
    for key in map(lambda k: Dot(k), AwsKeyStore.keys()):
        store = CostStore(key.aws_access_key_id)
        func_pairs = [
            [ store.awsDataTransfer, u'AWSDataTransfer' ],
            [ store.awsQueueService, u'AWSQueueService' ],
            [ store.amazonEC2, u'AmazonEC2' ],
            [ store.amazonES, u'AmazonES' ],
            [ store.amazonElastiCache, u'AmazonElastiCache' ],
            [ store.amazonRDS, u'AmazonRDS' ],
            [ store.amazonRoute53, u'AmazonRoute53' ],
            [ store.amazonS3, u'AmazonS3' ],
            [ store.amazonSNS, u'AmazonSNS' ],
            [ store.awskms, u'awskms' ]
        ]
        
        part = {}
        for f, name in func_pairs:
            data = f()
            part[name] = data
        ret[key.aws_access_key_id] = part
    
    return jsonify(**normalize(ret))

@auto.doc()
@app.route('/apis/monthly', methods=['GET'])
def get_monthly():
    '''
    get monthly costs.
    '''
    ret = {}
    
    for key in map(lambda k: Dot(k), AwsKeyStore.keys()):
        store = MonthlyCostStore(CostStore(key.aws_access_key_id))
        func_pairs = [
            [ store.awsDataTransfer, u'AWSDataTransfer' ],
            [ store.awsQueueService, u'AWSQueueService' ],
            [ store.amazonEC2, u'AmazonEC2' ],
            [ store.amazonES, u'AmazonES' ],
            [ store.amazonElastiCache, u'AmazonElastiCache' ],
            [ store.amazonRDS, u'AmazonRDS' ],
            [ store.amazonRoute53, u'AmazonRoute53' ],
            [ store.amazonS3, u'AmazonS3' ],
            [ store.amazonSNS, u'AmazonSNS' ],
            [ store.awskms, u'awskms' ]
        ]
        
        part = {}
        for f, name in func_pairs:
            data = f()
            part[name] = data
        ret[key.aws_access_key_id] = part
    
    return jsonify(**normalize(ret))

@auto.doc()
@app.route('/apis/awskeys', methods=['GET'])
def get_awskeys():
    '''
    get list of aws access key / aws secret key.
    '''
    awskeys = AwsKeyStore.keys()
    return jsonify(awskeys=awskeys)

@auto.doc()
@app.route('/apis/awskeys', methods=['POST'])
def post_awskey():
    '''
    {
      "name": "...",
      "aws_access_key_id": "...",
      "aws_secret_access_key": "..."
    }
    '''
    name, aws_access_key_id, aws_secret_access_key = json_params(
        u'name', u'aws_access_key_id', u'aws_secret_access_key')
    
    # update db.
    AwsKeyStore.putKey(name, aws_access_key_id, aws_secret_access_key)
    
    return jsonify(name=name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

def _fetch_billings_every_day(hour=14, minute=0, second=0):
    '''
    start daemon thread to fetch aws-billing.
    '''
    def _exec():
        # update db.
        for key in map(lambda k: Dot(k), AwsKeyStore.keys()):
            # fetch.
            o = aws_billing(key.aws_access_key_id, key.aws_secret_access_key)
            res = o.estimated_charge()
            
            store = CostStore(key.aws_access_key_id)
            func_pairs = [
                [ store.putAwsDataTransfer, u'AWSDataTransfer' ],
                [ store.putAwsQueueService, u'AWSQueueService' ],
                [ store.putAmazonEC2, u'AmazonEC2' ],
                [ store.putAmazonES, u'AmazonES' ],
                [ store.putAmazonElastiCache, u'AmazonElastiCache' ],
                [ store.putAmazonRDS, u'AmazonRDS' ],
                [ store.putAmazonRoute53, u'AmazonRoute53' ],
                [ store.putAmazonS3, u'AmazonS3' ],
                [ store.putAmazonSNS, u'AmazonSNS' ],
                [ store.putAwskms, u'awskms' ]
            ]
            
            for f, name in func_pairs:
                if not name in res or not res[name]:
                    continue
                
                data = Dot(res[name])
                f(data.Maximum, data.Timestamp)
        
        logger.info(u'called aws clougwatch api.')
        _fetch_billings_every_day(hour, minute, second) # call recursively.
    
    # next 23:00.
    now = datetime.datetime.utcnow()
    today = datetime.datetime(now.year, now.month, now.day, hour, minute, second)
    tommorow = datetime.datetime(now.year, now.month, now.day + 1, hour, minute, second)
    sec = int((today - now).total_seconds())
    sec = sec if sec > 0 else int((tommorow - now).total_seconds())
    
    # start next one.
    threading.Timer(sec, _exec).start()
    logger.info(u'scheduled next after (sec): %s' % (sec))


if __name__ == '__main__':
    # run daemon thread.
    _fetch_billings_every_day()
    
    # :see: http://askubuntu.com/questions/224392/how-to-allow-remote-connections-to-flask
    app.run(host='0.0.0.0', port=5001, threaded=True, use_reloader=False)
