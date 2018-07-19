import unittest

import mock

import SMS.db.models as mods


class TestBaseModel(unittest.TestCase):
    @mock.patch.object(mods, 'session_utils')
    @mock.patch('SMS.db.models.BaseModel.id',
                new_callable=mock.PropertyMock,
                return_value='1')
    @mock.patch('SMS.db.models.BaseModel.uuid',
                new_callable=mock.PropertyMock,
                return_value='stackrabbit')
    @mock.patch('uuid.uuid4')
    def test_save1(self, uuid4_mock, uu_mock, id_mock, session_mock):
        base = mods.BaseModel()
        ret = base.save(session=session_mock)

        uuid4_mock.assert_not_called()
        session_mock.add.assert_called_once_with(base)
        session_mock.flush.assert_called_once_with()
        session_mock.refresh.assert_called_once_with(base)
        self.assertEqual('1', ret)

    @mock.patch.object(mods, 'session_utils')
    @mock.patch('SMS.db.models.BaseModel.id',
                new_callable=mock.PropertyMock,
                return_value='1')
    @mock.patch('SMS.db.models.BaseModel.uuid',
                new_callable=mock.PropertyMock,
                return_value=None)
    @mock.patch('uuid.uuid4')
    def test_save2(self, uuid4_mock, uu_mock, id_mock, session_mock):
        base = mods.BaseModel()
        ret = base.save(session=session_mock)

        uuid4_mock.assert_called_once_with()
        session_mock.add.assert_called_once_with(base)
        session_mock.flush.assert_called_once_with()
        session_mock.refresh.assert_called_once_with(base)
        self.assertEqual('1', ret)
"""
    @mock.patch('SMS.db.models.BaseModel')
    def test_to_dict(self, base_mock):
        base_mock.return_value.__table__.return_value.columns.return_value =\
            ['base.id', 'base.uuid']
        ret = base_mock._to_dict()

        self.assertEqual({'id': base_mock.id, 'uuid': base_mock.uuid}, ret)
"""