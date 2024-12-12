# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Optional

from worldline.acquiring.sdk.domain.data_object import DataObject


class MerchantData(DataObject):

    __address: Optional[str] = None
    __city: Optional[str] = None
    __country_code: Optional[str] = None
    __merchant_category_code: Optional[int] = None
    __name: Optional[str] = None
    __postal_code: Optional[str] = None
    __state_code: Optional[str] = None

    @property
    def address(self) -> Optional[str]:
        """
        | Street address

        Type: str
        """
        return self.__address

    @address.setter
    def address(self, value: Optional[str]) -> None:
        self.__address = value

    @property
    def city(self) -> Optional[str]:
        """
        | Address city

        Type: str
        """
        return self.__city

    @city.setter
    def city(self, value: Optional[str]) -> None:
        self.__city = value

    @property
    def country_code(self) -> Optional[str]:
        """
        | Address country code, ISO 3166 international standard

        Type: str
        """
        return self.__country_code

    @country_code.setter
    def country_code(self, value: Optional[str]) -> None:
        self.__country_code = value

    @property
    def merchant_category_code(self) -> Optional[int]:
        """
        | Merchant category code (MCC)

        Type: int
        """
        return self.__merchant_category_code

    @merchant_category_code.setter
    def merchant_category_code(self, value: Optional[int]) -> None:
        self.__merchant_category_code = value

    @property
    def name(self) -> Optional[str]:
        """
        | Merchant name

        Type: str
        """
        return self.__name

    @name.setter
    def name(self, value: Optional[str]) -> None:
        self.__name = value

    @property
    def postal_code(self) -> Optional[str]:
        """
        | Address postal code

        Type: str
        """
        return self.__postal_code

    @postal_code.setter
    def postal_code(self, value: Optional[str]) -> None:
        self.__postal_code = value

    @property
    def state_code(self) -> Optional[str]:
        """
        | Address state code, only supplied if country is US or CA

        Type: str
        """
        return self.__state_code

    @state_code.setter
    def state_code(self, value: Optional[str]) -> None:
        self.__state_code = value

    def to_dictionary(self) -> dict:
        dictionary = super(MerchantData, self).to_dictionary()
        if self.address is not None:
            dictionary['address'] = self.address
        if self.city is not None:
            dictionary['city'] = self.city
        if self.country_code is not None:
            dictionary['countryCode'] = self.country_code
        if self.merchant_category_code is not None:
            dictionary['merchantCategoryCode'] = self.merchant_category_code
        if self.name is not None:
            dictionary['name'] = self.name
        if self.postal_code is not None:
            dictionary['postalCode'] = self.postal_code
        if self.state_code is not None:
            dictionary['stateCode'] = self.state_code
        return dictionary

    def from_dictionary(self, dictionary: dict) -> 'MerchantData':
        super(MerchantData, self).from_dictionary(dictionary)
        if 'address' in dictionary:
            self.address = dictionary['address']
        if 'city' in dictionary:
            self.city = dictionary['city']
        if 'countryCode' in dictionary:
            self.country_code = dictionary['countryCode']
        if 'merchantCategoryCode' in dictionary:
            self.merchant_category_code = dictionary['merchantCategoryCode']
        if 'name' in dictionary:
            self.name = dictionary['name']
        if 'postalCode' in dictionary:
            self.postal_code = dictionary['postalCode']
        if 'stateCode' in dictionary:
            self.state_code = dictionary['stateCode']
        return self
