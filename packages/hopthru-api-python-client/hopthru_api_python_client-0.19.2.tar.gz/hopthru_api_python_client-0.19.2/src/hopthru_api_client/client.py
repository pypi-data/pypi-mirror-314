import json
import os
import requests
import uuid

from datetime import date
from typing import Dict, List, Optional, Union

from .types import (
    APCExtractionInterval,
    AgencyReportsConfig,
    ApiKeyAuth,
    DateRangeFileUploadGroup,
    DateRangeFileUploadDict,
    UserNamePasswordAuth,
    UploadDateDict,
)

HOPTHRU_API_URL = "https://api.hopthru.com"
HOPTHRU_PLATFORM_URL = "https://django-backend-prod.herokuapp.com"

DEFAULT_USE_EXPANDED_DATA = False
DEFAULT_SHOW_ATYPICAL_DAYS = False


class HopthruClient:
    def __init__(
        self,
        auth: Union[ApiKeyAuth, UserNamePasswordAuth],
        agency_id: Optional[uuid.UUID] = None,
        agency_reports_config: Optional[AgencyReportsConfig] = None,
        server_url: str = HOPTHRU_API_URL,
        session: Optional[requests.Session] = None,
    ):
        self.session = session or requests.Session()
        self.server_url = server_url
        self.headers = {}
        self.switch_agency(agency_id, agency_reports_config)
        self.set_auth(auth)

    def set_auth(self, auth: Union[ApiKeyAuth, UserNamePasswordAuth]) -> None:
        self.auth = auth
        if auth.get("api_key"):
            self.headers.update({"Authorization": f"Api-Key {auth['api_key']}"})
        else:
            access_token, _ = self.login(auth)
            self.headers.update({"Authorization": f"Bearer {access_token}"})

    def login(self, auth: UserNamePasswordAuth) -> [str, str]:
        url = f"{self.server_url}/api/token/"

        resp = self.session.post(
            url, json={"username": auth["username"], "password": auth["password"]}
        )
        resp.raise_for_status()

        return resp.json()["access"], resp.json()["refresh"]

    def switch_agency(
        self, agency_id: uuid.UUID, agency_reports_config: Optional[AgencyReportsConfig]
    ):
        self.agency_id = agency_id
        if agency_reports_config:
            self.agency_reports_config = agency_reports_config
        else:
            self.agency_reports_config = AgencyReportsConfig(
                use_expanded_data=DEFAULT_USE_EXPANDED_DATA,
                show_atypical_days=DEFAULT_SHOW_ATYPICAL_DAYS,
            )

    def get_apc_data_extraction_interval(self) -> APCExtractionInterval:
        """
        Requests the time interval for which each APC data file should contain.
        At present, this is either weekly or monthly.
        """
        url = f"{self.server_url}/data/interval"
        response = self.session.get(url, headers=self.headers)
        response.raise_for_status()
        interval = response.json()
        return (
            APCExtractionInterval.MONTHLY
            if interval == "Monthly"
            else APCExtractionInterval.WEEKLY
        )

    def get_desired_apc_data_dates(self) -> List[UploadDateDict]:
        """
        Requests the a list of date ranges of APC data (correlated or raw) that should be uploaded to Hopthru.
        """
        url = f"{self.server_url}/data/upload_dates"
        response = self.session.get(url, headers=self.headers)
        response.raise_for_status()
        ranges = response.json()

        return [
            UploadDateDict(
                start_date=date.fromisoformat(r["start_date"]),
                end_date=date.fromisoformat(r["end_date"]),
            )
            for r in ranges
        ]

    def upload_correlated_apc_data(
        self,
        filepaths: List[str],
        start_date: date,
        end_date: date,
        metadata: Optional[dict],
    ) -> None:
        """
        Upload a file of already correlated APC data to Hopthru.

        Correlated files are expected to be groups of at most one file.
        So, upload them one by one.
        """
        self.upload_group_of_files(
            group_type="correlated_apc",
            filepaths=filepaths,
            start_date=start_date,
            end_date=end_date,
            metadata=metadata,
        )

    def create_file_upload_group(
        self,
        filepaths: List[str],
        group_type: str,
        start_date: date,
        end_date: date,
        metadata: Optional[dict],
    ) -> DateRangeFileUploadGroup:
        """
        Upload a file of already correlated APC data to Hopthru.
        """
        url = f"{self.server_url}/v1/date-range-file-uploads-groups"
        request_params = {
            "groupType": group_type,
            "startDate": start_date.isoformat(),
            "endDate": end_date.isoformat(),
            "hasManyItems": len(filepaths) > 1,
            "metadata": metadata,
        }
        response = self.session.post(url, headers=self.headers, json=request_params)
        response.raise_for_status()
        return DateRangeFileUploadGroup(**response.json())

    def add_file_upload_to_group(
        self,
        group_id: uuid.UUID,
        filepath: str,
    ) -> DateRangeFileUploadDict:
        """
        Upload a file of already correlated APC data to Hopthru.
        """
        url = f"{self.server_url}/v1/date-range-file-uploads-groups/{group_id}/date-range-file-uploads"
        request_params = {
            "filename": os.path.basename(filepath),
        }
        response = self.session.post(url, headers=self.headers, json=request_params)
        response.raise_for_status()
        return DateRangeFileUploadDict(**response.json())

    def update_file_upload_group(
        self,
        group_id: uuid.UUID,
        status: str,
    ) -> DateRangeFileUploadGroup:
        """
        Upload a file of already correlated APC data to Hopthru.
        """
        url = f"{self.server_url}/v1/date-range-file-uploads-groups/{group_id}"
        request_params = {
            "status": status,
        }
        response = self.session.put(url, headers=self.headers, json=request_params)
        response.raise_for_status()
        return DateRangeFileUploadGroup(**response.json())

    def upload_group_of_files(
        self,
        group_type: str,
        filepaths: List[str],
        start_date: date,
        end_date: date,
        metadata: Optional[dict],
    ) -> None:

        group = self.create_file_upload_group(
            filepaths=filepaths,
            group_type=group_type,
            start_date=start_date,
            end_date=end_date,
            metadata=metadata,
        )

        for filepath in filepaths:
            file_upload_params = self.add_file_upload_to_group(group["id"], filepath)

            with open(filepath, "rb") as fd:
                form_data = file_upload_params["uploadFormFields"]
                files = {"file": fd}
                response = self.session.post(
                    file_upload_params["uploadUrl"],
                    data=form_data,
                    files=files,
                )
                response.raise_for_status()
        self.update_file_upload_group(group["id"], "files_received")

    def upload_raw_apc_data(
        self,
        filepaths: List[str],
        start_date: date,
        end_date: date,
        metadata: Optional[dict],
    ) -> None:
        self.upload_group_of_files(
            group_type="raw_apc",
            filepaths=filepaths,
            start_date=start_date,
            end_date=end_date,
            metadata=metadata,
        )

    def get_me(self) -> Dict:
        url = f"{self.server_url}/me"
        resp = self.session.get(url, headers=self.headers)
        resp.raise_for_status()

        return resp.json()

    def get_time_ranges(self) -> List[Dict]:
        url = f"{self.server_url}/agencies/timeranges"

        req_payload = {"agency_id": str(self.agency_id)}

        resp = self.session.post(url, headers=self.headers, json=req_payload)
        resp.raise_for_status()

        return resp.json()

    def get_legacy_boardings_report(
        self,
        report: str,
        start_date: date,
        end_date: date,
        days: List[int],
        time_range: Optional[uuid.UUID],
        route_ids: Optional[List[uuid.UUID]] = None,
        trip_ids: Optional[List[uuid.UUID]] = None,
        stop_ids: Optional[List[uuid.UUID]] = None,
        request_args: Optional[Dict] = None,
        path_override: Optional[str] = None,
    ) -> Dict:
        url = self.server_url
        url = url + (f"/boardings/{report}" if path_override is None else path_override)

        date_range_args = {
            "startDate": start_date.isoformat(),
            "endDate": end_date.isoformat(),
            "days": days,
            "expanded": self.agency_reports_config["use_expanded_data"],
            "include_atypical_days": self.agency_reports_config["show_atypical_days"],
        }
        date_range_args["timeRange"] = str(time_range) if time_range is not None else ""
        if route_ids is not None:
            date_range_args["routeIds"] = [str(route_id) for route_id in route_ids]
        if trip_ids is not None:
            date_range_args["tripIds"] = [str(trip_id) for trip_id in trip_ids]
        if stop_ids is not None:
            date_range_args["stopIds"] = [str(stop_id) for stop_id in stop_ids]

        if request_args is not None and "firstDateRange" in request_args:
            date_range_args.update(request_args["firstDateRange"])
            request_args.pop("firstDateRange")

        req_payload = {
            "agency_id": str(self.agency_id),
            "firstDateRange": json.dumps(date_range_args),
        }
        if request_args is not None:
            req_payload.update(request_args)

        resp = self.session.post(url, headers=self.headers, json=req_payload)
        try:
            resp.raise_for_status()
        except requests.HTTPError as e:
            if e.response.status_code == 400:
                raise Exception("HTTP 400: " + resp.text)
            raise

        return resp.json()

    def get_report(
        self,
        path: str,
        start_date: date,
        end_date: date,
        days: List[int],
        time_range: Optional[uuid.UUID],
        route_ids: Optional[List[uuid.UUID]] = None,
        trip_ids: Optional[List[uuid.UUID]] = None,
        stop_ids: Optional[List[uuid.UUID]] = None,
        request_args: Optional[Dict] = None,
    ) -> Dict:
        url = f"{self.server_url}{path}"

        date_range_args = {
            "startDate": start_date.isoformat(),
            "endDate": end_date.isoformat(),
            "days": days,
            "expanded": self.agency_reports_config["use_expanded_data"],
            "include_atypical_days": self.agency_reports_config["show_atypical_days"],
        }

        if time_range is not None:
            date_range_args["timeRange"] = str(time_range)

        if route_ids is not None:
            date_range_args["routeIds"] = [str(route_id) for route_id in route_ids]
        if trip_ids is not None:
            date_range_args["tripIds"] = [str(trip_id) for trip_id in trip_ids]
        if stop_ids is not None:
            date_range_args["stopIds"] = [str(stop_id) for stop_id in stop_ids]

        if request_args is not None and "firstDateRange" in request_args:
            date_range_args.update(request_args["firstDateRange"])
            request_args.pop("firstDateRange")

        req_payload = {
            "agency_id": str(self.agency_id),
            "firstDateRange": date_range_args,
        }
        if request_args is not None:
            req_payload.update(request_args)

        resp = self.session.post(url, headers=self.headers, json=req_payload)
        resp.raise_for_status()

        return resp.json()

    def get_report_v2(
        self,
        path: str,
        start_date: date,
        end_date: date,
        days: List[int],
        time_range: Optional[uuid.UUID],
        route_ids: Optional[List[uuid.UUID]] = None,
        trip_ids: Optional[List[uuid.UUID]] = None,
        stop_ids: Optional[List[uuid.UUID]] = None,
        request_args: Optional[Dict] = None,
    ) -> Dict:
        url = f"{self.server_url}{path}"

        date_range_args = {
            "startDate": start_date.isoformat(),
            "endDate": end_date.isoformat(),
            "days": days,
            "expanded": self.agency_reports_config["use_expanded_data"],
            "include_atypical_days": self.agency_reports_config["show_atypical_days"],
        }

        if time_range is not None:
            date_range_args["timeRange"] = str(time_range)

        if route_ids is not None:
            date_range_args["routeIds"] = [str(route_id) for route_id in route_ids]
        if trip_ids is not None:
            date_range_args["tripIds"] = [str(trip_id) for trip_id in trip_ids]
        if stop_ids is not None:
            date_range_args["stopIds"] = [str(stop_id) for stop_id in stop_ids]

        if request_args is not None and "dateRange" in request_args:
            date_range_args.update(request_args["dateRange"])
            request_args.pop("dateRange")

        req_payload = {
            "dateRange": date_range_args,
        }
        if request_args is not None:
            req_payload.update(request_args)

        resp = self.session.post(url, headers=self.headers, json=req_payload)
        resp.raise_for_status()

        return resp.json()

    def get_insight_result(
        self,
        group_by: int,
        date_ranges: List[Dict],
        filters: Optional[List[Dict]] = None,
        limit: Optional[int] = 5000,
        offset: Optional[int] = 0,
    ) -> Dict:
        url = f"{self.server_url}/v1/agencies/{self.agency_id}/insights:run?limit={limit}&offset={offset}"

        insight = {
            "agencyId": str(self.agency_id),
            "dateRanges": date_ranges,
            "expanded": self.agency_reports_config["use_expanded_data"],
        }

        if filters is not None:
            insight["filters"] = filters

        resp = self.session.post(url, headers=self.headers, json=insight)
        resp.raise_for_status()

        return resp.json()

    def get_async_report_result(self, report_id: uuid.UUID) -> Dict:
        url = f"{self.server_url}/redis/status/{report_id}"
        resp = self.session.get(url, headers=self.headers)
        resp.raise_for_status()

        return resp.json()

    def get_system(
        self,
        start_date: date,
        end_date: date,
        days: List[int],
        time_range_id: Optional[uuid.UUID],
        route_ids: Optional[List[uuid.UUID]] = None,
        stop_ids: Optional[List[uuid.UUID]] = None,
    ) -> Dict:
        return self.get_legacy_boardings_report(
            "system", start_date, end_date, days, time_range_id, route_ids, stop_ids
        )

    def get_system_v2(
        self,
        start_date: date,
        end_date: date,
        days: List[int],
        time_range_id: Optional[uuid.UUID],
        route_ids: Optional[List[uuid.UUID]] = None,
        stop_ids: Optional[List[uuid.UUID]] = None,
    ) -> Dict:
        return self.get_report_v2(
            path=f"/v2/agencies/{self.agency_id}/boardings/system",
            start_date=start_date,
            end_date=end_date,
            days=days,
            time_range=time_range_id,
            route_ids=route_ids,
            stop_ids=stop_ids,
        )

    def get_dates(
        self,
        start_date: date,
        end_date: date,
        days: List[int],
        time_range_id: Optional[uuid.UUID],
        route_ids: Optional[List[uuid.UUID]] = None,
        stop_ids: Optional[List[uuid.UUID]] = None,
    ) -> Dict:
        return self.get_legacy_boardings_report(
            "dates", start_date, end_date, days, time_range_id, route_ids, stop_ids
        )

    def get_dates_v2(
        self,
        start_date: date,
        end_date: date,
        days: List[int],
        time_range_id: Optional[uuid.UUID],
        route_ids: Optional[List[uuid.UUID]] = None,
        stop_ids: Optional[List[uuid.UUID]] = None,
    ) -> Dict:
        return self.get_report_v2(
            path=f"/v2/agencies/{self.agency_id}/boardings/dates",
            start_date=start_date,
            end_date=end_date,
            days=days,
            time_range=time_range_id,
            route_ids=route_ids,
            stop_ids=stop_ids,
        )

    def get_days(
        self,
        start_date: date,
        end_date: date,
        days: List[int],
        time_range_id: Optional[uuid.UUID],
        route_ids: Optional[List[uuid.UUID]] = None,
        stop_ids: Optional[List[uuid.UUID]] = None,
    ) -> Dict:
        return self.get_legacy_boardings_report(
            "days", start_date, end_date, days, time_range_id, route_ids, stop_ids
        )

    def get_days_v2(
        self,
        start_date: date,
        end_date: date,
        days: List[int],
        time_range_id: Optional[uuid.UUID],
        route_ids: Optional[List[uuid.UUID]] = None,
        stop_ids: Optional[List[uuid.UUID]] = None,
    ) -> Dict:
        return self.get_report_v2(
            path=f"/v2/agencies/{self.agency_id}/boardings/days",
            start_date=start_date,
            end_date=end_date,
            days=days,
            time_range=time_range_id,
            route_ids=route_ids,
            stop_ids=stop_ids,
        )

    def get_periods(
        self,
        start_date: date,
        end_date: date,
        days: List[int],
        time_range_id: Optional[uuid.UUID],
        route_ids: Optional[List[uuid.UUID]] = None,
        stop_ids: Optional[List[uuid.UUID]] = None,
    ) -> Dict:
        return self.get_legacy_boardings_report(
            "periods", start_date, end_date, days, time_range_id, route_ids, stop_ids
        )

    def get_periods_v2(
        self,
        start_date: date,
        end_date: date,
        days: List[int],
        time_range_id: uuid.UUID,
        route_ids: Optional[List[uuid.UUID]] = None,
        stop_ids: Optional[List[uuid.UUID]] = None,
    ) -> Dict:
        return self.get_report_v2(
            f"/v2/agencies/{self.agency_id}/boardings/periods/{time_range_id}",
            start_date,
            end_date,
            days,
            time_range_id,
            route_ids,
            stop_ids,
        )

    def get_routes_list(
        self,
        start_date: date,
        end_date: date,
        days: List[int],
        time_range_id: Optional[uuid.UUID],
    ) -> Dict:
        return self.get_legacy_boardings_report(
            "routes/list", start_date, end_date, days, time_range_id
        )

    def get_routes_summary(
        self,
        start_date: date,
        end_date: date,
        days: List[int],
        time_range_id: Optional[uuid.UUID],
        request_shapes: bool,
    ) -> Dict:
        return self.get_legacy_boardings_report(
            "routes",
            start_date,
            end_date,
            days,
            time_range_id,
            request_args={"request_shapes": request_shapes},
        )

    def get_routes_summary_v2(
        self,
        start_date: date,
        end_date: date,
        days: List[int],
        time_range_id: Optional[uuid.UUID],
    ) -> Dict:
        return self.get_report_v2(
            f"/v2/agencies/{self.agency_id}/boardings/routes",
            start_date,
            end_date,
            days,
            time_range_id,
        )

    def get_routes_shapes(
        self,
        start_date: date,
        end_date: date,
        days: List[int],
        time_range_id: Optional[uuid.UUID],
    ) -> Dict:
        return self.get_report_v2(
            f"/v2/agencies/{self.agency_id}/routes/shapes",
            start_date,
            end_date,
            days,
            time_range_id,
        )

    def get_route_details(
        self,
        route_id: uuid.UUID,
        start_date: date,
        end_date: date,
        days: List[int],
        time_range_id: Optional[uuid.UUID],
        trip_id: Optional[uuid.UUID],
    ) -> Dict:
        return self.get_legacy_boardings_report(
            "routes/details",
            start_date,
            end_date,
            days,
            time_range_id,
            route_ids=[route_id],
            trip_ids=[trip_id] if trip_id is not None else None,
        )

    def get_route_details_v2(
        self,
        route_id: uuid.UUID,
        start_date: date,
        end_date: date,
        days: List[int],
        time_range_id: Optional[uuid.UUID],
        trip_id: Optional[uuid.UUID],
    ) -> Dict:
        return self.get_report_v2(
            path=f"/v2/agencies/{self.agency_id}/boardings/routes/{route_id}",
            start_date=start_date,
            end_date=end_date,
            days=days,
            time_range=time_range_id,
            trip_ids=[trip_id] if trip_id is not None else None,
        )

    def get_route_load(
        self,
        route_id: uuid.UUID,
        start_date: date,
        end_date: date,
        days: List[int],
        time_range_id: Optional[uuid.UUID],
        trip_id: Optional[uuid.UUID],
    ) -> Dict:
        return self.get_legacy_boardings_report(
            "routes/load",
            start_date,
            end_date,
            days,
            time_range_id,
            route_ids=[route_id],
            trip_ids=[trip_id] if trip_id is not None else None,
        )

    def get_route_load_v2(
        self,
        route_id: uuid.UUID,
        start_date: date,
        end_date: date,
        days: List[int],
        time_range_id: Optional[uuid.UUID],
        trip_id: Optional[uuid.UUID],
    ) -> Dict:
        return self.get_report_v2(
            path=f"/v2/agencies/{self.agency_id}/boardings/routes/{route_id}/load",
            start_date=start_date,
            end_date=end_date,
            days=days,
            time_range=time_range_id,
            trip_ids=[trip_id] if trip_id is not None else None,
        )

    def get_route_segments_v2(
        self,
        route_id: uuid.UUID,
        start_date: date,
        end_date: date,
        days: List[int],
        time_range_id: Optional[uuid.UUID],
        trip_id: Optional[uuid.UUID],
    ) -> Dict:
        return self.get_report_v2(
            path=f"/v2/agencies/{self.agency_id}/routes/{route_id}/segments",
            start_date=start_date,
            end_date=end_date,
            days=days,
            time_range=time_range_id,
            trip_ids=[trip_id] if trip_id is not None else None,
        )

    def get_route_description(self, route_id: uuid.UUID) -> Dict:
        url = f"{self.server_url}/agencies/master/routes/{route_id}/description"
        resp = self.session.get(url, headers=self.headers)
        resp.raise_for_status()

        return resp.json()

    def get_trip_variants(
        self,
        route_id: uuid.UUID,
        start_date: date,
        end_date: date,
        days: List[int],
        time_range_id: Optional[uuid.UUID],
        trip_id: Optional[uuid.UUID] = None,
    ) -> Dict:
        return self.get_report(
            f"/boardings/routes/{route_id}/trip_variants",
            start_date,
            end_date,
            days,
            time_range_id,
            trip_ids=[trip_id] if trip_id is not None else None,
        )

    def get_trip_variants_v2(
        self,
        route_id: uuid.UUID,
        start_date: date,
        end_date: date,
        days: List[int],
        time_range_id: Optional[uuid.UUID],
        trip_id: Optional[uuid.UUID] = None,
    ) -> Dict:
        return self.get_report_v2(
            path=f"/v2/agencies/{self.agency_id}/routes/{route_id}/trip_variants",
            start_date=start_date,
            end_date=end_date,
            days=days,
            time_range=time_range_id,
            trip_ids=[trip_id] if trip_id is not None else None,
        )

    def get_route_trips(
        self,
        route_id: uuid.UUID,
        start_date: date,
        end_date: date,
        days: List[int],
        time_range_id: Optional[uuid.UUID],
    ) -> Dict:
        return self.get_report(
            f"/v1/boardings/routes/{route_id}/trips",
            start_date,
            end_date,
            days,
            time_range_id,
        )

    def get_route_trips_v2(
        self,
        route_id: uuid.UUID,
        start_date: date,
        end_date: date,
        days: List[int],
        time_range_id: Optional[uuid.UUID],
    ) -> Dict:
        return self.get_report_v2(
            path=f"/v2/agencies/{self.agency_id}/boardings/routes/{route_id}/trips",
            start_date=start_date,
            end_date=end_date,
            days=days,
            time_range=time_range_id,
        )

    def get_route_trip(
        self,
        route_id: uuid.UUID,
        trip_id: uuid.UUID,
        start_date: date,
        end_date: date,
        days: List[int],
        time_range_id: Optional[uuid.UUID],
    ) -> Dict:
        return self.get_report(
            f"/v1/boardings/routes/{route_id}/trips:details",
            start_date,
            end_date,
            days,
            time_range_id,
            request_args={"trip_ids": [str(trip_id)]},
        )

    def get_route_trip_v2(
        self,
        route_id: uuid.UUID,
        trip_id: uuid.UUID,
        start_date: date,
        end_date: date,
        days: List[int],
        time_range_id: Optional[uuid.UUID],
    ) -> Dict:
        return self.get_report_v2(
            path=f"/v2/agencies/{self.agency_id}/boardings/routes/{route_id}/trips/{trip_id}",
            start_date=start_date,
            end_date=end_date,
            days=days,
            time_range=time_range_id,
        )

    def get_stops(
        self,
        start_date: date,
        end_date: date,
        days: List[int],
        time_range_id: Optional[uuid.UUID],
        request_shapes: bool,
    ) -> Dict:
        return self.get_legacy_boardings_report(
            "stops",
            start_date,
            end_date,
            days,
            time_range_id,
            None,
            request_args={"request_shapes": request_shapes},
        )

    def get_stops_v2(
        self,
        start_date: date,
        end_date: date,
        days: List[int],
        time_range_id: Optional[uuid.UUID],
    ) -> Dict:
        return self.get_report_v2(
            path=f"/v2/agencies/{self.agency_id}/boardings/stops",
            start_date=start_date,
            end_date=end_date,
            days=days,
            time_range=time_range_id,
        )

    def get_stop_description(
        self,
        stop_id: uuid.UUID,
        start_date: date,
        end_date: date,
        days: List[int],
        time_range_id: Optional[uuid.UUID],
    ) -> Dict:
        return self.get_legacy_boardings_report(
            "stops/description",
            start_date,
            end_date,
            days,
            time_range_id,
            None,
            stop_ids=[stop_id],
        )
