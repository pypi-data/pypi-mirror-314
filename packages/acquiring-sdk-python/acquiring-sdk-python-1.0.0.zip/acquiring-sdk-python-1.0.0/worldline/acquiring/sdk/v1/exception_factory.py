# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Any, Optional

from .api_exception import ApiException
from .authorization_exception import AuthorizationException
from .platform_exception import PlatformException
from .reference_exception import ReferenceException
from .validation_exception import ValidationException

from worldline.acquiring.sdk.call_context import CallContext
from worldline.acquiring.sdk.v1.domain.api_payment_error_response import ApiPaymentErrorResponse


def create_exception(status_code: int, body: str, error_object: Any, context: Optional[CallContext]) -> Exception:
    """Return a raisable API exception based on the error object given"""
    def create_exception_from_response_fields(type: Optional[str], title: Optional[str], status: Optional[int], detail: Optional[str], instance: Optional[str]) -> Exception:
        # get error based on status code, defaulting to ApiException
        return ERROR_MAP.get(status_code, ApiException)(status_code, body, type, title, status, detail, instance)

    if not isinstance(error_object, ApiPaymentErrorResponse):
        raise ValueError("Unsupported error object encountered: {}".format(error_object.__class__.__name__))

    return create_exception_from_response_fields(error_object.type, error_object.title, error_object.status, error_object.detail, error_object.instance)


ERROR_MAP = {
    400: ValidationException,
    403: AuthorizationException,
    404: ReferenceException,
    409: ReferenceException,
    410: ReferenceException,
    500: PlatformException,
    502: PlatformException,
    503: PlatformException,
}
