# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Mapping, Optional

from worldline.acquiring.sdk.api_resource import ApiResource
from worldline.acquiring.sdk.v1.acquirer.merchant.merchant_client import MerchantClient


class AcquirerClient(ApiResource):
    """
    Acquirer client. Thread-safe.
    """

    def __init__(self, parent: ApiResource, path_context: Optional[Mapping[str, str]]):
        """
        :param parent:       :class:`worldline.acquiring.sdk.api_resource.ApiResource`
        :param path_context: Mapping[str, str]
        """
        super(AcquirerClient, self).__init__(parent=parent, path_context=path_context)

    def merchant(self, merchant_id: str) -> MerchantClient:
        """
        Resource /processing/v1/{acquirerId}/{merchantId}

        :param merchant_id:  str
        :return: :class:`worldline.acquiring.sdk.v1.acquirer.merchant.merchant_client.MerchantClient`
        """
        sub_context = {
            "merchantId": merchant_id,
        }
        return MerchantClient(self, sub_context)
