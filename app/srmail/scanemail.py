#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
from threading import Thread
import logging
import re
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
                    # logger.debug('check inbox: %d email(s)' % count)
                    for num in range(count):
                        msg_num = num + 1
                        msg = mbox.fetch_message_as_json(msg_num)
                        process(mbox, msg_num, msg)
                        #break

            except:
                logger.exception("main loop exception")

            # check email every 30 seconds
            # TODO make configurable
            time.sleep(300)

        self.is_running = False


def process(mbox, msg_num, msg):

    # log message
    logger.info('%s Message %d %s' % ('-' * 30, msg_num, '-' * 30))
    for key in msg.keys():
        logger.info('%s = %s' % (key, msg[key]))

    msg['type'] = 'reply_comment_email'
    # TODO notify listeners
    #processor.enqueue(msg)

    # delete message
    #mbox.delete_message(msg_num)


def start(config):
    scanner = EmailScanner(config)
    scanner.start()
