#!/usr/bin/python
# -*- coding: UTF-8 -*-

import ast
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
    e_content = CharField()

    def to_dict(self):
        email_dict = ast.literal_eval(self.e_content)
        if 'to' in email_dict:
            del email_dict['to']
        return email_dict

    def to_summary_dict(self):
        email_dict = ast.literal_eval(self.e_content)
        if 'to' in email_dict:
            del email_dict['to']
        if 'parts' in email_dict:
            del email_dict['parts']
        return email_dict
    class Meta:
        database = get_db()
