import json

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import as_declarative
from datetime import datetime
from SMS.db import session as session_utils

# BaseModel TABLE
# id


@as_declarative()
class BaseModel(object):
    id = Column(Integer, primary_key=True)

    @session_utils.ensure_session
    def save(self, session=None):
        session.add(self)
        session.flush()
        session.refresh(self)
        return self.id

    def _to_dict(self):
        _dict = {col.name: datetime_convert(getattr(self, col.name))
                 for col in self.__table__.columns}
        return _dict


def ModelJsonEncoder(obj):
    if isinstance(obj, BaseModel):
        return obj._to_dict()
    else:
        return json.dumps(obj)


def datetime_convert(obj):
    # Had to do this particular convertor since datetime objects are not json
    # serializable AND I need a 'T' between date and time

    if isinstance(obj, datetime):
        return datetime.strftime(obj, '%Y-%m-%dT%H:%M:%S')
    else:
        return obj

# Usage TABLE
    # timestamp
    # cpu + other to be added later on


class Usage(BaseModel):
    __tablename__ = 'usages'

    hostname = Column(String(32))
    timestamp = Column(DateTime())
    metric_type = Column(String(20))
    metric_value = Column(Integer)
    metric_unit = Column(String(5))

    def __str__(self):
        return '{\
                 "hostname": %(user)s,\
                 "timestamp": %(timestamp)s,\
                 "metric_type": %(m_type)s,\
                 "metric_value": %(m_value)s,\
                 "metric_unit": %(m_unit)s\
                }' % {'user': self.hostname,
                      'timestamp': datetime.strftime(self.timestamp,
                                                     "%Y-%m-%dT%H:%M:%S%z"),
                      'm_type': self.metric_type,
                      'm_value': self.metric_value,
                      'm_unit': self.metric_unit}

    def __repr__(self):
        return str(self)
