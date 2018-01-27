#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika
import json
import logging
from threading import Thread
from conf import config
from core import emailer
from model.email import Email

logger = logging.getLogger(__name__)


def process_message(chan, method, properties, body):
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
            email.delete()
    else:
        logger.warn('unknown command {}'.format(topic))


class CommandConsumer(Thread):

    def run(self):

        credentials = pika.PlainCredentials(
            config.rabbitmq['username'], config.rabbitmq['password'])
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.rabbitmq['host'], port=config.rabbitmq[
                                             'port'], credentials=credentials, virtual_host=config.rabbitmq['vhost']))

        channel = connection.channel()
        channel.exchange_declare(exchange=config.rabbitmq['exchange'],
                                 exchange_type='topic')

        result = channel.queue_declare(exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange=config.rabbitmq['exchange'],
                           queue=queue_name,
                           routing_key='mail.command.*')
        channel.basic_consume(process_message,
                              queue=queue_name,
                              no_ack=True)
        channel.start_consuming()


def start():
    consumer = CommandConsumer()
    consumer.start()