#!/usr/bin/env python
# -*- coding:utf-8 -*-

import imaplib
import email
import logging


class Mailbox(object):

    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)

    def __enter__(self):
        host = self.config["imap"]["host"]
        port = self.config["imap"]["port"]
        use_ssl = self.config["imap"]["ssl"]
        if use_ssl:
            self.imap = imaplib.IMAP4_SSL(host, port)
        else:
            self.imap = imaplib.IMAP4(host, port)
        login = self.config["imap"]["login"]
        password = self.config["imap"]["password"]
        self.imap.login(login, password)
        return self

    def __exit__(self, type, value, traceback):
        self.imap.close()
        self.imap.logout()

    def get_count(self):
        self.imap.select('Inbox')
        status, data = self.imap.search(None, 'ALL')
        return sum(1 for num in data[0].split())

    def fetch_message(self, num):
        self.imap.select('Inbox')
        status, data = self.imap.fetch(str(num), '(RFC822)')
        email_msg = email.message_from_bytes(data[0][1])
        return email_msg

    def fetch_message_as_json(self, num):
        json_msg = {'Index': num}
        msg = self.fetch_message(num)
        for key in ('Date', 'From', 'To', 'Subject'):
            json_msg[key] = msg[key]
        parts = []
        for part in msg.walk():
            part_item = {}
            content = part.get_payload(decode=True)
            if content is None:
                self.logger.warn('ignore part ' + part.get_content_type())
            else:
                part_item['Content-Type'] = part.get_content_type()
                part_item['Content'] = content
                parts.append(part_item)
        json_msg['Parts'] = parts
        self.logger.debug(json_msg)
        return json_msg

    def delete_message(self, num):
        self.imap.select('Inbox')
        self.imap.store(str(num), '+FLAGS', r'\Deleted')
        self.imap.expunge()

    def delete_all(self):
        self.imap.select('Inbox')
        status, data = self.imap.search(None, 'ALL')
        for num in data[0].split():
            self.imap.store(num, '+FLAGS', r'\Deleted')
            self.imap.expunge()

    def print_msgs(self):
        self.imap.select('Inbox')
        status, data = self.imap.search(None, 'ALL')
        for num in reversed(data[0].split()):
            status, data = self.imap.fetch(num, '(RFC822)')
            self.logger.debug('Message %s\n%s\n' % (num, data[0][1]))
