import unittest

from checkout.entities.account import Account
from checkout.entities.credit import Credit
from checkout.entities.instrument import Instrument
from checkout.entities.token import Token


class InstrumentTest(unittest.TestCase):

    def test_instrument_initialization(self):
        """
        Test the initialization of the Instrument class.
        """
        account = Account(bankCode="001", bankName="Test Bank", accountType="Savings", accountNumber="1234567890")
        token = Token(token="test-token", expiry="2025-12-31")
        credit = Credit(code="CRED001", type="Credit", groupCode="GRP001", installment=12)

        instrument = Instrument(bank=account, token=token, credit=credit, pin="1234", password="secure_password")

        self.assertEqual(instrument.bank.bankCode, "001")
        self.assertEqual(instrument.token.token, "test-token")
        self.assertEqual(instrument.credit.code, "CRED001")
        self.assertEqual(instrument.pin, "1234")
        self.assertEqual(instrument.password, "secure_password")

    def test_instrument_to_dict(self):
        """
        Test the `to_dict` method.
        """
        account = Account(bankCode="001", bankName="Test Bank", accountType="Savings", accountNumber="1234567890")
        token = Token(token="test-token", expiry="2025-12-31")
        credit = Credit(code="CRED001", type="Credit", groupCode="GRP001", installment=12)

        instrument = Instrument(bank=account, token=token, credit=credit, pin="1234", password="secure_password")

        expected_dict = {
            "bank": account.to_dict(),
            "token": token.to_dict(),
            "credit": credit.to_dict(),
            "pin": "1234",
            "password": "secure_password",
        }

        self.assertEqual(instrument.to_dict(), expected_dict)

    def test_instrument_to_dict_without_optional_fields(self):
        """
        Test the `to_dict` method when optional fields are not set.
        """
        instrument = Instrument(pin="1234", password="secure_password")

        expected_dict = {
            "bank": None,
            "token": None,
            "credit": None,
            "pin": "1234",
            "password": "secure_password",
        }

        self.assertEqual(instrument.to_dict(), expected_dict)

    def test_instrument_initialization_with_defaults(self):
        """
        Test initialization of the Instrument class with default values.
        """
        instrument = Instrument()

        self.assertIsNone(instrument.bank)
        self.assertIsNone(instrument.token)
        self.assertIsNone(instrument.credit)
        self.assertEqual(instrument.pin, "")
        self.assertEqual(instrument.password, "")
