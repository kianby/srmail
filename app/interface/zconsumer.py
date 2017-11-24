#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zmq
from conf import config
from threading import Thread

TOPIC = ''

context = zmq.Context()


class Consumer(Thread):

    def run(self):
        subscriber = context.socket(zmq.SUB)
        subscriber.connect('tcp://127.0.0.1:{}'.format(config.zmq['pub_port']))
        subscriber.setsockopt_string(zmq.SUBSCRIBE, TOPIC)
        self.loop = True
        while self.loop:
            message = subscriber.recv()
            logger.info('read {}'.format(message))

    def stop(self):
        self.loop = False


def start():
    c = Consumer()
    c.start()
