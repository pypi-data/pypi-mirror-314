# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Optional

from worldline.acquiring.sdk.domain.data_object import DataObject


class AddressVerificationData(DataObject):

    __cardholder_address: Optional[str] = None
    __cardholder_postal_code: Optional[str] = None

    @property
    def cardholder_address(self) -> Optional[str]:
        """
        | Cardholder street address

        Type: str
        """
        return self.__cardholder_address

    @cardholder_address.setter
    def cardholder_address(self, value: Optional[str]) -> None:
        self.__cardholder_address = value

    @property
    def cardholder_postal_code(self) -> Optional[str]:
        """
        | Cardholder postal code, should be provided without spaces

        Type: str
        """
        return self.__cardholder_postal_code

    @cardholder_postal_code.setter
    def cardholder_postal_code(self, value: Optional[str]) -> None:
        self.__cardholder_postal_code = value

    def to_dictionary(self) -> dict:
        dictionary = super(AddressVerificationData, self).to_dictionary()
        if self.cardholder_address is not None:
            dictionary['cardholderAddress'] = self.cardholder_address
        if self.cardholder_postal_code is not None:
            dictionary['cardholderPostalCode'] = self.cardholder_postal_code
        return dictionary

    def from_dictionary(self, dictionary: dict) -> 'AddressVerificationData':
        super(AddressVerificationData, self).from_dictionary(dictionary)
        if 'cardholderAddress' in dictionary:
            self.cardholder_address = dictionary['cardholderAddress']
        if 'cardholderPostalCode' in dictionary:
            self.cardholder_postal_code = dictionary['cardholderPostalCode']
        return self
