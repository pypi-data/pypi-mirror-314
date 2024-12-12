# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Optional

from .e_commerce_data_for_response import ECommerceDataForResponse
from .point_of_sale_data_for_response import PointOfSaleDataForResponse

from worldline.acquiring.sdk.domain.data_object import DataObject


class CardPaymentDataForResponse(DataObject):

    __brand: Optional[str] = None
    __ecommerce_data: Optional[ECommerceDataForResponse] = None
    __point_of_sale_data: Optional[PointOfSaleDataForResponse] = None

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
    def ecommerce_data(self) -> Optional[ECommerceDataForResponse]:
        """
        Type: :class:`worldline.acquiring.sdk.v1.domain.e_commerce_data_for_response.ECommerceDataForResponse`
        """
        return self.__ecommerce_data

    @ecommerce_data.setter
    def ecommerce_data(self, value: Optional[ECommerceDataForResponse]) -> None:
        self.__ecommerce_data = value

    @property
    def point_of_sale_data(self) -> Optional[PointOfSaleDataForResponse]:
        """
        Type: :class:`worldline.acquiring.sdk.v1.domain.point_of_sale_data_for_response.PointOfSaleDataForResponse`
        """
        return self.__point_of_sale_data

    @point_of_sale_data.setter
    def point_of_sale_data(self, value: Optional[PointOfSaleDataForResponse]) -> None:
        self.__point_of_sale_data = value

    def to_dictionary(self) -> dict:
        dictionary = super(CardPaymentDataForResponse, self).to_dictionary()
        if self.brand is not None:
            dictionary['brand'] = self.brand
        if self.ecommerce_data is not None:
            dictionary['ecommerceData'] = self.ecommerce_data.to_dictionary()
        if self.point_of_sale_data is not None:
            dictionary['pointOfSaleData'] = self.point_of_sale_data.to_dictionary()
        return dictionary

    def from_dictionary(self, dictionary: dict) -> 'CardPaymentDataForResponse':
        super(CardPaymentDataForResponse, self).from_dictionary(dictionary)
        if 'brand' in dictionary:
            self.brand = dictionary['brand']
        if 'ecommerceData' in dictionary:
            if not isinstance(dictionary['ecommerceData'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['ecommerceData']))
            value = ECommerceDataForResponse()
            self.ecommerce_data = value.from_dictionary(dictionary['ecommerceData'])
        if 'pointOfSaleData' in dictionary:
            if not isinstance(dictionary['pointOfSaleData'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['pointOfSaleData']))
            value = PointOfSaleDataForResponse()
            self.point_of_sale_data = value.from_dictionary(dictionary['pointOfSaleData'])
        return self
