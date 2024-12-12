# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from datetime import datetime
from typing import Optional

from worldline.acquiring.sdk.domain.data_object import DataObject


class RateData(DataObject):

    __exchange_rate: Optional[float] = None
    __inverted_exchange_rate: Optional[float] = None
    __mark_up: Optional[float] = None
    __mark_up_basis: Optional[str] = None
    __quotation_date_time: Optional[datetime] = None

    @property
    def exchange_rate(self) -> Optional[float]:
        """
        | The exchange rate

        Type: float
        """
        return self.__exchange_rate

    @exchange_rate.setter
    def exchange_rate(self, value: Optional[float]) -> None:
        self.__exchange_rate = value

    @property
    def inverted_exchange_rate(self) -> Optional[float]:
        """
        | The inverted exchange rate

        Type: float
        """
        return self.__inverted_exchange_rate

    @inverted_exchange_rate.setter
    def inverted_exchange_rate(self, value: Optional[float]) -> None:
        self.__inverted_exchange_rate = value

    @property
    def mark_up(self) -> Optional[float]:
        """
        | The mark up applied on the rate (in percentage).

        Type: float
        """
        return self.__mark_up

    @mark_up.setter
    def mark_up(self, value: Optional[float]) -> None:
        self.__mark_up = value

    @property
    def mark_up_basis(self) -> Optional[str]:
        """
        | The source of the rate the markup is based upon. If the cardholder and the merchant are based in Europe, the mark up is calculated based on the rates provided by the European Central Bank.

        Type: str
        """
        return self.__mark_up_basis

    @mark_up_basis.setter
    def mark_up_basis(self, value: Optional[str]) -> None:
        self.__mark_up_basis = value

    @property
    def quotation_date_time(self) -> Optional[datetime]:
        """
        | The date and time of the quotation

        Type: datetime
        """
        return self.__quotation_date_time

    @quotation_date_time.setter
    def quotation_date_time(self, value: Optional[datetime]) -> None:
        self.__quotation_date_time = value

    def to_dictionary(self) -> dict:
        dictionary = super(RateData, self).to_dictionary()
        if self.exchange_rate is not None:
            dictionary['exchangeRate'] = self.exchange_rate
        if self.inverted_exchange_rate is not None:
            dictionary['invertedExchangeRate'] = self.inverted_exchange_rate
        if self.mark_up is not None:
            dictionary['markUp'] = self.mark_up
        if self.mark_up_basis is not None:
            dictionary['markUpBasis'] = self.mark_up_basis
        if self.quotation_date_time is not None:
            dictionary['quotationDateTime'] = DataObject.format_datetime(self.quotation_date_time)
        return dictionary

    def from_dictionary(self, dictionary: dict) -> 'RateData':
        super(RateData, self).from_dictionary(dictionary)
        if 'exchangeRate' in dictionary:
            self.exchange_rate = dictionary['exchangeRate']
        if 'invertedExchangeRate' in dictionary:
            self.inverted_exchange_rate = dictionary['invertedExchangeRate']
        if 'markUp' in dictionary:
            self.mark_up = dictionary['markUp']
        if 'markUpBasis' in dictionary:
            self.mark_up_basis = dictionary['markUpBasis']
        if 'quotationDateTime' in dictionary:
            self.quotation_date_time = DataObject.parse_datetime(dictionary['quotationDateTime'])
        return self
