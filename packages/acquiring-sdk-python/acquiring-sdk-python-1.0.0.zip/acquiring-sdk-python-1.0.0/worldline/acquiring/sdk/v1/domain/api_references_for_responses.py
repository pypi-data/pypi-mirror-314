# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Optional

from worldline.acquiring.sdk.domain.data_object import DataObject


class ApiReferencesForResponses(DataObject):

    __payment_account_reference: Optional[str] = None
    __retrieval_reference_number: Optional[str] = None
    __scheme_transaction_id: Optional[str] = None

    @property
    def payment_account_reference(self) -> Optional[str]:
        """
        | (PAR) Unique identifier associated with a specific cardholder PAN

        Type: str
        """
        return self.__payment_account_reference

    @payment_account_reference.setter
    def payment_account_reference(self, value: Optional[str]) -> None:
        self.__payment_account_reference = value

    @property
    def retrieval_reference_number(self) -> Optional[str]:
        """
        | Retrieval reference number for transaction, must be AN(12) if provided

        Type: str
        """
        return self.__retrieval_reference_number

    @retrieval_reference_number.setter
    def retrieval_reference_number(self, value: Optional[str]) -> None:
        self.__retrieval_reference_number = value

    @property
    def scheme_transaction_id(self) -> Optional[str]:
        """
        | ID assigned by the scheme to identify a transaction through its whole lifecycle.

        Type: str
        """
        return self.__scheme_transaction_id

    @scheme_transaction_id.setter
    def scheme_transaction_id(self, value: Optional[str]) -> None:
        self.__scheme_transaction_id = value

    def to_dictionary(self) -> dict:
        dictionary = super(ApiReferencesForResponses, self).to_dictionary()
        if self.payment_account_reference is not None:
            dictionary['paymentAccountReference'] = self.payment_account_reference
        if self.retrieval_reference_number is not None:
            dictionary['retrievalReferenceNumber'] = self.retrieval_reference_number
        if self.scheme_transaction_id is not None:
            dictionary['schemeTransactionId'] = self.scheme_transaction_id
        return dictionary

    def from_dictionary(self, dictionary: dict) -> 'ApiReferencesForResponses':
        super(ApiReferencesForResponses, self).from_dictionary(dictionary)
        if 'paymentAccountReference' in dictionary:
            self.payment_account_reference = dictionary['paymentAccountReference']
        if 'retrievalReferenceNumber' in dictionary:
            self.retrieval_reference_number = dictionary['retrievalReferenceNumber']
        if 'schemeTransactionId' in dictionary:
            self.scheme_transaction_id = dictionary['schemeTransactionId']
        return self
