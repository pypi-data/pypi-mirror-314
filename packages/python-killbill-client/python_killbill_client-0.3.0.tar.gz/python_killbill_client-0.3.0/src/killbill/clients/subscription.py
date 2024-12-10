from typing import List

from killbill.clients.base import BaseClientWithCustomFields
from killbill.enums import (
    Audit,
    BillingPeriod,
    BillingPolicy,
    EntitlementPolicy,
    ObjectType,
    ProductCategory,
)
from killbill.header import Header


class SubscriptionClient(BaseClientWithCustomFields):

    def create(
        self,
        header: Header,
        account_id: str,
        plan_name: str,
        start_date: str = None,
        external_key: str = None,
        product_name: str = None,
        product_category: ProductCategory = None,
        billing_period: BillingPeriod = None,
        price_list: str = None,
        bundle_id: str = None,
    ):
        """Create an subscription

        Returns:
            str or None: The subscription's ID or None if the request failed.
        """

        payload = {
            "accountId": account_id,
            "planName": plan_name,
            "externalKey": external_key,
            "productName": product_name,
            "productCategory": str(product_category) if product_category else None,
            "billingPeriod": str(billing_period) if billing_period else None,
            "priceList": price_list,
            "bundleId": bundle_id,
        }

        params = {
            "entitlementDate": start_date,
            "billingDate": start_date,
        }

        response = self._post(
            "subscriptions", headers=header.dict(), payload=payload, params=params
        )

        self._raise_for_status(response)

        return self._get_uuid(response.headers.get("Location"))

    def retrieve(self, header: Header, subscription_id: str, audit: Audit = Audit.NONE):
        """Retrieve a subscription by id"""

        response = self._get(
            f"subscriptions/{subscription_id}",
            headers=header.dict(),
            params={"audit": str(audit)},
        )

        self._raise_for_status(response)

        return response.json()

    def cancel(
        self,
        header: Header,
        subscription_id: str,
        requested_date: str = None,
        use_requested_date_for_billing: bool = False,
        entitlement_policy: EntitlementPolicy = None,
        billing_policy: BillingPolicy = None,
    ):
        """Cancel an entitlement plan"""

        params = {
            "requestedDate": requested_date,
            "entitlementPolicy": (
                str(entitlement_policy) if entitlement_policy else None
            ),
            "billingPolicy": str(billing_policy) if billing_policy else None,
            "useRequestedDateForBilling": use_requested_date_for_billing,
        }

        response = self._delete(
            f"subscriptions/{subscription_id}",
            headers=header.dict(),
            params=params,
        )

        self._raise_for_status(response)

    def uncancel(self, header: Header, subscription_id: str):
        """Un-cancel an entitlement"""

        response = self._put(
            f"subscriptions/{subscription_id}/uncancel",
            headers=header.dict(),
        )

        self._raise_for_status(response)

    def create_with_add_ons(
        self,
        header: Header,
        account_id: str,
        plan_name: str,
        add_ons_name: list[str],
        start_date: str = None,
    ):
        """Create an entitlement with addOn products

        Args:
            add_ons_name (list[str]): List of add-ons (plan name) to be added to the subscription

        Returns:
            str or None: The bundle's ID or None if the request failed.
        """

        payload = [
            {
                "accountId": account_id,
                "planName": plan_name,
            }
        ]

        params = {"entitlementDate": start_date, "billingDate": start_date}

        for add_ons in add_ons_name:
            payload.append(
                {
                    "accountId": account_id,
                    "planName": add_ons,
                }
            )

        response = self._post(
            "subscriptions/createSubscriptionWithAddOns",
            headers=header.dict(),
            payload=payload,
            params=params,
        )

        self._raise_for_status(response)

        return self._get_uuid(response.headers.get("Location"))

    def create_multiple_with_add_ons(
        self,
        header: Header,
        account_id: str,
        bundles: list[list],
        start_date: str = None,
    ):
        """Create multiple entitlements with addOn products

        >> Example
        ```python
        killbill.subscription.create_multiple_with_add_ons(
            header,
            account_id="3d52ce98-104e-4cfe-af7d-732f9a264a9a",
            bundles=[
                ["standard-monthly", "standard-monthly-add-on"],
                ["sport-monthly", "sport-monthly-add-on-1", "sport-monthly-add-on-2"],
            ],
        )
        ```
        """

        payload = []

        for bundle in bundles:
            base_and_add_ons = []
            for plan in bundle:
                base_and_add_ons.append(
                    {
                        "accountId": account_id,
                        "planName": plan,
                    }
                )

            payload.append({"baseEntitlementAndAddOns": base_and_add_ons})

        params = {"entitlementDate": start_date, "billingDate": start_date}

        response = self._post(
            "subscriptions/createSubscriptionsWithAddOns",
            headers=header.dict(),
            payload=payload,
            params=params,
        )

        self._raise_for_status(response)

    def add_custom_fields(
        self,
        header: Header,
        subscription_id: str,
        fields: dict,
    ):
        """Add custom fields to subscription"""

        self._add_custom_fields(
            header,
            path="subscriptions",
            object_id=subscription_id,
            fields=fields,
            object_type=ObjectType.SUBSCRIPTION,
        )

    def get_custom_fields(
        self, header: Header, subscription_id: str, audit: Audit = Audit.NONE
    ):
        """Retrieve subscription custom fields"""

        return self._get_custom_fields(
            header, path="subscriptions", object_id=subscription_id, audit=audit
        )

    def update_custom_fields(
        self,
        header: Header,
        subscription_id: str,
        fields: List[dict],
    ):
        """Modify custom fields to subscription

        Example:
        ```python
        killbill.subscription.update_custom_fields(
            header,
            subscription_id="subscription_id",
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
            path="subscriptions",
            object_id=subscription_id,
            fields=fields,
            object_type=ObjectType.SUBSCRIPTION,
        )

    def update_bill_cycle_date(
        self,
        header: Header,
        subscription_id: str,
        day: int,
        effective_from_date: str = None,
        force_new_bcd_with_past_effective_date: bool = False,
    ):
        """Allows you to change the Bill Cycle Date"""

        payload = {"billCycleDayLocal": day}

        params = {
            "effectiveFromDate": effective_from_date,
            "forceNewBcdWithPastEffectiveDate": force_new_bcd_with_past_effective_date,
        }

        response = self._put(
            f"subscriptions/{subscription_id}/bcd",
            headers=header.dict(),
            payload=payload,
            params=params,
        )

        self._raise_for_status(response)
