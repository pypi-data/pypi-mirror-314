import base64
import datetime
import hashlib
import random
from typing import Dict

from checkout.exceptions.checkout_exception import CheckoutException


class Authentication:
    def __init__(self, config: Dict):
        """
        Initialize Authentication with the necessary configuration.

        :param config: Dictionary containing 'login' and 'tranKey'.
        """
        if "login" not in config or "tranKey" not in config:
            raise CheckoutException("No login or tranKey provided for authentication")

        self.login: str = config["login"]
        self.tran_key: str = config["tranKey"]

        self.raw_nonce = self._generate_raw_nonce()
        self.seed = self._generate_seed()
        self.tran_key_digest = self._generate_tran_key()

    def _generate_raw_nonce(self) -> bytes:
        """
        Generate a raw random nonce (16 bytes).

        :return: Raw nonce in bytes.
        """
        return random.getrandbits(128).to_bytes(16, byteorder="big")

    def _generate_seed(self) -> str:
        """
        Generate the seed (timestamp in ISO format).

        :return: ISO formatted timestamp.
        """
        return datetime.datetime.now(datetime.timezone.utc).isoformat()

    def _generate_tran_key(self) -> str:
        """
        Generate the tranKey by hashing the raw_nonce, seed, and tran_key using SHA256.

        :return: Base64 encoded tranKey string.
        """
        digest_input = self.raw_nonce + self.seed.encode("utf-8") + self.tran_key.encode("utf-8")
        digest = hashlib.sha256(digest_input).digest()
        return base64.b64encode(digest).decode("utf-8")

    def to_dict(self) -> Dict:
        """
        Return the authentication data as a dictionary.

        :return: Authentication dictionary.
        """
        return {
            "login": self.login,
            "tranKey": self.tran_key_digest,
            "nonce": base64.b64encode(self.raw_nonce).decode("utf-8"),
            "seed": self.seed,
        }
