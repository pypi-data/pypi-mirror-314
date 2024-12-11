from typing import Union

from killbill.clients.base import BaseClient
from killbill.enums import BillingPeriod, ProductCategory, TrialTimeUnit
from killbill.header import Header


class CatalogClient(BaseClient):
    """Client for the Kill Bill catalog API"""

    def add_simple_plan(
        self,
        header: Header,
        plan_id: str,
        product_name: str,
        currency: str,
        product_category: ProductCategory = ProductCategory.BASE,
        amount: Union[float, int] = 0,
        trial_length: int = 0,
        trial_time_unit: TrialTimeUnit = TrialTimeUnit.UNLIMITED,
        billing_period: BillingPeriod = BillingPeriod.MONTHLY,
    ):
        """Create a new simple plan in the catalog.

        Args:
            plan_id (str): The ID of the plan.
            product_name (str): The name of the product.
            product_category (str): The category of the product.
            currency (str): The currency of the plan.
            amount (Union[float, int]): The amount of the plan.
            billing_period (str): The billing period of the plan.
            trial_length (int): The trial length of the plan.
            trial_time_unit (str): The trial time unit of the plan.
            api_key (str): The API key of the user.
            api_secret (str): The API secret of the user.
            created_by (str): The ID of the user who created the plan.
            reason (str, optional): The reason for creating the plan. Defaults to None.
            comment (str, optional): The comment for creating the plan. Defaults to None.
        """

        payload = {
            "planId": plan_id,
            "productName": product_name,
            "productCategory": str(product_category),
            "currency": currency,
            "amount": amount,
            "billingPeriod": str(billing_period),
            "trialLength": trial_length,
            "trialTimeUnit": str(trial_time_unit),
        }

        response = self._post(
            "catalog/simplePlan",
            payload=payload,
            headers=header.dict(),
        )

        self._raise_for_status(response)

    def retrieve(
        self,
        header: Header,
        account_id: str = None,
        requested_date: str = None,
        xml=False,
    ):
        """Retrieve catalogs.

        if `xml = True`, returns the XML representation of the overdue config

        if `xml = False`, returns the JSON representation of the overdue config
        """

        payload = {
            "accountId": account_id,
            "requestedDate": requested_date,
        }

        if xml:
            endpoint = "catalog/xml"
            headers = header.dict()
        else:
            endpoint = "catalog"
            headers = header.dict().copy()
            headers.update({"Accept": "application/json"})

        response = self._get(
            endpoint,
            payload=payload,
            headers=headers,
        )

        self._raise_for_status(response)

        return response.text if xml else response.json()

    def validate(self, header: Header, catalog_xml: str):
        """Validate a XML catalog

        Args:
            header created_by is required
        """

        response = self._post(
            "catalog/xml/validate",
            data=catalog_xml,
            headers=header.dict(),
        )

        self._raise_for_status(response)

        return response.json()

    def create(self, header: Header, catalog_xml: str):
        """Create a XML catalog

        Args:
            header created_by is required
        """

        response = self._post(
            "catalog/xml",
            data=catalog_xml,
            headers=header.dict(),
        )

        self._raise_for_status(response)

    def versions(self, header: Header):
        """Retrieve a list of catalog versions"""

        response = self._get(
            "catalog/versions",
            headers=header.dict(),
        )

        self._raise_for_status(response)

        return response.json()
