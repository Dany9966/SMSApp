import argparse

from SMS import config
from SMS.db import api as db_api
from SMS.server import amqp
from SMS import utils

CONF = config.CONF

parser = argparse.ArgumentParser(description='SMS RPC server.')
parser.add_argument('--config-path', required=True,
                    help='The config file path.')


def main():
    utils.setup_cmd(parser, CONF)

    db_api.initialize()
    db_api.create_tables()

    rmq = amqp.SMSServerAMQP()
    rmq.accept()
