from typing import Optional


class OAuth2Exception(RuntimeError):
    """
    Indicates an exception regarding the authorization with the Worldline OAuth2 Authorization Server.
    """

    def __init__(self, message: Optional[str] = None):
        super(OAuth2Exception, self).__init__(message)
