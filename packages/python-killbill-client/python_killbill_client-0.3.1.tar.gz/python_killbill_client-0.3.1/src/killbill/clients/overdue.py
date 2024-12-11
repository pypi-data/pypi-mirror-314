from killbill.clients.base import BaseClient
from killbill.header import Header


class OverdueClient(BaseClient):
    """Client for the Kill Bill overdue API"""

    def retrieve(self, header: Header, xml: bool = True):
        """Retrieve overdue config

        if `xml = True`, returns the XML representation of the overdue config

        if `xml = False`, returns the JSON representation of the overdue config
        """

        response = self._get(
            "overdue/xml" if xml else "overdue",
            headers=header.dict(),
        )

        self._raise_for_status(response)

        return response.text if xml else response.json()

    def upload(self, header: Header, overdue_config_xml: str):
        """Upload overdue config

        Args:
            overdue_config_xml (str): XML representation of the overdue config
        """

        response = self._post(
            "overdue/xml",
            data=overdue_config_xml,
            headers=header.dict(),
        )

        self._raise_for_status(response)
