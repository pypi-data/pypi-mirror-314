# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Optional

from .api_exception import ApiException


class PlatformException(ApiException):
    """
    Represents an error response from the Worldline Acquiring platform when something went wrong at the Worldline Acquiring platform or further downstream.
    """

    def __init__(self, status_code: int, response_body: str, type: Optional[str], title: Optional[str], status: Optional[int], detail: Optional[str], instance: Optional[str],
                 message: str = "The Worldline Acquiring platform returned an error response"):
        super(PlatformException, self).__init__(status_code, response_body, type, title, status, detail, instance, message)
