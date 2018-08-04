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
  return datetime.now().isoformat()


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
    # get list of metrics from conf file
    self.metric_list = CONF.metrics.list.split(", ")

    if self.metric_list == ['']:
      LOG.error('No metrics set! Exiting...')
      sys.exit()

    while True:
      # for every metric listed, add its usage to DB
      try:
        body_m_list = []
        for metric in self.metric_list:
          body_m_list.append(
              {'hostname': platform.node(),
               'timestamp': get_now(),
               'metric_type': metric,
               'metric_value': getattr(m_col, metric)()})

        body = json.dumps({'metrics': body_m_list})
        self.channel.basic_publish(exchange='',
                                   routing_key='usage',
                                   body=str(body))
        LOG.info('sent message: %s' % body)

        time.sleep(int(CONF.metrics.time_interval))
      except KeyboardInterrupt:
        LOG.warning('Interrupted')
        self.connection.close()
        break
