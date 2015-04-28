#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
from threading import Thread
import logging
import re
import requests 
import json
from srmail import imap

logger = logging.getLogger(__name__)


class EmailScanner(Thread):

    def __init__(self, config):
        super(EmailScanner, self).__init__()
        self.app_config = config


    def stop(self):
        logger.info("stop requested")
        self.is_running = False

    def run(self):

        self.is_running = True

        while self.is_running:

            try:
                with imap.Mailbox(self.app_config) as mbox:
                    count = mbox.get_count()
                    logger.debug('check inbox: %d email(s)' % count)
                    for num in range(count):
                        msg = mbox.fetch_message_as_json(num + 1)
                        process(mbox, msg,
                        self.app_config['global']['post_urls'])

            except:
                logger.exception("main loop exception")

            # check email every <polling> seconds
            time.sleep(self.app_config['global']['polling'])

        self.is_running = False


def process(mbox, msg, post_urls):

    headers = {'Content-Type': 'application/json; charset=utf-8'}

    for url in post_urls:

        try:
            r = requests.post(url, data=json.dumps(msg), headers=headers)
            if r.status_code in (200, 201):
                mbox.delete_message(msg['index'])
            else:
                logger.warn('bad status %d, keep message until next polling ' %
                        r.status_code)
        except:
            logger.exception('cannot post to %s' % url)


def start(config):
    scanner = EmailScanner(config)
    scanner.start()
