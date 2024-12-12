# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Optional

from worldline.acquiring.sdk.domain.data_object import DataObject


class NetworkTokenData(DataObject):

    __cryptogram: Optional[str] = None
    __eci: Optional[str] = None

    @property
    def cryptogram(self) -> Optional[str]:
        """
        | Network token cryptogram

        Type: str
        """
        return self.__cryptogram

    @cryptogram.setter
    def cryptogram(self, value: Optional[str]) -> None:
        self.__cryptogram = value

    @property
    def eci(self) -> Optional[str]:
        """
        | Electronic Commerce Indicator
        | Value that indicates the level of authentication.
        | Contains different values depending on the brand.

        Type: str
        """
        return self.__eci

    @eci.setter
    def eci(self, value: Optional[str]) -> None:
        self.__eci = value

    def to_dictionary(self) -> dict:
        dictionary = super(NetworkTokenData, self).to_dictionary()
        if self.cryptogram is not None:
            dictionary['cryptogram'] = self.cryptogram
        if self.eci is not None:
            dictionary['eci'] = self.eci
        return dictionary

    def from_dictionary(self, dictionary: dict) -> 'NetworkTokenData':
        super(NetworkTokenData, self).from_dictionary(dictionary)
        if 'cryptogram' in dictionary:
            self.cryptogram = dictionary['cryptogram']
        if 'eci' in dictionary:
            self.eci = dictionary['eci']
        return self
