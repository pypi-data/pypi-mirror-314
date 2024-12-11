from killbill.clients.account import AccountClient
from killbill.clients.bundle import BundleClient
from killbill.clients.catalog import CatalogClient
from killbill.clients.credit import CreditClient
from killbill.clients.invoice import InvoiceClient
from killbill.clients.overdue import OverdueClient
from killbill.clients.subscription import SubscriptionClient
from killbill.clients.tenant import TenantClient
from killbill.clients.test import TestClient


class KillBillClient:
    """Kill Bill Client"""

    def __init__(
        self,
        username: str,
        password: str,
        api_url: str = "http://localhost:8080",
        timeout: int = 30,
    ):
        self.tenant = TenantClient(username, password, api_url, timeout)
        self.catalog = CatalogClient(username, password, api_url, timeout)
        self.account = AccountClient(username, password, api_url, timeout)
        self.subscription = SubscriptionClient(username, password, api_url, timeout)
        self.bundle = BundleClient(username, password, api_url, timeout)
        self.overdue = OverdueClient(username, password, api_url, timeout)
        self.test = TestClient(username, password, api_url, timeout)
        self.invoice = InvoiceClient(username, password, api_url, timeout)
        self.credit = CreditClient(username, password, api_url, timeout)
