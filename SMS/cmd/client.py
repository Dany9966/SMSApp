import argparse

import SMS.config
from SMS.client import amqp
from SMS import utils

CONF = SMS.config.CONF

parser = argparse.ArgumentParser(description='SMS RPC client.')
parser.add_argument('--config-path', required=True,
                    help='The config file path.')


def main():
    utils.setup_cmd(parser, CONF)

    rmq = amqp.SMSClientAMQP()

    rmq.start_sending()
