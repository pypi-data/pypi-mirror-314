import logging

from configparser import SectionProxy
from typing import Any, List, Optional, Tuple

import sentry_sdk
import structlog
import requests

from structlog.processors import CallsiteParameter
from structlog.types import EventDict, WrappedLogger
from structlog_sentry import SentryJsonProcessor

from .__version__ import __version__

hopthru_config = None


def annotate_logs_with_hopthru_client_data(logger, log_method, event_dict):
    agency = hopthru_config.get("agency") if hopthru_config is not None else None
    if "agency" not in event_dict and agency:
        event_dict["agency"] = agency

    if "hopthru_api_client_version" not in event_dict:
        event_dict["hopthru_api_client_version"] = __version__

    return event_dict


def send_log_to_newrelic(logger, log_method, event_dict):

    api_key = (
        hopthru_config.get("newrelic_api_key") if hopthru_config is not None else None
    )

    if api_key is None:
        return

    headers = {"Api-Key": api_key}

    payload = {
        "message": f"{log_method} - {event_dict['logger']} - {event_dict.get('agency', '')} - {event_dict['event']}",
        "attributes": event_dict,
    }

    requests.post("https://log-api.newrelic.com/log/v1", json=payload, headers=headers)

    return event_dict


class HopthruApiClientRenderer(structlog.processors.KeyValueRenderer):
    def __init__(
        self,
        key_order: Optional[List[str]] = None,
        exclude_keys: Optional[List[str]] = None,
    ):
        super().__init__(key_order=key_order)

        def ordered_items(event_dict: EventDict) -> List[Tuple[str, Any]]:
            items = []
            for key in key_order:  # type: ignore
                value = event_dict.pop(key, None)
                items.append((key, value))

            for key, value in event_dict.items():  # type: ignore
                if key not in exclude_keys:
                    items.append((key, value))

            return items

        self._ordered_items = ordered_items

    def __call__(self, _: WrappedLogger, __: str, event_dict: EventDict) -> str:
        string = " ".join(
            k + "=" + self._repr(v) for k, v in self._ordered_items(event_dict)
        )
        return string


def setup_logging(
    log_level: int = logging.INFO,
    config: Optional[SectionProxy] = None,
) -> None:
    """
    Setup logging for the API client.
    :param log_level:
    :return:
    """
    # store the supplied config so we can access it later from the newrelic logger
    global hopthru_config
    hopthru_config = config
    agency = hopthru_config.get("agency") if hopthru_config is not None else None

    if config is not None:
        log_file = config.get("log_file", "hopthru_apc_log.txt")
        sentry_dsn = config.get("sentry_dsn")
        sentry_log_level = config.get("sentry_log_level", "30")
    else:
        log_file = None
        sentry_dsn = None
        sentry_log_level = "30"

    if sentry_dsn:
        sentry_sdk.init(
            dsn=sentry_dsn,
            release=f"hopthru-upload@{__version__}",
            environment=config.get("sentry_environment", "prod"),
        )
        if agency is not None:
            sentry_sdk.set_tag("agency", agency)

    logging.basicConfig(level=int(log_level), format="%(message)s")

    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.CallsiteParameterAdder(
                [
                    CallsiteParameter.FILENAME,
                    CallsiteParameter.FUNC_NAME,
                    CallsiteParameter.LINENO,
                ]
            ),
            SentryJsonProcessor(level=int(sentry_log_level)),
            annotate_logs_with_hopthru_client_data,
            send_log_to_newrelic,
            HopthruApiClientRenderer(
                key_order=["timestamp", "level", "filename", "lineno", "event"],
                exclude_keys=[
                    "logger",
                    "sentry",
                    "sentry_id",
                    "agency",
                    "hopthru_api_client_version",
                    "func_name",
                ],
            ),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Optionally log to a file
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(int(log_level))
        logging.getLogger().addHandler(file_handler)
    else:
        structlog.get_logger().warning("log_file_missing")
