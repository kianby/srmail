#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import json
import logging
from flask import Flask
from conf import config
from srmail import emailer

app = Flask(__name__)

def configure_logging(level):

    logger.setLevel(level)

    ch = logging.StreamHandler()
    ch.setLevel(level)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s'
                                  ' - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)


# configure logging
logger = logging.getLogger(__name__)
configure_logging(logging.DEBUG)

# set configuration
config.cwd = os.getcwd()

# we start email inbox polling thread
mailer = emailer.start()

# import API
from srmail import api

logger.info('Starting SRMAIL application')

app.run(host=config.http['host'],
        port=config.http['port'],
        debug=False, use_reloader=False)

# Exit application
if mailer:
    mailer.stop()

logger.info('Stopping SRMAIL application (%d)' % config.exit_code)
sys.exit(config.exit_code)