import json
import logging
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests
from requests.exceptions import RequestException

from checkout.exceptions.http_exceptions import ClientErrorException


class HttpClient:
    def __init__(
        self,
        base_url: str,
        timeout: Optional[int] = None,
        logger: Optional[logging.Logger] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        """
        Initialize the HTTP client.

        :param base_url: Base URL for the API.
        :param timeout: Timeout for requests in seconds.
        :param logger: Logger instance for logging requests and responses.
        """
        self.base_url = self._sanitize_base_url(base_url)
        self.timeout = timeout or 10
        self.logger = logger or self._default_logger()
        self.headers = headers or {"Content-Type": "application/json"}

    @staticmethod
    def _sanitize_base_url(base_url: str) -> str:
        """Ensure the base URL does not end with a trailing slash."""
        return urljoin(str(base_url).rstrip("/") + "/", "")

    def post(self, endpoint: str, json: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Make an HTTP POST request to the specified endpoint.

        :param endpoint: The API endpoint.
        :param json: The data to include in the request body.
        :param headers: Optional HTTP headers.
        :return: Parsed JSON response as a dictionary.
        :raises ClientErrorException: For client-side HTTP errors (4xx).
        :raises ServerErrorException: For server-side HTTP errors (5xx).
        """
        url = self._construct_url(endpoint)
        try:
            self._log_request(url, json)
            final_headers = {**self.headers, **(headers or {})}
            response = requests.post(url=url, json=json, headers=final_headers, timeout=self.timeout)
            response.raise_for_status()

            self._log_response(response)
            return response.json()
        except RequestException:
            raise ClientErrorException.from_response(response)
        except Exception as e:
            self._handle_generic_exception(e)
            raise

    def _construct_url(self, endpoint: str) -> str:
        """Construct the full URL for the API endpoint."""
        return f"{urljoin(str(self.base_url).rstrip('/') + '/', '')}{endpoint.lstrip('/')}"

    def _log_request(self, url: str, payload: Dict[str, Any]) -> None:
        """Log the details of an outgoing request."""
        try:
            payload_str = json.dumps(payload, ensure_ascii=False)
        except (TypeError, ValueError) as e:
            payload_str = f"Error serializing payload: {e}"

        self.logger.debug(f"REQUEST to {url}: {payload_str}")

    def _log_response(self, response: requests.Response) -> None:
        """Log the details of a received response."""
        self.logger.debug("RESPONSE", {"status_code": response.status_code, "result": response.text})

    def _handle_generic_exception(self, exception: Exception) -> None:
        """Handle unexpected exceptions."""
        self.logger.warning("GENERIC_EXCEPTION", {"error": str(exception)})
        raise exception

    @staticmethod
    def _default_logger() -> logging.Logger:
        """
        Create and configure a default logger.
        """
        logger = logging.getLogger("HttpClient")
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
