import unittest

import mock

import SMS.client.amqp


class TestSMSClientAMQP(unittest.TestCase):
    @mock.patch('pika.PlainCredentials')
    @mock.patch('pika.BlockingConnection')
    @mock.patch('pika.ConnectionParameters')
    @mock.patch.object(SMS.client.amqp, 'CONF')
    @mock.patch('psutil.cpu_percent')
    @mock.patch.object(SMS.client.amqp, 'LOG')
    def test_client(self,
                    log_mock,
                    cpu_mock,
                    conf_mock,
                    cp_mock,
                    bc_mock,
                    pc_mock):

        conf_mock.amqp.user = 'stackrabbit'
        conf_mock.amqp.password = 'Passw0rd'
        conf_mock.amqp.url = 'url'
        conf_mock.amqp.port = '1234'
        conf_mock.amqp.vhost = '/'
        conf_mock.amqp.time = '10'
        cpu_mock.return_value = 5.0
        log_mock.info.side_effect = KeyboardInterrupt

        client = SMS.client.amqp.SMSClientAMQP()

        pc_mock.assert_called_once_with('stackrabbit', 'Passw0rd')
        cp_mock.assert_called_once_with(host='url',
                                        port=1234,
                                        virtual_host='/',
                                        credentials=pc_mock.return_value)
        bc_mock.assert_called_once_with(cp_mock.return_value)
        channel_mock = bc_mock.return_value.channel.return_value
        bc_mock.return_value.channel.assert_called_once()

        client.start_sending()

        channel_mock.queue_declare.assert_called_once_with(queue='usage')
        cpu_mock.assert_called_with(interval=10)
        client.channel.basic_publish.assert_called_with(
            exchange='', routing_key='usage', body='5.0')
        log_mock.info.assert_called_with('sent message: 5.0')
        self.assertRaises(KeyboardInterrupt,
                          log_mock.info,
                          'sent message: 5.0')
        log_mock.warning.assert_called_once_with('Interrupted')
        client.connection.close.assert_called_once()
