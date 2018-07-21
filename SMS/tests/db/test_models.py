import unittest

import mock

import SMS.db.models as mods


class TestBaseModel(unittest.TestCase):
    @mock.patch.object(mods, 'session_utils')
    @mock.patch('SMS.db.models.BaseModel.id',
                new_callable=mock.PropertyMock,
                return_value='1')
    def test_save1(self, id_mock, session_mock):
        base = mods.BaseModel()
        ret = base.save(session=session_mock)

        session_mock.add.assert_called_once_with(base)
        session_mock.flush.assert_called_once_with()
        session_mock.refresh.assert_called_once_with(base)
        self.assertEqual('1', ret)
