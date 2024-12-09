import logging
from typing import Any, Dict, Optional
from urllib.parse import urljoin

from pydantic import BaseModel, Field, model_validator

from checkout.clients.authentication import Authentication
from checkout.clients.http_client import HttpClient
from checkout.contracts.carrier import Carrier


class Settings(BaseModel):
    """
    Configuration class for PlaceToPay integration using Pydantic.
    """

    model_config = {"arbitrary_types_allowed": True}

    base_url: str = Field(..., description="Base URL for the API")
    timeout: int = Field(default=15, description="Request timeout in seconds")
    login: str = Field(..., description="API login key")
    tranKey: str = Field(..., description="API transaction key")
    headers: Dict[str, str] = Field(default_factory=dict, description="Additional HTTP headers")
    auth_additional: Dict[str, Any] = Field(default_factory=dict, description="Additional authentication data")
    loggerConfig: Optional[Dict[str, Any]] = Field(default=None, description="Logger configuration")
    p2p_client: Optional[HttpClient] = Field(default=None, description="Optional pre-configured HttpClient")
    p2p_logger: Optional[logging.Logger] = Field(default=None)
    _carrier_instance: Optional[Carrier] = None

    @model_validator(mode="before")
    @classmethod
    def validate_base_url(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ensure the base_url ends with a slash and is valid.
        """
        base_url = values.get("base_url")
        if not base_url:
            raise ValueError("Base URL cannot be empty.")

        values["base_url"] = urljoin(base_url.rstrip("/") + "/", "")
        return values

    def base_url_with_endpoint(self, endpoint: str = "") -> str:
        """
        Construct the full URL for a given endpoint.

        :param endpoint: API endpoint.
        :return: Full URL as a string.
        """
        return f"{urljoin(self.base_url.rstrip('/') + '/', '')}{endpoint.lstrip('/')}"

    def get_client(self) -> HttpClient:
        """
        Return or create the HTTP client instance.

        :return: Configured `HttpClient`.
        :raises P2PException: If the existing client is not an instance of HttpClient.
        """
        if not self.p2p_client:
            self.p2p_client = HttpClient(
                base_url=str(self.base_url), timeout=self.timeout, logger=self.p2p_logger, headers=self.headers
            )

        return self.p2p_client

    def logger(self) -> logging.Logger:
        """
        Configure and return the logger.
        """
        if not self.p2p_logger:
            self.p2p_logger = self._create_logger()
        return self.p2p_logger

    def _create_logger(self) -> logging.Logger:
        """
        Create and configure a logger based on logger_config or a default setup.

        :return: Configured logger instance.
        """
        logger = logging.getLogger("P2P Checkout Logger")
        logger.setLevel(logging.DEBUG)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        if self.loggerConfig:
            logger.setLevel(self.loggerConfig.get("level", logging.DEBUG))
            custom_formatter = self.loggerConfig.get("formatter")
            if custom_formatter:
                logger.handlers[0].setFormatter(logging.Formatter(custom_formatter))

        return logger

    def authentication(self) -> Authentication:
        """
        Return an `Authentication` instance.
        """
        auth = Authentication(
            {
                "login": self.login,
                "tranKey": self.tranKey,
                "auth_additional": self.auth_additional,
            }
        )
        return auth

    def carrier(self) -> Carrier:
        """
        Return or create the carrier instance.
        """
        from checkout.clients.rest_client import RestCarrier

        if not isinstance(self._carrier_instance, RestCarrier):
            self._carrier_instance = RestCarrier(self)
        return self._carrier_instance
