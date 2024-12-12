from datetime import datetime, timedelta
from json import loads
from threading import Lock
from typing import Iterable, Optional, Sequence, Tuple
from urllib.parse import ParseResult

from .authenticator import Authenticator
from .oauth2_exception import OAuth2Exception

from worldline.acquiring.sdk.communicator_configuration import CommunicatorConfiguration
from worldline.acquiring.sdk.communication.default_connection import DefaultConnection
from worldline.acquiring.sdk.communication.request_header import RequestHeader


class OAuth2Authenticator(Authenticator):
    """
    OAuth2 Authenticator implementation.
    """

    def __init__(self, communicator_configuration: CommunicatorConfiguration):
        """
        Constructs a new OAuth2Authenticator instance using the provided CommunicatorConfiguration.

        :param communicator_configuration: The configuration object containing the OAuth2 client id, client secret
         and token URI, connection timeout, and socket timeout. None of these can be None or empty,
         and the timeout values must be positive.
        """
        Authenticator.__init__(self)

        if not communicator_configuration.oauth2_client_id:
            raise ValueError("oauth2_client_id is required")
        if not communicator_configuration.oauth2_client_secret:
            raise ValueError("oauth2_client_secret is required")
        if not communicator_configuration.oauth2_token_uri:
            raise ValueError("oauth2_client_token_uri is required")
        if communicator_configuration.connect_timeout <= 0:
            raise ValueError("connect_timeout must be positive")
        if communicator_configuration.socket_timeout <= 0:
            raise ValueError("socket_timeout must be positive")

        self.__client_id = communicator_configuration.oauth2_client_id
        self.__client_secret = communicator_configuration.oauth2_client_secret
        self.__token_uri = communicator_configuration.oauth2_token_uri
        self.__connect_timeout = communicator_configuration.connect_timeout
        self.__socket_timeout = communicator_configuration.socket_timeout
        self.__proxy_configuration = communicator_configuration.proxy_configuration

        # Only a limited amount of scopes may be sent in one request.
        # While at the moment all scopes fit in one request, keep this code so we can easily add more token types if necessary.
        # The empty path will ensure that all paths will match, as each full path ends with an empty string.
        self.__access_tokens = [
            self.__TokenType("", "processing_payment", "processing_refund", "processing_credittransfer",
                             "processing_accountverification",
                             "processing_operation_reverse", "processing_dcc_rate", "services_ping"),
        ]

    def get_authorization(self, http_method: Optional[str], resource_uri: Optional[ParseResult],
                          request_headers: Optional[Sequence[RequestHeader]]) -> str:
        token_type = self.get_token_type(resource_uri.path)
        with token_type.lock:
            if not token_type.access_token or token_type.access_token_expiration < datetime.now():
                token_type.access_token, token_type.access_token_expiration = self.__get_access_token(token_type.scopes)

            return "Bearer " + token_type.access_token

    def __get_access_token(self, scopes: str) -> Tuple[str, datetime]:
        with DefaultConnection(connect_timeout=self.__connect_timeout,
                               socket_timeout=self.__socket_timeout,
                               max_connections=1,
                               proxy_configuration=self.__proxy_configuration) as connection:

            request_headers = [RequestHeader("Content-Type", "application/x-www-form-urlencoded")]
            body = "grant_type=client_credentials&client_id=%s&client_secret=%s&scope=%s" \
                   % (self.__client_id, self.__client_secret, scopes)

            start_time = datetime.now()

            status, _, chunks = connection.post(self.__token_uri, request_headers, body)
            response_body = OAuth2Authenticator.__collect_chunks(chunks)
            access_token_response = loads(response_body)

            if status != 200:
                error_description = access_token_response["error_description"] if "error_description" in access_token_response else None
                raise OAuth2Exception("There was an error while retrieving the OAuth2 access token: %s - %s"
                                      % (access_token_response["error"], error_description))

            expiration_time = start_time + timedelta(seconds=access_token_response["expires_in"])
            return access_token_response["access_token"], expiration_time

    def get_token_type(self, path: str):
        for token_type_entry in self.__access_tokens:
            path_with_trailing_slash = token_type_entry.path + "/"
            if path.endswith(token_type_entry.path) or path_with_trailing_slash in path:
                return token_type_entry

        raise OAuth2Exception("Scope could not be found for path " + path)

    @staticmethod
    def __collect_chunks(chunks: Iterable[bytes]) -> str:
        collected_body = b""
        for chunk in chunks:
            collected_body += chunk
        return collected_body.decode('utf-8')

    class __TokenType:
        def __init__(self, path, *scopes):
            self.scopes = str.join(" ", scopes)
            self.path = path
            self.access_token = None
            self.access_token_expiration = None

            # Python does not provide a read-write lock implementation out-of-the-box.
            # Use a simple Lock instead. That does mean that multiple reads have to wait on each other,
            # but the read-only part is limited to checking the access token and its expiration timestamp,
            # which should take only a very short time
            self.lock = Lock()
