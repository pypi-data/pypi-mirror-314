from killbill.clients.base import BaseClient
from killbill.header import Header


class TestClient(BaseClient):
    """Client for the Kill Bill test API"""

    def clock(self, header: Header, requested_date: str):
        """Set the clock for the requested date"""

        params = {"requestedDate": requested_date}

        response = self._post("test/clock", params=params, headers=header.dict())

        self._raise_for_status(response)

    def retrieve_clock(self, header: Header):
        """Retrieve current clock"""

        response = self._get("test/clock", headers=header.dict())

        self._raise_for_status(response)

        return response.json()
