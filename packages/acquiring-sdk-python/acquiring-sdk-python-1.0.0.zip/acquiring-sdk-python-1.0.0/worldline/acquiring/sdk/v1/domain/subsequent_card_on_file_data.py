# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Optional

from worldline.acquiring.sdk.domain.data_object import DataObject


class SubsequentCardOnFileData(DataObject):

    __card_on_file_initiator: Optional[str] = None
    __initial_scheme_transaction_id: Optional[str] = None
    __transaction_type: Optional[str] = None

    @property
    def card_on_file_initiator(self) -> Optional[str]:
        """
        | Card on file initiator

        Type: str
        """
        return self.__card_on_file_initiator

    @card_on_file_initiator.setter
    def card_on_file_initiator(self, value: Optional[str]) -> None:
        self.__card_on_file_initiator = value

    @property
    def initial_scheme_transaction_id(self) -> Optional[str]:
        """
        | ID assigned by the scheme to identify a transaction through its whole lifecycle.

        Type: str
        """
        return self.__initial_scheme_transaction_id

    @initial_scheme_transaction_id.setter
    def initial_scheme_transaction_id(self, value: Optional[str]) -> None:
        self.__initial_scheme_transaction_id = value

    @property
    def transaction_type(self) -> Optional[str]:
        """
        | Transaction type

        Type: str
        """
        return self.__transaction_type

    @transaction_type.setter
    def transaction_type(self, value: Optional[str]) -> None:
        self.__transaction_type = value

    def to_dictionary(self) -> dict:
        dictionary = super(SubsequentCardOnFileData, self).to_dictionary()
        if self.card_on_file_initiator is not None:
            dictionary['cardOnFileInitiator'] = self.card_on_file_initiator
        if self.initial_scheme_transaction_id is not None:
            dictionary['initialSchemeTransactionId'] = self.initial_scheme_transaction_id
        if self.transaction_type is not None:
            dictionary['transactionType'] = self.transaction_type
        return dictionary

    def from_dictionary(self, dictionary: dict) -> 'SubsequentCardOnFileData':
        super(SubsequentCardOnFileData, self).from_dictionary(dictionary)
        if 'cardOnFileInitiator' in dictionary:
            self.card_on_file_initiator = dictionary['cardOnFileInitiator']
        if 'initialSchemeTransactionId' in dictionary:
            self.initial_scheme_transaction_id = dictionary['initialSchemeTransactionId']
        if 'transactionType' in dictionary:
            self.transaction_type = dictionary['transactionType']
        return self
