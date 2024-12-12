class AuthorizationType(object):
    OAUTH2 = "OAuth2"
    AUTHORIZATION_TYPES = [OAUTH2]

    @staticmethod
    def get_authorization(name: str) -> str:
        if name in AuthorizationType.AUTHORIZATION_TYPES:
            return name
        else:
            raise ValueError("Authorization '{}' not found".format(name))
