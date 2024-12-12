from configparser import ConfigParser, NoOptionError
from typing import Optional, Union
from urllib.parse import urlparse, ParseResult

from .proxy_configuration import ProxyConfiguration

from worldline.acquiring.sdk.authentication.authorization_type import AuthorizationType
from worldline.acquiring.sdk.domain.shopping_cart_extension import ShoppingCartExtension


# pylint: disable=too-many-instance-attributes
# Necessary to load information from config
class CommunicatorConfiguration(object):
    """
    Configuration for the communicator.
    """
    # The default number of maximum connections.
    DEFAULT_MAX_CONNECTIONS = 10

    __api_endpoint: Optional[ParseResult] = None
    __connect_timeout: Optional[int] = None
    __socket_timeout: Optional[int] = None
    __max_connections: Optional[int] = None
    __authorization_type: Optional[str] = None
    __authorization_id: Optional[str] = None
    __authorization_secret: Optional[str] = None
    __oauth2_token_uri: Optional[str] = None
    __proxy_configuration: Optional[ProxyConfiguration] = None
    __integrator: Optional[str] = None
    __shopping_cart_extension: Optional[ShoppingCartExtension] = None

    def __init__(self, properties: Optional[ConfigParser] = None,
                 api_endpoint: Union[str, ParseResult, None] = None,
                 authorization_id: Optional[str] = None, authorization_secret: Optional[str] = None,
                 oauth2_client_id: Optional[str] = None, oauth2_client_secret: Optional[str] = None,
                 oauth2_token_uri: Optional[str] = None,
                 authorization_type: Optional[str] = None,
                 connect_timeout: Optional[int] = None, socket_timeout: Optional[int] = None,
                 max_connections: Optional[int] = None, proxy_configuration: Optional[ProxyConfiguration] = None,
                 integrator: Optional[str] = None, shopping_cart_extension: Optional[ShoppingCartExtension] = None):
        """
        :param properties: a ConfigParser.ConfigParser object containing configuration data
        :param connect_timeout: connection timeout for the network communication in seconds
        :param socket_timeout: socket timeout for the network communication in seconds
        :param max_connections: The maximum number of connections in the connection pool
        """
        if properties and properties.sections() and properties.options("AcquiringSDK"):
            self.__api_endpoint = self.__get_endpoint(properties)
            authorization = properties.get("AcquiringSDK", "acquiring.api.authorizationType")
            self.__authorization_type = AuthorizationType.get_authorization(authorization)
            self.__connect_timeout = int(properties.get("AcquiringSDK", "acquiring.api.connectTimeout"))
            self.__socket_timeout = int(properties.get("AcquiringSDK", "acquiring.api.socketTimeout"))
            self.__max_connections = self.__get_property(properties, "acquiring.api.maxConnections",
                                                         self.DEFAULT_MAX_CONNECTIONS)
            try:
                self.oauth2_token_uri = properties.get("AcquiringSDK", "acquiring.api.oauth2.tokenUri")
            except NoOptionError:
                self.oauth2_token_uri = None
            try:
                proxy_uri = properties.get("AcquiringSDK", "acquiring.api.proxy.uri")
            except NoOptionError:
                proxy_uri = None
            try:
                proxy_user = properties.get("AcquiringSDK", "acquiring.api.proxy.username")
            except NoOptionError:
                proxy_user = None
            try:
                proxy_pass = properties.get("AcquiringSDK", "acquiring.api.proxy.password")
            except NoOptionError:
                proxy_pass = None
            if proxy_uri is not None:
                self.__proxy_configuration = ProxyConfiguration.from_uri(proxy_uri, proxy_user, proxy_pass)
            else:
                self.__proxy_configuration = None
            try:
                self.__integrator = properties.get("AcquiringSDK", "acquiring.api.integrator")
            except NoOptionError:
                self.__integrator = None
            try:
                self.__shopping_cart_extension = self.__get_shopping_cart_extension(properties)
            except NoOptionError:
                self.__shopping_cart_extension = None

        if api_endpoint:
            self.api_endpoint = api_endpoint
        if authorization_id:
            self.authorization_id = authorization_id
        if authorization_secret:
            self.authorization_secret = authorization_secret
        if oauth2_client_id:
            self.oauth2_client_id = oauth2_client_id
        if oauth2_client_secret:
            self.oauth2_client_secret = oauth2_client_secret
        if oauth2_token_uri:
            self.oauth2_token_uri = oauth2_token_uri
        if authorization_type:
            self.authorization_type = authorization_type
        if connect_timeout:
            self.connect_timeout = connect_timeout
        if socket_timeout:
            self.socket_timeout = socket_timeout
        if max_connections:
            self.max_connections = max_connections
        if proxy_configuration:
            self.proxy_configuration = proxy_configuration
        if integrator:
            self.integrator = integrator
        if shopping_cart_extension:
            self.shopping_cart_extension = shopping_cart_extension

    @staticmethod
    def __get_property(properties: ConfigParser, key: str, default_value: int) -> int:
        try:
            property_value = properties.get("AcquiringSDK", key)
        except NoOptionError:
            property_value = None
        if property_value is not None:
            return int(property_value)
        else:
            return default_value

    def __get_endpoint(self, properties: ConfigParser) -> ParseResult:
        host = properties.get("AcquiringSDK", "acquiring.api.endpoint.host")
        try:
            scheme = properties.get("AcquiringSDK", "acquiring.api.endpoint.scheme")
        except NoOptionError:
            scheme = None
        try:
            port = properties.get("AcquiringSDK", "acquiring.api.endpoint.port")
        except NoOptionError:
            port = None
        if scheme:
            if port:
                return self.__create_uri(scheme, host, int(port))
            else:
                return self.__create_uri(scheme, host, -1)
        elif port:
            return self.__create_uri("https", host, int(port))
        else:
            return self.__create_uri("https", host, -1)

    @staticmethod
    def __create_uri(scheme: str, host: str, port: int) -> ParseResult:
        if port != -1:
            uri = scheme + "://" + host + ":" + str(port)
        else:
            uri = scheme + "://" + host
        url = urlparse(uri)
        if not url.scheme.lower() in ["http", "https"] or not url.netloc:
            raise ValueError("Unable to construct endpoint URI")
        return url

    @staticmethod
    def __get_shopping_cart_extension(properties: ConfigParser) -> Optional[ShoppingCartExtension]:
        try:
            creator = properties.get("AcquiringSDK", "acquiring.api.shoppingCartExtension.creator")
        except NoOptionError:
            creator = None
        try:
            name = properties.get("AcquiringSDK", "acquiring.api.shoppingCartExtension.name")
        except NoOptionError:
            name = None
        try:
            version = properties.get("AcquiringSDK", "acquiring.api.shoppingCartExtension.version")
        except NoOptionError:
            version = None
        try:
            extension_id = properties.get("AcquiringSDK", "acquiring.api.shoppingCartExtension.extensionId")
        except NoOptionError:
            extension_id = None
        if creator is None and name is None and version is None and extension_id is None:
            return None
        else:
            return ShoppingCartExtension(creator, name, version, extension_id)

    @property
    def api_endpoint(self) -> Optional[ParseResult]:
        """
        The Worldline Acquiring platform API endpoint URI.
        """
        return self.__api_endpoint

    @api_endpoint.setter
    def api_endpoint(self, api_endpoint: Union[str, ParseResult, None]) -> None:
        if isinstance(api_endpoint, str):
            api_endpoint = urlparse(str(api_endpoint))
        if api_endpoint is not None and api_endpoint.path:
            raise ValueError("apiEndpoint should not contain a path")
        if api_endpoint is not None and \
                (api_endpoint.username is not None or api_endpoint.query or api_endpoint.fragment):
            raise ValueError("apiEndpoint should not contain user info, query or fragment")
        self.__api_endpoint = api_endpoint

    @property
    def authorization_id(self) -> Optional[str]:
        """
        An id used for authorization. The meaning of this id is different for each authorization type.
        For instance, for OAuth2 this is the client id.
        """
        return self.__authorization_id

    @authorization_id.setter
    def authorization_id(self, authorization_id: Optional[str]) -> None:
        self.__authorization_id = authorization_id

    @property
    def authorization_secret(self) -> Optional[str]:
        """
        A secret used for authorization. The meaning of this secret is different for each authorization type.
        For instance, for OAuth2 this is the client secret.
        """
        return self.__authorization_secret

    @authorization_secret.setter
    def authorization_secret(self, authorization_secret: Optional[str]) -> None:
        self.__authorization_secret = authorization_secret

    @ property
    def oauth2_client_id(self) -> Optional[str]:
        """
        The OAuth2 client id.

        This property is an alias for authorization_id
        """
        return self.authorization_id

    @ oauth2_client_id.setter
    def oauth2_client_id(self, oauth2_client_id: Optional[str]) -> None:
        self.authorization_id = oauth2_client_id

    @ property
    def oauth2_client_secret(self) -> Optional[str]:
        """
        The OAuth2 client secret.

        This property is an alias for authorization_secret
        """
        return self.__authorization_secret

    @ oauth2_client_secret.setter
    def oauth2_client_secret(self, oauth2_client_secret: Optional[str]) -> None:
        self.authorization_secret = oauth2_client_secret

    @ property
    def oauth2_token_uri(self) -> Optional[str]:
        return self.__oauth2_token_uri

    @ oauth2_token_uri.setter
    def oauth2_token_uri(self, oauth2_token_uri: Optional[str]) -> None:
        self.__oauth2_token_uri = oauth2_token_uri

    @property
    def authorization_type(self) -> Optional[str]:
        return self.__authorization_type

    @authorization_type.setter
    def authorization_type(self, authorization_type: Optional[str]) -> None:
        self.__authorization_type = authorization_type

    @property
    def connect_timeout(self) -> Optional[int]:
        """Connection timeout for the underlying network communication in seconds"""
        return self.__connect_timeout

    @connect_timeout.setter
    def connect_timeout(self, connect_timeout: Optional[int]) -> None:
        self.__connect_timeout = connect_timeout

    @property
    def socket_timeout(self) -> Optional[int]:
        """Socket timeout for the underlying network communication in seconds"""
        return self.__socket_timeout

    @socket_timeout.setter
    def socket_timeout(self, socket_timeout: Optional[int]) -> None:
        self.__socket_timeout = socket_timeout

    @property
    def max_connections(self) -> Optional[int]:
        return self.__max_connections

    @max_connections.setter
    def max_connections(self, max_connections: Optional[int]) -> None:
        self.__max_connections = max_connections

    @property
    def proxy_configuration(self) -> Optional[ProxyConfiguration]:
        return self.__proxy_configuration

    @proxy_configuration.setter
    def proxy_configuration(self, proxy_configuration: Optional[ProxyConfiguration]) -> None:
        self.__proxy_configuration = proxy_configuration

    @property
    def integrator(self) -> Optional[str]:
        return self.__integrator

    @integrator.setter
    def integrator(self, integrator: Optional[str]) -> None:
        self.__integrator = integrator

    @property
    def shopping_cart_extension(self) -> Optional[ShoppingCartExtension]:
        return self.__shopping_cart_extension

    @shopping_cart_extension.setter
    def shopping_cart_extension(self, shopping_cart_extension: Optional[ShoppingCartExtension]) -> None:
        self.__shopping_cart_extension = shopping_cart_extension
