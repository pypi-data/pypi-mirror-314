from typing import List

from killbill.clients.base import BaseClient
from killbill.header import Header


class CreditClient(BaseClient):
    """Client for the Kill Bill credit API"""

    def add(
        self,
        header: Header,
        account_id: str,
        amount: int | float,
        currency: str,
        description: str = None,
        auto_commit: bool = False,
        plugin_property: List[str] = None,
    ):
        """Add a credit"""

        payload = [
            {
                "accountId": account_id,
                "description": description,
                "amount": amount,
                "currency": currency,
            }
        ]

        params = {
            "autoCommit": auto_commit,
            "pluginProperty": plugin_property,
        }

        response = self._post(
            "credits", headers=header.dict(), payload=payload, params=params
        )

        self._raise_for_status(response)

        return response.json()
