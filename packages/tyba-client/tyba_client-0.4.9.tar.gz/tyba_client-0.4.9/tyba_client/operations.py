import datetime
from datetime import date
from typing import Optional


class Operations(object):
    def __init__(self, client):
        self.client = client

    def get(self, route, params=None):
        response = self.client.get(f"operations/{route}", params=params)
        response.raise_for_status()
        return response.text

    def performance_report(
            self,
            start_date: date,
            end_date: date,
            asset_name: str,
    ):
        return self.get(
            "internal_api/performance_report",
            params={
                "start_date": start_date,
                "end_date": end_date,
                "asset_name": asset_name,
            },
        )

    def da_snapshot(
            self,
            start_date: date,
            end_date: date,
            asset_name: str,
    ):
        return self.get(
            "internal_api/da_snapshot",
            params={
                "start_date": start_date,
                "end_date": end_date,
                "asset_name": asset_name,
            },
        )

    def telemetry(
            self,
            start_date: date,
            end_date: date,
            asset_name: str,
            interval_mins: int,
            metrics: list[str]
    ):
        return self.get(
            "internal_api/telemetry",
            params={
                "start_date": start_date,
                "end_date": end_date,
                "asset_name": asset_name,
                "interval_mins": interval_mins,
                "metrics": metrics,
            },
        )

    def asset_details(
            self,
            asset_name: str,
            date: Optional[datetime.date] = None,
    ):
        params = {"asset_name": asset_name}
        if date is not None:
            params["date"] = date
        return self.get("internal_api/asset_details", params=params)

    def assets(
            self,
            org_id: Optional[str] = None,
    ):
        params = {"org_id": org_id} if org_id else {}
        return self.get("internal_api/assets", params=params)
