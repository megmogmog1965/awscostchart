#!/usr/bin/env python
# encoding: utf-8

'''
Created on Jul 18, 2016

@author: Yusuke Kawatsu.
'''

# built-in modules.
import os
import logging
from logging.config import fileConfig

# my modules.
from flaskserver.constants import _ROOT_DIR


# setup logger.
conf_path = os.path.join(_ROOT_DIR, u'logging.ini')
fileConfig(conf_path)
logger = logging.getLogger(u'infraapp')

