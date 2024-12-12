# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Mapping, Optional

from worldline.acquiring.sdk.api_resource import ApiResource
from worldline.acquiring.sdk.call_context import CallContext
from worldline.acquiring.sdk.communication.response_exception import ResponseException
from worldline.acquiring.sdk.v1.domain.api_account_verification_request import ApiAccountVerificationRequest
from worldline.acquiring.sdk.v1.domain.api_account_verification_response import ApiAccountVerificationResponse
from worldline.acquiring.sdk.v1.domain.api_payment_error_response import ApiPaymentErrorResponse
from worldline.acquiring.sdk.v1.exception_factory import create_exception


class AccountVerificationsClient(ApiResource):
    """
    AccountVerifications client. Thread-safe.
    """

    def __init__(self, parent: ApiResource, path_context: Optional[Mapping[str, str]]):
        """
        :param parent:       :class:`worldline.acquiring.sdk.api_resource.ApiResource`
        :param path_context: Mapping[str, str]
        """
        super(AccountVerificationsClient, self).__init__(parent=parent, path_context=path_context)

    def process_account_verification(self, body: ApiAccountVerificationRequest, context: Optional[CallContext] = None) -> ApiAccountVerificationResponse:
        """
        Resource /processing/v1/{acquirerId}/{merchantId}/account-verifications - Verify account

        See also https://docs.acquiring.worldline-solutions.com/api-reference#tag/Account-Verifications/operation/processAccountVerification

        :param body:     :class:`worldline.acquiring.sdk.v1.domain.api_account_verification_request.ApiAccountVerificationRequest`
        :param context:  :class:`worldline.acquiring.sdk.call_context.CallContext`
        :return: :class:`worldline.acquiring.sdk.v1.domain.api_account_verification_response.ApiAccountVerificationResponse`
        :raise ValidationException: if the request was not correct and couldn't be processed (HTTP status code 400)
        :raise AuthorizationException: if the request was not allowed (HTTP status code 403)
        :raise ReferenceException: if an object was attempted to be referenced that doesn't exist or has been removed,
                   or there was a conflict (HTTP status code 404, 409 or 410)
        :raise PlatformException: if something went wrong at the Worldline Acquiring platform,
                   the Worldline Acquiring platform was unable to process a message from a downstream partner/acquirer,
                   or the service that you're trying to reach is temporary unavailable (HTTP status code 500, 502 or 503)
        :raise ApiException: if the Worldline Acquiring platform returned any other error
        """
        uri = self._instantiate_uri("/processing/v1/{acquirerId}/{merchantId}/account-verifications", None)
        try:
            return self._communicator.post(
                    uri,
                    None,
                    None,
                    body,
                    ApiAccountVerificationResponse,
                    context)

        except ResponseException as e:
            error_type = ApiPaymentErrorResponse
            error_object = self._communicator.marshaller.unmarshal(e.body, error_type)
            raise create_exception(e.status_code, e.body, error_object, context)
