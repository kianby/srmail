#!/usr/bin/env python
# -*- coding:utf-8 -*-

import imaplib
import email
import logging
import base64
import re
import datetime

filename_re = re.compile("filename=\"(.+)\"|filename=([^;\n\r\"\']+)", re.I|re.S)

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

    def _parse_date(self, v):
        if v is None:
            return datetime.datetime.now()

        tt = email.utils.parsedate_tz(v)

        if tt is None:
            return datetime.datetime.now()

        timestamp = email.utils.mktime_tz(tt)
        date = datetime.datetime.fromtimestamp(timestamp)
        return date

    def fetch_message_as_json(self, num):
        msg = self.fetch_message(num)
        json_msg = {}
        json_msg['encoding'] = 'UTF-8'
        json_msg['index'] = num
        json_msg['datetime'] = self._parse_date(msg['Date']).strftime("%Y-%m-%d %H:%M:%S")
        json_msg['from'] = msg['From']
        json_msg['to'] = msg['To']
        json_msg['subject'] = msg['Subject']
        parts = []
        attachments = []
        for part in msg.walk():
            if part.is_multipart():
                continue

            content_disposition = part.get("Content-Disposition", None)
            if content_disposition:
                # we have attachment
                r = filename_re.findall(content_disposition)
                if r:
                    filename = sorted(r[0])[1]
                else:
                    filename = "undefined"
                a = { "filename": filename, "content": base64.b64encode(part.get_payload(decode = True)).decode(), "content-type": part.get_content_type() }
                attachments.append(a)
            else:
                part_item = {}
                content = part.get_payload(decode=True)
                content_type = part.get_content_type()
                try:
                    charset = part.get_param('charset', None)
                    if charset:
                        content = content.decode(charset).encode('UTF-8').decode('UTF-8')
                except:
                    self.logger.exception()
                part_item['content'] = content
                part_item['content-type'] = content_type
                parts.append(part_item)
        if parts:
            json_msg['parts'] = parts
        if attachments: 
                json_msg['attachments'] = attachments
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
