import json
import uuid
import time

from datetime import date

import httpretty

from hopthru_api_client.client import HopthruClient
from hopthru_api_client.types import (
    APCExtractionInterval,
    UploadDateDict,
    ApiKeyAuth,
    UserNamePasswordAuth,
)


def register_login_url():
    login_url = "https://api.hopthru.com/api/token/"

    httpretty.register_uri(
        httpretty.POST,
        login_url,
        responses=[
            httpretty.Response(
                body=json.dumps(
                    {
                        "refresh": "refresh-token",
                        "access": "access-token",
                    }
                ),
                status=200,
            ),
        ],
    )


@httpretty.activate
def test_get_apc_data_extraction_interval_weekly():
    url = "https://api.hopthru.com/data/interval"

    httpretty.register_uri(
        httpretty.GET,
        url,
        responses=[
            httpretty.Response(
                body=json.dumps("Weekly"),
                status=200,
            ),
        ],
    )
    client = HopthruClient(ApiKeyAuth(api_key="api-key"))

    assert client.get_apc_data_extraction_interval() == APCExtractionInterval.WEEKLY


@httpretty.activate
def test_get_apc_data_extraction_interval_monthly():
    url = "https://api.hopthru.com/data/interval"

    httpretty.register_uri(
        httpretty.GET,
        url,
        responses=[
            httpretty.Response(
                body=json.dumps("Monthly"),
                status=200,
            ),
        ],
    )

    client = HopthruClient(ApiKeyAuth(api_key="api-key"))

    assert client.get_apc_data_extraction_interval() == APCExtractionInterval.MONTHLY


@httpretty.activate
def test_get_desired_apc_data_dates():
    url = "https://api.hopthru.com/data/upload_dates"

    expected_dates = [
        UploadDateDict(
            start_date=date(2019, 1, 1),
            end_date=date(2019, 1, 31),
        ),
        UploadDateDict(
            start_date=date(2020, 1, 1),
            end_date=date(2020, 1, 31),
        ),
    ]

    json_response = []
    for dt in expected_dates:
        json_response.append(
            {
                "start_date": dt["start_date"].isoformat(),
                "end_date": dt["end_date"].isoformat(),
            }
        )

    httpretty.register_uri(
        httpretty.GET,
        url,
        responses=[
            httpretty.Response(
                body=json.dumps(json_response),
                status=200,
            ),
        ],
    )

    client = HopthruClient(ApiKeyAuth(api_key="api-key"))

    assert client.get_desired_apc_data_dates() == expected_dates


@httpretty.activate
def test_upload_correlated_apc_data():
    create_upload_group_url = (
        "https://api.hopthru.com/v1/date-range-file-uploads-groups"
    )

    upload_group_id = uuid.uuid4()
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
            )
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

    client = HopthruClient(ApiKeyAuth(api_key="api-key"))
    file_name = "tests/fixtures/nctd_apc_122120_122720.csv"

    client.upload_correlated_apc_data(
        [file_name],
        start_date=date(2020, 1, 1),
        end_date=date(2020, 1, 31),
        metadata=None,
    )

    sent_reqs = httpretty.latest_requests()

    # Note: there's a bug in httpretty that causes the requerst to be recorded twice
    # https://github.com/gabrielfalcao/HTTPretty/issues/425
    assert len(sent_reqs) / 2 == 4

    assert sent_reqs[0].url == create_upload_group_url
    sent_request = json.loads(sent_reqs[0].body)

    assert sent_request == {
        "groupType": "correlated_apc",
        "startDate": "2020-01-01",
        "endDate": "2020-01-31",
        "hasManyItems": False,
        "metadata": None,
    }

    assert sent_reqs[2].url == add_file_to_group_url

    assert sent_reqs[4].url == upload_url
    assert (
        sent_reqs[4]
        .headers["Content-Type"]
        .startswith("multipart/form-data; boundary=")
    )
    assert (
        'Content-Disposition: form-data; name="file"; filename="nctd_apc_122120_122720.csv"'
        in str(sent_reqs[4].body)
    )

    assert sent_reqs[6].url == update_group_url
    request_body = json.loads(sent_reqs[6].body)
    assert request_body == {
        "status": "files_received",
    }


@httpretty.activate
def test_upload_raw_apc_data():
    create_upload_group_url = (
        "https://api.hopthru.com/v1/date-range-file-uploads-groups"
    )

    upload_group_id = uuid.uuid4()
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
            )
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

    client = HopthruClient(ApiKeyAuth(api_key="api-key"))
    file_name = "tests/fixtures/nctd_apc_122120_122720.csv"

    client.upload_raw_apc_data(
        [file_name],
        start_date=date(2020, 1, 1),
        end_date=date(2020, 1, 31),
        metadata={"foo": "bar"},
    )

    sent_reqs = httpretty.latest_requests()

    # Note: there's a bug in httpretty that causes the requerst to be recorded twice
    # https://github.com/gabrielfalcao/HTTPretty/issues/425
    assert len(sent_reqs) / 2 == 4

    assert sent_reqs[0].url == create_upload_group_url
    sent_request = json.loads(sent_reqs[0].body)

    assert sent_request == {
        "groupType": "raw_apc",
        "startDate": "2020-01-01",
        "endDate": "2020-01-31",
        "hasManyItems": False,
        "metadata": {"foo": "bar"},
    }

    assert sent_reqs[2].url == add_file_to_group_url

    assert sent_reqs[4].url == upload_url
    assert (
        sent_reqs[4]
        .headers["Content-Type"]
        .startswith("multipart/form-data; boundary=")
    )
    assert (
        'Content-Disposition: form-data; name="file"; filename="nctd_apc_122120_122720.csv"'
        in str(sent_reqs[4].body)
    )

    assert sent_reqs[6].url == update_group_url
    request_body = json.loads(sent_reqs[6].body)
    assert request_body == {
        "status": "files_received",
    }


@httpretty.activate
def test_login():
    register_login_url()

    # instantiating the client will trigger the login
    HopthruClient(UserNamePasswordAuth(username="foo", password="bar"))

    sent_request = httpretty.last_request()
    sent_request_json = json.loads(sent_request.body)

    assert sent_request_json == {
        "username": "foo",
        "password": "bar",
    }
    assert sent_request.url.endswith("/api/token/")


