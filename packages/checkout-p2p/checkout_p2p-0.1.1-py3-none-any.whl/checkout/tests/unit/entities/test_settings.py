import base64
import hashlib
import unittest
from unittest import mock

import pytest

from checkout.clients.authentication import Authentication
from checkout.exceptions.checkout_exception import CheckoutException


class AuthenticationTest(unittest.TestCase):

    @mock.patch("checkout.clients.authentication.random.getrandbits")
    @mock.patch("checkout.clients.authentication.datetime")
    def test_authentication_initialization(self, mock_datetime, mock_getrandbits):
        # Mock datetime and random.getrandbits
        mock_now = mock.Mock()
        mock_now.isoformat.return_value = "2024-10-22T04:39:18.810868+00:00"
        mock_datetime.datetime.now.return_value = mock_now
        mock_datetime.timezone.utc = mock.Mock()
        mock_getrandbits.return_value = int("927342197", 10)

        config = {
            "login": "test_login",
            "tranKey": "test_tran_key",
        }

        auth = Authentication(config)

        raw_nonce = mock_getrandbits.return_value.to_bytes(16, byteorder="big")
        expected_nonce = base64.b64encode(raw_nonce).decode("utf-8")
        expected_seed = "2024-10-22T04:39:18.810868+00:00"
        digest_input = raw_nonce + expected_seed.encode("utf-8") + config["tranKey"].encode("utf-8")
        expected_tran_key = base64.b64encode(hashlib.sha256(digest_input).digest()).decode("utf-8")

        expected_dict = {
            "login": config["login"],
            "tranKey": expected_tran_key,
            "nonce": expected_nonce,
            "seed": expected_seed,
        }

        self.assertEqual(auth.to_dict(), expected_dict)

    def test_fails_not_login_and_tran_key_provided(self):
        with pytest.raises(CheckoutException) as exc_info:
            Authentication({})

        self.assertEqual(str(exc_info.value), "No login or tranKey provided for authentication")
