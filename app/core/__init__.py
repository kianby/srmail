#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import logging
from flask import Flask
from conf import config
from core import emailer
from core import database

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

# initialize database
database.setup()

# start emailer service
mailer = emailer.start()

# initialize REST API
from interface import api
from interface import admin
from interface import zconsumer

logger.info('Starting SRMAIL application')

# start NSQ connector
if( config.zmq['active']):
    zconsumer.start()

# start HTTP server
if( config.http['active']):
    app.run(host=config.http['host'],
            port=config.http['port'],
            debug=False, use_reloader=False)
else:
    input("\nPress Enter to stop.")

# Exit application
if mailer:
    mailer.stop()

logger.info('Stopping SRMAIL application')
sys.exit(0)
