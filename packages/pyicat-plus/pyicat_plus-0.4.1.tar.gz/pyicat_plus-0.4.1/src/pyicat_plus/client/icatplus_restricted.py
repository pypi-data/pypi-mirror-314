import datetime
from typing import Optional, List
from urllib.parse import urljoin

import requests

from ..utils.url import normalize_url


class IcatPlusRestrictedClient:
    """Client for the restricted part of the ICAT+ REST API.

    REST API docs:
    https://icatplus.esrf.fr/api-docs/

    The ICAT+ server project:
    https://gitlab.esrf.fr/icat/icat-plus/-/blob/master/README.md
    """

    DEFAULT_SCHEME = "https"

    def __init__(self, url: str, password: Optional[str] = None):
        url = normalize_url(url, default_scheme=self.DEFAULT_SCHEME)

        path = "catalogue/{icat_session_id}/investigation"
        self.__investigation_url = urljoin(url, path)

        path = "tracking/{icat_session_id}/parcel"
        self.__parcel_url = urljoin(url, path)

        path = "session"
        self._authentication_url = urljoin(url, path)

        self._authentication_result = None
        if password:
            self.login(password)

    def login(self, password: str) -> dict:
        credentials = {"plugin": "esrf", "password": password}
        response = requests.post(self._authentication_url, json=credentials)
        response.raise_for_status()
        self._authentication_result = response.json()
        return self._authentication_result

    @property
    def authentication_result(self) -> dict:
        if not self._authentication_result:
            raise RuntimeError("Login is required.")
        return self._authentication_result

    @property
    def icat_session_id(self) -> str:
        return self.authentication_result["sessionId"]

    @property
    def _investigation_url(self) -> str:
        return self.__investigation_url.format(icat_session_id=self.icat_session_id)

    @property
    def _parcel_url(self) -> str:
        return self.__parcel_url.format(icat_session_id=self.icat_session_id)

    def get_investigations_by(
        self,
        filter: Optional[str] = None,
        instrument_name: Optional[str] = None,
        start_date: Optional[datetime.datetime] = None,
        end_date: Optional[datetime.datetime] = None,
    ) -> List[dict]:
        """Returns a list of investigations matching the provided criteria."""
        params = dict()
        if filter:
            params["filter"] = filter
        if instrument_name:
            params["instrumentName"] = instrument_name
        if start_date:
            params["startDate"] = start_date.strftime("%Y-%m-%d")
        if end_date:
            params["endDate"] = end_date.strftime("%Y-%m-%d")

        url = self._investigation_url
        if params:
            query = "&".join([f"{k}={v}" for k, v in params.items()])
            url = f"{url}?{query}"

        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_parcels_by(self, investigation_id: str) -> List[dict]:
        """Returns the list of parcels associated to an investigation."""
        url = f"{self._parcel_url}?investigation_id={investigation_id}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
