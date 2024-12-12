from typing import Mapping, Optional

from .communicator import Communicator


class ApiResource(object):
    """
    Base class of all Worldline Acquiring platform API resources.
    """

    def __init__(self, parent: Optional['ApiResource'] = None, communicator: Optional[Communicator] = None,
                 path_context: Optional[Mapping[str, str]] = None):
        """
        The parent and/or communicator must be given.
        """
        if not parent and not communicator:
            raise ValueError("parent and/or communicator is required")
        self.__parent = parent
        self.__communicator = communicator if communicator else parent._communicator
        self.__path_context = path_context

    @property
    def _communicator(self) -> Communicator:
        return self.__communicator

    def _instantiate_uri(self, uri: str, path_context: Optional[Mapping[str, str]]) -> str:
        uri = self.__replace_all(uri, path_context)
        uri = self.__instantiate_uri(uri)
        return uri

    def __instantiate_uri(self, uri: str) -> str:
        uri = self.__replace_all(uri, self.__path_context)
        if self.__parent is not None:
            uri = self.__parent.__instantiate_uri(uri)
        return uri

    @staticmethod
    def __replace_all(uri: str, path_context: Optional[Mapping[str, str]]) -> str:
        if path_context:
            for key, value in path_context.items():
                uri = uri.replace("{" + key + "}", value)
        return uri
