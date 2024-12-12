# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Optional

from worldline.acquiring.sdk.domain.data_object import DataObject


class PointOfSaleDataForDcc(DataObject):

    __terminal_country_code: Optional[str] = None
    __terminal_id: Optional[str] = None

    @property
    def terminal_country_code(self) -> Optional[str]:
        """
        | ISO 3166 Country code of the terminal

        Type: str
        """
        return self.__terminal_country_code

    @terminal_country_code.setter
    def terminal_country_code(self, value: Optional[str]) -> None:
        self.__terminal_country_code = value

    @property
    def terminal_id(self) -> Optional[str]:
        """
        | The terminal ID

        Type: str
        """
        return self.__terminal_id

    @terminal_id.setter
    def terminal_id(self, value: Optional[str]) -> None:
        self.__terminal_id = value

    def to_dictionary(self) -> dict:
        dictionary = super(PointOfSaleDataForDcc, self).to_dictionary()
        if self.terminal_country_code is not None:
            dictionary['terminalCountryCode'] = self.terminal_country_code
        if self.terminal_id is not None:
            dictionary['terminalId'] = self.terminal_id
        return dictionary

    def from_dictionary(self, dictionary: dict) -> 'PointOfSaleDataForDcc':
        super(PointOfSaleDataForDcc, self).from_dictionary(dictionary)
        if 'terminalCountryCode' in dictionary:
            self.terminal_country_code = dictionary['terminalCountryCode']
        if 'terminalId' in dictionary:
            self.terminal_id = dictionary['terminalId']
        return self
