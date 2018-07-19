import unittest

import mock

import SMS.cmd.client


class TestClient(unittest.TestCase):
    @mock.patch.object(SMS.cmd.client, 'parser')
    @mock.patch.object(SMS.cmd.client, 'CONF')
    @mock.patch('SMS.log.configure_logging')
    @mock.patch('SMS.client.amqp.SMSClientAMQP')
    def test_main(self, amqp_mock, log_mock, conf_mock, parser_mock):
        args = parser_mock.parse_args.return_value

        SMS.cmd.client.main()

        parser_mock.parse_args.assert_called_once()
        conf_mock.load_config.assert_called_once_with(args.config_path)
        log_mock.assert_called_once()
        amqp_mock.assert_called_once()
        amqp_mock.return_value.start_sending.assert_called_once()
