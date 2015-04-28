#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from flask import request, make_response
from json import dumps
from srmail import app
from srmail import imap
from srmail import emailer

logger = logging.getLogger(__name__)


def jsonify(status=200, indent=4, sort_keys=True, **kwargs):
    response = make_response(dumps(dict(**kwargs), indent=indent, sort_keys=sort_keys))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['mimetype'] = 'application/json'
    response.status_code = status
    return response


@app.route('/mbox', methods=['GET'])
def get_message_count():

    count = -1
    try:
        with imap.Mailbox(app.config['app']) as mbox:
            count = mbox.get_count()
    except:
        logger.exception('mbox exception')
    return jsonify(count=count)


@app.route('/mbox', methods=['POST'])
def send_message():

    status_code = 500
    try:
        content = request.json
        emailer.mail(app.config['app']['smtp'], content)
        status_code = 200
    except:
        logger.exception('mbox exception')
    return ('send', status_code)


@app.route('/mbox/<int:index>', methods=['GET'])
def get_message(index):

    msg = {}
    try:
        with imap.Mailbox(app.config['app']) as mbox:
            msg = mbox.fetch_message_as_json(index)
    except:
        logger.exception("mbox exception")
    return jsonify(**msg)


@app.route('/mbox/<int:index>', methods=['DELETE'])
def delete_message(index):

    status_code = 500
    try:
        with imap.Mailbox(app.config['app']) as mbox:
            msg = mbox.delete_message(index)
            status_code = 200
    except:
        logger.exception("mbox exception")
    return ('deleted', status_code)


@app.route('/testing/post', methods=['POST'])
def post_url():
    # Sample POST URL for testing purpose 
    logger.info(request.json)
    # Return an error status code to prevent from deleting the message
    return ('internal error', 500, )


def init():
    pass
