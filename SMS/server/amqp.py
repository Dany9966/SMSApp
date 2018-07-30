import json
from datetime import datetime

import pika

import SMS.config
from SMS.db import api as db_api
# from SMS.db import session as sess
# from SMS.db import models
from SMS import log

CONF = SMS.config.CONF
LOG = log.get_logger()


def get_datetime_obj(datetime_str):
    return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S.%f')


class SMSServerAMQP(object):
    def __init__(self):
        # self.session = sess.get_new_session()
        self.creds = pika.PlainCredentials(CONF.amqp.user,
                                           CONF.amqp.password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=CONF.amqp.url,
                                      port=int(CONF.amqp.port),
                                      virtual_host=CONF.amqp.vhost,
                                      credentials=self.creds))

        self.channel = self.connection.channel()

    def accept(self):
        self.channel.queue_declare(queue='usage')
        self.channel.basic_consume(self.on_receive,
                                   queue='usage',
                                   no_ack=True)
        print("Waiting for usages")

        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            # print('interrupt')
            LOG.warning('Interrupted')
            self.connection.close()

    def on_receive(self, ch, method, props, body):
        rec_usage = json.loads(body)
        LOG.info('Got metrics: %s' % body)

        for metric in rec_usage['metrics']:
            datetime_obj = get_datetime_obj(metric.get('timestamp'))

            row = db_api.add_usage(
                name=metric.get('hostname'),
                timestamp=datetime_obj,
                m_type=metric.get('metric_type'),
                m_value=metric.get('metric_value'))

            if row:
                LOG.info('%s added to DB' % row)
                LOG.info('%s' % body)
