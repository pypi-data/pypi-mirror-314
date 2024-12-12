# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Optional

from worldline.acquiring.sdk.domain.data_object import DataObject


class DccData(DataObject):

    __amount: Optional[int] = None
    __conversion_rate: Optional[float] = None
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
    def conversion_rate(self) -> Optional[float]:
        """
        | Currency conversion rate in decimal notation.

        Type: float
        """
        return self.__conversion_rate

    @conversion_rate.setter
    def conversion_rate(self, value: Optional[float]) -> None:
        self.__conversion_rate = value

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
        dictionary = super(DccData, self).to_dictionary()
        if self.amount is not None:
            dictionary['amount'] = self.amount
        if self.conversion_rate is not None:
            dictionary['conversionRate'] = self.conversion_rate
        if self.currency_code is not None:
            dictionary['currencyCode'] = self.currency_code
        if self.number_of_decimals is not None:
            dictionary['numberOfDecimals'] = self.number_of_decimals
        return dictionary

    def from_dictionary(self, dictionary: dict) -> 'DccData':
        super(DccData, self).from_dictionary(dictionary)
        if 'amount' in dictionary:
            self.amount = dictionary['amount']
        if 'conversionRate' in dictionary:
            self.conversion_rate = dictionary['conversionRate']
        if 'currencyCode' in dictionary:
            self.currency_code = dictionary['currencyCode']
        if 'numberOfDecimals' in dictionary:
            self.number_of_decimals = dictionary['numberOfDecimals']
        return self
