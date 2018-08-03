import argparse
import threading

import SMS.config

from SMS.db import api as db_api
from SMS.server import amqp
from SMS import log
import SMS.app

CONF = SMS.config.CONF

parser = argparse.ArgumentParser(description='SMS RPC server.')
parser.add_argument('--config-path', required=True,
                    help='The config file path.')


def main():
    args = parser.parse_args()
    CONF.load_config(args.config_path)

    log.configure_logging()

    db_api.initialize()
    db_api.create_tables()
    threading.Thread(target=SMS.app.app.run).start()
    rmq = amqp.SMSServerAMQP()
    rmq.accept()
