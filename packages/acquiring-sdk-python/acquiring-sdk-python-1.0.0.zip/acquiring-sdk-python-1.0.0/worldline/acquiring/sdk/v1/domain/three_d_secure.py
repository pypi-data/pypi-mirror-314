# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Optional

from worldline.acquiring.sdk.domain.data_object import DataObject


class ThreeDSecure(DataObject):

    __authentication_value: Optional[str] = None
    __directory_server_transaction_id: Optional[str] = None
    __eci: Optional[str] = None
    __three_d_secure_type: Optional[str] = None
    __version: Optional[str] = None

    @property
    def authentication_value(self) -> Optional[str]:
        """
        | MasterCard AAV in original base64 encoding or Visa, DinersClub, UnionPay or JCB CAVV in either hexadecimal or base64 encoding

        Type: str
        """
        return self.__authentication_value

    @authentication_value.setter
    def authentication_value(self, value: Optional[str]) -> None:
        self.__authentication_value = value

    @property
    def directory_server_transaction_id(self) -> Optional[str]:
        """
        | 3D Secure 2.x directory server transaction ID

        Type: str
        """
        return self.__directory_server_transaction_id

    @directory_server_transaction_id.setter
    def directory_server_transaction_id(self, value: Optional[str]) -> None:
        self.__directory_server_transaction_id = value

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

    @property
    def three_d_secure_type(self) -> Optional[str]:
        """
        | 3D Secure type used in the transaction

        Type: str
        """
        return self.__three_d_secure_type

    @three_d_secure_type.setter
    def three_d_secure_type(self, value: Optional[str]) -> None:
        self.__three_d_secure_type = value

    @property
    def version(self) -> Optional[str]:
        """
        | 3D Secure version

        Type: str
        """
        return self.__version

    @version.setter
    def version(self, value: Optional[str]) -> None:
        self.__version = value

    def to_dictionary(self) -> dict:
        dictionary = super(ThreeDSecure, self).to_dictionary()
        if self.authentication_value is not None:
            dictionary['authenticationValue'] = self.authentication_value
        if self.directory_server_transaction_id is not None:
            dictionary['directoryServerTransactionId'] = self.directory_server_transaction_id
        if self.eci is not None:
            dictionary['eci'] = self.eci
        if self.three_d_secure_type is not None:
            dictionary['threeDSecureType'] = self.three_d_secure_type
        if self.version is not None:
            dictionary['version'] = self.version
        return dictionary

    def from_dictionary(self, dictionary: dict) -> 'ThreeDSecure':
        super(ThreeDSecure, self).from_dictionary(dictionary)
        if 'authenticationValue' in dictionary:
            self.authentication_value = dictionary['authenticationValue']
        if 'directoryServerTransactionId' in dictionary:
            self.directory_server_transaction_id = dictionary['directoryServerTransactionId']
        if 'eci' in dictionary:
            self.eci = dictionary['eci']
        if 'threeDSecureType' in dictionary:
            self.three_d_secure_type = dictionary['threeDSecureType']
        if 'version' in dictionary:
            self.version = dictionary['version']
        return self
