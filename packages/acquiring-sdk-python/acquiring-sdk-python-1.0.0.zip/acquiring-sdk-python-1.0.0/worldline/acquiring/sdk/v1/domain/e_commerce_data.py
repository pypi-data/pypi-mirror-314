# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Optional

from .address_verification_data import AddressVerificationData
from .three_d_secure import ThreeDSecure

from worldline.acquiring.sdk.domain.data_object import DataObject


class ECommerceData(DataObject):

    __address_verification_data: Optional[AddressVerificationData] = None
    __sca_exemption_request: Optional[str] = None
    __three_d_secure: Optional[ThreeDSecure] = None

    @property
    def address_verification_data(self) -> Optional[AddressVerificationData]:
        """
        | Address Verification System data

        Type: :class:`worldline.acquiring.sdk.v1.domain.address_verification_data.AddressVerificationData`
        """
        return self.__address_verification_data

    @address_verification_data.setter
    def address_verification_data(self, value: Optional[AddressVerificationData]) -> None:
        self.__address_verification_data = value

    @property
    def sca_exemption_request(self) -> Optional[str]:
        """
        | Strong customer authentication exemption request

        Type: str
        """
        return self.__sca_exemption_request

    @sca_exemption_request.setter
    def sca_exemption_request(self, value: Optional[str]) -> None:
        self.__sca_exemption_request = value

    @property
    def three_d_secure(self) -> Optional[ThreeDSecure]:
        """
        | 3D Secure data.
        | Please note that if AAV or CAVV or equivalent is missing, transaction should not be flagged as 3D Secure.

        Type: :class:`worldline.acquiring.sdk.v1.domain.three_d_secure.ThreeDSecure`
        """
        return self.__three_d_secure

    @three_d_secure.setter
    def three_d_secure(self, value: Optional[ThreeDSecure]) -> None:
        self.__three_d_secure = value

    def to_dictionary(self) -> dict:
        dictionary = super(ECommerceData, self).to_dictionary()
        if self.address_verification_data is not None:
            dictionary['addressVerificationData'] = self.address_verification_data.to_dictionary()
        if self.sca_exemption_request is not None:
            dictionary['scaExemptionRequest'] = self.sca_exemption_request
        if self.three_d_secure is not None:
            dictionary['threeDSecure'] = self.three_d_secure.to_dictionary()
        return dictionary

    def from_dictionary(self, dictionary: dict) -> 'ECommerceData':
        super(ECommerceData, self).from_dictionary(dictionary)
        if 'addressVerificationData' in dictionary:
            if not isinstance(dictionary['addressVerificationData'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['addressVerificationData']))
            value = AddressVerificationData()
            self.address_verification_data = value.from_dictionary(dictionary['addressVerificationData'])
        if 'scaExemptionRequest' in dictionary:
            self.sca_exemption_request = dictionary['scaExemptionRequest']
        if 'threeDSecure' in dictionary:
            if not isinstance(dictionary['threeDSecure'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['threeDSecure']))
            value = ThreeDSecure()
            self.three_d_secure = value.from_dictionary(dictionary['threeDSecure'])
        return self
