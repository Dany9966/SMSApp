import time
import sys
import platform
from datetime import datetime

import pika
import json

import SMS.config
from SMS import log
import SMS.client.metric_collector as m_col

CONF = SMS.config.CONF
LOG = log.get_logger()


def get_now():
  return datetime.now()


class SMSClientAMQP(object):
  metric_list = []

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
    # for metrics, get list of trues

    for name, value in CONF._parser.items('metrics')[1:]:
      if value.lower() == "true":
        self.metric_list.append(name)

    if self.metric_list == []:
      LOG.error('No metrics set! Exiting...')
      sys.exit()

    while True:
      # for every metric listed, add its usage to DB
      try:
        for metric in self.metric_list:

          body = json.dumps(
              {'hostname': platform.node(),
               'timestamp': str(get_now()),
               'metric_type': metric,
               'metric_value': getattr(m_col, metric)()})

          self.channel.basic_publish(exchange='',
                                     routing_key='usage',
                                     body=str(body))
          LOG.info('sent message: %s' % body)

        time.sleep(int(CONF.metrics.time_interval))
      except KeyboardInterrupt:
        LOG.warning('Interrupted')
        self.connection.close()
        break
