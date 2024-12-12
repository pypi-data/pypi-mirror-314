# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Optional

from worldline.acquiring.sdk.domain.data_object import DataObject


class PaymentReferences(DataObject):

    __dynamic_descriptor: Optional[str] = None
    __merchant_reference: Optional[str] = None

    @property
    def dynamic_descriptor(self) -> Optional[str]:
        """
        | Dynamic descriptor gives you the ability to control the descriptor on the credit card statement of the customer.

        Type: str
        """
        return self.__dynamic_descriptor

    @dynamic_descriptor.setter
    def dynamic_descriptor(self, value: Optional[str]) -> None:
        self.__dynamic_descriptor = value

    @property
    def merchant_reference(self) -> Optional[str]:
        """
        | Reference for the transaction to allow the merchant to reconcile their payments in our report files.
        | It is advised to submit a unique value per transaction.
        | The value provided here is returned in the baseTrxType/addlMercData element of the MRX file.

        Type: str
        """
        return self.__merchant_reference

    @merchant_reference.setter
    def merchant_reference(self, value: Optional[str]) -> None:
        self.__merchant_reference = value

    def to_dictionary(self) -> dict:
        dictionary = super(PaymentReferences, self).to_dictionary()
        if self.dynamic_descriptor is not None:
            dictionary['dynamicDescriptor'] = self.dynamic_descriptor
        if self.merchant_reference is not None:
            dictionary['merchantReference'] = self.merchant_reference
        return dictionary

    def from_dictionary(self, dictionary: dict) -> 'PaymentReferences':
        super(PaymentReferences, self).from_dictionary(dictionary)
        if 'dynamicDescriptor' in dictionary:
            self.dynamic_descriptor = dictionary['dynamicDescriptor']
        if 'merchantReference' in dictionary:
            self.merchant_reference = dictionary['merchantReference']
        return self
