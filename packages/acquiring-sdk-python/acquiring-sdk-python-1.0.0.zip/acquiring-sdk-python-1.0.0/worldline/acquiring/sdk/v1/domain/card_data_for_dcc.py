# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Optional

from worldline.acquiring.sdk.domain.data_object import DataObject


class CardDataForDcc(DataObject):

    __bin: Optional[str] = None
    __brand: Optional[str] = None
    __card_country_code: Optional[str] = None
    __card_entry_mode: Optional[str] = None

    @property
    def bin(self) -> Optional[str]:
        """
        | Used to determine the currency of the card. The first 12 digits of the card number. The BIN number is on the first 6 or 8 digits. Some issuers are using subranges for different countries on digits 9-12.

        Type: str
        """
        return self.__bin

    @bin.setter
    def bin(self, value: Optional[str]) -> None:
        self.__bin = value

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

    @property
    def card_country_code(self) -> Optional[str]:
        """
        | The ISO 3166 country code of the card

        Type: str
        """
        return self.__card_country_code

    @card_country_code.setter
    def card_country_code(self, value: Optional[str]) -> None:
        self.__card_country_code = value

    @property
    def card_entry_mode(self) -> Optional[str]:
        """
        | Card entry mode used in the transaction

        Type: str
        """
        return self.__card_entry_mode

    @card_entry_mode.setter
    def card_entry_mode(self, value: Optional[str]) -> None:
        self.__card_entry_mode = value

    def to_dictionary(self) -> dict:
        dictionary = super(CardDataForDcc, self).to_dictionary()
        if self.bin is not None:
            dictionary['bin'] = self.bin
        if self.brand is not None:
            dictionary['brand'] = self.brand
        if self.card_country_code is not None:
            dictionary['cardCountryCode'] = self.card_country_code
        if self.card_entry_mode is not None:
            dictionary['cardEntryMode'] = self.card_entry_mode
        return dictionary

    def from_dictionary(self, dictionary: dict) -> 'CardDataForDcc':
        super(CardDataForDcc, self).from_dictionary(dictionary)
        if 'bin' in dictionary:
            self.bin = dictionary['bin']
        if 'brand' in dictionary:
            self.brand = dictionary['brand']
        if 'cardCountryCode' in dictionary:
            self.card_country_code = dictionary['cardCountryCode']
        if 'cardEntryMode' in dictionary:
            self.card_entry_mode = dictionary['cardEntryMode']
        return self
