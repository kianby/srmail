#!/usr/bin/env python
# -*- coding: utf-8 -*-

import profig

# constants
FLASK_APP = "flask.app"

DB_URL = "main.db_url"
POLLING = "main.polling"

HTTP_HOST = "http.host"
HTTP_PORT = "http.port"

IMAP_SSL = "imap.ssl"
IMAP_HOST = "imap.host"
IMAP_PORT = "imap.port"
IMAP_LOGIN = "imap.login"
IMAP_PASSWORD = "imap.password"

SMTP_STARTTLS = "smtp.starttls"
SMTP_HOST = "smtp.host"
SMTP_PORT = "smtp.port"
SMTP_LOGIN = "smtp.login"
SMTP_PASSWORD = "smtp.password"

# variable
params = dict()


def initialize(config_pathname, flask_app):
    cfg = profig.Config(config_pathname)
    cfg.sync()
    params.update(cfg)
    params.update({FLASK_APP: flask_app})


def get(key):
    return params[key]


def flaskapp():
    return params[FLASK_APP]
