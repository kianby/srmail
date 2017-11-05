#!/usr/bin/python
# -*- coding: UTF-8 -*-

from conf import config
import functools
from playhouse.db_url import connect


def get_db():
    return connect(config.general['db_url'])


def provide_db(func):

    @functools.wraps(func)
    def new_function(*args, **kwargs):
        return func(get_db(), *args, **kwargs)

    return new_function


@provide_db
def setup(db):
    from model.email import Email
    db.create_tables([Email], safe=True)
