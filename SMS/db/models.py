import json
import uuid

from sqlalchemy import ForeignKey, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import relationship, backref

from SMS.db import session as session_utils


# BaseModel TABLE
# id
@as_declarative()
class BaseModel(object):
    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), nullable=True)

    @session_utils.ensure_session
    def save(self, session=None):
        if not self.uuid:
            self.uuid = str(uuid.uuid4())

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
    # username
    # pass?
class User(BaseModel):
    __tablename__ = 'users'

    username = Column(String(32))

    def __str__(self):
        return 'Username: %s' % self.username

    def __repr__(self):
        return str(self)


# Usage TABLE
    # timestamp
    # cpu
class Usage(BaseModel):
    __tablename__ = 'usages'

    timestamp = Column(DateTime())
    cpu = Column(Integer)
    user_id = Column(ForeignKey('users.id'))

    user = relationship("User", backref=backref('usages'),
                        order_by='User.id', lazy='joined')

    def __str__(self):
        return '%(user)s: %(timestamp)s - %(cpu)s'\
            % {'user': self.user.name,
               'message': self.timestamp,
               'cpu': self.cpu}

    def __repr__(self):
        return str(self)
