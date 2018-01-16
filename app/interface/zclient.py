#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zmq
from conf import config
from threading import Thread
import logging

logger = logging.getLogger(__name__)

context = zmq.Context()


class Consumer(Thread):

    def run(self):
        zsub = context.socket(zmq.SUB)
        zsub.connect('tcp://127.0.0.1:{}'.format(config.zmq['pub_port']))
        zsub.setsockopt_string(zmq.SUBSCRIBE, '')
        self.loop = True
        while self.loop:
            message = zsub.recv()
            logger.info('read {}'.format(message))

    def stop(self):
        self.loop = False


def start():
    c = Consumer()
    c.start()
