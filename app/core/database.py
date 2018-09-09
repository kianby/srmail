#!/usr/bin/python
# -*- coding: UTF-8 -*-

from conf import config
import functools
from playhouse.db_url import connect

def get_db():
    return connect(config.get(config.DB_URL))

def setup():
    from model.email import Email
    get_db().create_tables([Email], safe=True)
