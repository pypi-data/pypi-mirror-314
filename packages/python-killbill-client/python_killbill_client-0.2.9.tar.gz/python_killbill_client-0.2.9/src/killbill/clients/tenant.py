from typing import Union

from killbill.clients.base import BaseClient
from killbill.header import Header


class TenantClient(BaseClient):
    """Client for the Kill Bill tenant API"""

    def create(
        self,
        api_key: str,
        api_secret: str,
        created_by: str,
        reason: str = None,
        comment: str = None,
    ) -> Union[str, None]:
        """Creates a new tenant.

        Returns:
            str or None: The tenant's ID or None if the request failed.
        """

        payload = {
            "apiKey": api_key,
            "apiSecret": api_secret,
        }

        response = self._post(
            "tenants",
            payload=payload,
            headers={
                "X-Killbill-CreatedBy": created_by,
                "X-Killbill-Reason": reason,
                "X-Killbill-Comment": comment,
            },
        )

        self._raise_for_status(response)

        return self._get_uuid(response.headers.get("Location"))

    def retrieve_configuration(self, header: Header):
        """Retrieve a per tenant configuration (system properties)"""

        response = self._get(
            "tenants/uploadPerTenantConfig",
            headers=header.dict(),
        )

        self._raise_for_status(response)

        return response.json()

    def add_configuration(self, header: Header, config: str):
        """Add a per tenant configuration (system properties)


        >> Example
        ```python
        killbill.tenant.add_configuration(
            header, config='{"org.killbill.payment.retry.days":"1,8,4,7"}'
        )
        ```
        """

        response = self._post(
            "tenants/uploadPerTenantConfig",
            data=config,
            headers=header.dict(),
        )

        self._raise_for_status(response)

    def delete_configuration(self, header: Header):
        """Delete a per tenant configuration (system properties)"""

        response = self._delete(
            "tenants/uploadPerTenantConfig",
            headers=header.dict(),
        )

        self._raise_for_status(response)

    def retrieve_push_notifications(self, header: Header):
        """Retrieve all push notification subscriptions for the tenant."""

        response = self._get(
            "tenants/registerNotificationCallback",
            headers=header.dict(),
        )

        self._raise_for_status(response)

        return response.json()

    def create_push_notification(self, header: Header, callback_url: str) -> None:
        """Create a new push notification subscription for the tenant.

        Args:
            header (Header): The authentication headers.
            callback_url (str): The callback URL for push notifications.
        """
        params = {
            "cb": callback_url,
        }

        response = self._post(
            "tenants/registerNotificationCallback",
            params=params,
            headers=header.dict(),
        )
        self._raise_for_status(response)

    def delete_push_notification(self, header: Header):
        """Delete all existing push notification subscription.

        Args:
            header (Header): The authentication headers.
        """
        response = self._delete(
            f"tenants/registerNotificationCallback/",
            headers=header.dict(),
        )

        self._raise_for_status(response)
