from sqlalchemy.orm import joinedload


from SMS.db import models
from SMS.db import session as session_utils


def initialize():
    session_utils.initialize()


def create_tables():
    models.BaseModel.metadata.create_all(session_utils.engine)


@session_utils.ensure_session
def add_usage(name, timestamp, m_type, m_value, session=None):
    usage = models.Usage(hostname=name, timestamp=timestamp,
                         metric_type=m_type, metric_value=m_value)
    return usage.save()


@session_utils.ensure_session
def get_usages(user_id=None, session=None):
    if user_id:
        return session.query(models.Usage).options(
            joinedload(models.Usage.user)).filter_by(id=user_id).\
            order_by(models.Usage.cpu).all()

    return session.query(models.Usage).options(
        joinedload(models.Usage.user)).\
        order_by(models.Usage.cpu).all()
