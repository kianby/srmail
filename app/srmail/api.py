#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from flask import request, make_response
from json import dumps
from srmail import app
from srmail import imap

logger = logging.getLogger(__name__)


def jsonify(status=200, indent=4, sort_keys=True, **kwargs):
    response = make_response(dumps(dict(**kwargs), indent=indent, sort_keys=sort_keys))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['mimetype'] = 'application/json'
    response.status_code = status
    return response

@app.route('/mbox/count', methods=['GET'])
def get_message_count():

    count = -1
    try:
        with imap.Mailbox(app.config['app']) as mbox:
            count = mbox.get_count()
    except:
        logger.exception('mbox exception')
    return jsonify(count=count)


@app.route('/mbox/<int:index>', methods=['GET'])
def get_message(index):

    msg = {}
    try:
        with imap.Mailbox(app.config['app']) as mbox:
            msg = mbox.fetch_message_as_json(index)
    except:
        logger.exception("mbox exception")
    return jsonify(**msg)


def init():
    pass
