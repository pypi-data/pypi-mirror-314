# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Optional

from worldline.acquiring.sdk.domain.data_object import DataObject


class AmountData(DataObject):

    __amount: Optional[int] = None
    __currency_code: Optional[str] = None
    __number_of_decimals: Optional[int] = None

    @property
    def amount(self) -> Optional[int]:
        """
        | Amount of transaction formatted according to card scheme specifications. E.g. 100 for 1.00 EUR.

        Type: int
        """
        return self.__amount

    @amount.setter
    def amount(self, value: Optional[int]) -> None:
        self.__amount = value

    @property
    def currency_code(self) -> Optional[str]:
        """
        | Alpha-numeric ISO 4217 currency code for transaction, e.g. EUR

        Type: str
        """
        return self.__currency_code

    @currency_code.setter
    def currency_code(self, value: Optional[str]) -> None:
        self.__currency_code = value

    @property
    def number_of_decimals(self) -> Optional[int]:
        """
        | Number of decimals in the amount

        Type: int
        """
        return self.__number_of_decimals

    @number_of_decimals.setter
    def number_of_decimals(self, value: Optional[int]) -> None:
        self.__number_of_decimals = value

    def to_dictionary(self) -> dict:
        dictionary = super(AmountData, self).to_dictionary()
        if self.amount is not None:
            dictionary['amount'] = self.amount
        if self.currency_code is not None:
            dictionary['currencyCode'] = self.currency_code
        if self.number_of_decimals is not None:
            dictionary['numberOfDecimals'] = self.number_of_decimals
        return dictionary

    def from_dictionary(self, dictionary: dict) -> 'AmountData':
        super(AmountData, self).from_dictionary(dictionary)
        if 'amount' in dictionary:
            self.amount = dictionary['amount']
        if 'currencyCode' in dictionary:
            self.currency_code = dictionary['currencyCode']
        if 'numberOfDecimals' in dictionary:
            self.number_of_decimals = dictionary['numberOfDecimals']
        return self
