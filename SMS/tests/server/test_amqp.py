import unittest

import mock

import SMS.server.amqp


class TestSMSServerAMQP(unittest.TestCase):
    @mock.patch('pika.PlainCredentials')
    @mock.patch('pika.BlockingConnection')
    @mock.patch('pika.ConnectionParameters')
    @mock.patch.object(SMS.server.amqp, 'CONF')
    def test_init(self, conf_mock, cp_mock, bc_mock, pc_mock):
        conf_mock.amqp.user = 'user'
        conf_mock.amqp.password = 'pass'
        conf_mock.amqp.url = 'url'
        conf_mock.amqp.port = '1234'
        conf_mock.amqp.vhost = '/'

        SMS.server.amqp.SMSServerAMQP()

        pc_mock.assert_called_once_with('user', 'pass')
        cp_mock.assert_called_once_with(host='url',
                                        port=1234,
                                        virtual_host='/',
                                        credentials=pc_mock.return_value)
        bc_mock.assert_called_once_with(cp_mock.return_value)
        bc_mock.return_value.channel.assert_called_once_with()

        return SMS.server.amqp.SMSServerAMQP()

    @mock.patch.object(SMS.server.amqp, 'LOG')
    @mock.patch('pika.PlainCredentials')
    @mock.patch('pika.BlockingConnection')
    @mock.patch('pika.ConnectionParameters')
    @mock.patch.object(SMS.server.amqp, 'CONF')
    def test_accept(self, conf_mock, cp_mock, bc_mock, pc_mock, log_mock):

        obj = self.test_init()
        obj.accept()

        obj.channel.queue_declare(queue='usage')
        obj.channel.basic_consume.assert_called_once_with(
            obj.on_receive, queue='usage', no_ack=True)
        obj.channel.start_consuming.side_effect = KeyboardInterrupt
        obj.channel.start_consuming.assert_called_once_with()
        self.assertRaises(KeyboardInterrupt, obj.channel.start_consuming)
        # log_mock.warning.assert_called_once_with('Interrupted')
        # obj.connection.close.assert_called_once_with()

    @mock.patch('SMS.db.api.add_usage', return_value=1)
    @mock.patch('SMS.server.amqp.get_datetime_obj', return_value='obj')
    @mock.patch.object(SMS.server.amqp, 'LOG')
    @mock.patch('json.loads', return_value={'metrics':
                                            [{'hostname': 'host',
                                              'timestamp': 'now',
                                              'metric_type': 'cpu',
                                              'metric_value': '2'}]})
    @mock.patch('pika.PlainCredentials')
    @mock.patch('pika.BlockingConnection')
    @mock.patch('pika.ConnectionParameters')
    @mock.patch.object(SMS.server.amqp, 'CONF')
    def test_on_receive(self, conf_mock, cp_mock, bc_mock, pc_mock,
                        json_mock, log_mock, date_mock, api_mock):
        body = "{'metrics': \
            [{'hostname': 'node',\
             'timestamp': 'now',\
             'metric_type': 'cpu',\
             'metric_value': '2'}]}"

        obj = self.test_init()
        obj.on_receive(None, None, None, body)

        json_mock.assert_called_once_with(body)
        date_mock.assert_called_once_with(
            json_mock.return_value['metrics'][0]['timestamp'])
        api_mock.assert_called_once_with(
            name=json_mock.return_value['metrics'][0]['hostname'],
            timestamp=date_mock.return_value,
            m_type=json_mock.return_value['metrics'][0]['metric_type'],
            m_value=json_mock.return_value['metrics'][0]['metric_value'])
