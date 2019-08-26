from datetime import datetime
import json
import platform

from SMS import config
from SMS import log
from SMS.client import metrics as metric_methods

CONF = config.CONF
LOG = log.get_logger()


def get_now():
    return datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S")


def collect():
    # get list of metrics from conf file
    metric_list = CONF.metrics.list.split(", ")
    if metric_list == ['']:
        LOG.error('No metrics set! Exiting...')
        raise Exception

    body_m_list = []
    # for every metric listed in CONF, add its usage to body
    for metric in metric_list:
        body_m_list.append(
            {'hostname': platform.node(),
             'timestamp': get_now(),
             'metric': getattr(metric_methods, metric)()})

    return json.dumps({'metrics': body_m_list})