@httpretty.activate
def test_me():
    register_login_url()

    resp_expected = {
        "first_name": "Brock",
        "last_name": "Haywood",
        "username": "brock@hopthru.com",
        "user_id": "1b7ec2b4-174c-49ab-ae98-d54f602710d7",
        "user_roles": [
            {
                "id": "cf5fc0e6-7b03-4a6b-b572-c4e843a4fb74",
                "name": "Admin (Owner)",
                "agency": {
                    "id": "1dfa00fe-563f-48b6-8f6d-4101ba22fd37",
                    "name": "NCTD",
                    "latitude": 33.1975104,
                    "longitude": -117.3774688,
                    "data_start_date": "2021-06-01",
                    "show_offs": True,
                    "show_direction": True,
                    "show_load": True,
                    "show_maxload": True,
                    "show_activity": True,
                    "show_bprh": True,
                    "show_pdt": False,
                    "show_trips": True,
                    "show_atypical_days": False,
                    "show_expand": True,
                    "distance_type": 1,
                    "use_stop_code": True,
                },
                "description": "All available permissions plus ability to remove admins.",
                "edit_team_members": True,
                "edit_tags": True,
                "edit_links": True,
                "export_data": True,
            }
        ],
    }

    httpretty.register_uri(
        httpretty.GET,
        "https://api.hopthru.com/me",
        responses=[
            httpretty.Response(
                body=json.dumps(resp_expected),
                status=200,
            ),
        ],
    )

    client = HopthruClient(UserNamePasswordAuth(username="foo", password="bar"))
    resp_actual = client.get_me()

    assert resp_actual == resp_expected

    sent_request = httpretty.last_request()
    assert sent_request.url.endswith("/me")


@httpretty.activate
def test_get_time_ranges():
    register_login_url()

    resp_expected = [
        {
            "id": "5ca222f1-ac0c-4c53-8ec5-64afc08e310b",
            "str": "NCTD - Early Morning (3:00AM-5:00AM)",
            "short_name": "Early Morning",
            "long_name": "Early Morning (3:00AM-5:00AM)",
        },
        {
            "id": "a071823a-1e30-4cd6-9bad-1c6e75a2b2fe",
            "str": "NCTD - Peak Morning (5:00AM-9:00AM)",
            "short_name": "Peak Morning",
            "long_name": "Peak Morning (5:00AM-9:00AM)",
        },
    ]

    httpretty.register_uri(
        httpretty.POST,
        "https://api.hopthru.com/agencies/timeranges",
        responses=[
            httpretty.Response(
                body=json.dumps(resp_expected),
                status=200,
            ),
        ],
    )

    client = HopthruClient(
        auth=UserNamePasswordAuth(username="foo", password="bar"),
        agency_id=uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37"),
    )
    resp_actual = client.get_time_ranges()

    assert resp_actual == resp_expected

    sent_request = httpretty.last_request()
    assert sent_request.url.endswith("/agencies/timeranges")


@httpretty.activate
def test_get_system():
    register_login_url()

    resp_expected = {
        "data": {
            "first": {
                "sum_ons": 0,
                "sum_offs": 0,
                "maxload": None,
                "avg_load": 0.0,
                "sum_passenger_distance_travelled": 0.0,
                "total_days": 0,
                "avg_passenger_distance_travelled": 0,
                "sum_activity": 0,
                "avg_ons": 0,
                "boardings_per_revenue_hour": 0.0,
                "avg_offs": 0,
                "avg_activity": 0,
                "unexpanded_trip_count": 0,
                "total_trip_count": 0,
            }
        }
    }

    httpretty.register_uri(
        httpretty.POST,
        "https://api.hopthru.com/boardings/system",
        responses=[
            httpretty.Response(
                body=json.dumps(resp_expected),
                status=200,
            ),
        ],
    )

    client = HopthruClient(
        auth=UserNamePasswordAuth(username="foo", password="bar"),
        agency_id=uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37"),
    )
    resp_actual = client.get_system(
        date(2021, 1, 1), date(2021, 1, 2), [1, 1, 1, 1, 1, 1, 1], None, None
    )

    assert resp_actual == resp_expected

    sent_request = httpretty.last_request()
    assert sent_request.url.endswith("/boardings/system")


@httpretty.activate
def test_get_system_v2():
    register_login_url()

    agency_id = uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37")
    job_id = str(uuid.uuid4())

    resp_expected = {
        "data": {
            "id": job_id,
            "status": "finished",
            "updatedAt": "2021-05-02T12:37:05",
            "jobData": {
                "sumOns": 16,
                "sumOffs": 15,
                "maxLoad": 5.00,
                "avgLoad": 1.94,
                "sumActivity": 31,
                "avgOns": 8,
                "boardingsPerRevenueHour": 0.85,
                "avgOffs": 8,
                "avgActivity": 16,
                "unexpandedTripCount": 0,  # these trip counts are only non-zero when we include expanded data
                "totalTripCount": 0,
                "avgPassengerDistanceTravelled": 14.01,
                "sumPassengerDistanceTravelled": 28.01,
            },
        },
        "links": [],
    }

    httpretty.register_uri(
        httpretty.POST,
        f"https://api.hopthru.com/v2/agencies/{agency_id}/boardings/system",
        responses=[
            httpretty.Response(
                body=json.dumps(resp_expected),
                status=200,
            ),
        ],
    )

    client = HopthruClient(
        auth=UserNamePasswordAuth(username="foo", password="bar"),
        agency_id=uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37"),
    )
    resp_actual = client.get_system_v2(
        date(2021, 1, 1), date(2021, 1, 2), [1, 1, 1, 1, 1, 1, 1], None, None
    )

    assert resp_actual == resp_expected

    sent_request = httpretty.last_request()
    assert sent_request.url.endswith("/boardings/system")


@httpretty.activate
def test_get_dates():
    register_login_url()

    resp_expected = {
        "data": [
            {
                "first_start_date": "2021-01-01",
                "first_end_date": "2021-01-03",
                "first_sum_ons": 0,
                "first_sum_offs": 0,
                "first_maxload": 0,
                "first_avg_load": 0,
                "first_sum_passenger_distance_travelled": 0,
                "first_avg_passenger_distance_travelled": 0,
                "first_sum_activity": 0,
                "first_avg_ons": 0,
                "first_avg_offs": 0,
                "first_avg_activity": 0,
                "first_boardings_per_revenue_hour": 0,
            },
        ]
    }

    httpretty.register_uri(
        httpretty.POST,
        "https://api.hopthru.com/boardings/dates",
        responses=[
            httpretty.Response(
                body=json.dumps(resp_expected),
                status=200,
            ),
        ],
    )

    client = HopthruClient(
        auth=UserNamePasswordAuth(username="foo", password="bar"),
        agency_id=uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37"),
    )
    resp_actual = client.get_dates(
        date(2021, 1, 1), date(2021, 1, 3), [1, 1, 1, 1, 1, 1, 1], None, None
    )

    assert resp_actual == resp_expected

    sent_request = httpretty.last_request()
    assert sent_request.url.endswith("/boardings/dates")


