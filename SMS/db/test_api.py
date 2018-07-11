import api
import unittest


class TestApi(unittest.TestCase):
    def setUp(self):
        api.initialize()
        api.create_tables()

    def test_add_user(self):
        self.assertEqual(api.add_user('someuser').__repr__(),
                         'Username: someuser')


if __name__ == '__main__':
    unittest.main()
