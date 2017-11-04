#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import time
import re
from threading import Thread
import logging
import requests
import json
import smtplib
from email.mime.text import MIMEText
from conf import config
from srmail import imap

logger = logging.getLogger(__name__)


class Emailer(Thread):

    def __init__(self):
        super(Emailer, self).__init__()

    def stop(self):
        logger.info("stop requested")
        self.is_running = False

    def run(self):

        exit_on_error = config.general.get('exit_on_error', False)
        logger.info("exit_on_error = %s" % exit_on_error)
        self.is_running = True

        while self.is_running:

            try:
                with imap.Mailbox() as mbox:
                    count = mbox.get_count()
                    logger.debug('check inbox: %d email(s)' % count)
                    for num in range(count):
                        msg = mbox.fetch_message_as_json(num + 1)
                        if process(mbox, msg, config.post):
                            mbox.delete_message(msg['index'])
                            time.sleep(10)
            except:
                logger.exception("main loop exception")
                if exit_on_error:
                    stop_on_error()

            # check email every <polling> seconds
            sleep_time = 0
            while sleep_time < config.general['polling']:
                if not self.is_running:
                    break
                time.sleep(1)
                sleep_time = sleep_time + 1

        self.is_running = False


def stop_on_error():
    error_code = 126
    shutdown_url = 'http://%s:%d/shutdown' % (config.http['host'], config.http['port'])
    logger.warn("exit_on_error enabled: code %d (%s)" % (error_code,
                                                         shutdown_url))
    r = requests.post(shutdown_url)
    sys.exit(error_code)


def process(mbox, msg, post):

    logger.info('Process msg [%s] with post config: %s' % (msg, post))
    processed = False
    recipient_found = False
    for route in post['routing']:
        if re.match(route['regex'], msg['subject'], re.I):
            recipient_found = True
            processed = post_msg(route['url'], msg)
    if not recipient_found and post['default']:
        processed = post_msg(post['default'], msg)
    return processed


def post_msg(url, msg):

    posted = False
    try:
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        r = requests.post(url, data=json.dumps(msg), headers=headers)
        if r.status_code not in (200, 201):
            logger.warn('bad status %d keep message until '
                        'next polling ' % r.status_code)
        else:
            posted = True
    except:
        logger.exception('cannot post to %s' % url)
    return posted


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
