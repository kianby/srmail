#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import pika
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

        # broadcast stored emails on startup
        broadcast_emails()

        while self.is_running:

            try:
                with imap.Mailbox() as mbox:
                    try:
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
            except:
                logger.exception("cannot open mailbox exception")

            # check email every <polling> seconds
            sleep_time = 0
            while sleep_time < config.general['polling']:
                if not self.is_running:
                    break
                time.sleep(1)
                sleep_time = sleep_time + 1

        self.is_running = False


def pub_rabbitmq_mail_messages(emails):
    if not emails:
        return
    credentials = pika.PlainCredentials(
        config.rabbitmq['username'], config.rabbitmq['password'])
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.rabbitmq['host'], port=config.rabbitmq[
                                         'port'], credentials=credentials, virtual_host=config.rabbitmq['vhost']))
    channel = connection.channel()

    for email in emails:
        channel.basic_publish(exchange=config.rabbitmq['exchange'],
                              routing_key='mail.message',
                              body=json.dumps(email.to_dict(), indent=False, sort_keys=False))
    connection.close()


def broadcast_emails():
    if not config.rabbitmq['active']:
        return
    emails = []
    for email in Email.select():
        emails.append(email)
    pub_rabbitmq_mail_messages(emails)


def persist(msg):

    logger.info('Persist msg [%s]' % msg)

    content = dict(msg)
    del content['index']
    del content['to']

    json_content = json.dumps(content, indent=False, sort_keys=False)
    email = Email(
        encoding=msg['encoding'],
        date=msg['datetime'],
        fromaddr=msg['from'],
        toaddr=msg['to'],
        subject=msg['subject'],
        content= json_content
    )
    success = email.save()

    if config.rabbitmq['active'] and success:
        pub_rabbitmq_mail_messages([email])

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
