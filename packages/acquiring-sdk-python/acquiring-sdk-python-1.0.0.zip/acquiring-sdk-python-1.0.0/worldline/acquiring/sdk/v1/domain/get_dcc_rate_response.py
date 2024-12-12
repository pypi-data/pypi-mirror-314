# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Optional

from .dcc_proposal import DccProposal

from worldline.acquiring.sdk.domain.data_object import DataObject


class GetDccRateResponse(DataObject):

    __disclaimer_display: Optional[str] = None
    __disclaimer_receipt: Optional[str] = None
    __proposal: Optional[DccProposal] = None
    __result: Optional[str] = None

    @property
    def disclaimer_display(self) -> Optional[str]:
        """
        | The disclaimer display

        Type: str
        """
        return self.__disclaimer_display

    @disclaimer_display.setter
    def disclaimer_display(self, value: Optional[str]) -> None:
        self.__disclaimer_display = value

    @property
    def disclaimer_receipt(self) -> Optional[str]:
        """
        | The disclaimer receipt

        Type: str
        """
        return self.__disclaimer_receipt

    @disclaimer_receipt.setter
    def disclaimer_receipt(self, value: Optional[str]) -> None:
        self.__disclaimer_receipt = value

    @property
    def proposal(self) -> Optional[DccProposal]:
        """
        Type: :class:`worldline.acquiring.sdk.v1.domain.dcc_proposal.DccProposal`
        """
        return self.__proposal

    @proposal.setter
    def proposal(self, value: Optional[DccProposal]) -> None:
        self.__proposal = value

    @property
    def result(self) -> Optional[str]:
        """
        | The result of the operation

        Type: str
        """
        return self.__result

    @result.setter
    def result(self, value: Optional[str]) -> None:
        self.__result = value

    def to_dictionary(self) -> dict:
        dictionary = super(GetDccRateResponse, self).to_dictionary()
        if self.disclaimer_display is not None:
            dictionary['disclaimerDisplay'] = self.disclaimer_display
        if self.disclaimer_receipt is not None:
            dictionary['disclaimerReceipt'] = self.disclaimer_receipt
        if self.proposal is not None:
            dictionary['proposal'] = self.proposal.to_dictionary()
        if self.result is not None:
            dictionary['result'] = self.result
        return dictionary

    def from_dictionary(self, dictionary: dict) -> 'GetDccRateResponse':
        super(GetDccRateResponse, self).from_dictionary(dictionary)
        if 'disclaimerDisplay' in dictionary:
            self.disclaimer_display = dictionary['disclaimerDisplay']
        if 'disclaimerReceipt' in dictionary:
            self.disclaimer_receipt = dictionary['disclaimerReceipt']
        if 'proposal' in dictionary:
            if not isinstance(dictionary['proposal'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['proposal']))
            value = DccProposal()
            self.proposal = value.from_dictionary(dictionary['proposal'])
        if 'result' in dictionary:
            self.result = dictionary['result']
        return self
