import argparse

import SMS.config
from SMS.client import rpc
from SMS import log

CONF = SMS.config.CONF

parser = argparse.ArgumentParser(description='SMS RPC client.')
parser.add_argument('--config-path', required=True,
                    help='The config file path.')


def main():
    args = parser.parse_args()

    CONF.load_config(args.config_path)
    log.configure_logging()

    # rpc_server = rpc.SMSClientRPCAPI()  # noqa

    # Ran out of time before adding some CLI. Here, have
    # a PDB breakpoint instead.
    # from SMS.db import api  # noqa
    # import pdb; pdb.set_trace()  # noqa

    # rpc_server.call()  # noqa
