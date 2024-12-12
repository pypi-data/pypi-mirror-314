# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Optional


class ApiException(RuntimeError):
    """
    Represents an error response from the Worldline Acquiring platform.
    """

    def __init__(self, status_code: int, response_body: str, type: Optional[str], title: Optional[str], status: Optional[int], detail: Optional[str], instance: Optional[str],
                 message: str = "The Worldline Acquiring platform returned an error response"):
        super(ApiException, self).__init__(message)
        self.__status_code = status_code
        self.__response_body = response_body
        self.__type = type
        self.__title = title
        self.__status = status
        self.__detail = detail
        self.__instance = instance

    @property
    def status_code(self) -> int:
        """
        :return: The HTTP status code that was returned by the Worldline Acquiring platform.
        """
        return self.__status_code

    @property
    def response_body(self) -> str:
        """
        :return: The raw response body that was returned by the Worldline Acquiring platform.
        """
        return self.__response_body

    @property
    def type(self) -> Optional[str]:
        """
        :return: The type received from the Worldline Acquiring platform if available.
        """
        return self.__type

    @property
    def title(self) -> Optional[str]:
        """
        :return: The title received from the Worldline Acquiring platform if available.
        """
        return self.__title

    @property
    def status(self) -> Optional[int]:
        """
        :return: The status received from the Worldline Acquiring platform if available.
        """
        return self.__status

    @property
    def detail(self) -> Optional[str]:
        """
        :return: The detail received from the Worldline Acquiring platform if available.
        """
        return self.__detail

    @property
    def instance(self) -> Optional[str]:
        """
        :return: The instance received from the Worldline Acquiring platform if available.
        """
        return self.__instance

    def __str__(self):
        string = super(ApiException, self).__str__()
        if self.__status_code > 0:
            string += "; status_code=" + str(self.__status_code)
        if self.__response_body:
            string += "; response_body='" + self.__response_body + "'"
        return str(string)
