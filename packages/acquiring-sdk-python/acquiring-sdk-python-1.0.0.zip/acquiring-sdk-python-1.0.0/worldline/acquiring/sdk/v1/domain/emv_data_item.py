# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Optional

from worldline.acquiring.sdk.domain.data_object import DataObject


class EmvDataItem(DataObject):

    __tag: Optional[str] = None
    __value: Optional[str] = None

    @property
    def tag(self) -> Optional[str]:
        """
        | EMV tag

        Type: str
        """
        return self.__tag

    @tag.setter
    def tag(self, value: Optional[str]) -> None:
        self.__tag = value

    @property
    def value(self) -> Optional[str]:
        """
        | EMV value encoded in base64

        Type: str
        """
        return self.__value

    @value.setter
    def value(self, value: Optional[str]) -> None:
        self.__value = value

    def to_dictionary(self) -> dict:
        dictionary = super(EmvDataItem, self).to_dictionary()
        if self.tag is not None:
            dictionary['tag'] = self.tag
        if self.value is not None:
            dictionary['value'] = self.value
        return dictionary

    def from_dictionary(self, dictionary: dict) -> 'EmvDataItem':
        super(EmvDataItem, self).from_dictionary(dictionary)
        if 'tag' in dictionary:
            self.tag = dictionary['tag']
        if 'value' in dictionary:
            self.value = dictionary['value']
        return self
