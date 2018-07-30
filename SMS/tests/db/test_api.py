import unittest

import mock

import SMS.db.api as db_api


class TestAPI(unittest.TestCase):
    @mock.patch('SMS.db.session.initialize')
    def test_initialize(self, sess_mock):
        db_api.initialize()
        sess_mock.assert_called_once()

    @mock.patch('SMS.db.models.BaseModel.metadata.create_all')
    @mock.patch('SMS.db.session.engine')
    def test_create_tables(self, eng_mock, create_mock):
        db_api.create_tables()
        create_mock.assert_called_once_with(eng_mock)

    @mock.patch('SMS.db.session.ensure_session')
    @mock.patch('SMS.db.models.Usage')
    def test_add_usage(self, usage_mock, session_mock):
        usage_mock.return_value.save.return_value = '1'

        ret = db_api.add_usage(name='host',
                               timestamp='some time',
                               m_type='cpu',
                               m_value='23',
                               session=session_mock)

        usage_mock.assert_called_once()

        usage_mock.return_value.save.assert_called_once_with()
        self.assertEqual('1', ret)

    @mock.patch('SMS.db.session')
    @mock.patch('SMS.db.models.Usage')
    def test_get_usages1(self, usage_mock, session_mock):
        # if user_id = '1'
        session_mock.query.return_value.options.return_value.filter_by.\
            return_value.order_by.return_value.all.\
            return_value = 'filtered users'

        ret = db_api.get_usages(user_id='1', session=session_mock)
        session_mock.query.assert_called_once_with(usage_mock)
        session_mock.query.return_value.options.return_value.filter_by.\
            assert_called_once_with(id='1')
        session_mock.query.return_value.options.return_value.filter_by.\
            return_value.order_by.assert_called_once_with(usage_mock.cpu)

        self.assertEqual('filtered users', ret)

    @mock.patch('SMS.db.session')
    @mock.patch('SMS.db.models.Usage')
    def test_get_usages2(self, usage_mock, session_mock):

        # if user_id = None
        session_mock.query.return_value.options.return_value.order_by.\
            return_value.all.return_value = 'no filter'

        ret = db_api.get_usages(user_id=None, session=session_mock)

        session_mock.query.assert_called_once_with(usage_mock)
        session_mock.query.return_value.options.return_value.order_by.\
            assert_called_once_with(usage_mock.cpu)

        self.assertEqual('no filter', ret)
