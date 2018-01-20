#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import zmq
from threading import Thread
from conf import config
from core import emailer
from model.email import Email

logger = logging.getLogger(__name__)


def process(message):
    data = json.loads(message)
    if data['topic'] == 'email:send':
        logger.info('send mail => {}'.format(data))
        emailer.mail(data)
    elif data['topic'] == 'email:delete':
        logger.info('delete mail => {}'.format(data))
        email = Email.get(Email.id ==data['id'])
        if email is None:
            logger.info('cannot retrieve email {}'.format(data))
        else:
            email.delete()


class Consumer(Thread):

    def __init__(self):
        super(Consumer, self).__init__()

    def run(self):
        logger.info('start zclient')
        context = zmq.Context()
        zsub = context.socket(zmq.SUB)
        zsub.connect('tcp://127.0.0.1:{}'.format(config.zmq['pub_port']))
        zsub.setsockopt_string(zmq.SUBSCRIBE, '')
        self.loop = True
        while self.loop:
            message = zsub.recv()
            try:
                process(message)
            except:
                logger.exception('cannot process zbroker message')

    def stop(self):
        self.loop = False


def start():
    client = Consumer()
    client.start()
    return client
