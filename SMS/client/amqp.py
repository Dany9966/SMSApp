import time

import pika
# import json
import psutil

import SMS.config
from SMS import log

CONF = SMS.config.CONF
LOG = log.get_logger()


class SMSClientAMQP(object):
    def __init__(self):
        self.creds = pika.PlainCredentials(CONF.amqp.user,
                                           CONF.amqp.password)

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=CONF.amqp.url,
                                      port=int(CONF.amqp.port),
                                      virtual_host=CONF.amqp.vhost,
                                      credentials=self.creds))

        self.channel = self.connection.channel()

    def start_sending(self):
        self.channel.queue_declare(queue='usage')

        while True:
            try:
                message = psutil.cpu_percent(interval=int(CONF.amqp.time))

                self.channel.basic_publish(exchange='',
                                           routing_key='usage',
                                           body=str(message))
                LOG.info('sent message: %s' % message)
            except KeyboardInterrupt:
                LOG.warning('Interrupted')
                self.connection.close()
                break
