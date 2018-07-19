import unittest

import mock

import SMS.cmd.server


class TestServer(unittest.TestCase):
    @mock.patch('SMS.cmd.server.parser.parse_args')
    @mock.patch('SMS.cmd.server.CONF.load_config')
    @mock.patch('SMS.log.configure_logging')
    @mock.patch.object(SMS.cmd.server, 'db_api')
    @mock.patch('SMS.server.amqp.SMSServerAMQP')
    def test_main(self, server_mock, api_mock, log_mock, conf_mock, prs_mock):
        SMS.cmd.server.main()

        prs_mock.assert_called_once()
        conf_mock.assert_called_once_with(prs_mock.return_value.config_path)
        log_mock.assert_called_once()
        api_mock.initialize.assert_called_once()
        api_mock.create_tables.assert_called_once()
        server_mock.assert_called_once()
        server_mock.return_value.accept.assert_called_once()
