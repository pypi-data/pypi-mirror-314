# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from datetime import datetime
from typing import Optional

from .amount_data import AmountData

from worldline.acquiring.sdk.domain.data_object import DataObject


class TransactionDataForDcc(DataObject):

    __amount: Optional[AmountData] = None
    __transaction_timestamp: Optional[datetime] = None
    __transaction_type: Optional[str] = None

    @property
    def amount(self) -> Optional[AmountData]:
        """
        | Amount for the operation.

        Type: :class:`worldline.acquiring.sdk.v1.domain.amount_data.AmountData`
        """
        return self.__amount

    @amount.setter
    def amount(self, value: Optional[AmountData]) -> None:
        self.__amount = value

    @property
    def transaction_timestamp(self) -> Optional[datetime]:
        """
        | The date and time of the transaction

        Type: datetime
        """
        return self.__transaction_timestamp

    @transaction_timestamp.setter
    def transaction_timestamp(self, value: Optional[datetime]) -> None:
        self.__transaction_timestamp = value

    @property
    def transaction_type(self) -> Optional[str]:
        """
        | The transaction type

        Type: str
        """
        return self.__transaction_type

    @transaction_type.setter
    def transaction_type(self, value: Optional[str]) -> None:
        self.__transaction_type = value

    def to_dictionary(self) -> dict:
        dictionary = super(TransactionDataForDcc, self).to_dictionary()
        if self.amount is not None:
            dictionary['amount'] = self.amount.to_dictionary()
        if self.transaction_timestamp is not None:
            dictionary['transactionTimestamp'] = DataObject.format_datetime(self.transaction_timestamp)
        if self.transaction_type is not None:
            dictionary['transactionType'] = self.transaction_type
        return dictionary

    def from_dictionary(self, dictionary: dict) -> 'TransactionDataForDcc':
        super(TransactionDataForDcc, self).from_dictionary(dictionary)
        if 'amount' in dictionary:
            if not isinstance(dictionary['amount'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['amount']))
            value = AmountData()
            self.amount = value.from_dictionary(dictionary['amount'])
        if 'transactionTimestamp' in dictionary:
            self.transaction_timestamp = DataObject.parse_datetime(dictionary['transactionTimestamp'])
        if 'transactionType' in dictionary:
            self.transaction_type = dictionary['transactionType']
        return self
