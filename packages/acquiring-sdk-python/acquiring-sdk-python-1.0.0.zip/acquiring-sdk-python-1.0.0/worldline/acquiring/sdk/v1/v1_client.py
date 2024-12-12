# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Mapping, Optional

from worldline.acquiring.sdk.api_resource import ApiResource
from worldline.acquiring.sdk.v1.acquirer.acquirer_client import AcquirerClient
from worldline.acquiring.sdk.v1.ping.ping_client import PingClient


class V1Client(ApiResource):
    """
    V1 client.

    Thread-safe.
    """
    def __init__(self, parent: ApiResource, path_context: Optional[Mapping[str, str]]):
        """
        :param parent:       :class:`worldline.acquiring.sdk.api_resource.ApiResource`
        :param path_context: Mapping[str, str]
        """
        super(V1Client, self).__init__(parent=parent, path_context=path_context)

    def acquirer(self, acquirer_id: str) -> AcquirerClient:
        """
        Resource /processing/v1/{acquirerId}

        :param acquirer_id:  str
        :return: :class:`worldline.acquiring.sdk.v1.acquirer.acquirer_client.AcquirerClient`
        """
        sub_context = {
            "acquirerId": acquirer_id,
        }
        return AcquirerClient(self, sub_context)

    def ping(self) -> PingClient:
        """
        Resource /services/v1/ping

        :return: :class:`worldline.acquiring.sdk.v1.ping.ping_client.PingClient`
        """
        return PingClient(self, None)
