import json

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import as_declarative

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
        _dict = {col.name: getattr(self, col.name)
                 for col in self.__table__.columns}
        return _dict


def ModelJsonEncoder(obj):
    if isinstance(obj, BaseModel):
        return obj._to_dict()
    else:
        return json.dumps(obj)


# Usage TABLE
    # timestamp
    # cpu + other to be added later on
class Usage(BaseModel):
    __tablename__ = 'usages'

    hostname = Column(String(32))
    timestamp = Column(String(26))
    metric_type = Column(String(20))
    metric_value = Column(Integer)

    def __str__(self):
        return '%(user)s: %(timestamp)s - %(m_type)s : %(m_value)s'\
            % {'user': self.hostname,
               'timestamp': self.timestamp,
               'm_type': self.metric_type,
               'm_value': self.metric_value}

    def __repr__(self):
        return str(self)
