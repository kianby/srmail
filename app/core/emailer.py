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

logger = logging.getLogger(__name__)


class Emailer(Thread):

    def __init__(self):
        super(Emailer, self).__init__()

    def stop(self):
        logger.info("stop requested")
        self.is_running = False

    def run(self):

        self.is_running = True

        while self.is_running:

            try:
                with imap.Mailbox() as mbox:
                    count = mbox.get_count()
                    if not count:
                        continue
                    logger.debug('inbox: %d email(s)' % count)
                    for num in range(count):
                        msg = mbox.fetch_message_as_json(num + 1)
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


def persist(msg):

    logger.info('Persist msg [%s]' % msg)
    email = Email(
        e_encoding = msg['encoding'],
        e_date = msg['datetime'],
        e_from = msg['from'],
        e_to = msg['to'],
        e_subject = msg['subject'],
        e_parts = msg['parts']
    )
    email.save()
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
    if config['starttls']:
        s.starttls()
    s.login(config.smtp['login'], config.smtp['password'])
    # s.sendmail(from_email, m['to'], msg.as_bytes())
    s.send_message(msg)
    s.quit()


def start():
    emailer = Emailer()
    emailer.start()
    return emailer
