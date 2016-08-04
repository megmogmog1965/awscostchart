#!/usr/bin/env python
# encoding: utf-8

'''
Created on Aug 4, 2016

@author: Yusuke Kawatsu.
'''

# built-in modules.
import os
import logging
from logging.config import fileConfig

# my modules.
from server.util import root_dir


# setup logger.
_conf_path = os.path.join(root_dir(), u'logging.ini')
fileConfig(_conf_path)
logger = logging.getLogger(u'awscostchart')
