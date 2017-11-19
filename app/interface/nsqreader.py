#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nsq
from conf import config

def handler(message):
    print(message)
    return True

def start():
    r = nsq.Reader(message_handler=handler,
               nsqd_tcp_addresses=['{}:{}'.format(config.nsq['host'], config.nsq['port'])],
               topic='nsq_reader', channel='asdf', lookupd_poll_interval=15)
    nsq.run()
