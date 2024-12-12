# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import List, Optional

from worldline.acquiring.sdk.domain.data_object import DataObject


class TerminalData(DataObject):

    __allow_single_tap: Optional[bool] = None
    __card_reading_capabilities: Optional[List[str]] = None
    __cardholder_activated_terminal_level: Optional[str] = None
    __is_attended_terminal: Optional[bool] = None
    __pin_entry_capability: Optional[str] = None
    __terminal_id: Optional[str] = None
    __terminal_location: Optional[str] = None

    @property
    def allow_single_tap(self) -> Optional[bool]:
        """
        | Indicate whether the terminal allow one single tap for a contactless transaction followed by a PIN entry if the contactless transaction is refused

        Type: bool
        """
        return self.__allow_single_tap

    @allow_single_tap.setter
    def allow_single_tap(self, value: Optional[bool]) -> None:
        self.__allow_single_tap = value

    @property
    def card_reading_capabilities(self) -> Optional[List[str]]:
        """
        | Card reading capabilities of the terminal.

        Type: list[str]
        """
        return self.__card_reading_capabilities

    @card_reading_capabilities.setter
    def card_reading_capabilities(self, value: Optional[List[str]]) -> None:
        self.__card_reading_capabilities = value

    @property
    def cardholder_activated_terminal_level(self) -> Optional[str]:
        """
        | Level of security for a terminal activated with the use of a card (Cardholder Activated Terminal)

        Type: str
        """
        return self.__cardholder_activated_terminal_level

    @cardholder_activated_terminal_level.setter
    def cardholder_activated_terminal_level(self, value: Optional[str]) -> None:
        self.__cardholder_activated_terminal_level = value

    @property
    def is_attended_terminal(self) -> Optional[bool]:
        """
        | Indicate whether the terminal is attended or not

        Type: bool
        """
        return self.__is_attended_terminal

    @is_attended_terminal.setter
    def is_attended_terminal(self, value: Optional[bool]) -> None:
        self.__is_attended_terminal = value

    @property
    def pin_entry_capability(self) -> Optional[str]:
        """
        | The capabilities of the terminal to enter the PIN
        
        * UNKNOWN : Unspecified or unknown
        * PRESENT : Terminal has PIN entry capability
        * ABSENT : Terminal does not have PIN entry capability
        * MPOS_SOFTWARE_BASED_PIN : Mobile POS with PIN entry capability
        * NOT_OPERATIVE : Terminal has PIN entry capability but PIN pad is not currently operative

        Type: str
        """
        return self.__pin_entry_capability

    @pin_entry_capability.setter
    def pin_entry_capability(self, value: Optional[str]) -> None:
        self.__pin_entry_capability = value

    @property
    def terminal_id(self) -> Optional[str]:
        """
        | The identifier of the terminal

        Type: str
        """
        return self.__terminal_id

    @terminal_id.setter
    def terminal_id(self, value: Optional[str]) -> None:
        self.__terminal_id = value

    @property
    def terminal_location(self) -> Optional[str]:
        """
        | The location of the terminal

        Type: str
        """
        return self.__terminal_location

    @terminal_location.setter
    def terminal_location(self, value: Optional[str]) -> None:
        self.__terminal_location = value

    def to_dictionary(self) -> dict:
        dictionary = super(TerminalData, self).to_dictionary()
        if self.allow_single_tap is not None:
            dictionary['allowSingleTap'] = self.allow_single_tap
        if self.card_reading_capabilities is not None:
            dictionary['cardReadingCapabilities'] = []
            for element in self.card_reading_capabilities:
                if element is not None:
                    dictionary['cardReadingCapabilities'].append(element)
        if self.cardholder_activated_terminal_level is not None:
            dictionary['cardholderActivatedTerminalLevel'] = self.cardholder_activated_terminal_level
        if self.is_attended_terminal is not None:
            dictionary['isAttendedTerminal'] = self.is_attended_terminal
        if self.pin_entry_capability is not None:
            dictionary['pinEntryCapability'] = self.pin_entry_capability
        if self.terminal_id is not None:
            dictionary['terminalId'] = self.terminal_id
        if self.terminal_location is not None:
            dictionary['terminalLocation'] = self.terminal_location
        return dictionary

    def from_dictionary(self, dictionary: dict) -> 'TerminalData':
        super(TerminalData, self).from_dictionary(dictionary)
        if 'allowSingleTap' in dictionary:
            self.allow_single_tap = dictionary['allowSingleTap']
        if 'cardReadingCapabilities' in dictionary:
            if not isinstance(dictionary['cardReadingCapabilities'], list):
                raise TypeError('value \'{}\' is not a list'.format(dictionary['cardReadingCapabilities']))
            self.card_reading_capabilities = []
            for element in dictionary['cardReadingCapabilities']:
                self.card_reading_capabilities.append(element)
        if 'cardholderActivatedTerminalLevel' in dictionary:
            self.cardholder_activated_terminal_level = dictionary['cardholderActivatedTerminalLevel']
        if 'isAttendedTerminal' in dictionary:
            self.is_attended_terminal = dictionary['isAttendedTerminal']
        if 'pinEntryCapability' in dictionary:
            self.pin_entry_capability = dictionary['pinEntryCapability']
        if 'terminalId' in dictionary:
            self.terminal_id = dictionary['terminalId']
        if 'terminalLocation' in dictionary:
            self.terminal_location = dictionary['terminalLocation']
        return self
