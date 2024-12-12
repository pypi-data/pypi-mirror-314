# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Optional

from worldline.acquiring.sdk.domain.data_object import DataObject


class PlainCardData(DataObject):

    __card_number: Optional[str] = None
    __card_security_code: Optional[str] = None
    __expiry_date: Optional[str] = None

    @property
    def card_number(self) -> Optional[str]:
        """
        | Card number (PAN, network token or DPAN).

        Type: str
        """
        return self.__card_number

    @card_number.setter
    def card_number(self, value: Optional[str]) -> None:
        self.__card_number = value

    @property
    def card_security_code(self) -> Optional[str]:
        """
        | The security code indicated on the card
        | Based on the card brand, it can be 3 or 4 digits long
        | and have different names: CVV2, CVC2, CVN2, CID, CVC, CAV2, etc.

        Type: str
        """
        return self.__card_security_code

    @card_security_code.setter
    def card_security_code(self, value: Optional[str]) -> None:
        self.__card_security_code = value

    @property
    def expiry_date(self) -> Optional[str]:
        """
        | Card or token expiry date in format MMYYYY

        Type: str
        """
        return self.__expiry_date

    @expiry_date.setter
    def expiry_date(self, value: Optional[str]) -> None:
        self.__expiry_date = value

    def to_dictionary(self) -> dict:
        dictionary = super(PlainCardData, self).to_dictionary()
        if self.card_number is not None:
            dictionary['cardNumber'] = self.card_number
        if self.card_security_code is not None:
            dictionary['cardSecurityCode'] = self.card_security_code
        if self.expiry_date is not None:
            dictionary['expiryDate'] = self.expiry_date
        return dictionary

    def from_dictionary(self, dictionary: dict) -> 'PlainCardData':
        super(PlainCardData, self).from_dictionary(dictionary)
        if 'cardNumber' in dictionary:
            self.card_number = dictionary['cardNumber']
        if 'cardSecurityCode' in dictionary:
            self.card_security_code = dictionary['cardSecurityCode']
        if 'expiryDate' in dictionary:
            self.expiry_date = dictionary['expiryDate']
        return self
