# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Optional

from .amount_data import AmountData
from .rate_data import RateData

from worldline.acquiring.sdk.domain.data_object import DataObject


class DccProposal(DataObject):

    __original_amount: Optional[AmountData] = None
    __rate: Optional[RateData] = None
    __rate_reference_id: Optional[str] = None
    __resulting_amount: Optional[AmountData] = None

    @property
    def original_amount(self) -> Optional[AmountData]:
        """
        | Amount for the operation.

        Type: :class:`worldline.acquiring.sdk.v1.domain.amount_data.AmountData`
        """
        return self.__original_amount

    @original_amount.setter
    def original_amount(self, value: Optional[AmountData]) -> None:
        self.__original_amount = value

    @property
    def rate(self) -> Optional[RateData]:
        """
        Type: :class:`worldline.acquiring.sdk.v1.domain.rate_data.RateData`
        """
        return self.__rate

    @rate.setter
    def rate(self, value: Optional[RateData]) -> None:
        self.__rate = value

    @property
    def rate_reference_id(self) -> Optional[str]:
        """
        | The rate reference ID

        Type: str
        """
        return self.__rate_reference_id

    @rate_reference_id.setter
    def rate_reference_id(self, value: Optional[str]) -> None:
        self.__rate_reference_id = value

    @property
    def resulting_amount(self) -> Optional[AmountData]:
        """
        | Amount for the operation.

        Type: :class:`worldline.acquiring.sdk.v1.domain.amount_data.AmountData`
        """
        return self.__resulting_amount

    @resulting_amount.setter
    def resulting_amount(self, value: Optional[AmountData]) -> None:
        self.__resulting_amount = value

    def to_dictionary(self) -> dict:
        dictionary = super(DccProposal, self).to_dictionary()
        if self.original_amount is not None:
            dictionary['originalAmount'] = self.original_amount.to_dictionary()
        if self.rate is not None:
            dictionary['rate'] = self.rate.to_dictionary()
        if self.rate_reference_id is not None:
            dictionary['rateReferenceId'] = self.rate_reference_id
        if self.resulting_amount is not None:
            dictionary['resultingAmount'] = self.resulting_amount.to_dictionary()
        return dictionary

    def from_dictionary(self, dictionary: dict) -> 'DccProposal':
        super(DccProposal, self).from_dictionary(dictionary)
        if 'originalAmount' in dictionary:
            if not isinstance(dictionary['originalAmount'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['originalAmount']))
            value = AmountData()
            self.original_amount = value.from_dictionary(dictionary['originalAmount'])
        if 'rate' in dictionary:
            if not isinstance(dictionary['rate'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['rate']))
            value = RateData()
            self.rate = value.from_dictionary(dictionary['rate'])
        if 'rateReferenceId' in dictionary:
            self.rate_reference_id = dictionary['rateReferenceId']
        if 'resultingAmount' in dictionary:
            if not isinstance(dictionary['resultingAmount'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['resultingAmount']))
            value = AmountData()
            self.resulting_amount = value.from_dictionary(dictionary['resultingAmount'])
        return self
