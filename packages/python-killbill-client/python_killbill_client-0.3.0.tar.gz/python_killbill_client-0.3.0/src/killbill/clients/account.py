from typing import List, Union

from killbill.clients.base import BaseClient
from killbill.enums import Audit, BlockingStateType, TransactionType
from killbill.header import Header


class AccountClient(BaseClient):
    """Client for the Kill Bill account API"""

    def create(
        self,
        header: Header,
        name=None,
        first_name_length=None,
        external_key=None,
        email=None,
        bill_cycle_day_local=None,
        currency=None,
        time_zone=None,
        locale=None,
        address1=None,
        address2=None,
        postal_code=None,
        company=None,
        city=None,
        state=None,
        country=None,
        phone=None,
        notes=None,
        is_migrated: bool = None,
    ):
        """Creates account

        Returns:
            str or None: The account's ID or None if the request failed.
        """

        payload = {
            "name": name,
            "firstNameLength": first_name_length,
            "externalKey": external_key,
            "email": email,
            "billCycleDayLocal": bill_cycle_day_local,
            "currency": currency,
            "timeZone": time_zone,
            "locale": locale,
            "address1": address1,
            "address2": address2,
            "postalCode": postal_code,
            "company": company,
            "city": city,
            "state": state,
            "country": country,
            "phone": phone,
            "notes": notes,
            "isMigrated": is_migrated,
        }

        response = self._post(
            "accounts",
            payload=payload,
            headers=header.dict(),
        )

        self._raise_for_status(response)

        return self._get_uuid(response.headers.get("Location"))

    def list(
        self,
        header: Header,
        offset: int = 0,
        limit: int = 100,
        account_with_balance: bool = False,
        account_with_balance_and_cba: bool = False,
        audit: Audit = Audit.NONE,
    ):
        """List accounts

        Args:
            audit : "NONE", "MINIMAL", "FULL"
        """

        payload = {
            "offset": offset,
            "limit": limit,
            "accountWithBalance": account_with_balance,
            "accountWithBalanceAndCBA": account_with_balance_and_cba,
            "audit": str(audit),
        }

        response = self._get(
            "accounts/pagination",
            payload=payload,
            headers=header.dict(),
        )

        self._raise_for_status(response)

        return response.json()

    def close(
        self,
        header: Header,
        account_id: str,
        cancel_all_subscriptions: bool = False,
        write_off_unpaid_invoices: bool = False,
        item_adjust_unpaid_invoices: bool = False,
        remove_future_notifications: bool = True,
    ):
        """Close account

        Args:
            account_id (str): uuid
            cancel_all_subscriptions (bool, optional): Defaults to False.
            write_off_unpaid_invoices (bool, optional): Defaults to False.
            item_adjust_unpaid_invoices (bool, optional): Defaults to False.
            remove_future_notifications (bool, optional): Defaults to True.

        """

        response = self._delete(
            f"accounts/{account_id}",
            headers=header.dict(),
            params={
                "cancelAllSubscriptions": cancel_all_subscriptions,
                "writeOffUnpaidInvoices": write_off_unpaid_invoices,
                "itemAdjustUnpaidInvoices": item_adjust_unpaid_invoices,
                "removeFutureNotifications": remove_future_notifications,
            },
        )

        self._raise_for_status(response)

        return True

    def add_payment_method(
        self,
        header: Header,
        account_id: str,
        plugin_name: str = "__EXTERNAL_PAYMENT__",
        is_default: bool = False,
        pay_all_unpaid_invoices: bool = False,
        external_key: str = None,
    ):
        """Add a payment method

        Returns:
            str or None: The payment method's ID or None if the request failed.
        """

        payload = {"pluginName": plugin_name, "externalKey": external_key}

        response = self._post(
            f"accounts/{account_id}/paymentMethods",
            headers=header.dict(),
            payload=payload,
            params={
                "isDefault": is_default,
                "payAllUnpaidInvoices": pay_all_unpaid_invoices,
            },
        )

        self._raise_for_status(response)

        return self._get_uuid(response.headers.get("Location"))

    def get_payment_methods(
        self,
        header: Header,
        account_id: str,
        with_plugin_info: bool = False,
        included_deleted=False,
        plugin_property: List[str] = None,
        audit: Audit = Audit.NONE,
    ):
        """Retrieve account payment methods"""

        params = {
            "withPluginInfo": with_plugin_info,
            "includedDeleted": included_deleted,
            "pluginProperty": plugin_property,
            "audit": str(audit),
        }

        response = self._get(
            f"accounts/{account_id}/paymentMethods",
            headers=header.dict(),
            params=params,
        )

        self._raise_for_status(response)

        return response.json()

    def invoices(
        self,
        header: Header,
        account_id: str,
        start_date: str = None,
        end_date: str = None,
        with_migration_invoices: bool = False,
        unpaid_invoices_only: bool = False,
        include_voided_invoices: bool = False,
        include_invoice_components: bool = False,
        audit: Audit = Audit.NONE,
    ):
        """Retrieve account invoices"""

        response = self._get(
            f"accounts/{account_id}/invoices",
            headers=header.dict(),
            params={
                "startDate": start_date,
                "endDate": end_date,
                "withMigrationInvoices": with_migration_invoices,
                "unpaidInvoicesOnly": unpaid_invoices_only,
                "includeVoidedInvoices": include_voided_invoices,
                "includeInvoiceComponents": include_invoice_components,
                "audit": str(audit),
            },
        )

        self._raise_for_status(response)

        return response.json()

    def retrieve(
        self,
        header: Header,
        external_key: str,
        account_with_balance: bool = False,
        account_with_balance_and_cba: bool = False,
        audit: Audit = Audit.NONE,
    ):
        """Retrieve an account by external key"""

        params = {
            "externalKey": external_key,
            "accountWithBalance": account_with_balance,
            "accountWithBalanceAndCBA": account_with_balance_and_cba,
            "audit": str(audit),
        }

        response = self._get(
            "accounts",
            params=params,
            headers=header.dict(),
        )

        self._raise_for_status(response)

        return response.json()

    def get_blocking_states(
        self,
        header: Header,
        account_id: str,
        blocking_state_types: Union[
            BlockingStateType, List[BlockingStateType]
        ] = BlockingStateType.ACCOUNT,
        blocking_state_svcs: Union[str, List[str]] = None,
        audit: Audit = Audit.NONE,
    ):
        """Retrieve account blocking states"""

        if isinstance(blocking_state_types, list):
            blocking_state_types = [str(x) for x in blocking_state_types]
        else:
            blocking_state_types = str(blocking_state_types)

        params = {
            "blockingStateTypes": blocking_state_types,
            "blockingStateSvcs": blocking_state_svcs,
            "audit": str(audit),
        }

        response = self._get(
            f"accounts/{account_id}/block", headers=header.dict(), params=params
        )

        self._raise_for_status(response)

        return response.json()

    def bundles(
        self,
        header: Header,
        account_id: str,
        external_key: str = None,
        bundles_filter: str = None,
        audit: Audit = Audit.NONE,
    ):
        """Retrieve bundles for account"""

        params = {
            "externalKey": external_key,
            "bundlesFilter": bundles_filter,
            "audit": str(audit),
        }

        response = self._get(
            f"accounts/{account_id}/bundles", headers=header.dict(), params=params
        )

        self._raise_for_status(response)

        return response.json()

    def overdue(self, header: Header, account_id: str):
        """Retrieve overdue state for account"""

        response = self._get(
            f"accounts/{account_id}/overdue",
            headers=header.dict(),
        )

        self._raise_for_status(response)

        return response.json()

    def retrieve_by_id(
        self,
        header: Header,
        account_id: str,
        account_with_balance: bool = False,
        account_with_balance_and_cba: bool = False,
        audit: Audit = Audit.NONE,
    ):
        """Retrieve account by id"""

        params = {
            "accountWithBalance": account_with_balance,
            "accountWithBalanceAndCBA": account_with_balance_and_cba,
            "audit": str(audit),
        }

        response = self._get(
            f"accounts/{account_id}",
            params=params,
            headers=header.dict(),
        )

        self._raise_for_status(response)

        return response.json()

    def payments(
        self,
        header: Header,
        account_id: str,
        transaction_type: TransactionType,
        amount: int | float,
        payment_method_id: str | None = None,
        control_plugin_name: List[str] | None = None,
        plugin_property: List[str] | None = None,
    ):
        """Trigger a payment (authorization, purchase or credit) and return the payment id"""

        payload = {
            "transactionType": str(transaction_type),
            "amount": amount,
        }

        params = {
            "paymentMethodId": payment_method_id,
            "controlPluginName": control_plugin_name,
            "pluginProperty": plugin_property,
        }

        response = self._post(
            f"accounts/{account_id}/payments",
            headers=header.dict(),
            payload=payload,
            params=params,
        )

        self._raise_for_status(response)

        return self._get_uuid(response.headers.get("Location"))

    def invoice_payments(
        self,
        header: Header,
        account_id: str,
        payment_method_id: str = None,
        external_payment: bool = False,
        payment_amount: int = None,
        target_date: str = None,
    ):
        """Trigger a payment for all unpaid invoices"""

        params = {
            "paymentMethodId": payment_method_id,
            "externalPayment": external_payment,
            "paymentAmount": payment_amount,
            "targetDate": target_date,
        }

        response = self._post(
            f"accounts/{account_id}/invoicePayments",
            headers=header.dict(),
            params=params,
        )

        self._raise_for_status(response)
