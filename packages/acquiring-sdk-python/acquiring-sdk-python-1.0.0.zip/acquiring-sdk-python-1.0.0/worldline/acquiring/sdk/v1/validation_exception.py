# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Optional

from .api_exception import ApiException


class ValidationException(ApiException):
    """
    Represents an error response from the Worldline Acquiring platform when validation of requests failed.
    """

    def __init__(self, status_code: int, response_body: str, type: Optional[str], title: Optional[str], status: Optional[int], detail: Optional[str], instance: Optional[str],
                 message: str = "The Worldline Acquiring platform returned an incorrect request error response"):
        super(ValidationException, self).__init__(status_code, response_body, type, title, status, detail, instance, message)
