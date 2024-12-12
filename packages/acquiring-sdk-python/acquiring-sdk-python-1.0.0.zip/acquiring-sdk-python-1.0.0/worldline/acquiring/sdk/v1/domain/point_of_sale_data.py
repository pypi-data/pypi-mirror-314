# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import List, Optional

from .emv_data_item import EmvDataItem

from worldline.acquiring.sdk.domain.data_object import DataObject


class PointOfSaleData(DataObject):

    __emv_data: Optional[List[EmvDataItem]] = None
    __encrypted_pin_block: Optional[str] = None
    __is_response_to_pin_request: Optional[bool] = None
    __is_retry_with_the_same_operation_id: Optional[bool] = None
    __pin_master_key_reference: Optional[str] = None
    __track2_data: Optional[str] = None

    @property
    def emv_data(self) -> Optional[List[EmvDataItem]]:
        """
        | EMV data of the card as tag/value pairs.
        | It is needed when cardEntryMode is CHIP or CONTACTLESS.

        Type: list[:class:`worldline.acquiring.sdk.v1.domain.emv_data_item.EmvDataItem`]
        """
        return self.__emv_data

    @emv_data.setter
    def emv_data(self, value: Optional[List[EmvDataItem]]) -> None:
        self.__emv_data = value

    @property
    def encrypted_pin_block(self) -> Optional[str]:
        """
        | Encrypted data containing a PIN

        Type: str
        """
        return self.__encrypted_pin_block

    @encrypted_pin_block.setter
    def encrypted_pin_block(self, value: Optional[str]) -> None:
        self.__encrypted_pin_block = value

    @property
    def is_response_to_pin_request(self) -> Optional[bool]:
        """
        | Indicate whether the request is made after a first one that resulted in a PIN request

        Type: bool
        """
        return self.__is_response_to_pin_request

    @is_response_to_pin_request.setter
    def is_response_to_pin_request(self, value: Optional[bool]) -> None:
        self.__is_response_to_pin_request = value

    @property
    def is_retry_with_the_same_operation_id(self) -> Optional[bool]:
        """
        | Indicate whether the request is a retry with the same operation ID after a first request that resulted in a PIN request

        Type: bool
        """
        return self.__is_retry_with_the_same_operation_id

    @is_retry_with_the_same_operation_id.setter
    def is_retry_with_the_same_operation_id(self, value: Optional[bool]) -> None:
        self.__is_retry_with_the_same_operation_id = value

    @property
    def pin_master_key_reference(self) -> Optional[str]:
        """
        | Reference to the master key used to encrypt the PIN

        Type: str
        """
        return self.__pin_master_key_reference

    @pin_master_key_reference.setter
    def pin_master_key_reference(self, value: Optional[str]) -> None:
        self.__pin_master_key_reference = value

    @property
    def track2_data(self) -> Optional[str]:
        """
        | Track 2 data from the card
        | It is needed when cardEntryMode is MAGNETIC_STRIPE.

        Type: str
        """
        return self.__track2_data

    @track2_data.setter
    def track2_data(self, value: Optional[str]) -> None:
        self.__track2_data = value

    def to_dictionary(self) -> dict:
        dictionary = super(PointOfSaleData, self).to_dictionary()
        if self.emv_data is not None:
            dictionary['emvData'] = []
            for element in self.emv_data:
                if element is not None:
                    dictionary['emvData'].append(element.to_dictionary())
        if self.encrypted_pin_block is not None:
            dictionary['encryptedPinBlock'] = self.encrypted_pin_block
        if self.is_response_to_pin_request is not None:
            dictionary['isResponseToPinRequest'] = self.is_response_to_pin_request
        if self.is_retry_with_the_same_operation_id is not None:
            dictionary['isRetryWithTheSameOperationId'] = self.is_retry_with_the_same_operation_id
        if self.pin_master_key_reference is not None:
            dictionary['pinMasterKeyReference'] = self.pin_master_key_reference
        if self.track2_data is not None:
            dictionary['track2Data'] = self.track2_data
        return dictionary

    def from_dictionary(self, dictionary: dict) -> 'PointOfSaleData':
        super(PointOfSaleData, self).from_dictionary(dictionary)
        if 'emvData' in dictionary:
            if not isinstance(dictionary['emvData'], list):
                raise TypeError('value \'{}\' is not a list'.format(dictionary['emvData']))
            self.emv_data = []
            for element in dictionary['emvData']:
                value = EmvDataItem()
                self.emv_data.append(value.from_dictionary(element))
        if 'encryptedPinBlock' in dictionary:
            self.encrypted_pin_block = dictionary['encryptedPinBlock']
        if 'isResponseToPinRequest' in dictionary:
            self.is_response_to_pin_request = dictionary['isResponseToPinRequest']
        if 'isRetryWithTheSameOperationId' in dictionary:
            self.is_retry_with_the_same_operation_id = dictionary['isRetryWithTheSameOperationId']
        if 'pinMasterKeyReference' in dictionary:
            self.pin_master_key_reference = dictionary['pinMasterKeyReference']
        if 'track2Data' in dictionary:
            self.track2_data = dictionary['track2Data']
        return self
