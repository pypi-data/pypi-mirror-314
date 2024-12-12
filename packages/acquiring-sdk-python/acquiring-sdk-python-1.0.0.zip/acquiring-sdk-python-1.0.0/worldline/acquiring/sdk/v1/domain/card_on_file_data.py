# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Optional

from .initial_card_on_file_data import InitialCardOnFileData
from .subsequent_card_on_file_data import SubsequentCardOnFileData

from worldline.acquiring.sdk.domain.data_object import DataObject


class CardOnFileData(DataObject):

    __initial_card_on_file_data: Optional[InitialCardOnFileData] = None
    __is_initial_transaction: Optional[bool] = None
    __subsequent_card_on_file_data: Optional[SubsequentCardOnFileData] = None

    @property
    def initial_card_on_file_data(self) -> Optional[InitialCardOnFileData]:
        """
        Type: :class:`worldline.acquiring.sdk.v1.domain.initial_card_on_file_data.InitialCardOnFileData`
        """
        return self.__initial_card_on_file_data

    @initial_card_on_file_data.setter
    def initial_card_on_file_data(self, value: Optional[InitialCardOnFileData]) -> None:
        self.__initial_card_on_file_data = value

    @property
    def is_initial_transaction(self) -> Optional[bool]:
        """
        | Indicate whether this is the initial Card on File transaction or not

        Type: bool
        """
        return self.__is_initial_transaction

    @is_initial_transaction.setter
    def is_initial_transaction(self, value: Optional[bool]) -> None:
        self.__is_initial_transaction = value

    @property
    def subsequent_card_on_file_data(self) -> Optional[SubsequentCardOnFileData]:
        """
        Type: :class:`worldline.acquiring.sdk.v1.domain.subsequent_card_on_file_data.SubsequentCardOnFileData`
        """
        return self.__subsequent_card_on_file_data

    @subsequent_card_on_file_data.setter
    def subsequent_card_on_file_data(self, value: Optional[SubsequentCardOnFileData]) -> None:
        self.__subsequent_card_on_file_data = value

    def to_dictionary(self) -> dict:
        dictionary = super(CardOnFileData, self).to_dictionary()
        if self.initial_card_on_file_data is not None:
            dictionary['initialCardOnFileData'] = self.initial_card_on_file_data.to_dictionary()
        if self.is_initial_transaction is not None:
            dictionary['isInitialTransaction'] = self.is_initial_transaction
        if self.subsequent_card_on_file_data is not None:
            dictionary['subsequentCardOnFileData'] = self.subsequent_card_on_file_data.to_dictionary()
        return dictionary

    def from_dictionary(self, dictionary: dict) -> 'CardOnFileData':
        super(CardOnFileData, self).from_dictionary(dictionary)
        if 'initialCardOnFileData' in dictionary:
            if not isinstance(dictionary['initialCardOnFileData'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['initialCardOnFileData']))
            value = InitialCardOnFileData()
            self.initial_card_on_file_data = value.from_dictionary(dictionary['initialCardOnFileData'])
        if 'isInitialTransaction' in dictionary:
            self.is_initial_transaction = dictionary['isInitialTransaction']
        if 'subsequentCardOnFileData' in dictionary:
            if not isinstance(dictionary['subsequentCardOnFileData'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['subsequentCardOnFileData']))
            value = SubsequentCardOnFileData()
            self.subsequent_card_on_file_data = value.from_dictionary(dictionary['subsequentCardOnFileData'])
        return self
