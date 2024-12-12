# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Optional

from worldline.acquiring.sdk.domain.data_object import DataObject


class PointOfSaleDataForResponse(DataObject):

    __pan_last4_digits: Optional[str] = None
    __pin_retry_counter: Optional[int] = None

    @property
    def pan_last4_digits(self) -> Optional[str]:
        """
        | Last 4 digits of the PAN

        Type: str
        """
        return self.__pan_last4_digits

    @pan_last4_digits.setter
    def pan_last4_digits(self, value: Optional[str]) -> None:
        self.__pan_last4_digits = value

    @property
    def pin_retry_counter(self) -> Optional[int]:
        """
        | Number of PIN retries

        Type: int
        """
        return self.__pin_retry_counter

    @pin_retry_counter.setter
    def pin_retry_counter(self, value: Optional[int]) -> None:
        self.__pin_retry_counter = value

    def to_dictionary(self) -> dict:
        dictionary = super(PointOfSaleDataForResponse, self).to_dictionary()
        if self.pan_last4_digits is not None:
            dictionary['panLast4Digits'] = self.pan_last4_digits
        if self.pin_retry_counter is not None:
            dictionary['pinRetryCounter'] = self.pin_retry_counter
        return dictionary

    def from_dictionary(self, dictionary: dict) -> 'PointOfSaleDataForResponse':
        super(PointOfSaleDataForResponse, self).from_dictionary(dictionary)
        if 'panLast4Digits' in dictionary:
            self.pan_last4_digits = dictionary['panLast4Digits']
        if 'pinRetryCounter' in dictionary:
            self.pin_retry_counter = dictionary['pinRetryCounter']
        return self
