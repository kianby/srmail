#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import time
import re
from threading import Thread
import logging
import json
import smtplib
from email.mime.text import MIMEText
from conf import config
from core import imap
from model.email import Email
import zmq

logger = logging.getLogger(__name__)

if config.zmq['active']:
    context = zmq.Context()
    zpub = context.socket(zmq.PUB)
    zpub.connect('tcp://127.0.0.1:{}'.format(config.zmq['sub_port']))


class Emailer(Thread):

    def __init__(self):
        super(Emailer, self).__init__()

    def stop(self):
        logger.info("stop requested")
        self.is_running = False

    def run(self):

        self.is_running = True

        # broadcast stored emails on startup
        broadcast_zmq()

        while self.is_running:

            try:
                with imap.Mailbox() as mbox:
                    count = mbox.get_count()
                    if not count:
                        continue
                    logger.debug('inbox: %d email(s)' % count)
                    for num in range(count):
                        msg = mbox.fetch_message(num + 1)
                        if persist(msg):
                            mbox.delete_message(msg['index'])
                            time.sleep(10)
            except:
                logger.exception("main loop exception")

            # check email every <polling> seconds
            sleep_time = 0
            while sleep_time < config.general['polling']:
                if not self.is_running:
                    break
                time.sleep(1)
                sleep_time = sleep_time + 1

        self.is_running = False


def broadcast_zmq():
    if not config.zmq['active']:
        return

    for email in Email.select():
        z_msg = email.to_dict()
        z_msg['topic'] = 'email:newmail'
        zpub.send_string(json.dumps(z_msg, indent=False, sort_keys=False))


def persist(msg):

    logger.info('Persist msg [%s]' % msg)

    content = dict(msg)
    del content['index']
    del content['to']

    email = Email(
        encoding=msg['encoding'],
        date=msg['datetime'],
        fromaddr=msg['from'],
        toaddr=msg['to'],
        subject=msg['subject'],
        content=content
    )
    email = email.save()

    # send message to ZMQ
    if config.zmq['active']:
        for email in Email.select():
            z_msg = email.to_dict()
        z_msg['topic'] = 'email:newmail'
        zpub.send_string(json.dumps(z_msg, indent=False, sort_keys=False))

    return True


def mail(m):

    from_email = config.smtp['login']
    if 'from' in m:
        from_email = m['from']

    # Create the container (outer) email message.
    msg = MIMEText(m['content'])
    msg['Subject'] = m['subject']
    msg['To'] = m['to']
    msg['From'] = from_email

    s = smtplib.SMTP(config.smtp['host'], config.smtp['port'])
    if config.smtp['starttls']:
        s.starttls()
    s.login(config.smtp['login'], config.smtp['password'])
    # s.sendmail(from_email, m['to'], msg.as_bytes())
    s.send_message(msg)
    s.quit()


def start():
    emailer = Emailer()
    emailer.start()
    return emailer
