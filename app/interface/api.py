#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from flask import request, make_response
import json
from core import app
from core import imap
from core import emailer
from model.email import Email


logger = logging.getLogger(__name__)


def jsonify(status=200, indent=4, sort_keys=True, **kwargs):
    response = make_response(json.dumps(dict(**kwargs), indent=indent,
                                        sort_keys=sort_keys))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['mimetype'] = 'application/json'
    response.status_code = status
    return response


@app.route('/mbox', methods=['GET'])
def get_message_count():

    count = -1
    emails = []
    try:
        count = Email.select().count()
        for row in Email.select():
            emails.append(row.to_summary_dict())
    except:
        logger.exception('mbox exception')
    return jsonify(count=count, emails=emails)


@app.route('/mbox/<int:index>', methods=['GET'])
def get_message(index):

    result = {}
    try:
        row = Email.select().where(Email.id == index).get()
        if row:
            result = jsonify(email=row.to_dict())
        else:
            result = jsonify(status=404)
    except:
        logger.exception("mbox exception")
    return result


@app.route('/mbox/<int:index>', methods=['DELETE'])
def delete_message(index):

    status_code = 404
    try:
        row = Email.select().where(Email.id == index).get()
        if row:
            row.delete_instance()
            status_code = 200
    except:
        logger.exception("mbox exception")
    return jsonify(status=status_code)


@app.route('/mbox', methods=['POST'])
def send_message():

    status_code = 500
    try:
        content = request.json
        emailer.mail(content)
        status_code = 200
    except:
        logger.exception('mbox exception')
    return jsonify(status=status_code)
