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
    encoding = CharField()
    date = DateTimeField()
    fromaddr = CharField()
    toaddr = CharField()
    subject = CharField()
    content = CharField()

    def to_dict(self):
        email_dict = ast.literal_eval(self.content)
        email_dict['id'] = self.id
        return email_dict

    def to_summary_dict(self):
        email_dict = ast.literal_eval(self.content)
        if 'parts' in email_dict:
            del email_dict['parts']
        return email_dict

    class Meta:
        database = get_db()
