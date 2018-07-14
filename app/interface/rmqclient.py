#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika
import json
import logging
from threading import Thread
from conf import config
from core import emailer
from util import rabbit
from model.email import Email

logger = logging.getLogger(__name__)


class MailConsumer(rabbit.Consumer):

    def process(self, channel, method, properties, body):
        topic = method.routing_key
        data = json.loads(body)
        if topic == 'mail.command.send':
            logger.info('send mail => {}'.format(data))
            emailer.mail(data)
        elif topic == 'mail.command.delete':
            logger.info('delete mail => {}'.format(data))
            email = Email.get(Email.id == data['id'])
            if email is None:
                logger.info('cannot retrieve email to delete: {}'.format(data))
            else:
                email.delete_instance()
        else:
            logger.warn('unknown command {}'.format(topic))


def start():

    logger.info('start rmqclient')

    credentials = pika.PlainCredentials(
        config.rabbitmq['username'], config.rabbitmq['password'])
    parameters = pika.ConnectionParameters(
        host=config.rabbitmq['host'],
        port=config.rabbitmq['port'],
        credentials=credentials,
        virtual_host=config.rabbitmq['vhost']
    )

    connection = rabbit.Connection(parameters)
    c = MailConsumer(connection, config.rabbitmq['exchange'], 'mail.command.*')
    c.start()
