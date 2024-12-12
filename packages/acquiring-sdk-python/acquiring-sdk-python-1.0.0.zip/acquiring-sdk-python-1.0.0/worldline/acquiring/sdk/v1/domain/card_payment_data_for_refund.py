# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Optional

from .network_token_data import NetworkTokenData
from .plain_card_data import PlainCardData

from worldline.acquiring.sdk.domain.data_object import DataObject


class CardPaymentDataForRefund(DataObject):

    __brand: Optional[str] = None
    __brand_selector: Optional[str] = None
    __capture_immediately: Optional[bool] = None
    __card_data: Optional[PlainCardData] = None
    __card_entry_mode: Optional[str] = None
    __cardholder_verification_method: Optional[str] = None
    __network_token_data: Optional[NetworkTokenData] = None
    __wallet_id: Optional[str] = None

    @property
    def brand(self) -> Optional[str]:
        """
        | The card brand

        Type: str
        """
        return self.__brand

    @brand.setter
    def brand(self, value: Optional[str]) -> None:
        self.__brand = value

    @property
    def brand_selector(self) -> Optional[str]:
        """
        | The party responsible for the brand selection.

        Type: str
        """
        return self.__brand_selector

    @brand_selector.setter
    def brand_selector(self, value: Optional[str]) -> None:
        self.__brand_selector = value

    @property
    def capture_immediately(self) -> Optional[bool]:
        """
        | If true the transaction will be authorized and captured immediately

        Type: bool
        """
        return self.__capture_immediately

    @capture_immediately.setter
    def capture_immediately(self, value: Optional[bool]) -> None:
        self.__capture_immediately = value

    @property
    def card_data(self) -> Optional[PlainCardData]:
        """
        | Card data in plain text

        Type: :class:`worldline.acquiring.sdk.v1.domain.plain_card_data.PlainCardData`
        """
        return self.__card_data

    @card_data.setter
    def card_data(self, value: Optional[PlainCardData]) -> None:
        self.__card_data = value

    @property
    def card_entry_mode(self) -> Optional[str]:
        """
        | Card entry mode used in the transaction

        Type: str
        """
        return self.__card_entry_mode

    @card_entry_mode.setter
    def card_entry_mode(self, value: Optional[str]) -> None:
        self.__card_entry_mode = value

    @property
    def cardholder_verification_method(self) -> Optional[str]:
        """
        | Cardholder verification method used in the transaction

        Type: str
        """
        return self.__cardholder_verification_method

    @cardholder_verification_method.setter
    def cardholder_verification_method(self, value: Optional[str]) -> None:
        self.__cardholder_verification_method = value

    @property
    def network_token_data(self) -> Optional[NetworkTokenData]:
        """
        Type: :class:`worldline.acquiring.sdk.v1.domain.network_token_data.NetworkTokenData`
        """
        return self.__network_token_data

    @network_token_data.setter
    def network_token_data(self, value: Optional[NetworkTokenData]) -> None:
        self.__network_token_data = value

    @property
    def wallet_id(self) -> Optional[str]:
        """
        | Type of wallet, values are assigned by card schemes, e.g. 101 for MasterPass in eCommerce, 102 for MasterPass NFC, 103 for Apple Pay, 216 for Google Pay and 217 for Samsung Pay

        Type: str
        """
        return self.__wallet_id

    @wallet_id.setter
    def wallet_id(self, value: Optional[str]) -> None:
        self.__wallet_id = value

    def to_dictionary(self) -> dict:
        dictionary = super(CardPaymentDataForRefund, self).to_dictionary()
        if self.brand is not None:
            dictionary['brand'] = self.brand
        if self.brand_selector is not None:
            dictionary['brandSelector'] = self.brand_selector
        if self.capture_immediately is not None:
            dictionary['captureImmediately'] = self.capture_immediately
        if self.card_data is not None:
            dictionary['cardData'] = self.card_data.to_dictionary()
        if self.card_entry_mode is not None:
            dictionary['cardEntryMode'] = self.card_entry_mode
        if self.cardholder_verification_method is not None:
            dictionary['cardholderVerificationMethod'] = self.cardholder_verification_method
        if self.network_token_data is not None:
            dictionary['networkTokenData'] = self.network_token_data.to_dictionary()
        if self.wallet_id is not None:
            dictionary['walletId'] = self.wallet_id
        return dictionary

    def from_dictionary(self, dictionary: dict) -> 'CardPaymentDataForRefund':
        super(CardPaymentDataForRefund, self).from_dictionary(dictionary)
        if 'brand' in dictionary:
            self.brand = dictionary['brand']
        if 'brandSelector' in dictionary:
            self.brand_selector = dictionary['brandSelector']
        if 'captureImmediately' in dictionary:
            self.capture_immediately = dictionary['captureImmediately']
        if 'cardData' in dictionary:
            if not isinstance(dictionary['cardData'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['cardData']))
            value = PlainCardData()
            self.card_data = value.from_dictionary(dictionary['cardData'])
        if 'cardEntryMode' in dictionary:
            self.card_entry_mode = dictionary['cardEntryMode']
        if 'cardholderVerificationMethod' in dictionary:
            self.cardholder_verification_method = dictionary['cardholderVerificationMethod']
        if 'networkTokenData' in dictionary:
            if not isinstance(dictionary['networkTokenData'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['networkTokenData']))
            value = NetworkTokenData()
            self.network_token_data = value.from_dictionary(dictionary['networkTokenData'])
        if 'walletId' in dictionary:
            self.wallet_id = dictionary['walletId']
        return self
