# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Mapping, Optional

from worldline.acquiring.sdk.api_resource import ApiResource
from worldline.acquiring.sdk.v1.acquirer.merchant.accountverifications.account_verifications_client import AccountVerificationsClient
from worldline.acquiring.sdk.v1.acquirer.merchant.balanceinquiries.balance_inquiries_client import BalanceInquiriesClient
from worldline.acquiring.sdk.v1.acquirer.merchant.dynamiccurrencyconversion.dynamic_currency_conversion_client import DynamicCurrencyConversionClient
from worldline.acquiring.sdk.v1.acquirer.merchant.payments.payments_client import PaymentsClient
from worldline.acquiring.sdk.v1.acquirer.merchant.refunds.refunds_client import RefundsClient
from worldline.acquiring.sdk.v1.acquirer.merchant.technicalreversals.technical_reversals_client import TechnicalReversalsClient


class MerchantClient(ApiResource):
    """
    Merchant client. Thread-safe.
    """

    def __init__(self, parent: ApiResource, path_context: Optional[Mapping[str, str]]):
        """
        :param parent:       :class:`worldline.acquiring.sdk.api_resource.ApiResource`
        :param path_context: Mapping[str, str]
        """
        super(MerchantClient, self).__init__(parent=parent, path_context=path_context)

    def payments(self) -> PaymentsClient:
        """
        Resource /processing/v1/{acquirerId}/{merchantId}/payments

        :return: :class:`worldline.acquiring.sdk.v1.acquirer.merchant.payments.payments_client.PaymentsClient`
        """
        return PaymentsClient(self, None)

    def refunds(self) -> RefundsClient:
        """
        Resource /processing/v1/{acquirerId}/{merchantId}/refunds

        :return: :class:`worldline.acquiring.sdk.v1.acquirer.merchant.refunds.refunds_client.RefundsClient`
        """
        return RefundsClient(self, None)

    def account_verifications(self) -> AccountVerificationsClient:
        """
        Resource /processing/v1/{acquirerId}/{merchantId}/account-verifications

        :return: :class:`worldline.acquiring.sdk.v1.acquirer.merchant.accountverifications.account_verifications_client.AccountVerificationsClient`
        """
        return AccountVerificationsClient(self, None)

    def balance_inquiries(self) -> BalanceInquiriesClient:
        """
        Resource /processing/v1/{acquirerId}/{merchantId}/balance-inquiries

        :return: :class:`worldline.acquiring.sdk.v1.acquirer.merchant.balanceinquiries.balance_inquiries_client.BalanceInquiriesClient`
        """
        return BalanceInquiriesClient(self, None)

    def technical_reversals(self) -> TechnicalReversalsClient:
        """
        Resource /processing/v1/{acquirerId}/{merchantId}/operations/{operationId}/reverse

        :return: :class:`worldline.acquiring.sdk.v1.acquirer.merchant.technicalreversals.technical_reversals_client.TechnicalReversalsClient`
        """
        return TechnicalReversalsClient(self, None)

    def dynamic_currency_conversion(self) -> DynamicCurrencyConversionClient:
        """
        Resource /services/v1/{acquirerId}/{merchantId}/dcc-rates

        :return: :class:`worldline.acquiring.sdk.v1.acquirer.merchant.dynamiccurrencyconversion.dynamic_currency_conversion_client.DynamicCurrencyConversionClient`
        """
        return DynamicCurrencyConversionClient(self, None)
