# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Optional

from .e_commerce_data import ECommerceData
from .plain_card_data import PlainCardData
from .point_of_sale_data import PointOfSaleData

from worldline.acquiring.sdk.domain.data_object import DataObject


class CardPaymentDataForBalanceInquiry(DataObject):

    __brand: Optional[str] = None
    __brand_selector: Optional[str] = None
    __card_data: Optional[PlainCardData] = None
    __card_entry_mode: Optional[str] = None
    __cardholder_verification_method: Optional[str] = None
    __ecommerce_data: Optional[ECommerceData] = None
    __point_of_sale_data: Optional[PointOfSaleData] = None
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
    def ecommerce_data(self) -> Optional[ECommerceData]:
        """
        | Request data for eCommerce transactions

        Type: :class:`worldline.acquiring.sdk.v1.domain.e_commerce_data.ECommerceData`
        """
        return self.__ecommerce_data

    @ecommerce_data.setter
    def ecommerce_data(self, value: Optional[ECommerceData]) -> None:
        self.__ecommerce_data = value

    @property
    def point_of_sale_data(self) -> Optional[PointOfSaleData]:
        """
        | Request data for Point Of Sale (POS) or "in person" Transaction

        Type: :class:`worldline.acquiring.sdk.v1.domain.point_of_sale_data.PointOfSaleData`
        """
        return self.__point_of_sale_data

    @point_of_sale_data.setter
    def point_of_sale_data(self, value: Optional[PointOfSaleData]) -> None:
        self.__point_of_sale_data = value

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
        dictionary = super(CardPaymentDataForBalanceInquiry, self).to_dictionary()
        if self.brand is not None:
            dictionary['brand'] = self.brand
        if self.brand_selector is not None:
            dictionary['brandSelector'] = self.brand_selector
        if self.card_data is not None:
            dictionary['cardData'] = self.card_data.to_dictionary()
        if self.card_entry_mode is not None:
            dictionary['cardEntryMode'] = self.card_entry_mode
        if self.cardholder_verification_method is not None:
            dictionary['cardholderVerificationMethod'] = self.cardholder_verification_method
        if self.ecommerce_data is not None:
            dictionary['ecommerceData'] = self.ecommerce_data.to_dictionary()
        if self.point_of_sale_data is not None:
            dictionary['pointOfSaleData'] = self.point_of_sale_data.to_dictionary()
        if self.wallet_id is not None:
            dictionary['walletId'] = self.wallet_id
        return dictionary

    def from_dictionary(self, dictionary: dict) -> 'CardPaymentDataForBalanceInquiry':
        super(CardPaymentDataForBalanceInquiry, self).from_dictionary(dictionary)
        if 'brand' in dictionary:
            self.brand = dictionary['brand']
        if 'brandSelector' in dictionary:
            self.brand_selector = dictionary['brandSelector']
        if 'cardData' in dictionary:
            if not isinstance(dictionary['cardData'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['cardData']))
            value = PlainCardData()
            self.card_data = value.from_dictionary(dictionary['cardData'])
        if 'cardEntryMode' in dictionary:
            self.card_entry_mode = dictionary['cardEntryMode']
        if 'cardholderVerificationMethod' in dictionary:
            self.cardholder_verification_method = dictionary['cardholderVerificationMethod']
        if 'ecommerceData' in dictionary:
            if not isinstance(dictionary['ecommerceData'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['ecommerceData']))
            value = ECommerceData()
            self.ecommerce_data = value.from_dictionary(dictionary['ecommerceData'])
        if 'pointOfSaleData' in dictionary:
            if not isinstance(dictionary['pointOfSaleData'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['pointOfSaleData']))
            value = PointOfSaleData()
            self.point_of_sale_data = value.from_dictionary(dictionary['pointOfSaleData'])
        if 'walletId' in dictionary:
            self.wallet_id = dictionary['walletId']
        return self
