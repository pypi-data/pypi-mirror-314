import json
import time
import uuid

from datetime import date
from unittest.mock import MagicMock, patch

import httpretty

from hopthru_api_client.apc_data import (
    get_apc_data_extraction_dates,
    upload_correlated_apc_data,
    upload_raw_apc_data,
)
from hopthru_api_client.types import APCExtractionInterval, UploadDateDict


def test_get_apc_data_extraction_dates_weekly():
    start_date = date(2021, 1, 1)
    end_date = date(2021, 1, 31)
    client_mock = MagicMock()
    client_mock.get_apc_data_extraction_interval.return_value = (
        APCExtractionInterval.WEEKLY
    )

    date_ranges = get_apc_data_extraction_dates(start_date, end_date, client_mock)

    assert date_ranges == [
        UploadDateDict(start_date=date(2021, 1, 1), end_date=date(2021, 1, 3)),
        UploadDateDict(start_date=date(2021, 1, 4), end_date=date(2021, 1, 10)),
        UploadDateDict(start_date=date(2021, 1, 11), end_date=date(2021, 1, 17)),
        UploadDateDict(start_date=date(2021, 1, 18), end_date=date(2021, 1, 24)),
        UploadDateDict(start_date=date(2021, 1, 25), end_date=date(2021, 1, 31)),
    ]


def test_get_apc_data_extraction_dates_monthly():
    start_date = date(2021, 1, 15)
    end_date = date(2021, 3, 17)
    client_mock = MagicMock()
    client_mock.get_apc_data_extraction_interval.return_value = (
        APCExtractionInterval.MONTHLY
    )

    date_ranges = get_apc_data_extraction_dates(start_date, end_date, client_mock)

    assert date_ranges == [
        UploadDateDict(start_date=date(2021, 1, 15), end_date=date(2021, 1, 31)),
        UploadDateDict(start_date=date(2021, 2, 1), end_date=date(2021, 2, 28)),
        UploadDateDict(start_date=date(2021, 3, 1), end_date=date(2021, 3, 17)),
    ]