@httpretty.activate
def test_get_dates_v2():
    register_login_url()

    agency_id = uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37")
    job_id = str(uuid.uuid4())

    resp_expected = {
        "data": {
            "id": job_id,
            "status": "finished",
            "updatedAt": "2021-05-02T12:37:05",
            "jobData": [
                {
                    "startDate": "2020-12-21",
                    "endDate": "2020-12-21",
                    "activity": {
                        "sumOns": 14,
                        "sumOffs": 13,
                        "maxLoad": 5,
                        "sumActivity": 27,
                        "avgOns": 14,
                        "avgOffs": 13,
                        "avgActivity": 27,
                        "boardingsPerRevenueHour": 2.98,
                        "avgLoad": 1.94,
                        "avgPassengerDistanceTravelled": 28.01,
                        "sumPassengerDistanceTravelled": 28.01,
                    },
                }
            ],
        },
        "links": [],
    }

    httpretty.register_uri(
        httpretty.POST,
        f"https://api.hopthru.com/v2/agencies/{agency_id}/boardings/dates",
        responses=[
            httpretty.Response(
                body=json.dumps(resp_expected),
                status=200,
            ),
        ],
    )

    client = HopthruClient(
        auth=UserNamePasswordAuth(username="foo", password="bar"),
        agency_id=uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37"),
    )
    resp_actual = client.get_dates_v2(
        date(2021, 1, 1), date(2021, 1, 3), [1, 1, 1, 1, 1, 1, 1], None, None
    )

    assert resp_actual == resp_expected

    sent_request = httpretty.last_request()
    assert sent_request.url.endswith("/boardings/dates")


@httpretty.activate
def test_get_days():
    register_login_url()

    resp_expected = {
        "data": [
            {
                "name": "Su",
                "first_sum_ons": 28368,
                "first_sum_offs": 26964,
                "first_maxload": 65.0,
                "first_avg_load": 5.43,
                "first_sum_passenger_distance_travelled": 172159.74,
                "first_avg_passenger_distance_travelled": 43039.93,
                "first_sum_activity": 55332,
                "first_avg_ons": 7092,
                "first_avg_offs": 6741,
                "first_avg_activity": 13833,
                "first_boardings_per_revenue_hour": 13.43,
            },
            {
                "name": "M",
                "first_sum_ons": 44981,
                "first_sum_offs": 43537,
                "first_maxload": 60.0,
                "first_avg_load": 4.63,
                "first_sum_passenger_distance_travelled": 264048.92,
                "first_avg_passenger_distance_travelled": 66012.23,
                "first_sum_activity": 88518,
                "first_avg_ons": 11245,
                "first_avg_offs": 10884,
                "first_avg_activity": 22130,
                "first_boardings_per_revenue_hour": 10.92,
            },
        ]
    }

    httpretty.register_uri(
        httpretty.POST,
        "https://api.hopthru.com/boardings/days",
        responses=[
            httpretty.Response(
                body=json.dumps(resp_expected),
                status=200,
            ),
        ],
    )

    client = HopthruClient(
        auth=UserNamePasswordAuth(username="foo", password="bar"),
        agency_id=uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37"),
    )
    resp_actual = client.get_days(
        date(2021, 1, 1), date(2021, 1, 2), [1, 1, 0, 0, 0, 0, 0], None, None
    )

    assert resp_actual == resp_expected

    sent_request = httpretty.last_request()
    assert sent_request.url.endswith("/boardings/days")


@httpretty.activate
def test_get_days_v2():
    register_login_url()

    agency_id = uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37")
    job_id = str(uuid.uuid4())

    resp_expected = {
        "data": {
            "id": job_id,
            "status": "finished",
            "updatedAt": "2021-05-02T12:37:05",
            "jobData": [
                {
                    "name": "M",
                    "activity": {
                        "sumOns": 14,
                        "sumOffs": 13,
                        "maxLoad": 5,
                        "sumActivity": 27,
                        "avgOns": 14,
                        "avgOffs": 13,
                        "avgActivity": 27,
                        "avgLoad": 1.94,
                        "boardingsPerRevenueHour": 2.98,
                        "avgPassengerDistanceTravelled": 28.01,
                        "sumPassengerDistanceTravelled": 28.01,
                    },
                }
            ],
        },
        "links": [],
    }

    httpretty.register_uri(
        httpretty.POST,
        f"https://api.hopthru.com/v2/agencies/{agency_id}/boardings/days",
        responses=[
            httpretty.Response(
                body=json.dumps(resp_expected),
                status=200,
            ),
        ],
    )

    client = HopthruClient(
        auth=UserNamePasswordAuth(username="foo", password="bar"),
        agency_id=uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37"),
    )
    resp_actual = client.get_days_v2(
        date(2021, 1, 1), date(2021, 1, 3), [1, 1, 1, 1, 1, 1, 1], None, None
    )

    assert resp_actual == resp_expected

    sent_request = httpretty.last_request()
    assert sent_request.url.endswith("/boardings/days")


@httpretty.activate
def test_get_periods():
    register_login_url()

    resp_expected = {
        "data": [
            {
                "name": "Early Morning",
                "first_sum_ons": 5244,
                "first_sum_offs": 4010,
                "first_maxload": 20.0,
                "first_avg_load": 2.55,
                "first_sum_passenger_distance_travelled": 14905.13,
                "first_avg_passenger_distance_travelled": 496.84,
                "first_sum_activity": 9254,
                "first_avg_ons": 175,
                "first_avg_offs": 134,
                "first_avg_activity": 308,
                "first_boardings_per_revenue_hour": 20.46,
            }
        ]
    }

    httpretty.register_uri(
        httpretty.POST,
        "https://api.hopthru.com/boardings/periods",
        responses=[
            httpretty.Response(
                body=json.dumps(resp_expected),
                status=200,
            ),
        ],
    )

    client = HopthruClient(
        auth=UserNamePasswordAuth(username="foo", password="bar"),
        agency_id=uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37"),
    )
    resp_actual = client.get_periods(
        date(2021, 1, 1), date(2021, 1, 2), [1, 1, 0, 0, 0, 0, 0], uuid.uuid4(), None
    )

    assert resp_actual == resp_expected

    sent_request = httpretty.last_request()
    assert sent_request.url.endswith("/boardings/periods")


