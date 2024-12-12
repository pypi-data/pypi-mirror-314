# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Optional

from .api_exception import ApiException


class ReferenceException(ApiException):
    """
    Represents an error response from the Worldline Acquiring platform when a non-existing or removed object is trying to be accessed.
    """

    def __init__(self, status_code: int, response_body: str, type: Optional[str], title: Optional[str], status: Optional[int], detail: Optional[str], instance: Optional[str],
                 message: str = "The Worldline Acquiring platform returned a reference error response"):
        super(ReferenceException, self).__init__(status_code, response_body, type, title, status, detail, instance, message)
