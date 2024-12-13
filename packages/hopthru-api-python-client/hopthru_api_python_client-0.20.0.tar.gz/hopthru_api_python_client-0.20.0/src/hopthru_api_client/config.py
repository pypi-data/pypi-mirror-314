import configparser
from configparser import SectionProxy
from typing import Optional


def get_config(
    config_file_name: str = "hopthru.ini", section_override: Optional[str] = None
) -> SectionProxy:
    config = configparser.ConfigParser()
    config.read(config_file_name)

    section = config["hopthru"]
    if section_override:
        section.update(config[section_override])

    return section
