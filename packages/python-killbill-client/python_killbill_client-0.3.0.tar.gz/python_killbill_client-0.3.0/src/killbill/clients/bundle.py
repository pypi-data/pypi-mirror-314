from typing import List

from killbill.clients.base import BaseClientWithCustomFields
from killbill.enums import Audit, ObjectType
from killbill.header import Header


class BundleClient(BaseClientWithCustomFields):

    def list(
        self,
        header: Header,
        offset: int = 0,
        limit: int = 100,
        audit: Audit = Audit.NONE,
    ):
        """List bundles"""

        response = self._get(
            "bundles/pagination",
            headers=header.dict(),
            params={"offset": offset, "limit": limit, "audit": str(audit)},
        )

        self._raise_for_status(response)

        return response.json()

    def pause(self, header: Header, bundle_id: str, requested_date: str = None):
        """Pause a bundle"""

        response = self._put(
            f"bundles/{bundle_id}/pause",
            headers=header.dict(),
            params={"requestedDate": requested_date},
        )

        self._raise_for_status(response)

    def resume(self, header: Header, bundle_id: str, requested_date: str = None):
        """Resume a bundle"""

        response = self._put(
            f"bundles/{bundle_id}/resume",
            headers=header.dict(),
            params={"requestedDate": requested_date},
        )

        self._raise_for_status(response)

    def retrieve(self, header: Header, bundle_id: str, audit: Audit = Audit.NONE):
        """Retrieve a bundle by id"""

        params = {"audit": str(audit)}

        response = self._get(
            f"bundles/{bundle_id}", headers=header.dict(), params=params
        )

        self._raise_for_status(response)

        return response.json()

    def add_custom_fields(
        self,
        header: Header,
        bundle_id: str,
        fields: dict,
    ):
        """Add custom fields to bundle"""

        self._add_custom_fields(
            header,
            path="bundles",
            object_id=bundle_id,
            fields=fields,
            object_type=ObjectType.BUNDLE,
        )

    def get_custom_fields(
        self, header: Header, bundle_id: str, audit: Audit = Audit.NONE
    ):
        """Retrieve bunlde custom fields"""

        return self._get_custom_fields(
            header, path="bundles", object_id=bundle_id, audit=audit
        )

    def update_custom_fields(
        self,
        header: Header,
        bundle_id: str,
        fields: List[dict],
    ):
        """Modify custom fields to bundle

        Example:
        ```python
        killbill.bundle.update_custom_fields(
            header,
            bundle_id="bundle_id",
            fields=[
                {
                    "name": "name",
                    "value": "value",
                    "field_id": "field_id",
                }
            ],
        )

        ```
        """
        self._update_custom_fields(
            header,
            path="bundles",
            object_id=bundle_id,
            fields=fields,
            object_type=ObjectType.BUNDLE,
        )
