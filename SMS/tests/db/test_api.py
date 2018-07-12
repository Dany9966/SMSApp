import unittest
from mock import patch, Mock
import SMS.db.api as db_api


class TestAPI(unittest.TestCase):
    def test_add_user(self):
        # Mocking User object
        with patch('SMS.db.models.User', return_value=Mock()) as user_mock:
            user_mock.save.return_value = '1'

            ret = db_api.add_user(name='someuser', session=None)
            # assertions
            user_mock.assert_called_once_with('someuser')
            user_mock.save.assert_called_once()
            self.assertEqual(ret, '1')


if __name__ == '__main__':
    unittest.main()
