import json
import pika

import SMS.config
from SMS.db import api as db_api
from SMS.db import models
from SMS import log

CONF = SMS.config.CONF
LOG = log.get_logger()


class SMSServerRPCAPI(object):
  def __init__(self):
    creds = pika.PlainCredentials(CONF.amqp.user,
                                  CONF.amqp.password)
    self._conn = pika.BlockingConnection(
        pika.ConnectionParameters(host=CONF.amqp.url,
                                  port=int(CONF.amqp.port),
                                  virtual_host=CONF.amqp.vhost,
                                  credentials=creds))
    self._channel = self._conn.channel()
    self._channel.basic_qos(prefetch_count=1)
    self._channel.queue_declare(queue='SMS.amqp.queue')
    self._channel.basic_consume(self._on_request,
                                queue='SMS.amqp.queue')

  def _on_request(self, ch, method, props, body):
    req = json.loads(body)
    LOG.info('Got request: %s' % req)

    response = {}
    func_name = req['func_name']
    args = req['args']
    kwargs = req['kwargs']

    try:
      func = getattr(db_api, func_name)
      response['ret_val'] = func(*args, **kwargs)
    except Exception as exc:
      response['err_message'] = exc.message
    LOG.info('Sending back response: %s' % response)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(
                         correlation_id=props.correlation_id),
                     body=json.dumps(response,
                                     default=models.ModelJsonEncoder))
    ch.basic_ack(delivery_tag=method.delivery_tag)

  def accept(self):
    # import pdb; pdb.set_trace()
    self._channel.start_consuming()
