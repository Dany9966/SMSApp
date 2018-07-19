import argparse

import SMS.config
from SMS.client import amqp
from SMS import log

CONF = SMS.config.CONF

parser = argparse.ArgumentParser(description='SMS RPC client.')
parser.add_argument('--config-path', required=True,
                    help='The config file path.')


def main():
    args = parser.parse_args()

    CONF.load_config(args.config_path)

    log.configure_logging()

    rmq = amqp.SMSClientAMQP()

    rmq.start_sending()
