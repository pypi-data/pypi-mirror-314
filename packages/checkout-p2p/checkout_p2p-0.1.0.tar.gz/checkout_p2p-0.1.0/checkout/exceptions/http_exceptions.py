import json

from requests import Response


class HttpException(Exception):
    """Base class for HTTP-related exceptions."""

    @classmethod
    def from_response(cls, response: Response) -> "HttpException":
        """
        Create an exception from a Response object.
        """
        try:
            error_details = response.json()
        except json.JSONDecodeError:
            error_details = {"status_code": response.status_code, "message": response.text}

        return cls(
            json.dumps(
                {
                    "status_code": response.status_code,
                    "error_details": error_details,
                }
            )
        )


class ClientErrorException(HttpException):
    """Exception for 4xx HTTP errors."""


class ServerErrorException(HttpException):
    """Exception for 5xx HTTP errors."""
