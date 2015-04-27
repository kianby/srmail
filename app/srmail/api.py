#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from flask import request, jsonify
from srmail import app
from srmail import imap

logger = logging.getLogger(__name__)


@app.route("/mbox/count", methods=['GET'])
def get_message_count():

    count = -1
    try:
        with imap.Mailbox(app.config['app']) as mbox:
            count = mbox.get_count()
    except:
        logger.exception("mbox count exception")
    return jsonify(count=count)


def init():
    pass
