from SMS.db import models
from SMS.db import session as session_utils


def initialize():
    session_utils.initialize()


def create_tables():
    models.BaseModel.metadata.create_all(session_utils.engine)


@session_utils.ensure_session
def add_usage(name, timestamp, m_type, m_value, m_unit, session=None):
    usage = models.Usage(hostname=name, timestamp=timestamp,
                         metric_type=m_type, metric_value=m_value,
                         metric_unit=m_unit)
    return usage.save()


@session_utils.ensure_session
def get_usage(hostname=None, m_type=None, start_time=None, end_time=None,
              session=None):
    q = session.query(models.Usage)
    if hostname is not None:
        q = q.filter_by(hostname=hostname)
    if m_type is not None:
        q = q.filter_by(metric_type=m_type)
    if start_time is not None:
        q = q.filter(models.Usage.timestamp >= start_time)
    if end_time is not None:
        q = q.filter(models.Usage.timestamp <= end_time)

    return q.all()