@httpretty.activate
def test_get_period_v2():
    register_login_url()

    agency_id = uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37")
    time_range = uuid.uuid4()
    job_id = str(uuid.uuid4())

    resp_expected = {
        "data": {
            "id": job_id,
            "status": "finished",
            "updatedAt": "2021-05-02T12:37:05",
            "jobData": {
                "name": "Early Morning",
                "activity": {
                    "sumOns": 5244,
                    "sumOffs": 4010,
                    "sumActivity": 9254,
                    "avgOns": 175,
                    "avgOffs": 134,
                    "avgActivity": 308,
                    "maxLoad": 20.0,
                    "avgLoad": 2.55,
                    "sumPassengerDistanceTravelled": 14905.13,
                    "avgPassengerDistanceTravelled": 496.84,
                    "boardingsPerRevenueHour": 20.46,
                },
            },
        },
        "links": [],
    }

    httpretty.register_uri(
        httpretty.POST,
        f"https://api.hopthru.com/v2/agencies/{agency_id}/boardings/periods/{time_range}",
        responses=[
            httpretty.Response(
                body=json.dumps(resp_expected),
                status=200,
            ),
        ],
    )

    client = HopthruClient(
        auth=UserNamePasswordAuth(username="foo", password="bar"),
        agency_id=uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37"),
    )
    resp_actual = client.get_periods_v2(
        date(2021, 1, 1), date(2021, 1, 2), [1, 1, 0, 0, 0, 0, 0], time_range
    )

    assert resp_actual == resp_expected

    sent_request = httpretty.last_request()
    assert sent_request.url.endswith(
        f"/v2/agencies/{agency_id}/boardings/periods/{time_range}"
    )


@httpretty.activate
def test_get_routes_list():
    register_login_url()

    resp_expected = {
        "data": [
            {
                "id": "1d1c63f1-512b-4e49-a243-30e159064175",
                "route_id": "301",
                "route_short_name": "101",
            },
            {
                "id": "2c4fdfd3-0bbc-435f-b93e-e141ad6f8634",
                "route_id": "302",
                "route_short_name": "302",
            },
        ]
    }

    httpretty.register_uri(
        httpretty.POST,
        "https://api.hopthru.com/boardings/routes/list",
        responses=[
            httpretty.Response(
                body=json.dumps(resp_expected),
                status=200,
            ),
        ],
    )

    client = HopthruClient(
        auth=UserNamePasswordAuth(username="foo", password="bar"),
        agency_id=uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37"),
    )
    resp_actual = client.get_routes_list(
        date(2021, 1, 1), date(2021, 1, 2), [1, 1, 0, 0, 0, 0, 0], None
    )

    assert resp_actual == resp_expected

    sent_request = httpretty.last_request()
    assert sent_request.url.endswith("/boardings/routes/list")


@httpretty.activate
def test_get_routes_summary():
    register_login_url()

    resp_expected = {
        "data": [
            {
                "id": "1d1c63f1-512b-4e49-a243-30e159064175",
                "route_id": "301",
                "route_short_name": "101",
                "non_gtfs": False,
                "first": {
                    "sum_ons": 34759,
                    "sum_offs": 31152,
                    "maxload": 55.0,
                    "avg_load": 5.46,
                    "sum_passenger_distance_travelled": 15856.65,
                    "avg_passenger_distance_travelled": 528.55,
                    "sum_activity": 65911,
                    "avg_ons": 1159,
                    "avg_offs": 1038,
                    "avg_activity": 2197,
                    "unexpanded_trip_count": 0,
                    "total_trip_count": 0,
                    "boardings_per_revenue_hour": 9.96,
                },
            }
        ]
    }

    httpretty.register_uri(
        httpretty.POST,
        "https://api.hopthru.com/boardings/routes",
        responses=[
            httpretty.Response(
                body=json.dumps(resp_expected),
                status=200,
            ),
        ],
    )

    client = HopthruClient(
        auth=UserNamePasswordAuth(username="foo", password="bar"),
        agency_id=uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37"),
    )
    resp_actual = client.get_routes_summary(
        date(2021, 1, 1), date(2021, 1, 2), [1, 1, 0, 0, 0, 0, 0], None, False
    )

    assert resp_actual == resp_expected

    sent_request = httpretty.last_request()
    assert sent_request.url.endswith("/boardings/routes")


@httpretty.activate
def test_get_routes_summary_v2():
    register_login_url()

    agency_id = uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37")
    job_id = str(uuid.uuid4())

    resp_expected = {
        "data": {
            "id": job_id,
            "status": "finished",
            "updatedAt": "2021-05-02T12:37:05",
            "jobData": [
                {
                    "id": "1d1c63f1-512b-4e49-a243-30e159064175",
                    "gtfsId": "301",
                    "shortName": "101",
                    "nonGtfs": False,
                    "activity": {
                        "sumOns": 34759,
                        "sumOffs": 31152,
                        "sumActivity": 65911,
                        "avgOns": 1159,
                        "avgOffs": 1038,
                        "avgActivity": 2197,
                        "maxLoad": 55.0,
                        "avgLoad": 5.46,
                        "sumPassengerDistanceTravelled": 15856.65,
                        "avgPassengerDistanceTravelled": 528.55,
                        "boardingsPerRevenueHour": 9.96,
                    },
                }
            ],
        },
        "links": [],
    }

    httpretty.register_uri(
        httpretty.POST,
        f"https://api.hopthru.com/v2/agencies/{agency_id}/boardings/routes",
        responses=[
            httpretty.Response(
                body=json.dumps(resp_expected),
                status=200,
            ),
        ],
    )

    client = HopthruClient(
        auth=UserNamePasswordAuth(username="foo", password="bar"),
        agency_id=uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37"),
    )
    resp_actual = client.get_routes_summary_v2(
        date(2021, 1, 1), date(2021, 1, 2), [1, 1, 0, 0, 0, 0, 0], None
    )

    assert resp_actual == resp_expected

    sent_request = httpretty.last_request()
    assert sent_request.url.endswith(f"/v2/agencies/{agency_id}/boardings/routes")


@httpretty.activate
def test_get_route_shapes_v2():
    register_login_url()

    agency_id = uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37")
    job_id = str(uuid.uuid4())

    resp_expected = {
        "data": {
            "id": job_id,
            "status": "finished",
            "updatedAt": "2021-05-02T12:37:05",
            "jobData": [
                {
                    "tripMetaDataId": "15245597-NC2010-NCTD-Holiday1-11-1111111",
                    "lineString": {
                        "type": "LineString",
                        "coordinates": [
                            [-117.186116, 33.147743],
                            [-117.186384, 33.147962],
                        ],
                    },
                },
                {
                    "tripMetaDataId": "15245600-NC2010-NCTD-Holiday1-11-1111111",
                    "lineString": {
                        "type": "LineString",
                        "coordinates": [
                            [-117.318812, 33.109745],
                            [-117.318609, 33.10923],
                        ],
                    },
                },
            ],
            "links": [],
        }
    }

    httpretty.register_uri(
        httpretty.POST,
        f"https://api.hopthru.com/v2/agencies/{agency_id}/routes/shapes",
        responses=[
            httpretty.Response(
                body=json.dumps(resp_expected),
                status=200,
            ),
        ],
    )

    client = HopthruClient(
        auth=UserNamePasswordAuth(username="foo", password="bar"),
        agency_id=uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37"),
    )
    resp_actual = client.get_routes_shapes(
        date(2021, 1, 1), date(2021, 1, 2), [1, 1, 0, 0, 0, 0, 0], None
    )

    assert resp_actual == resp_expected

    sent_request = httpretty.last_request()
    assert sent_request.url.endswith(f"/v2/agencies/{agency_id}/routes/shapes")