@httpretty.activate
@patch("hopthru_api_client.apc_data.get_apc_data_extraction_dates")
def test_upload_correlated_apc_data(extraction_dates_mock):
    create_upload_group_url = (
        "https://api.hopthru.com/v1/date-range-file-uploads-groups"
    )

    upload_group_id = uuid.uuid4()
    upload_group_id2 = uuid.uuid4()

    httpretty.register_uri(
        httpretty.POST,
        create_upload_group_url,
        responses=[
            httpretty.Response(
                body=json.dumps(
                    {
                        "id": str(upload_group_id),
                        "groupType": "correlated_apc",
                        "groupStatus": "waiting_for_files",
                        "startDate": "2021-01-01",
                        "endDate": "2021-01-31",
                        "hasManyItems": False,
                        "metadata": None,
                    }
                ),
                status=201,
            ),
            httpretty.Response(
                body=json.dumps(
                    {
                        "id": str(upload_group_id2),
                        "groupType": "correlated_apc",
                        "groupStatus": "waiting_for_files",
                        "startDate": "2020-02-01",
                        "endDate": "2020-02-28",
                        "hasManyItems": False,
                        "metadata": None,
                    }
                ),
                status=201,
            ),
        ],
    )

    add_file_to_group_url = f"https://api.hopthru.com/v1/date-range-file-uploads-groups/{upload_group_id}/date-range-file-uploads"
    upload_url = "https://hopthru-fileupload.s3.amazonaws.com/"

    httpretty.register_uri(
        httpretty.POST,
        add_file_to_group_url,
        responses=[
            httpretty.Response(
                body=json.dumps(
                    {
                        "id": str(uuid.uuid4()),
                        "uploadUrlExpiry": int(time.time() + 3600),
                        "uploadUrl": upload_url,
                        "uploadFormFields": {
                            "key": "nctd/foo.csv",
                            "AWSAccessKeyId": "AKIAZYTC44JK7DL5HD6C",
                            "policy": "grhoghregoerghtrogrehotb",
                            "signature": "mKPRXaWIts7Xc3jOo9v+CHbx5ic=",
                        },
                    }
                ),
                status=200,
            ),
        ],
    )

    add_file_to_group_url2 = f"https://api.hopthru.com/v1/date-range-file-uploads-groups/{upload_group_id2}/date-range-file-uploads"

    httpretty.register_uri(
        httpretty.POST,
        add_file_to_group_url2,
        responses=[
            httpretty.Response(
                body=json.dumps(
                    {
                        "id": str(uuid.uuid4()),
                        "uploadUrlExpiry": int(time.time() + 3600),
                        "uploadUrl": upload_url,
                        "uploadFormFields": {
                            "key": "nctd/foo.csv",
                            "AWSAccessKeyId": "AKIAZYTC44JK7DL5HD6C",
                            "policy": "grhoghregoerghtrogrehotb",
                            "signature": "mKPRXaWIts7Xc3jOo9v+CHbx5ic=",
                        },
                    }
                ),
                status=200,
            ),
        ],
    )

    httpretty.register_uri(
        httpretty.POST,
        upload_url,
        responses=[
            httpretty.Response(
                body="",
                status=200,
            ),
        ],
    )

    update_group_url = (
        f"https://api.hopthru.com/v1/date-range-file-uploads-groups/{upload_group_id}"
    )

    httpretty.register_uri(
        httpretty.PUT,
        update_group_url,
        responses=[
            httpretty.Response(
                body=json.dumps(
                    {
                        "id": str(upload_group_id),
                        "groupType": "correlated_apc",
                        "groupStatus": "files_received",
                        "startDate": "2020-01-01",
                        "endDate": "2020-01-31",
                        "hasManyItems": False,
                        "metadata": None,
                    }
                ),
                status=200,
            ),
        ],
    )

    update_group_url2 = (
        f"https://api.hopthru.com/v1/date-range-file-uploads-groups/{upload_group_id2}"
    )

    httpretty.register_uri(
        httpretty.PUT,
        update_group_url2,
        responses=[
            httpretty.Response(
                body=json.dumps(
                    {
                        "id": str(upload_group_id2),
                        "groupType": "correlated_apc",
                        "groupStatus": "files_received",
                        "startDate": "2020-02-01",
                        "endDate": "2020-02-28",
                        "hasManyItems": False,
                        "metadata": None,
                    }
                ),
                status=200,
            ),
        ],
    )

    extraction_dates_mock.return_value = [
        UploadDateDict(start_date=date(2021, 1, 1), end_date=date(2021, 1, 31)),
        UploadDateDict(start_date=date(2021, 2, 1), end_date=date(2021, 2, 28)),
    ]

    apc_data_func_mock = MagicMock()
    apc_data_func_mock.side_effect = [
        ["tests/fixtures/nctd_apc_20210101_20210131.csv"],
        ["tests/fixtures/nctd_apc_20210201_20210228.csv"],
    ]

    upload_correlated_apc_data(
        api_key="api-key",
        apc_data_func=apc_data_func_mock,
        start_date=date(2021, 1, 1),
        end_date=date(2021, 2, 28),
    )

    sent_reqs = httpretty.latest_requests()

    # Note: there's a bug in httpretty that causes the requests to be recorded twice
    # https://github.com/gabrielfalcao/HTTPretty/issues/425
    assert len(sent_reqs) / 2 == 8

    assert sent_reqs[0].url == create_upload_group_url
    request_body = json.loads(sent_reqs[0].body)

    assert request_body == {
        "groupType": "correlated_apc",
        "startDate": "2021-01-01",
        "endDate": "2021-01-31",
        "hasManyItems": False,
        "metadata": None,
    }

    assert sent_reqs[2].url == add_file_to_group_url
    request_body = json.loads(sent_reqs[2].body)
    assert request_body == {
        "filename": "nctd_apc_20210101_20210131.csv",
    }

    assert sent_reqs[4].url == upload_url
    assert (
        sent_reqs[4]
        .headers["Content-Type"]
        .startswith("multipart/form-data; boundary=")
    )
    assert (
        'Content-Disposition: form-data; name="file"; filename="nctd_apc_20210101_20210131.csv"'
        in str(sent_reqs[4].body)
    )

    assert sent_reqs[6].url == update_group_url
    request_body = json.loads(sent_reqs[6].body)
    assert request_body == {
        "status": "files_received",
    }

    assert sent_reqs[8].url == create_upload_group_url
    request_body = json.loads(sent_reqs[8].body)
    assert request_body == {
        "groupType": "correlated_apc",
        "startDate": "2021-02-01",
        "endDate": "2021-02-28",
        "hasManyItems": False,
        "metadata": None,
    }

    assert sent_reqs[10].url == add_file_to_group_url2
    request_body = json.loads(sent_reqs[10].body)
    assert request_body == {
        "filename": "nctd_apc_20210201_20210228.csv",
    }
    assert sent_reqs[12].url == upload_url
    assert (
        sent_reqs[12]
        .headers["Content-Type"]
        .startswith("multipart/form-data; boundary=")
    )
    assert (
        'Content-Disposition: form-data; name="file"; filename="nctd_apc_20210201_20210228.csv"'
        in str(sent_reqs[12].body)
    )

    assert sent_reqs[14].url == update_group_url2
    request_body = json.loads(sent_reqs[14].body)
    assert request_body == {
        "status": "files_received",
    }


