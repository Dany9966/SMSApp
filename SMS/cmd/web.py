import argparse

from SMS import config
from SMS.app import app as flask_app
from SMS.db import api as db_api
from SMS import utils

CONF = config.CONF

parser = argparse.ArgumentParser(description='SMS web server.')
parser.add_argument('--config-path', required=True,
                    help='The config file path.')


def main():
    utils.setup_cmd(parser, CONF)
    db_api.initialize()
    flask_app.run()