@httpretty.activate
def test_get_route_load():
    register_login_url()

    first_resp_expected = {
        "status": "ok",
        "redis_id": "f48ed8e4-20c9-4c80-9b47-62fdd61a358c",
    }

    second_resp_expected = {"status": "started", "result": {}}

    final_resp_expected = {
        "status": "finished",
        "result": {
            "data": {
                "stops": {
                    "04d1aeef-2955-48e4-b907-b6ee8bcd3816_7b253155-871a-4408-9615-b6fb30834a9f": {
                        "id": "04d1aeef-2955-48e4-b907-b6ee8bcd3816_7b253155-871a-4408-9615-b6fb30834a9f",
                        "stop_id": "22073",
                        "stop_code": "22073",
                        "first": {
                            "maxload": 17.0,
                            "avg_load": 5.14,
                            "unexpanded_trip_count": 269,
                            "total_trip_count": 271,
                        },
                    }
                },
                "segments": [
                    {
                        "id": "deb87c62-0114-4ea4-a822-62c233bec5db_7110ce53-29d2-413e-bd3a-e72596fd5543",
                        "direction_id": 0,
                        "stop_segment": {
                            "type": "LineString",
                            "coordinates": [
                                [-117.292548, 33.045543],
                                [-117.292451, 33.044794],
                                [-117.293667, 33.044682],
                                [-117.294689, 33.051017],
                                [-117.29669008180888, 33.05423449178984],
                            ],
                        },
                        "stop_point": {
                            "type": "Point",
                            "coordinates": [-117.292548, 33.045543],
                        },
                        "stop_name": "Encinitas Station",
                        "stop_id": "deb87c62-0114-4ea4-a822-62c233bec5db",
                        "following_stop_point": {
                            "type": "Point",
                            "coordinates": [-117.29669008180888, 33.05423449178984],
                        },
                        "following_stop_name": "Highway 101 & Marcheta St",
                        "following_stop_id": "7110ce53-29d2-413e-bd3a-e72596fd5543",
                    }
                ],
            }
        },
    }

    httpretty.register_uri(
        httpretty.POST,
        "https://api.hopthru.com/boardings/routes/load",
        responses=[
            httpretty.Response(
                body=json.dumps(first_resp_expected),
                status=200,
            )
        ],
    )

    httpretty.register_uri(
        httpretty.GET,
        "https://api.hopthru.com/redis/status/f48ed8e4-20c9-4c80-9b47-62fdd61a358c",
        responses=[
            httpretty.Response(
                body=json.dumps(second_resp_expected),
                status=200,
            ),
            httpretty.Response(
                body=json.dumps(final_resp_expected),
                status=200,
            ),
        ],
    )

    client = HopthruClient(
        auth=UserNamePasswordAuth(username="foo", password="bar"),
        agency_id=uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37"),
    )
    resp_actual = client.get_route_load(
        uuid.UUID("1d1c63f1-512b-4e49-a243-30e159064175"),
        date(2021, 1, 1),
        date(2021, 1, 2),
        [1, 1, 0, 0, 0, 0, 0],
        None,
        None,
    )

    assert resp_actual == first_resp_expected

    sent_request = httpretty.last_request()
    assert sent_request.url.endswith("/boardings/routes/load")

    report_id = resp_actual["redis_id"]

    second_resp_actual = client.get_async_report_result(report_id)

    assert second_resp_actual == second_resp_expected

    final_resp_actual = client.get_async_report_result(report_id)

    assert final_resp_actual == final_resp_expected


@httpretty.activate
def test_get_route_load_v2():
    register_login_url()

    agency_id = uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37")
    route_id = uuid.UUID("e85c1169-06b0-4431-a608-c9f2994db4ca")
    job_id = str(uuid.uuid4())

    resp_expected = {
        "data": {
            "id": job_id,
            "status": "finished",
            "updatedAt": "2021-05-02T12:37:05",
            "jobData": [
                {
                    "id": str(uuid.uuid4()),
                    "followingId": str(uuid.uuid4()),
                    "gtfsId": "stop id 1",
                    "stopCode": "stop code 1",
                    "activity": {
                        "maxLoad": 3.00,
                        "avgLoad": 3.00,
                        "unexpandedTripCount": 0,
                        "totalTripCount": 0,
                    },
                }
            ],
        },
        "links": [],
    }

    httpretty.register_uri(
        httpretty.POST,
        f"https://api.hopthru.com/v2/agencies/{agency_id}/boardings/routes/{route_id}/load",
        responses=[
            httpretty.Response(
                body=json.dumps(resp_expected),
                status=200,
            ),
        ],
    )

    client = HopthruClient(
        auth=UserNamePasswordAuth(username="foo", password="bar"),
        agency_id=uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37"),
    )
    resp_actual = client.get_route_load_v2(
        route_id, date(2021, 1, 1), date(2021, 1, 2), [1, 1, 0, 0, 0, 0, 0], None, None
    )

    assert resp_actual == resp_expected

    sent_request = httpretty.last_request()
    assert sent_request.url.endswith(
        f"/v2/agencies/{agency_id}/boardings/routes/{route_id}/load"
    )


@httpretty.activate
def test_get_route_segments_v2():
    register_login_url()

    agency_id = uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37")
    route_id = uuid.UUID("e85c1169-06b0-4431-a608-c9f2994db4ca")
    job_id = str(uuid.uuid4())

    resp_expected = {
        "data": {
            "id": job_id,
            "status": "finished",
            "updatedAt": "2021-05-02T12:37:05",
            "jobData": [
                {
                    "id": str(uuid.uuid4()),
                    "followingId": str(uuid.uuid4()),
                    "gtfsId": "gtfs stop id",
                    "stopCode": "code 1",
                    "stopName": "name 1",
                    "direction": 1,
                    "stopSegment": {
                        "type": "LineString",
                        "coordinates": [
                            [-117.2736898089991, 33.12157206527434],
                            [-117.27359924832851, 33.11982499900424],
                        ],
                    },
                }
            ],
        },
        "links": [],
    }

    httpretty.register_uri(
        httpretty.POST,
        f"https://api.hopthru.com/v2/agencies/{agency_id}/routes/{route_id}/segments",
        responses=[
            httpretty.Response(
                body=json.dumps(resp_expected),
                status=200,
            ),
        ],
    )

    client = HopthruClient(
        auth=UserNamePasswordAuth(username="foo", password="bar"),
        agency_id=uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37"),
    )
    resp_actual = client.get_route_segments_v2(
        route_id, date(2021, 1, 1), date(2021, 1, 2), [1, 1, 0, 0, 0, 0, 0], None, None
    )

    assert resp_actual == resp_expected

    sent_request = httpretty.last_request()
    assert sent_request.url.endswith(
        f"/v2/agencies/{agency_id}/routes/{route_id}/segments"
    )


