# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Mapping, Optional

from .get_payment_status_params import GetPaymentStatusParams

from worldline.acquiring.sdk.api_resource import ApiResource
from worldline.acquiring.sdk.call_context import CallContext
from worldline.acquiring.sdk.communication.response_exception import ResponseException
from worldline.acquiring.sdk.v1.domain.api_action_response import ApiActionResponse
from worldline.acquiring.sdk.v1.domain.api_action_response_for_refund import ApiActionResponseForRefund
from worldline.acquiring.sdk.v1.domain.api_capture_request import ApiCaptureRequest
from worldline.acquiring.sdk.v1.domain.api_increment_request import ApiIncrementRequest
from worldline.acquiring.sdk.v1.domain.api_increment_response import ApiIncrementResponse
from worldline.acquiring.sdk.v1.domain.api_payment_error_response import ApiPaymentErrorResponse
from worldline.acquiring.sdk.v1.domain.api_payment_refund_request import ApiPaymentRefundRequest
from worldline.acquiring.sdk.v1.domain.api_payment_request import ApiPaymentRequest
from worldline.acquiring.sdk.v1.domain.api_payment_resource import ApiPaymentResource
from worldline.acquiring.sdk.v1.domain.api_payment_response import ApiPaymentResponse
from worldline.acquiring.sdk.v1.domain.api_payment_reversal_request import ApiPaymentReversalRequest
from worldline.acquiring.sdk.v1.domain.api_reversal_response import ApiReversalResponse
from worldline.acquiring.sdk.v1.exception_factory import create_exception


