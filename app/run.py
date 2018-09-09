#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
import os

import sys
from clize import Clize, run
from flask import Flask
from flask_apscheduler import APScheduler
from conf import config


# configure logging
def configure_logging(level):
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    # create formatter
    formatter = logging.Formatter("[%(asctime)s] %(name)s %(levelname)s %(message)s")
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    root_logger.addHandler(ch)


class JobConfig(object):

    JOBS = []

    def __init__(self, polling_seconds):
        self.JOBS = [
            {
                "id": "fetch_mail",
                "func": "core.emailer:fetch_email",
                "trigger": "interval",
                "seconds": polling_seconds,
            }
        ]


@Clize
def srmail_server(config_pathname):

    app = Flask(__name__)
    config.initialize(config_pathname, app)

    # configure logging
    logger = logging.getLogger(__name__)
    configure_logging(logging.INFO)

    # initialize database
    from core import database

    database.setup()

    # cron email fetcher
    app.config.from_object(JobConfig(config.getInt(config.IMAP_POLLING)))
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    logger.info("Starting SRMAIL application")

    # start Flask
    from interface import api

    logger.debug("Load interface %s" % api)

    app.run(
        host=config.get(config.HTTP_HOST),
        port=config.get(config.HTTP_PORT),
        debug=False,
        use_reloader=False,
    )

    # Exit application
    logger.info("Stopping SRMAIL application")


if __name__ == "__main__":
    run(srmail_server)
