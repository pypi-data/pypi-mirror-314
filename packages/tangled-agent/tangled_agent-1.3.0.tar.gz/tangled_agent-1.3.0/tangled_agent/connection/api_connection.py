from __future__ import annotations

import certifi
from tangled_game_client import Configuration, ApiClient, DefaultApi
from typing import Optional, Type, Any, Tuple, List
import logging

class ConnectionClient:
    """
    A context manager for managing API client connections.

    Attributes:
        host (str): The host address of the API.
        api_client (Optional[ApiClient]): The API client instance.
        api_instance (Optional[DefaultApi]): The default API instance.
    """

    host: str = None
    auth_token: str = None
    api_client: Optional[ApiClient] = None
    api_instance: Optional[DefaultApi] = None

    def __init__(self, host: str, auth_token:str) -> None:
        """
        Initializes the ConnectionClient with a specified host.

        Args:
            host (str): The host address of the API.
        """
        logging.info(f"Connecting to {host}")
        self.host = host
        self.auth_token = auth_token
        self.api_client = None
        self.api_instance = None

    def __enter__(self) -> DefaultApi:
        """
        Enters the runtime context for this object.

        Returns:
            DefaultApi: The default API instance.
        """
        configuration = Configuration(host=self.host, access_token=self.auth_token, ssl_ca_cert=certifi.where())
        self.api_client = ApiClient(configuration)
        self.api_instance = DefaultApi(self.api_client)
        return self.api_instance

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[Any]) -> None:
        """
        Exits the runtime context for this object.

        Args:
            exc_type (Optional[Type[BaseException]]): The exception type.
            exc_val (Optional[BaseException]): The exception value.
            exc_tb (Optional[Any]): The traceback object.
        """
        if self.api_client:
            self.api_client.__exit__(exc_type, exc_val, exc_tb)

__all__ = ["ConnectionClient"]
