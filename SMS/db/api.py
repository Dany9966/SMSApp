import platform

from sqlalchemy.orm import joinedload


from SMS.db import models
from SMS.db import session as session_utils


def initialize():
    session_utils.initialize()


def create_tables():
    models.BaseModel.metadata.create_all(session_utils.engine)


@session_utils.ensure_session
def add_user(session=None):
    user = models.User(hostname=platform.node())
    return user.save()


@session_utils.ensure_session
def add_usage(user_id, timestamp, cpu, session=None):
    usage = models.Usage(timestamp=timestamp, cpu=cpu, user_id=user_id)
    return usage.save()


@session_utils.ensure_session
def get_users(session=None):
    users = session.query(models.User).order_by(models.User.id).all()

    return users


@session_utils.ensure_session
def get_user(user_id=None, session=None):
    query = session.query(models.User)
    return query.filter_by(id=user_id).one()


@session_utils.ensure_session
def get_usages(user_id=None, session=None):
    if user_id:
        return session.query(models.Usage).options(
            joinedload(models.Usage.user)).filter_by(id=user_id).\
            order_by(models.Usage.cpu).all()

    return session.query(models.Usage).options(
        joinedload(models.Usage.user)).\
        order_by(models.Usage.cpu).all()