class PaymentsClient(ApiResource):
    """
    Payments client. Thread-safe.
    """

    def __init__(self, parent: ApiResource, path_context: Optional[Mapping[str, str]]):
        """
        :param parent:       :class:`worldline.acquiring.sdk.api_resource.ApiResource`
        :param path_context: Mapping[str, str]
        """
        super(PaymentsClient, self).__init__(parent=parent, path_context=path_context)

    def process_payment(self, body: ApiPaymentRequest, context: Optional[CallContext] = None) -> ApiPaymentResponse:
        """
        Resource /processing/v1/{acquirerId}/{merchantId}/payments - Create payment

        See also https://docs.acquiring.worldline-solutions.com/api-reference#tag/Payments/operation/processPayment

        :param body:     :class:`worldline.acquiring.sdk.v1.domain.api_payment_request.ApiPaymentRequest`
        :param context:  :class:`worldline.acquiring.sdk.call_context.CallContext`
        :return: :class:`worldline.acquiring.sdk.v1.domain.api_payment_response.ApiPaymentResponse`
        :raise ValidationException: if the request was not correct and couldn't be processed (HTTP status code 400)
        :raise AuthorizationException: if the request was not allowed (HTTP status code 403)
        :raise ReferenceException: if an object was attempted to be referenced that doesn't exist or has been removed,
                   or there was a conflict (HTTP status code 404, 409 or 410)
        :raise PlatformException: if something went wrong at the Worldline Acquiring platform,
                   the Worldline Acquiring platform was unable to process a message from a downstream partner/acquirer,
                   or the service that you're trying to reach is temporary unavailable (HTTP status code 500, 502 or 503)
        :raise ApiException: if the Worldline Acquiring platform returned any other error
        """
        uri = self._instantiate_uri("/processing/v1/{acquirerId}/{merchantId}/payments", None)
        try:
            return self._communicator.post(
                    uri,
                    None,
                    None,
                    body,
                    ApiPaymentResponse,
                    context)

        except ResponseException as e:
            error_type = ApiPaymentErrorResponse
            error_object = self._communicator.marshaller.unmarshal(e.body, error_type)
            raise create_exception(e.status_code, e.body, error_object, context)

    def get_payment_status(self, payment_id: str, query: GetPaymentStatusParams, context: Optional[CallContext] = None) -> ApiPaymentResource:
        """
        Resource /processing/v1/{acquirerId}/{merchantId}/payments/{paymentId} - Retrieve payment

        See also https://docs.acquiring.worldline-solutions.com/api-reference#tag/Payments/operation/getPaymentStatus

        :param payment_id:  str
        :param query:       :class:`worldline.acquiring.sdk.v1.acquirer.merchant.payments.get_payment_status_params.GetPaymentStatusParams`
        :param context:     :class:`worldline.acquiring.sdk.call_context.CallContext`
        :return: :class:`worldline.acquiring.sdk.v1.domain.api_payment_resource.ApiPaymentResource`
        :raise ValidationException: if the request was not correct and couldn't be processed (HTTP status code 400)
        :raise AuthorizationException: if the request was not allowed (HTTP status code 403)
        :raise ReferenceException: if an object was attempted to be referenced that doesn't exist or has been removed,
                   or there was a conflict (HTTP status code 404, 409 or 410)
        :raise PlatformException: if something went wrong at the Worldline Acquiring platform,
                   the Worldline Acquiring platform was unable to process a message from a downstream partner/acquirer,
                   or the service that you're trying to reach is temporary unavailable (HTTP status code 500, 502 or 503)
        :raise ApiException: if the Worldline Acquiring platform returned any other error
        """
        path_context = {
            "paymentId": payment_id,
        }
        uri = self._instantiate_uri("/processing/v1/{acquirerId}/{merchantId}/payments/{paymentId}", path_context)
        try:
            return self._communicator.get(
                    uri,
                    None,
                    query,
                    ApiPaymentResource,
                    context)

        except ResponseException as e:
            error_type = ApiPaymentErrorResponse
            error_object = self._communicator.marshaller.unmarshal(e.body, error_type)
            raise create_exception(e.status_code, e.body, error_object, context)

    def simple_capture_of_payment(self, payment_id: str, body: ApiCaptureRequest, context: Optional[CallContext] = None) -> ApiActionResponse:
        """
        Resource /processing/v1/{acquirerId}/{merchantId}/payments/{paymentId}/captures - Capture payment

        See also https://docs.acquiring.worldline-solutions.com/api-reference#tag/Payments/operation/simpleCaptureOfPayment

        :param payment_id:  str
        :param body:        :class:`worldline.acquiring.sdk.v1.domain.api_capture_request.ApiCaptureRequest`
        :param context:     :class:`worldline.acquiring.sdk.call_context.CallContext`
        :return: :class:`worldline.acquiring.sdk.v1.domain.api_action_response.ApiActionResponse`
        :raise ValidationException: if the request was not correct and couldn't be processed (HTTP status code 400)
        :raise AuthorizationException: if the request was not allowed (HTTP status code 403)
        :raise ReferenceException: if an object was attempted to be referenced that doesn't exist or has been removed,
                   or there was a conflict (HTTP status code 404, 409 or 410)
        :raise PlatformException: if something went wrong at the Worldline Acquiring platform,
                   the Worldline Acquiring platform was unable to process a message from a downstream partner/acquirer,
                   or the service that you're trying to reach is temporary unavailable (HTTP status code 500, 502 or 503)
        :raise ApiException: if the Worldline Acquiring platform returned any other error
        """
        path_context = {
            "paymentId": payment_id,
        }
        uri = self._instantiate_uri("/processing/v1/{acquirerId}/{merchantId}/payments/{paymentId}/captures", path_context)
        try:
            return self._communicator.post(
                    uri,
                    None,
                    None,
                    body,
                    ApiActionResponse,
                    context)

        except ResponseException as e:
            error_type = ApiPaymentErrorResponse
            error_object = self._communicator.marshaller.unmarshal(e.body, error_type)
            raise create_exception(e.status_code, e.body, error_object, context)

    def reverse_authorization(self, payment_id: str, body: ApiPaymentReversalRequest, context: Optional[CallContext] = None) -> ApiReversalResponse:
        """
        Resource /processing/v1/{acquirerId}/{merchantId}/payments/{paymentId}/authorization-reversals - Reverse authorization

        See also https://docs.acquiring.worldline-solutions.com/api-reference#tag/Payments/operation/reverseAuthorization

        :param payment_id:  str
        :param body:        :class:`worldline.acquiring.sdk.v1.domain.api_payment_reversal_request.ApiPaymentReversalRequest`
        :param context:     :class:`worldline.acquiring.sdk.call_context.CallContext`
        :return: :class:`worldline.acquiring.sdk.v1.domain.api_reversal_response.ApiReversalResponse`
        :raise ValidationException: if the request was not correct and couldn't be processed (HTTP status code 400)
        :raise AuthorizationException: if the request was not allowed (HTTP status code 403)
        :raise ReferenceException: if an object was attempted to be referenced that doesn't exist or has been removed,
                   or there was a conflict (HTTP status code 404, 409 or 410)
        :raise PlatformException: if something went wrong at the Worldline Acquiring platform,
                   the Worldline Acquiring platform was unable to process a message from a downstream partner/acquirer,
                   or the service that you're trying to reach is temporary unavailable (HTTP status code 500, 502 or 503)
        :raise ApiException: if the Worldline Acquiring platform returned any other error
        """
        path_context = {
            "paymentId": payment_id,
        }
        uri = self._instantiate_uri("/processing/v1/{acquirerId}/{merchantId}/payments/{paymentId}/authorization-reversals", path_context)
        try:
            return self._communicator.post(
                    uri,
                    None,
                    None,
                    body,
                    ApiReversalResponse,
                    context)

        except ResponseException as e:
            error_type = ApiPaymentErrorResponse
            error_object = self._communicator.marshaller.unmarshal(e.body, error_type)
            raise create_exception(e.status_code, e.body, error_object, context)

    def increment_payment(self, payment_id: str, body: ApiIncrementRequest, context: Optional[CallContext] = None) -> ApiIncrementResponse:
        """
        Resource /processing/v1/{acquirerId}/{merchantId}/payments/{paymentId}/increments - Increment authorization

        See also https://docs.acquiring.worldline-solutions.com/api-reference#tag/Payments/operation/incrementPayment

        :param payment_id:  str
        :param body:        :class:`worldline.acquiring.sdk.v1.domain.api_increment_request.ApiIncrementRequest`
        :param context:     :class:`worldline.acquiring.sdk.call_context.CallContext`
        :return: :class:`worldline.acquiring.sdk.v1.domain.api_increment_response.ApiIncrementResponse`
        :raise ValidationException: if the request was not correct and couldn't be processed (HTTP status code 400)
        :raise AuthorizationException: if the request was not allowed (HTTP status code 403)
        :raise ReferenceException: if an object was attempted to be referenced that doesn't exist or has been removed,
                   or there was a conflict (HTTP status code 404, 409 or 410)
        :raise PlatformException: if something went wrong at the Worldline Acquiring platform,
                   the Worldline Acquiring platform was unable to process a message from a downstream partner/acquirer,
                   or the service that you're trying to reach is temporary unavailable (HTTP status code 500, 502 or 503)
        :raise ApiException: if the Worldline Acquiring platform returned any other error
        """
        path_context = {
            "paymentId": payment_id,
        }
        uri = self._instantiate_uri("/processing/v1/{acquirerId}/{merchantId}/payments/{paymentId}/increments", path_context)
        try:
            return self._communicator.post(
                    uri,
                    None,
                    None,
                    body,
                    ApiIncrementResponse,
                    context)

        except ResponseException as e:
            error_type = ApiPaymentErrorResponse
            error_object = self._communicator.marshaller.unmarshal(e.body, error_type)
            raise create_exception(e.status_code, e.body, error_object, context)

    def create_refund(self, payment_id: str, body: ApiPaymentRefundRequest, context: Optional[CallContext] = None) -> ApiActionResponseForRefund:
        """
        Resource /processing/v1/{acquirerId}/{merchantId}/payments/{paymentId}/refunds - Refund payment

        See also https://docs.acquiring.worldline-solutions.com/api-reference#tag/Payments/operation/createRefund

        :param payment_id:  str
        :param body:        :class:`worldline.acquiring.sdk.v1.domain.api_payment_refund_request.ApiPaymentRefundRequest`
        :param context:     :class:`worldline.acquiring.sdk.call_context.CallContext`
        :return: :class:`worldline.acquiring.sdk.v1.domain.api_action_response_for_refund.ApiActionResponseForRefund`
        :raise ValidationException: if the request was not correct and couldn't be processed (HTTP status code 400)
        :raise AuthorizationException: if the request was not allowed (HTTP status code 403)
        :raise ReferenceException: if an object was attempted to be referenced that doesn't exist or has been removed,
                   or there was a conflict (HTTP status code 404, 409 or 410)
        :raise PlatformException: if something went wrong at the Worldline Acquiring platform,
                   the Worldline Acquiring platform was unable to process a message from a downstream partner/acquirer,
                   or the service that you're trying to reach is temporary unavailable (HTTP status code 500, 502 or 503)
        :raise ApiException: if the Worldline Acquiring platform returned any other error
        """
        path_context = {
            "paymentId": payment_id,
        }
        uri = self._instantiate_uri("/processing/v1/{acquirerId}/{merchantId}/payments/{paymentId}/refunds", path_context)
        try:
            return self._communicator.post(
                    uri,
                    None,
                    None,
                    body,
                    ApiActionResponseForRefund,
                    context)

        except ResponseException as e:
            error_type = ApiPaymentErrorResponse
            error_object = self._communicator.marshaller.unmarshal(e.body, error_type)
            raise create_exception(e.status_code, e.body, error_object, context)
