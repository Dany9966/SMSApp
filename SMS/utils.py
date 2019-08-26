from SMS import log


def setup_cmd(parser, config):
    args = parser.parse_args()
    config.load_config(args.config_path)
    log.configure_logging()
