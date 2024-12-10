from typing import List
from urllib.parse import urlparse

import requests
from requests.exceptions import JSONDecodeError

from killbill.enums import Audit, ObjectType
from killbill.exceptions import AuthError, KillBillError, NotFoundError, UnknownError
from killbill.header import Header


class BaseClient:
    """Base class for the Kill Bill API client"""

    def __init__(
        self,
        username: str,
        password: str,
        api_url: str = "http://localhost:8080",
        timeout: int = 30,
    ):
        self.api_url = api_url
        self.username = username
        self.password = password
        self.timeout = timeout

    def _post(
        self,
        endpoint: str,
        headers: dict,
        payload: dict = None,
        data=None,
        params: dict = None,
    ):
        """Make a POST request to the Kill Bill API"""

        response = requests.post(
            f"{self.api_url}/1.0/kb/{endpoint}",
            json=payload,
            data=data,
            timeout=self.timeout,
            auth=(self.username, self.password),
            headers=headers,
            params=params,
        )
        return response

    def _delete(
        self,
        endpoint: str,
        headers: dict,
        payload: dict = None,
        data=None,
        params: dict = None,
    ):
        """Make a DELETE request to the Kill Bill API"""

        response = requests.delete(
            f"{self.api_url}/1.0/kb/{endpoint}",
            json=payload,
            data=data,
            timeout=self.timeout,
            auth=(self.username, self.password),
            headers=headers,
            params=params,
        )
        return response

    def _get(
        self,
        endpoint: str,
        headers: dict,
        payload: dict = None,
        params: dict = None,
    ):
        """Make a GET request to the Kill Bill API"""

        response = requests.get(
            f"{self.api_url}/1.0/kb/{endpoint}",
            json=payload,
            timeout=self.timeout,
            auth=(self.username, self.password),
            headers=headers,
            params=params,
        )
        return response

    def _put(
        self,
        endpoint: str,
        headers: dict,
        payload: dict = None,
        data=None,
        params: dict = None,
    ):
        """Make a POST request to the Kill Bill API"""

        response = requests.put(
            f"{self.api_url}/1.0/kb/{endpoint}",
            json=payload,
            data=data,
            timeout=self.timeout,
            auth=(self.username, self.password),
            headers=headers,
            params=params,
        )
        return response

    def _raise_for_status(self, response):
        """Raise an exception if the response status code is not 2xx"""

        status_code = response.status_code

        if status_code >= 400:

            if status_code == 401:
                raise AuthError

            if status_code == 404:
                raise NotFoundError

            # Try get error message from kill bill api
            error_message = None

            try:
                error_message = response.json().get("message")
            except JSONDecodeError:
                error_message = response.text

            if error_message:
                raise KillBillError(error_message)

            raise UnknownError

    def _get_uuid(self, url: str = None):
        """Return uuid from url location"""

        print(urlparse(url).path.split("/")[-1])

        if url:

            data = [p for p in urlparse(url).path.split("/") if p != ""]

            return data[-1]


class BaseClientWithCustomFields(BaseClient):
    """Base class for the Kill Bill custom fields apis"""

    def _add_custom_fields(
        self,
        header: Header,
        path: str,
        object_id: str,
        fields: dict,
        object_type: ObjectType,
    ):
        """Add custom fields to object"""

        payload = []

        for item in fields.items():
            payload.append(
                {
                    "objectType": str(object_type),
                    "name": item[0],
                    "value": item[1],
                }
            )

        response = self._post(
            f"{path}/{object_id}/customFields",
            headers=header.dict(),
            payload=payload,
        )

        self._raise_for_status(response)

    def _get_custom_fields(
        self,
        header: Header,
        path: str,
        object_id: str,
        audit: Audit = Audit.NONE,
    ):
        """Retrieve object custom fields"""

        params = {"audit": str(audit)}

        response = self._get(
            f"{path}/{object_id}/customFields",
            headers=header.dict(),
            params=params,
        )

        self._raise_for_status(response)

        return response.json()

    def _update_custom_fields(
        self,
        header: Header,
        path: str,
        object_id: str,
        fields: List[dict],
        object_type: ObjectType,
    ):
        """Modify custom fields to subscription"""

        if not isinstance(fields, (list, tuple)):
            raise TypeError("fields must be a list or tuple")

        for item in fields:
            if not isinstance(item, dict):
                raise TypeError("fields must be a list of dict")

            if not item.get("name"):
                raise ValueError("name is required")

            if not item.get("value"):
                raise ValueError("value is required")

            if not item.get("field_id"):
                raise ValueError("field_id is required")

        payload = []

        for item in fields:
            payload.append(
                {
                    "objectType": str(object_type),
                    "name": item.get("name"),
                    "value": item.get("value"),
                    "customFieldId": item.get("field_id"),
                }
            )

        response = self._put(
            f"{path}/{object_id}/customFields",
            headers=header.dict(),
            payload=payload,
        )

        self._raise_for_status(response)
