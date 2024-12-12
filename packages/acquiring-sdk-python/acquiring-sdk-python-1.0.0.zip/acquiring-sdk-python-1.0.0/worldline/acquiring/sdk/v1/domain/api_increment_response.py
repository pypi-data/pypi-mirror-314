# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Optional

from .amount_data import AmountData
from .api_action_response import ApiActionResponse


class ApiIncrementResponse(ApiActionResponse):

    __authorization_code: Optional[str] = None
    __total_authorized_amount: Optional[AmountData] = None

    @property
    def authorization_code(self) -> Optional[str]:
        """
        | Authorization approval code

        Type: str
        """
        return self.__authorization_code

    @authorization_code.setter
    def authorization_code(self, value: Optional[str]) -> None:
        self.__authorization_code = value

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
        dictionary = super(ApiIncrementResponse, self).to_dictionary()
        if self.authorization_code is not None:
            dictionary['authorizationCode'] = self.authorization_code
        if self.total_authorized_amount is not None:
            dictionary['totalAuthorizedAmount'] = self.total_authorized_amount.to_dictionary()
        return dictionary

    def from_dictionary(self, dictionary: dict) -> 'ApiIncrementResponse':
        super(ApiIncrementResponse, self).from_dictionary(dictionary)
        if 'authorizationCode' in dictionary:
            self.authorization_code = dictionary['authorizationCode']
        if 'totalAuthorizedAmount' in dictionary:
            if not isinstance(dictionary['totalAuthorizedAmount'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['totalAuthorizedAmount']))
            value = AmountData()
            self.total_authorized_amount = value.from_dictionary(dictionary['totalAuthorizedAmount'])
        return self
