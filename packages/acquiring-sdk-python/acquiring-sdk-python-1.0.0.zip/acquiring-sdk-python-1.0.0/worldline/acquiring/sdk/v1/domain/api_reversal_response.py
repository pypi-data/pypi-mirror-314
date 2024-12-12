# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Optional

from .amount_data import AmountData
from .api_action_response import ApiActionResponse


class ApiReversalResponse(ApiActionResponse):

    __total_authorized_amount: Optional[AmountData] = None

    @property
    def total_authorized_amount(self) -> Optional[AmountData]:
        """
        | Amount for the operation.

        Type: :class:`worldline.acquiring.sdk.v1.domain.amount_data.AmountData`
        """
        return self.__total_authorized_amount

    @total_authorized_amount.setter
    def total_authorized_amount(self, value: Optional[AmountData]) -> None:
        self.__total_authorized_amount = value

    def to_dictionary(self) -> dict:
        dictionary = super(ApiReversalResponse, self).to_dictionary()
        if self.total_authorized_amount is not None:
            dictionary['totalAuthorizedAmount'] = self.total_authorized_amount.to_dictionary()
        return dictionary

    def from_dictionary(self, dictionary: dict) -> 'ApiReversalResponse':
        super(ApiReversalResponse, self).from_dictionary(dictionary)
        if 'totalAuthorizedAmount' in dictionary:
            if not isinstance(dictionary['totalAuthorizedAmount'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['totalAuthorizedAmount']))
            value = AmountData()
            self.total_authorized_amount = value.from_dictionary(dictionary['totalAuthorizedAmount'])
        return self