@httpretty.activate
def test_get_route_description():
    register_login_url()

    resp_expected = {
        "id": "81d080dd-2530-41a1-a740-a4fff3e31f4d",
        "route_id": "1762",
        "route_short_name": "1",
        "route_long_name": "Northgate – North Pointe – Horton Rd/Guess Rd",
        "hidden": False,
        "non_gtfs": False,
    }

    httpretty.register_uri(
        httpretty.GET,
        "https://api.hopthru.com/agencies/master/routes/81d080dd-2530-41a1-a740-a4fff3e31f4d/description",
        responses=[
            httpretty.Response(
                body=json.dumps(resp_expected),
                status=200,
            ),
        ],
    )

    client = HopthruClient(
        auth=UserNamePasswordAuth(username="foo", password="bar"),
        agency_id=uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37"),
    )
    resp_actual = client.get_route_description(
        uuid.UUID("81d080dd-2530-41a1-a740-a4fff3e31f4d"),
    )

    assert resp_actual == resp_expected

    sent_request = httpretty.last_request()
    assert sent_request.url.endswith("description")


@httpretty.activate
def test_get_route_trip_variants():
    register_login_url()

    resp_expected = [
        {
            "id": "398975d4cae71908273b6cd61829c569075dc0d4e77c0522f35bb4897c44647b",
            "direction": 0,
            "length": "28.79 mi",
            "stop_count": 69,
            "trip_count": 62,
        },
        {
            "id": "4b69f13f581fedcaf972a75c32e561d91c7039e7cb7b34fbec6dc1710fa8070c",
            "direction": 1,
            "length": "12.31 mi",
            "stop_count": 35,
            "trip_count": 1,
        },
    ]

    httpretty.register_uri(
        httpretty.POST,
        "https://api.hopthru.com/boardings/routes/1d1c63f1-512b-4e49-a243-30e159064175/trip_variants",
        responses=[
            httpretty.Response(
                body=json.dumps(resp_expected),
                status=200,
            ),
        ],
    )

    client = HopthruClient(
        auth=UserNamePasswordAuth(username="foo", password="bar"),
        agency_id=uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37"),
    )
    resp_actual = client.get_trip_variants(
        uuid.UUID("1d1c63f1-512b-4e49-a243-30e159064175"),
        date(2021, 1, 1),
        date(2021, 1, 2),
        [1, 1, 0, 0, 0, 0, 0],
        None,
    )

    assert resp_actual == resp_expected

    sent_request = httpretty.last_request()
    assert sent_request.url.endswith("variants")


@httpretty.activate
def test_get_route_trip_variants_v2():
    register_login_url()

    agency_id = uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37")
    route_id = uuid.UUID("e85c1169-06b0-4431-a608-c9f2994db4ca")
    job_id = str(uuid.uuid4())

    resp_expected = {
        "data": {
            "id": job_id,
            "status": "finished",
            "updatedAt": "2021-05-02T12:37:05",
            "jobData": [
                {
                    "id": str(uuid.uuid4()),
                    "direction": 0,
                    "length": "12.22 mi",
                    "stopCount": 37,
                    "tripCount": 2,
                },
            ],
        },
        "links": [],
    }

    httpretty.register_uri(
        httpretty.POST,
        f"https://api.hopthru.com/v2/agencies/{agency_id}/routes/{route_id}/trip_variants",
        responses=[
            httpretty.Response(
                body=json.dumps(resp_expected),
                status=200,
            ),
        ],
    )

    client = HopthruClient(
        auth=UserNamePasswordAuth(username="foo", password="bar"),
        agency_id=uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37"),
    )
    resp_actual = client.get_trip_variants_v2(
        route_id, date(2021, 1, 1), date(2021, 1, 2), [1, 1, 0, 0, 0, 0, 0], None, None
    )

    assert resp_actual == resp_expected

    sent_request = httpretty.last_request()
    assert sent_request.url.endswith(
        f"/v2/agencies/{agency_id}/routes/{route_id}/trip_variants"
    )


@httpretty.activate
def test_get_route_trips():
    register_login_url()

    resp_expected = {
        "trips": [
            {
                "ids": ["0059cc4c-db85-4325-b66d-9dfa711136a0"],
                "trip_id": "15349878-NC2104-NCTD-Saturday-05",
                "headsign": None,
                "variants": [
                    "4b69f13f581fedcaf972a75c32e561d91c7039e7cb7b34fbec6dc1710fa8070c"
                ],
                "direction": 1,
                "start_time": "08:41:00",
                "end_time": "10:24:00",
                "departure_time_next_day": False,
                "first": {
                    "sum_ons": 148,
                    "sum_offs": 133,
                    "sum_activity": 281,
                    "avg_ons": 21,
                    "avg_offs": 19,
                    "avg_activity": 40,
                    "maxload": 18,
                    "avg_load": 5,
                    "avg_passenger_distance_travelled": 7.32,
                    "sum_passenger_distance_travelled": 51.23,
                },
            }
        ]
    }

    httpretty.register_uri(
        httpretty.POST,
        "https://api.hopthru.com/v1/boardings/routes/1d1c63f1-512b-4e49-a243-30e159064175/trips",
        responses=[
            httpretty.Response(
                body=json.dumps(resp_expected),
                status=200,
            ),
        ],
    )

    client = HopthruClient(
        auth=UserNamePasswordAuth(username="foo", password="bar"),
        agency_id=uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37"),
    )
    resp_actual = client.get_route_trips(
        uuid.UUID("1d1c63f1-512b-4e49-a243-30e159064175"),
        date(2021, 1, 1),
        date(2021, 1, 2),
        [1, 1, 0, 0, 0, 0, 0],
        None,
    )

    assert resp_actual == resp_expected

    sent_request = httpretty.last_request()
    assert sent_request.url.endswith("trips")


