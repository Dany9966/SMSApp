import unittest

import mock

import SMS.db.session as sessionmod


class TestSession(unittest.TestCase):
    @mock.patch.object(sessionmod, 'CONF')
    # @mock.patch.object(sessionmod, 'engine')
    # @mock.patch.object(sessionmod, 'SessionClass')
    @mock.patch('SMS.db.session.create_engine')
    @mock.patch('SMS.db.session.sessionmaker')
    # @mock.patch('sqlalchemy.orm.sessionmaker')
    def test_initialize(self, sm_mock, cr_mock, conf_mock):
        conf_mock.db.logging.lower.return_value = "true"
        sessionmod.initialize()
        cr_mock.assert_called_once_with(
            conf_mock.db.url,
            echo=True)
        sm_mock(bind=cr_mock.return_value, expire_on_commit=False)

    @mock.patch.object(sessionmod, 'SessionClass')
    def test_get_new_session(self, sess_mock):
        ret = sessionmod.get_new_session()
        self.assertEqual(sess_mock.return_value, ret)
