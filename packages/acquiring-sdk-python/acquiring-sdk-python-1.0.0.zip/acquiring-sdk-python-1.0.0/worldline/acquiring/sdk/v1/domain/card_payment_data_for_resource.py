# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Optional

from worldline.acquiring.sdk.domain.data_object import DataObject


class CardPaymentDataForResource(DataObject):

    __brand: Optional[str] = None

    @property
    def brand(self) -> Optional[str]:
        """
        | The card brand

        Type: str
        """
        return self.__brand

    @brand.setter
    def brand(self, value: Optional[str]) -> None:
        self.__brand = value

    def to_dictionary(self) -> dict:
        dictionary = super(CardPaymentDataForResource, self).to_dictionary()
        if self.brand is not None:
            dictionary['brand'] = self.brand
        return dictionary

    def from_dictionary(self, dictionary: dict) -> 'CardPaymentDataForResource':
        super(CardPaymentDataForResource, self).from_dictionary(dictionary)
        if 'brand' in dictionary:
            self.brand = dictionary['brand']
        return self
