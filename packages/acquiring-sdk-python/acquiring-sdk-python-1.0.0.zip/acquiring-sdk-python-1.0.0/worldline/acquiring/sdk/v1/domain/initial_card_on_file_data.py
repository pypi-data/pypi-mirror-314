# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Optional

from worldline.acquiring.sdk.domain.data_object import DataObject


class InitialCardOnFileData(DataObject):

    __future_use: Optional[str] = None
    __transaction_type: Optional[str] = None

    @property
    def future_use(self) -> Optional[str]:
        """
        | Future use

        Type: str
        """
        return self.__future_use

    @future_use.setter
    def future_use(self, value: Optional[str]) -> None:
        self.__future_use = value

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
        dictionary = super(InitialCardOnFileData, self).to_dictionary()
        if self.future_use is not None:
            dictionary['futureUse'] = self.future_use
        if self.transaction_type is not None:
            dictionary['transactionType'] = self.transaction_type
        return dictionary

    def from_dictionary(self, dictionary: dict) -> 'InitialCardOnFileData':
        super(InitialCardOnFileData, self).from_dictionary(dictionary)
        if 'futureUse' in dictionary:
            self.future_use = dictionary['futureUse']
        if 'transactionType' in dictionary:
            self.transaction_type = dictionary['transactionType']
        return self
