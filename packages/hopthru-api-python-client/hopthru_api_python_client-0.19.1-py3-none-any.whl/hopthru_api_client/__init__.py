import argparse
import datetime
import os

from argparse import Namespace
from configparser import SectionProxy
from typing import Tuple

from .__version__ import __version__  # noqa
from .config import get_config


def create_argument_parser():
    parser = argparse.ArgumentParser(description="Upload data to Hopthru")

    # These options let users specify their own date range.
    parser.add_argument(
        "start_date",
        nargs="?",
        default=None,
        type=datetime.date.fromisoformat,
        help="The first date to upload, in YYYY-MM-DD format"
        " - leave blank to ask Hopthru",
    )
    parser.add_argument(
        "end_date",
        nargs="?",
        default=None,
        type=datetime.date.fromisoformat,
        help="The last date to upload, in YYYY-MM-DD format"
        " - leave blank to ask Hopthru",
    )
    # This option lets users test the script.
    parser.add_argument(
        "--dry_run",
        action="store_true",
        help="Create files without uploading to Hopthru",
    )

    parser.add_argument(
        "--config",
        nargs="?",
        default="hopthru.ini",
        help="Config File",
    )

    parser.add_argument(
        "--config_section",
        nargs="?",
        default=None,
        help="Config Section to use",
    )

    return parser


def initialize_hopthru_api_client() -> Tuple[Namespace, SectionProxy]:
    from .logging import setup_logging
    from .apc_data import DEFAULT_LOCAL_DATA_DIR

    parser = create_argument_parser()
    options = parser.parse_args()

    config = get_config(
        config_file_name=options.config, section_override=options.config_section
    )
    setup_logging(config=config)

    local_data_dir = config.get("local_data_dir", DEFAULT_LOCAL_DATA_DIR)
    if not os.path.isdir(local_data_dir):
        os.makedirs(local_data_dir)
    config["local_data_dir"] = local_data_dir

    return options, config
