import unittest
from mock import patch
import SMS.db.api as db_api


class TestAPI(unittest.TestCase):
    @patch('SMS.db.session.ensure_session')
    @patch('SMS.db.models.User')
    def test_add_user(self, user_mock, session_mock):
        # Mocking User object
        user_mock.return_value.save.return_value = '1'

        ret = db_api.add_user(name='someuser', session=session_mock)
        # assertions
        user_mock.assert_called_once_with(username='someuser')
        user_mock.return_value.save.assert_called_once()
        self.assertEqual('1', ret)
