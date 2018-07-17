import pika

import SMS.config
# from SMS.db import api as db_api
# from SMS.db import models
from SMS import log

CONF = SMS.config.CONF
LOG = log.get_logger()


class SMSServerAMQP(object):
  def __init__(self):
    self.creds = pika.PlainCredentials(CONF.amqp.user,
                                       CONF.amqp.password)
    self.connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=CONF.amqp.url,
                                  port=CONF.amqp.port,
                                  virtual_host=CONF.amqp.vhost,
                                  credentials=self.creds))

    self.channel = self.connection.channel()

    self.channel.queue_declare(queue='usage')

  def accept(self):
    self.channel.basic_consume(self.on_receive,
                               queue='usage',
                               no_ack=True)
    print("Waiting for cpu usages")
    self.channel.start_consuming()

  def on_receive(self, ch, method, props, body):
    print('Percentage: %s' % body)
