# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Mapping, Optional

from .get_refund_params import GetRefundParams

from worldline.acquiring.sdk.api_resource import ApiResource
from worldline.acquiring.sdk.call_context import CallContext
from worldline.acquiring.sdk.communication.response_exception import ResponseException
from worldline.acquiring.sdk.v1.domain.api_action_response_for_refund import ApiActionResponseForRefund
from worldline.acquiring.sdk.v1.domain.api_capture_request_for_refund import ApiCaptureRequestForRefund
from worldline.acquiring.sdk.v1.domain.api_payment_error_response import ApiPaymentErrorResponse
from worldline.acquiring.sdk.v1.domain.api_payment_reversal_request import ApiPaymentReversalRequest
from worldline.acquiring.sdk.v1.domain.api_refund_request import ApiRefundRequest
from worldline.acquiring.sdk.v1.domain.api_refund_resource import ApiRefundResource
from worldline.acquiring.sdk.v1.domain.api_refund_response import ApiRefundResponse
from worldline.acquiring.sdk.v1.exception_factory import create_exception


class RefundsClient(ApiResource):
    """
    Refunds client. Thread-safe.
    """

    def __init__(self, parent: ApiResource, path_context: Optional[Mapping[str, str]]):
        """
        :param parent:       :class:`worldline.acquiring.sdk.api_resource.ApiResource`
        :param path_context: Mapping[str, str]
        """
        super(RefundsClient, self).__init__(parent=parent, path_context=path_context)

    def process_standalone_refund(self, body: ApiRefundRequest, context: Optional[CallContext] = None) -> ApiRefundResponse:
        """
        Resource /processing/v1/{acquirerId}/{merchantId}/refunds - Create standalone refund

        See also https://docs.acquiring.worldline-solutions.com/api-reference#tag/Refunds/operation/processStandaloneRefund

        :param body:     :class:`worldline.acquiring.sdk.v1.domain.api_refund_request.ApiRefundRequest`
        :param context:  :class:`worldline.acquiring.sdk.call_context.CallContext`
        :return: :class:`worldline.acquiring.sdk.v1.domain.api_refund_response.ApiRefundResponse`
        :raise ValidationException: if the request was not correct and couldn't be processed (HTTP status code 400)
        :raise AuthorizationException: if the request was not allowed (HTTP status code 403)
        :raise ReferenceException: if an object was attempted to be referenced that doesn't exist or has been removed,
                   or there was a conflict (HTTP status code 404, 409 or 410)
        :raise PlatformException: if something went wrong at the Worldline Acquiring platform,
                   the Worldline Acquiring platform was unable to process a message from a downstream partner/acquirer,
                   or the service that you're trying to reach is temporary unavailable (HTTP status code 500, 502 or 503)
        :raise ApiException: if the Worldline Acquiring platform returned any other error
        """
        uri = self._instantiate_uri("/processing/v1/{acquirerId}/{merchantId}/refunds", None)
        try:
            return self._communicator.post(
                    uri,
                    None,
                    None,
                    body,
                    ApiRefundResponse,
                    context)

        except ResponseException as e:
            error_type = ApiPaymentErrorResponse
            error_object = self._communicator.marshaller.unmarshal(e.body, error_type)
            raise create_exception(e.status_code, e.body, error_object, context)

    def get_refund(self, refund_id: str, query: GetRefundParams, context: Optional[CallContext] = None) -> ApiRefundResource:
        """
        Resource /processing/v1/{acquirerId}/{merchantId}/refunds/{refundId} - Retrieve refund

        See also https://docs.acquiring.worldline-solutions.com/api-reference#tag/Refunds/operation/getRefund

        :param refund_id:  str
        :param query:      :class:`worldline.acquiring.sdk.v1.acquirer.merchant.refunds.get_refund_params.GetRefundParams`
        :param context:    :class:`worldline.acquiring.sdk.call_context.CallContext`
        :return: :class:`worldline.acquiring.sdk.v1.domain.api_refund_resource.ApiRefundResource`
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
            "refundId": refund_id,
        }
        uri = self._instantiate_uri("/processing/v1/{acquirerId}/{merchantId}/refunds/{refundId}", path_context)
        try:
            return self._communicator.get(
                    uri,
                    None,
                    query,
                    ApiRefundResource,
                    context)

        except ResponseException as e:
            error_type = ApiPaymentErrorResponse
            error_object = self._communicator.marshaller.unmarshal(e.body, error_type)
            raise create_exception(e.status_code, e.body, error_object, context)

    def capture_refund(self, refund_id: str, body: ApiCaptureRequestForRefund, context: Optional[CallContext] = None) -> ApiActionResponseForRefund:
        """
        Resource /processing/v1/{acquirerId}/{merchantId}/refunds/{refundId}/captures - Capture refund

        See also https://docs.acquiring.worldline-solutions.com/api-reference#tag/Refunds/operation/captureRefund

        :param refund_id:  str
        :param body:       :class:`worldline.acquiring.sdk.v1.domain.api_capture_request_for_refund.ApiCaptureRequestForRefund`
        :param context:    :class:`worldline.acquiring.sdk.call_context.CallContext`
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
            "refundId": refund_id,
        }
        uri = self._instantiate_uri("/processing/v1/{acquirerId}/{merchantId}/refunds/{refundId}/captures", path_context)
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

    def reverse_refund_authorization(self, refund_id: str, body: ApiPaymentReversalRequest, context: Optional[CallContext] = None) -> ApiActionResponseForRefund:
        """
        Resource /processing/v1/{acquirerId}/{merchantId}/refunds/{refundId}/authorization-reversals - Reverse refund authorization

        See also https://docs.acquiring.worldline-solutions.com/api-reference#tag/Refunds/operation/reverseRefundAuthorization

        :param refund_id:  str
        :param body:       :class:`worldline.acquiring.sdk.v1.domain.api_payment_reversal_request.ApiPaymentReversalRequest`
        :param context:    :class:`worldline.acquiring.sdk.call_context.CallContext`
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
            "refundId": refund_id,
        }
        uri = self._instantiate_uri("/processing/v1/{acquirerId}/{merchantId}/refunds/{refundId}/authorization-reversals", path_context)
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