@httpretty.activate
def test_get_route_trips_v2():
    register_login_url()

    agency_id = uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37")
    route_id = uuid.UUID("e85c1169-06b0-4431-a608-c9f2994db4ca")
    job_id = str(uuid.uuid4())

    resp_expected = {
        "data": {
            "id": job_id,
            "status": "finished",
            "updatedAt": "2021-05-02T12:37:05",
            "jobData": {
                "trips": [
                    {
                        "id": "5db38976-c23f-4603-9143-01606610d970",
                        "direction": 1,
                        "startTime": "06:36:00",
                        "departureTimeNextDay": False,
                        "variant": "0fae9bf001d130ed38945fcc7d8cb4101a44e7a982460011e4de94ee357c796d",
                        "activity": {
                            "sumOns": 0,
                            "sumOffs": 0,
                            "sumActivity": 0,
                            "avgOns": 0,
                            "avgOffs": 0,
                            "avgActivity": 0,
                            "maxLoad": 0.0,
                            "avgLoad": 0.0,
                            "avgPassengerDistanceTravelled": 0.0,
                            "sumPassengerDistanceTravelled": 0.0,
                        },
                    }
                ]
            },
        },
        "links": [],
    }

    httpretty.register_uri(
        httpretty.POST,
        f"https://api.hopthru.com/v2/agencies/{agency_id}/boardings/routes/{route_id}/trips",
        responses=[
            httpretty.Response(
                body=json.dumps(resp_expected),
                status=200,
            ),
        ],
    )

    client = HopthruClient(
        auth=UserNamePasswordAuth(username="foo", password="bar"),
        agency_id=uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37"),
    )
    resp_actual = client.get_route_trips_v2(
        route_id, date(2021, 1, 1), date(2021, 1, 2), [1, 1, 0, 0, 0, 0, 0], None
    )

    assert resp_actual == resp_expected

    sent_request = httpretty.last_request()
    assert sent_request.url.endswith(
        f"/v2/agencies/{agency_id}/boardings/routes/{route_id}/trips"
    )


@httpretty.activate
def test_get_route_trip():
    register_login_url()

    resp_expected = {
        "trip": {
            "ids": ["087c0131-02e6-49b6-864c-1524b5598846"],
            "variants": [
                "4b9fdbf90c0aa99922586770ce2f62e9e2713491b37523fa5953c1536f009033"
            ],
            "direction": 1,
            "start_time": "05:26:00",
            "departure_time_next_day": False,
            "first": {
                "sum_ons": 110,
                "sum_offs": 122,
                "sum_activity": 232,
                "avg_ons": 6,
                "avg_offs": 6,
                "avg_activity": 12,
                "maxload": 24,
                "avg_load": 3,
                "avg_passenger_distance_travelled": 21594.88,
                "sum_passenger_distance_travelled": 410302.75,
            },
        },
        "stops": [
            {
                "id": "6bc2b8fc-bb62-493c-82f4-c0634311afa8",
                "stop_id": "779677",
                "stop_code": "6272",
                "stop_name": "TW Alexander Dr at Miami Blvd (WB)",
                "stop_point": {"type": "Point", "coordinates": [-78.845353, 35.9239]},
                "first": {
                    "sum_ons": 7,
                    "sum_offs": 0,
                    "sum_activity": 7,
                    "avg_ons": 0,
                    "avg_offs": 0,
                    "avg_activity": 0,
                },
            }
        ],
    }

    httpretty.register_uri(
        httpretty.POST,
        "https://api.hopthru.com/v1/boardings/routes/1d1c63f1-512b-4e49-a243-30e159064175/trips:details",
        responses=[
            httpretty.Response(
                body=json.dumps(resp_expected),
                status=200,
            ),
        ],
    )

    client = HopthruClient(
        auth=UserNamePasswordAuth(username="foo", password="bar"),
        agency_id=uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37"),
    )
    resp_actual = client.get_route_trip(
        uuid.UUID("1d1c63f1-512b-4e49-a243-30e159064175"),
        uuid.UUID("087c0131-02e6-49b6-864c-1524b5598846"),
        date(2021, 1, 1),
        date(2021, 1, 2),
        [1, 1, 0, 0, 0, 0, 0],
        None,
    )

    assert resp_actual == resp_expected

    sent_request = httpretty.last_request()
    assert sent_request.url.endswith("trips:details")


@httpretty.activate
def test_get_route_trip_v2():
    register_login_url()

    agency_id = uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37")
    route_id = uuid.UUID("e85c1169-06b0-4431-a608-c9f2994db4ca")
    trip_id = uuid.UUID("0f6737f7-1d73-4ffd-84b3-702e9bb4a60b")
    job_id = str(uuid.uuid4())

    resp_expected = {
        "data": {
            "id": job_id,
            "status": "finished",
            "updatedAt": "2021-05-02T12:37:05",
            "jobData": {
                "trip": {
                    "id": str(trip_id),
                    "direction": 1,
                    "startTime": "16:29:00",
                    "departureTimeNextDay": False,
                    "variant": "egbreighreogrehtgore",
                    "activity": {
                        "sumOns": 10,
                        "sumOffs": 10,
                        "sumActivity": 20,
                        "avgOns": 10,
                        "avgOffs": 10,
                        "avgActivity": 20,
                        "maxLoad": 5.0,
                        "avgLoad": 1.94,
                        "avgPassengerDistanceTravelled": 28.01,
                        "sumPassengerDistanceTravelled": 28.01,
                    },
                },
                "stops": [],
            },
        },
        "links": [],
    }

    httpretty.register_uri(
        httpretty.POST,
        f"https://api.hopthru.com/v2/agencies/{agency_id}/boardings/routes/{route_id}/trips/{trip_id}",
        responses=[
            httpretty.Response(
                body=json.dumps(resp_expected),
                status=200,
            ),
        ],
    )

    client = HopthruClient(
        auth=UserNamePasswordAuth(username="foo", password="bar"),
        agency_id=uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37"),
    )
    resp_actual = client.get_route_trip_v2(
        route_id,
        trip_id,
        date(2021, 1, 1),
        date(2021, 1, 2),
        [1, 1, 0, 0, 0, 0, 0],
        None,
    )

    assert resp_actual == resp_expected

    sent_request = httpretty.last_request()
    assert sent_request.url.endswith(
        f"/v2/agencies/{agency_id}/boardings/routes/{route_id}/trips/{trip_id}"
    )


