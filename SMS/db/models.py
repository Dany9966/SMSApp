import json

from sqlalchemy import ForeignKey, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import relationship

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


# USER TABLE
    # hostname
class User(BaseModel):
    __tablename__ = 'users'

    hostname = Column(String(32))

    def __str__(self):
        return 'Hostname: %s' % self.hostname

    def __repr__(self):
        return str(self)


# Usage TABLE
    # timestamp
    # cpu + other to be added later on
class Usage(BaseModel):
    __tablename__ = 'usages'

    timestamp = Column(DateTime())
    cpu = Column(Integer)
    user_id = Column(ForeignKey('users.id'))

    user = relationship("User",
                        back_populates='usages',
                        order_by=User.id)

    def __str__(self):
        return '%(user)s: %(timestamp)s - %(cpu)s'\
            % {'user': self.user.hostname,
               'message': self.timestamp,
               'cpu': self.cpu}

    def __repr__(self):
        return str(self)


User.usages = relationship("Usage",
                           back_populates='users',
                           order_by=Usage.id)