@httpretty.activate
@patch("hopthru_api_client.apc_data.get_apc_data_extraction_dates")
def test_upload_raw_apc_data(extraction_dates_mock):
    create_upload_group_url = (
        "https://api.hopthru.com/v1/date-range-file-uploads-groups"
    )

    upload_group_id = uuid.uuid4()
    upload_group_id2 = uuid.uuid4()

    httpretty.register_uri(
        httpretty.POST,
        create_upload_group_url,
        responses=[
            httpretty.Response(
                body=json.dumps(
                    {
                        "id": str(upload_group_id),
                        "groupType": "raw_apc",
                        "groupStatus": "waiting_for_files",
                        "startDate": "2021-01-01",
                        "endDate": "2021-01-31",
                        "hasManyItems": False,
                        "metadata": {"rawDataType": "dilax"},
                    }
                ),
                status=201,
            ),
            httpretty.Response(
                body=json.dumps(
                    {
                        "id": str(upload_group_id2),
                        "groupType": "raw_apc",
                        "groupStatus": "waiting_for_files",
                        "startDate": "2020-02-01",
                        "endDate": "2020-02-28",
                        "hasManyItems": False,
                        "metadata": {"rawDataType": "dilax"},
                    }
                ),
                status=201,
            ),
        ],
    )

    add_file_to_group_url = f"https://api.hopthru.com/v1/date-range-file-uploads-groups/{upload_group_id}/date-range-file-uploads"
    upload_url = "https://hopthru-fileupload.s3.amazonaws.com/"

    httpretty.register_uri(
        httpretty.POST,
        add_file_to_group_url,
        responses=[
            httpretty.Response(
                body=json.dumps(
                    {
                        "id": str(uuid.uuid4()),
                        "uploadUrlExpiry": int(time.time() + 3600),
                        "uploadUrl": upload_url,
                        "uploadFormFields": {
                            "key": "nctd/foo.csv",
                            "AWSAccessKeyId": "AKIAZYTC44JK7DL5HD6C",
                            "policy": "grhoghregoerghtrogrehotb",
                            "signature": "mKPRXaWIts7Xc3jOo9v+CHbx5ic=",
                        },
                    }
                ),
                status=200,
            ),
        ],
    )

    add_file_to_group_url2 = f"https://api.hopthru.com/v1/date-range-file-uploads-groups/{upload_group_id2}/date-range-file-uploads"

    httpretty.register_uri(
        httpretty.POST,
        add_file_to_group_url2,
        responses=[
            httpretty.Response(
                body=json.dumps(
                    {
                        "id": str(uuid.uuid4()),
                        "uploadUrlExpiry": int(time.time() + 3600),
                        "uploadUrl": upload_url,
                        "uploadFormFields": {
                            "key": "nctd/foo.csv",
                            "AWSAccessKeyId": "AKIAZYTC44JK7DL5HD6C",
                            "policy": "grhoghregoerghtrogrehotb",
                            "signature": "mKPRXaWIts7Xc3jOo9v+CHbx5ic=",
                        },
                    }
                ),
                status=200,
            ),
        ],
    )

    httpretty.register_uri(
        httpretty.POST,
        upload_url,
        responses=[
            httpretty.Response(
                body="",
                status=200,
            ),
        ],
    )

    update_group_url = (
        f"https://api.hopthru.com/v1/date-range-file-uploads-groups/{upload_group_id}"
    )

    httpretty.register_uri(
        httpretty.PUT,
        update_group_url,
        responses=[
            httpretty.Response(
                body=json.dumps(
                    {
                        "id": str(upload_group_id),
                        "groupType": "raw_apc",
                        "groupStatus": "files_received",
                        "startDate": "2020-01-01",
                        "endDate": "2020-01-31",
                        "hasManyItems": False,
                        "metadata": {"rawDataType": "dilax"},
                    }
                ),
                status=200,
            ),
        ],
    )

    update_group_url2 = (
        f"https://api.hopthru.com/v1/date-range-file-uploads-groups/{upload_group_id2}"
    )

    httpretty.register_uri(
        httpretty.PUT,
        update_group_url2,
        responses=[
            httpretty.Response(
                body=json.dumps(
                    {
                        "id": str(upload_group_id2),
                        "groupType": "raw_apc",
                        "groupStatus": "files_received",
                        "startDate": "2020-02-01",
                        "endDate": "2020-02-28",
                        "hasManyItems": False,
                        "metadata": {"rawDataType": "dilax"},
                    }
                ),
                status=200,
            ),
        ],
    )

    extraction_dates_mock.return_value = [
        UploadDateDict(start_date=date(2021, 1, 1), end_date=date(2021, 1, 31)),
        UploadDateDict(start_date=date(2021, 2, 1), end_date=date(2021, 2, 28)),
    ]

    apc_data_func_mock = MagicMock()
    apc_data_func_mock.side_effect = [
        ["tests/fixtures/nctd_apc_raw_20210101_20210131.csv"],
        ["tests/fixtures/nctd_apc_raw_20210201_20210228.csv"],
    ]

    upload_raw_apc_data(
        api_key="api-key",
        apc_data_func=apc_data_func_mock,
        start_date=date(2021, 1, 1),
        end_date=date(2021, 2, 28),
        metadata={"rawDataType": "dilax"},
    )

    sent_reqs = httpretty.latest_requests()

    # Note: there's a bug in httpretty that causes the requests to be recorded twice
    # https://github.com/gabrielfalcao/HTTPretty/issues/425
    assert len(sent_reqs) / 2 == 8

    assert sent_reqs[0].url == create_upload_group_url
    request_body = json.loads(sent_reqs[0].body)

    assert request_body == {
        "groupType": "raw_apc",
        "startDate": "2021-01-01",
        "endDate": "2021-01-31",
        "hasManyItems": False,
        "metadata": {"rawDataType": "dilax"},
    }

    assert sent_reqs[2].url == add_file_to_group_url
    request_body = json.loads(sent_reqs[2].body)
    assert request_body == {
        "filename": "nctd_apc_raw_20210101_20210131.csv",
    }

    assert sent_reqs[4].url == upload_url
    assert (
        sent_reqs[4]
        .headers["Content-Type"]
        .startswith("multipart/form-data; boundary=")
    )
    assert (
        'Content-Disposition: form-data; name="file"; filename="nctd_apc_raw_20210101_20210131.csv"'
        in str(sent_reqs[4].body)
    )

    assert sent_reqs[6].url == update_group_url
    request_body = json.loads(sent_reqs[6].body)
    assert request_body == {
        "status": "files_received",
    }

    assert sent_reqs[8].url == create_upload_group_url
    request_body = json.loads(sent_reqs[8].body)
    assert request_body == {
        "groupType": "raw_apc",
        "startDate": "2021-02-01",
        "endDate": "2021-02-28",
        "hasManyItems": False,
        "metadata": {"rawDataType": "dilax"},
    }

    assert sent_reqs[10].url == add_file_to_group_url2
    request_body = json.loads(sent_reqs[10].body)
    assert request_body == {
        "filename": "nctd_apc_raw_20210201_20210228.csv",
    }
    assert sent_reqs[12].url == upload_url
    assert (
        sent_reqs[12]
        .headers["Content-Type"]
        .startswith("multipart/form-data; boundary=")
    )
    assert (
        'Content-Disposition: form-data; name="file"; filename="nctd_apc_raw_20210201_20210228.csv"'
        in str(sent_reqs[12].body)
    )

    assert sent_reqs[14].url == update_group_url2
    request_body = json.loads(sent_reqs[14].body)
    assert request_body == {
        "status": "files_received",
    }