@httpretty.activate
def test_get_stops():
    register_login_url()

    first_resp_expected = {
        "status": "ok",
        "redis_id": "f48ed8e4-20c9-4c80-9b47-62fdd61a358c",
    }

    second_resp_expected = {"status": "started", "result": {}}

    final_resp_expected = {
        "status": "finished",
        "result": {
            "data": [
                {
                    "id": "003ddf36-7573-4d8a-8ea6-b21f2e85bdaa",
                    "stop_id": "25045",
                    "stop_code": "25045",
                    "stop_name": "Faraday Av & Van Allen Way",
                    "stop_point": '{ "type": "Point", "coordinates": [ -117.287902, 33.136617 ] }',
                    "first": {
                        "sum_ons": 2,
                        "sum_offs": 1,
                        "sum_activity": 3,
                        "avg_ons": 0,
                        "avg_offs": 0,
                        "avg_activity": 0,
                        "unexpanded_trip_count": 0,
                        "total_trip_count": 0,
                    },
                }
            ]
        },
    }

    httpretty.register_uri(
        httpretty.POST,
        "https://api.hopthru.com/boardings/stops",
        responses=[
            httpretty.Response(
                body=json.dumps(first_resp_expected),
                status=200,
            )
        ],
    )

    httpretty.register_uri(
        httpretty.GET,
        "https://api.hopthru.com/redis/status/f48ed8e4-20c9-4c80-9b47-62fdd61a358c",
        responses=[
            httpretty.Response(
                body=json.dumps(second_resp_expected),
                status=200,
            ),
            httpretty.Response(
                body=json.dumps(final_resp_expected),
                status=200,
            ),
        ],
    )

    client = HopthruClient(
        auth=UserNamePasswordAuth(username="foo", password="bar"),
        agency_id=uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37"),
    )
    resp_actual = client.get_stops(
        date(2021, 1, 1),
        date(2021, 1, 2),
        [1, 1, 0, 0, 0, 0, 0],
        None,
        True,
    )

    assert resp_actual == first_resp_expected

    sent_request = httpretty.last_request()
    assert sent_request.url.endswith("/boardings/stops")

    report_id = resp_actual["redis_id"]

    second_resp_actual = client.get_async_report_result(report_id)

    assert second_resp_actual == second_resp_expected

    final_resp_actual = client.get_async_report_result(report_id)

    assert final_resp_actual == final_resp_expected


@httpretty.activate
def test_get_stops_v2():
    register_login_url()

    agency_id = uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37")
    stop_id = uuid.UUID("e85c1169-06b0-4431-a608-c9f2994db4ca")
    job_id = str(uuid.uuid4())

    resp_expected = {
        "data": {
            "id": job_id,
            "status": "finished",
            "updatedAt": "2021-05-02T12:37:05",
            "jobData": [
                {
                    "id": str(stop_id),
                    "gtfsId": "12345",
                    "stopCode": "54321",
                    "stopName": "super stop a",
                    "stopPoint": {
                        "type": "Point",
                        "coordinates": [-117.249175, 33.1334],
                    },
                    "activity": {
                        "sumOns": 0,
                        "sumOffs": 2,
                        "sumActivity": 2,
                        "avgOns": 0,
                        "avgOffs": 1,
                        "avgActivity": 1,
                        "unexpandedTripCount": 1,
                        "totalTripCount": 2,
                    },
                }
            ],
        },
        "links": [],
    }

    httpretty.register_uri(
        httpretty.POST,
        f"https://api.hopthru.com/v2/agencies/{agency_id}/boardings/stops",
        responses=[
            httpretty.Response(
                body=json.dumps(resp_expected),
                status=200,
            ),
        ],
    )

    client = HopthruClient(
        auth=UserNamePasswordAuth(username="foo", password="bar"),
        agency_id=uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37"),
    )
    resp_actual = client.get_stops_v2(
        date(2021, 1, 1), date(2021, 1, 2), [1, 1, 0, 0, 0, 0, 0], None
    )

    assert resp_actual == resp_expected

    sent_request = httpretty.last_request()
    assert sent_request.url.endswith(f"/v2/agencies/{agency_id}/boardings/stops")


@httpretty.activate
def test_get_stop_description():
    register_login_url()

    resp_expected = {
        "data": {
            "id": "fe20a2aa-06a3-4848-912b-4a0704143736",
            "stop_id": "20730",
            "stop_code": "20730",
            "stop_name": "Mission Rd & Avenida Chapala",
            "stop_point": '{ "type": "Point", "coordinates": [ -117.131128, 33.136939 ] }',
            "routes": [
                {
                    "route_id": "bfb42f1f-f95e-4ae2-b7ee-15c2c681bc33",
                    "route_short_name": "305",
                }
            ],
        }
    }

    httpretty.register_uri(
        httpretty.POST,
        "https://api.hopthru.com/boardings/stops/description",
        responses=[
            httpretty.Response(
                body=json.dumps(resp_expected),
                status=200,
            ),
        ],
    )

    client = HopthruClient(
        auth=UserNamePasswordAuth(username="foo", password="bar"),
        agency_id=uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37"),
    )
    resp_actual = client.get_stop_description(
        uuid.UUID("fe20a2aa-06a3-4848-912b-4a0704143736"),
        date(2021, 1, 1),
        date(2021, 1, 2),
        [1, 1, 0, 0, 0, 0, 0],
        None,
    )

    assert resp_actual == resp_expected

    sent_request = httpretty.last_request()
    assert sent_request.url.endswith("description")


@httpretty.activate
def test_get_insight_result():
    register_login_url()

    agency_id = uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37")
    job_id = str(uuid.uuid4())

    resp_expected = {
        "data": {
            "id": job_id,
            "status": "finished",
            "updatedAt": "2021-05-02T12:37:05",
            "jobData": {
                "data": [
                    {
                        "avgOns": 5,
                        "sumOns": 111,
                        "avgOffs": 3,
                        "sumOffs": 70,
                        "avgActivity": 8,
                        "sumActivity": 181,
                        "maxLoad": 16,
                        "avgLoad": 1.62,
                        "avgMaxLoad": 6.535,
                        "sumPassengerDistanceTravelled": 0,
                        "avgPassengerDistanceTravelled": 0,
                        "boardingsPerRevenueHour": 0.01,
                    }
                ],
                "insight": {
                    "insightType": "system",
                    "dateRanges": [
                        {
                            "dateRangeType": "custom",
                            "startDate": date(2021, 1, 1).isoformat(),
                            "endDate": date(2021, 1, 2).isoformat(),
                            "days": [1, 1, 0, 0, 0, 0, 0],
                        }
                    ],
                    "hidden": False,
                    "isFavorited": False,
                    "isSubscribed": False,
                    "public": False,
                },
            },
        },
        "links": [],
    }

    httpretty.register_uri(
        httpretty.POST,
        f"https://api.hopthru.com/v1/agencies/{agency_id}/insights:run",
        responses=[
            httpretty.Response(
                body=json.dumps(resp_expected),
                status=200,
            ),
        ],
    )

    client = HopthruClient(
        auth=UserNamePasswordAuth(username="foo", password="bar"),
        agency_id=uuid.UUID("1dfa00fe-563f-48b6-8f6d-4101ba22fd37"),
    )
    resp_actual = client.get_insight_result(
        0,
        [
            {
                "dateRangeType": "custom",
                "startDate": date(2021, 1, 1).isoformat(),
                "endDate": date(2021, 1, 2).isoformat(),
                "days": [1, 1, 0, 0, 0, 0, 0],
            }
        ],
    )

    assert resp_actual == resp_expected

    sent_request = httpretty.last_request()
    assert sent_request.url.endswith(
        f"/v1/agencies/{agency_id}/insights:run?limit=5000&offset=0"
    )
