import unittest

import mock

import SMS.client.amqp


class TestSMSClientAMQP(unittest.TestCase):
    @mock.patch('pika.PlainCredentials')
    @mock.patch('pika.BlockingConnection')
    @mock.patch('pika.ConnectionParameters')
    @mock.patch.object(SMS.client.amqp, 'CONF')
    def test_init(self, conf_mock, cp_mock, bc_mock, pc_mock):
        conf_mock.amqp.user = 'user'
        conf_mock.amqp.password = 'pass'
        conf_mock.amqp.url = 'url'
        conf_mock.amqp.port = '1234'
        conf_mock.amqp.vhost = '/'

        SMS.client.amqp.SMSClientAMQP()

        pc_mock.assert_called_once_with('user', 'pass')
        cp_mock.assert_called_once_with(host='url',
                                        port=1234,
                                        virtual_host='/',
                                        credentials=pc_mock.return_value)
        bc_mock.assert_called_once_with(cp_mock.return_value)
        bc_mock.return_value.channel.assert_called_once_with()
        return SMS.client.amqp.SMSClientAMQP()

    @mock.patch.object(SMS.client.amqp, 'LOG')
    @mock.patch('pika.PlainCredentials')
    @mock.patch('pika.BlockingConnection')
    @mock.patch('pika.ConnectionParameters')
    @mock.patch.object(SMS.client.amqp, 'CONF')
    def test_start_sending1(self, conf_mock, cp_mock, bc_mock, pc_mock,
                            log_mock):
        conf_mock._parser.items.return_value = [
            ('time', '5'), ('cpu_percentage_used', 'false'),
            ('memory', 'false')]

        client = self.test_init()
        with self.assertRaises(SystemExit):
            client.start_sending()

        client.channel.queue_declare.assert_called_once_with(queue='usage')
        conf_mock._parser.items.assert_called_once_with('metrics')
        self.assertEqual([], client.metric_list)
        log_mock.error.assert_called_once_with('No metrics set! Exiting...')

    @mock.patch('time.sleep', side_effect=KeyboardInterrupt)
    @mock.patch('SMS.client.amqp.m_col.cpu_percentage_used', return_value='2')
    @mock.patch('SMS.client.amqp.get_now', return_value='now')
    @mock.patch('platform.node', return_value='node')
    @mock.patch('json.dumps')
    @mock.patch.object(SMS.client.amqp, 'LOG')
    @mock.patch('pika.PlainCredentials')
    @mock.patch('pika.BlockingConnection')
    @mock.patch('pika.ConnectionParameters')
    @mock.patch.object(SMS.client.amqp, 'CONF')
    def test_start_sending2(self, conf_mock, cp_mock, bc_mock, pc_mock,
                            log_mock, json_mock, node_mock, now_mock,
                            m_col_mock, time_mock):
        conf_mock._parser.items.return_value = [
            ('time', '5'), ('cpu_percentage_used', 'true'),
            ('memory', 'false')]
        json_mock.return_value = "\
            {'hostname': 'node',\
             'timestamp': 'now',\
             'metric_type': 'cpu_percentage_used',\
             'metric_value': '2'}"
        conf_mock.metrics.time_interval = '5'

        client = self.test_init()
        client.start_sending()

        client.channel.queue_declare.assert_called_once_with(queue='usage')
        conf_mock._parser.items.assert_called_once_with('metrics')
        self.assertEqual(['cpu_percentage_used'], client.metric_list)
        json_mock.assert_called_once()
        m_col_mock.assert_called_once_with()
        client.channel.basic_publish.assert_called_once_with(
            exchange='',
            routing_key='usage',
            body=json_mock.return_value)
        log_mock.info.assert_called_once_with('sent message: %s' %
                                              json_mock.return_value)
        time_mock.assert_called_once_with(5)
        self.assertRaises(KeyboardInterrupt, time_mock)
        log_mock.warning.assert_called_once_with('Interrupted')
        client.connection.close.assert_called_once_with()
