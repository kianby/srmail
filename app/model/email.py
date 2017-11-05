#!/usr/bin/python
# -*- coding: UTF-8 -*-

from peewee import Model
from peewee import CharField
from peewee import TextField
from peewee import DateTimeField
from peewee import BooleanField
from core.database import get_db


class Email(Model):
    e_encoding = CharField()
    e_date = DateTimeField()
    e_from = CharField()
    e_to = CharField()
    e_subject = CharField()
    e_parts = CharField()

    class Meta:
        database = get_db()
