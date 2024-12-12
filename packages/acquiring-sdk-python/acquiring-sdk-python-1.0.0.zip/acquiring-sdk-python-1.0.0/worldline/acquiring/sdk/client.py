# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from datetime import timedelta

from .api_resource import ApiResource
from .communicator import Communicator

from worldline.acquiring.sdk.log.body_obfuscator import BodyObfuscator
from worldline.acquiring.sdk.log.communicator_logger import CommunicatorLogger
from worldline.acquiring.sdk.log.header_obfuscator import HeaderObfuscator
from worldline.acquiring.sdk.log.logging_capable import LoggingCapable
from worldline.acquiring.sdk.log.obfuscation_capable import ObfuscationCapable
from worldline.acquiring.sdk.v1.v1_client import V1Client


class Client(ApiResource, LoggingCapable, ObfuscationCapable):
    """
    Worldline Acquiring platform client.

    Thread-safe.
    """

    def __init__(self, communicator: Communicator):
        """
        :param communicator:  :class:`worldline.acquiring.sdk.communicator.Communicator`
        """
        super(Client, self).__init__(communicator=communicator)

    def close_idle_connections(self, idle_time: timedelta) -> None:
        """
        Utility method that delegates the call to this client's communicator.

        :param idle_time: a datetime.timedelta object indicating the idle time
        """
        self._communicator.close_idle_connections(idle_time)

    def close_expired_connections(self) -> None:
        """
        Utility method that delegates the call to this client's communicator.
        """
        self._communicator.close_expired_connections()

    def set_body_obfuscator(self, body_obfuscator: BodyObfuscator) -> None:
        # delegate to the communicator
        self._communicator.set_body_obfuscator(body_obfuscator)

    def set_header_obfuscator(self, header_obfuscator: HeaderObfuscator) -> None:
        # delegate to the communicator
        self._communicator.set_header_obfuscator(header_obfuscator)

    def enable_logging(self, communicator_logger: CommunicatorLogger) -> None:
        # delegate to the communicator
        self._communicator.enable_logging(communicator_logger)

    def disable_logging(self) -> None:
        # delegate to the communicator
        self._communicator.disable_logging()

    def close(self) -> None:
        """
        Releases any system resources associated with this object.
        """
        self._communicator.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def v1(self) -> V1Client:
        return V1Client(self, None)
