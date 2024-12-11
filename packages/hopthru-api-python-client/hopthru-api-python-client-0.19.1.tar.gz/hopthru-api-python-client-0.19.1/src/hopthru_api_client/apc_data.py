from datetime import date, timedelta
from typing import List, Optional

import structlog

from .client import HopthruClient, HOPTHRU_API_URL
from .dates import last_day_of_month, last_day_of_week
from .types import APCExtractionInterval, ApiKeyAuth, UploadDateDict

logger = structlog.get_logger("hopthru_api_client")


DEFAULT_LOCAL_DATA_DIR = "hopthru_data"


def get_apc_data_extraction_dates(
    start_date: date, end_date: date, client: HopthruClient
) -> List[UploadDateDict]:
    """
    Break down the date range into a list of date ranges based on the configured extraction interval for
    this agency.
    :param start_date:
    :param end_date:
    :param client:
    :return:
    """
    date_ranges = list()

    interval = client.get_apc_data_extraction_interval()

    while start_date <= end_date:
        first_date = start_date
        if interval == APCExtractionInterval.MONTHLY:
            second_date = min(last_day_of_month(first_date), end_date)
        else:
            second_date = min(last_day_of_week(first_date), end_date)

        date_ranges.append(
            UploadDateDict(
                start_date=first_date,
                end_date=second_date,
            )
        )

        start_date = second_date + timedelta(days=1)

    return date_ranges


def upload_apc_data(
    apc_data_func: callable,
    apc_upload_func: callable,
    apc_desired_dates_func: callable,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    client: Optional[HopthruClient] = None,
    dry_run: bool = False,
    metadata: Optional[dict] = None,
) -> None:
    """
    Uploads APC data to the Hopthru API. Calls the provided function to fetch data from the agency and then
    uploads the resulting CSV files to the Hopthru API.

    :param apc_data_func:
    :param apc_upload_func:
    :param apc_desired_dates_func:
    :param start_date:
    :param end_date:
    :param client:
    :param dry_run:
    :return:
    """
    # First is to determine what date ranges we need.
    if start_date is None:
        # Find out from the Hopthru API.
        try:
            date_ranges = apc_desired_dates_func()
        except Exception as e:
            logger.exception("fetch_date_ranges_failed", exc=str(e))
            return
    else:
        if end_date is None:
            end_date = date.today()

        logger.info(
            "manual_run",
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
        )
        if not dry_run:
            date_ranges = get_apc_data_extraction_dates(start_date, end_date, client)
        else:
            date_ranges = [
                UploadDateDict(
                    start_date=start_date,
                    end_date=end_date,
                )
            ]

    logger.info(
        "determined_date_ranges",
        date_ranges=[
            {
                "start_date": range["start_date"].isoformat(),
                "end_date": range["end_date"].isoformat(),
            }
            for range in date_ranges
        ],
    )

    # There might not be any date ranges to transfer.
    if not date_ranges:
        return

    for range in date_ranges:
        start_date = range["start_date"]
        end_date = range["end_date"]

        # Call the agency-supplied ridership function.
        try:
            filepaths = apc_data_func(start_date, end_date)
        except Exception as e:
            logger.exception(
                "ridership_query_error",
                start_date=start_date.isoformat(),
                end_date=end_date.isoformat(),
                apc_data_func=str(apc_data_func),
                exc=str(e),
            )
            continue

        if len(filepaths) == 0:
            logger.warning(
                "ridership_files_not_found",
                start_date=start_date.isoformat(),
                end_date=end_date.isoformat(),
            )
        elif dry_run:
            logger.info(
                "ridership_files_created",
                filepaths=filepaths,
                dry_run=True,
                metadata=metadata,
                start_date=start_date.isoformat(),
                end_date=end_date.isoformat(),
            )
        else:
            logger.info(
                "ridership_files_created",
                filepaths=filepaths,
                dry_run=False,
                metadata=metadata,
                start_date=start_date.isoformat(),
                end_date=end_date.isoformat(),
            )
            try:
                apc_upload_func(
                    filepaths=filepaths,
                    start_date=start_date,
                    end_date=end_date,
                    metadata=metadata,
                )
            except Exception as e:
                logger.exception(
                    "ridership_upload_failed",
                    filepaths=filepaths,
                    start_date=start_date.isoformat(),
                    end_date=end_date.isoformat(),
                    dry_run=False,
                    exc=str(e),
                    metadata=metadata,
                )
            else:
                logger.info(
                    "ridership_uploaded",
                    filepaths=filepaths,
                    dry_run=False,
                    start_date=start_date.isoformat(),
                    end_date=end_date.isoformat(),
                    metadata=metadata,
                )


def upload_correlated_apc_data(
    api_key: str,
    apc_data_func: callable,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    hopthru_api_url: Optional[str] = None,
    dry_run: bool = False,
) -> None:
    """
    Uploads APC data to the Hopthru API. Calls the provided function to fetch data from the agency and then
    uploads the resulting CSV files to the Hopthru API.

    :param api_key:
    :param apc_data_func:
    :param start_date:
    :param end_date:
    :param hopthru_api_url:
    :param dry_run:
    :return:
    """
    client = HopthruClient(
        ApiKeyAuth(api_key=api_key),
        server_url=HOPTHRU_API_URL if hopthru_api_url is None else hopthru_api_url,
    )

    upload_apc_data(
        apc_data_func=apc_data_func,
        apc_upload_func=client.upload_correlated_apc_data,
        apc_desired_dates_func=client.get_desired_apc_data_dates,
        start_date=start_date,
        end_date=end_date,
        client=client,
        dry_run=dry_run,
    )


def upload_raw_apc_data(
    api_key: str,
    apc_data_func: callable,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    hopthru_api_url: Optional[str] = None,
    dry_run: bool = False,
    metadata: Optional[dict] = None,
) -> None:
    """
    Uploads raw APC data to the Hopthru API. Calls the provided function to fetch data from the agency and then
    uploads the resulting CSV files to the Hopthru API.

    :param api_key:
    :param apc_data_func:
    :param start_date:
    :param end_date:
    :param hopthru_api_url:
    :param dry_run:
    :param metadata:
    :return:
    """
    client = HopthruClient(
        ApiKeyAuth(api_key=api_key),
        server_url=HOPTHRU_API_URL if hopthru_api_url is None else hopthru_api_url,
    )

    upload_apc_data(
        apc_data_func=apc_data_func,
        apc_upload_func=client.upload_raw_apc_data,
        apc_desired_dates_func=client.get_desired_apc_data_dates,
        start_date=start_date,
        end_date=end_date,
        client=client,
        dry_run=dry_run,
        metadata=metadata,
    )
