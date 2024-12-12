# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import List, Optional

from worldline.acquiring.sdk.communication.param_request import ParamRequest
from worldline.acquiring.sdk.communication.request_param import RequestParam


class GetRefundParams(ParamRequest):
    """
    Query parameters for Retrieve refund

    See also https://docs.acquiring.worldline-solutions.com/api-reference#tag/Refunds/operation/getRefund
    """

    __return_operations: Optional[bool] = None

    @property
    def return_operations(self) -> Optional[bool]:
        """
        | If true, the response will contain the operations of the payment. False by default.

        Type: bool
        """
        return self.__return_operations

    @return_operations.setter
    def return_operations(self, value: Optional[bool]) -> None:
        self.__return_operations = value

    def to_request_parameters(self) -> List[RequestParam]:
        """
        :return: list[RequestParam]
        """
        result = []
        if self.return_operations is not None:
            result.append(RequestParam("returnOperations", str(self.return_operations)))
        return result
