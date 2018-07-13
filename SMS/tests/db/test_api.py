import unittest

import mock

import SMS.db.api as db_api


class TestAPI(unittest.TestCase):
    @mock.patch('SMS.db.session.ensure_session')
    @mock.patch('SMS.db.models.User')
    def test_add_user(self, user_mock, session_mock):
        # Mocking User object
        user_mock.return_value.save.return_value = '1'

        ret = db_api.add_user(name='someuser', session=session_mock)
        # assertions
        user_mock.assert_called_once_with(username='someuser')
        user_mock.return_value.save.assert_called_once()
        self.assertEqual('1', ret)

    @mock.patch('SMS.db.session.ensure_session')
    @mock.patch('SMS.db.models.Usage')
    def test_add_usage(self, usage_mock, session_mock):
        usage_mock.return_value.save.return_value = '1'
        timestamp = mock.Mock()
        cpu = mock.Mock()
        user_id = '1'

        ret = db_api.add_usage(user_id=user_id, timestamp=timestamp, cpu=cpu,
                               session=session_mock)

        usage_mock.assert_called_once_with(timestamp=timestamp, cpu=cpu,
                                           user_id=user_id)
        usage_mock.return_value.save.assert_called_once()
        self.assertEqual('1', ret)

    @mock.patch('SMS.db.session')
    def test_get_users(self, session_mock):
        session_mock.query().order_by().all.return_value = ['user1', 'user2']

        ret = db_api.get_users(session=session_mock)

        session_mock.query().order_by().all.assert_called_once()
        self.assertEqual(['user1', 'user2'], ret)

    @mock.patch('SMS.db.models.User')
    @mock.patch('SMS.db.session')
    def test_get_user(self, session_mock, user_mock):
        session_mock.query().filter_by().one.return_value = 'user'

        ret = db_api.get_user(user_id='1', session=session_mock)

        session_mock.query.assert_called_with(user_mock)
        self.assertEqual('user', ret)

    @mock.patch('SMS.db.session')
    @mock.patch('SMS.db.models.Usage')
    def test_get_usages(self, usage_mock, session_mock):
        session_mock.query().options().filter_by().order_by().all.\
            return_value = 'filtered users'
        session_mock.query.options().order_by().all.return_value = 'no filter'

        ret1 = db_api.get_usages(user_id='1', session=session_mock)
        ret2 = db_api.get_usages(user_id=None, session=session_mock)

        # session_mock.query.assert_called_with(usage_mock)
        # session_mock.query.options.filter_by.assert_called_with('1')
        # session_mock.query.options.order_by.assert_called_once_with(
        #    usage_mock.cpu)
        # session_mock.query.options.filter_by.order_by.all.assert_called_once()
        # session_mock.query.options.order_by.all.assert_called_once()
        self.assertEqual('filtered users', ret1)
        self.assertEqual('no filter', ret2)


if __name__ == '__main__':
    unittest.main()
