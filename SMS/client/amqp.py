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
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=CONF.amqp.url,
                                      port=int(CONF.amqp.port),
                                      virtual_host=CONF.amqp.vhost))

        self.channel = self.connection.channel()

    def start_sending(self):
        self.channel.queue_declare(queue='usage')

        psutil.cpu_percent(interval=1)
        while True:
            try:
                time.sleep(int(CONF.amqp.time))
                message = psutil.cpu_percent(interval=None)

                self.channel.basic_publish(exchange='',
                                           routing_key='usage',
                                           body=str(message))
                LOG.info('sent message: %s' % message)
            except KeyboardInterrupt:
                LOG.info('Interrupted')
                self.connection.close()
                break
