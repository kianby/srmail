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


def fetch_email():
    try:
        with imap.Mailbox(
            config.get(config.IMAP_HOST),
            config.getInt(config.IMAP_PORT),
            config.getBool(config.IMAP_SSL),
            config.get(config.IMAP_LOGIN),
            config.get(config.IMAP_PASSWORD),
        ) as mbox:
            count = mbox.get_count()
            for num in range(count):
                msg = mbox.fetch_message(num + 1)
                if persist(msg):
                    mbox.delete_message(msg["index"])
                    time.sleep(10)
    except:
        logger.exception("fetch mail exception")


def persist(msg):

    logger.info("Persist msg [%s]" % msg)

    content = dict(msg)
    del content["index"]
    del content["to"]

    json_content = json.dumps(content, indent=False, sort_keys=False)
    email = Email(
        encoding=msg["encoding"],
        date=msg["datetime"],
        fromaddr=msg["from"],
        toaddr=msg["to"],
        subject=msg["subject"],
        content=json_content,
    )
    return email.save()


def mail(m):

    from_email = config.get(config.SMTP_LOGIN)
    if "from" in m:
        from_email = m["from"]

    # Create the container (outer) email message.
    msg = MIMEText(m["content"])
    msg["Subject"] = m["subject"]
    msg["To"] = m["to"]
    msg["From"] = from_email

    s = smtplib.SMTP(config.get(config.SMTP_HOST), config.getInt(config.SMTP_PORT))
    if config.getBool(config.SMTP_STARTTLS):
        s.starttls()
    s.login(config.get(config.SMTP_LOGIN), config.get(config.SMTP_PASSWORD))
    s.send_message(msg)
    s.quit()
