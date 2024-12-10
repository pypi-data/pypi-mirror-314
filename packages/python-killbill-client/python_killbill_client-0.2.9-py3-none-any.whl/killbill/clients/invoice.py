from killbill.clients.base import BaseClient
from killbill.enums import Audit
from killbill.header import Header


class InvoiceClient(BaseClient):
    """Client for the Kill Bill invoice API"""

    def retrieve(
        self,
        header: Header,
        invoice_id: str,
        with_children_items: bool = False,
        audit: Audit = Audit.NONE,
    ):
        """Retrieve an invoice by id"""

        params = {
            "withChildrenItems": with_children_items,
            "audit": str(audit),
        }

        response = self._get(
            f"invoices/{invoice_id}", headers=header.dict(), params=params
        )

        self._raise_for_status(response)

        return response.json()
