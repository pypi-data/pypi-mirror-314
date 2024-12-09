import json
from typing import Any, Callable
from unittest.mock import Mock

import requests
from requests.models import Response


class RedirectResponseMock:
    @staticmethod
    def get_mock_response(file_name: str, status_code: int) -> Mock:
        """
        Load mock response data from a file and return a fully mocked Response object.

        :param file_name: Name of the file containing the mock response.
        :param status_code: HTTP status code to set for the response.
        :return: A mocked Response object.
        """
        file_path = f"checkout/tests/mocks/responses/{file_name}.json"
        with open(file_path, "r") as file:
            body = json.load(file)

        mock_response = Mock(spec=Response)
        mock_response.status_code = status_code
        mock_response.json.return_value = body
        mock_response.text = json.dumps(body)
        mock_response.headers = {
            200: {
                "Content-Type": "application/json",
                "X-Mock-Status": "Success",
            },
            400: {
                "Content-Type": "application/json",
                "X-Mock-Status": "Bad Request",
            },
            401: {
                "Content-Type": "application/json",
                "X-Mock-Status": "Unauthorized",
                "WWW-Authenticate": 'Bearer realm="Access to the staging site"',
            },
        }.get(status_code, {"Content-Type": "application/json"})

        if status_code >= 400:
            mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
                f"{status_code} Client Error: Unauthorized for url",
                response=mock_response,
            )
        else:
            mock_response.raise_for_status = lambda: {}

        return mock_response

    @staticmethod
    def mock_response_decorator(file_name: str, status_code: int = 200) -> Callable:
        """
        A decorator that injects a mock response into the test function.

        :param file_name: Name of the file containing the mock response.
        :param status_code: HTTP status code to determine the response (default: 200).
        :return: A decorator function that modifies the test function to include the mock response.
        """

        def decorator(test_func: Callable) -> Callable:
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                mock_response = RedirectResponseMock.get_mock_response(file_name, status_code)
                return test_func(*args, mock_response=mock_response, **kwargs)

            return wrapper

        return decorator
