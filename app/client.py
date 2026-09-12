"""
Adapter layer talking to the legacy Urja Meter Ops portal.

THIS FILE IS INTENTIONALLY A SKELETON.
Fill in the TODOs after completing DevTools reconnaissance (see PROTOCOL.md).
Do not guess field names/selectors - confirm them against real responses.
"""
import httpx
from bs4 import BeautifulSoup
from typing import Optional
from datetime import datetime, timezone

from app.config import settings


class SessionExpiredError(Exception):
    pass


class UrjaPortalClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.client = httpx.Client(
            timeout=settings.REQUEST_TIMEOUT,
            follow_redirects=True,
        )
        self._authenticated = False
        self._last_login_at: Optional[datetime] = None

    def login(self, username: str, password: str) -> bool:
        login_url = f"{self.base_url}{settings.LOGIN_PATH}"

        payload = {"email": username, "password": password}
        headers = {
            "Origin": self.base_url,
            "Referer": login_url
        }

        response = self.client.post(login_url, data=payload, headers=headers)

        ok = response.status_code in (200, 302) and (
            settings.SESSION_COOKIE_NAME in self.client.cookies
            or response.status_code == 302
        )
        self._authenticated = ok
        if ok:
            self._last_login_at = datetime.now(timezone.utc)
        return ok

    def _ensure_authenticated(self):
        if not self._authenticated:
            if not self.login(settings.URJA_USERNAME, settings.URJA_PASSWORD):
                raise SessionExpiredError("Could not authenticate with Urja portal")

    def _get(self, path: str) -> httpx.Response:
        self._ensure_authenticated()
        url = f"{self.base_url}{path}"
        response = self.client.get(url)

        if response.status_code == 401 or (
            response.status_code in (302, 303) and "login" in response.headers.get("location", "")
        ):
            # Session expired mid-flight -> re-auth once and retry
            self._authenticated = False
            self._ensure_authenticated()
            response = self.client.get(url)

        return response

    def list_meters(self) -> list[dict]:
        """
        TODO: confirm real path. Try /api/v1/meters first (check Network tab
        for XHR/fetch calls); fall back to scraping /meters HTML listing page.
        """
        response = self._get("/meters")

        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type:
            return response.json()

        # HTML fallback: parse table rows
        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.select("table tbody tr")  # TODO: confirm real selector
        meters = []
        for row in rows:
            cells = [c.get_text(strip=True) for c in row.find_all("td")]
            if cells:
                meters.append({"raw_cells": cells})  # TODO: map to real fields
        return meters

    def get_meter_details(self, meter_id: str) -> dict:
        response = self._get(f"/meters/{meter_id}")

        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type:
            return response.json()

        soup = BeautifulSoup(response.text, "html.parser")
        serial_elem = soup.find("span", {"id": "meter-serial"})  # TODO: confirm
        status_elem = soup.find("td", {"class": "status-value"})  # TODO: confirm

        return {
            "meter_id": meter_id,
            "serial_number": serial_elem.text.strip() if serial_elem else None,
            "status": status_elem.text.strip() if status_elem else None,
        }

    def get_consumption(self, meter_id: str) -> list[dict]:
        response = self._get(f"/meters/{meter_id}/consumption")  # TODO: confirm path

        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type:
            return response.json()

        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.select("table tbody tr")  # TODO: confirm selector
        points = []
        for row in rows:
            cells = [c.get_text(strip=True) for c in row.find_all("td")]
            if len(cells) >= 2:
                points.append({"timestamp_raw": cells[0], "value_raw": cells[1]})
        return points

    @staticmethod
    def normalize_numeric(value: str) -> Optional[float]:
        """Convert '124.50' or '1,245.50 kWh' style strings to float."""
        if value is None:
            return None
        cleaned = value.replace(",", "").replace("kWh", "").strip()
        try:
            return float(cleaned)
        except ValueError:
            return None
