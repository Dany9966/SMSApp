import unittest

import mock

import SMS.client.amqp
import SMS.config


class TestSMSClientAMQP(unittest.TestCase):
    @mock.patch('pika.BlockingConnection')
    @mock.patch('pika.ConnectionParameters')
    @mock.patch('SMS.config.CONF')
    def test_init(self, conf_mock, cp_mock, bc_mock):
        conf_mock.return_value.amqp.return_value.url.return_value = 'url'
        conf_mock.port = '1234'
        conf_mock.vhost = '/'

        SMS.client.amqp.SMSClientAMQP()

        cp_mock.assert_called_once_with(host='url', port=1234, vhost='/')
        bc_mock.assert_called_once_with(cp_mock)
        bc_mock.return_value.channel.assert_called_once()
