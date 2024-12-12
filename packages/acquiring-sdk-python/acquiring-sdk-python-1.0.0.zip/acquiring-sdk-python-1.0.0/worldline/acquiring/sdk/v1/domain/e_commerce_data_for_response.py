# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Optional

from worldline.acquiring.sdk.domain.data_object import DataObject


class ECommerceDataForResponse(DataObject):

    __address_verification_result: Optional[str] = None
    __card_security_code_result: Optional[str] = None

    @property
    def address_verification_result(self) -> Optional[str]:
        """
        | Result of Address Verification Result
        | Possible values:
        
        * MATCH
        * ADDRESS_MATCH_POSTAL_CODE_MISMATCH
        * ADDRESS_MISMATCH_POSTAL_CODE_MATCH
        * ADDRESS_MATCH_POSTAL_CODE_NOT_VERIFIED
        * ADDRESS_NOT_VERIFIED_POSTAL_CODE_MATCH
        * MISMATCH
        * ERROR
        * NOT_VERIFIED

        Type: str
        """
        return self.__address_verification_result

    @address_verification_result.setter
    def address_verification_result(self, value: Optional[str]) -> None:
        self.__address_verification_result = value

    @property
    def card_security_code_result(self) -> Optional[str]:
        """
        | Result of card security code check
        | Possible values:
        
        * MATCH
        * MISMATCH
        * NOT_VERIFIED
        * OMITTED
        * MISSING

        Type: str
        """
        return self.__card_security_code_result

    @card_security_code_result.setter
    def card_security_code_result(self, value: Optional[str]) -> None:
        self.__card_security_code_result = value

    def to_dictionary(self) -> dict:
        dictionary = super(ECommerceDataForResponse, self).to_dictionary()
        if self.address_verification_result is not None:
            dictionary['addressVerificationResult'] = self.address_verification_result
        if self.card_security_code_result is not None:
            dictionary['cardSecurityCodeResult'] = self.card_security_code_result
        return dictionary

    def from_dictionary(self, dictionary: dict) -> 'ECommerceDataForResponse':
        super(ECommerceDataForResponse, self).from_dictionary(dictionary)
        if 'addressVerificationResult' in dictionary:
            self.address_verification_result = dictionary['addressVerificationResult']
        if 'cardSecurityCodeResult' in dictionary:
            self.card_security_code_result = dictionary['cardSecurityCodeResult']
        return self
