import time

import pika

import SMS.config
from SMS import log
from SMS.client import metric_collector

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
                body = metric_collector.collect()
                self.channel.basic_publish(exchange='',
                                           routing_key='usage',
                                           body=str(body))
                LOG.info('sent message: %s' % body)

                time.sleep(int(CONF.metrics.time_interval))
            except KeyboardInterrupt:
                LOG.warning('Interrupted')
                self.connection.close()
                break
