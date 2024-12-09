import unittest

from checkout.entities.account import Account
from checkout.entities.status import Status
from checkout.enums.status_enum import StatusEnum


class AccountTest(unittest.TestCase):

    def test_account_initialization(self):
        account = Account(
            bankCode="001",
            bankName="Test Bank",
            accountType="Savings",
            accountNumber="1234567890",
            status=Status(status=StatusEnum.OK, reason="Active"),
        )

        assert account.bankCode == "001"
        assert account.bankName == "Test Bank"
        assert account.accountType == "Savings"
        assert account.accountNumber == "1234567890"
        assert account.status.status == StatusEnum.OK
        assert account.status.reason == "Active"
        assert account.last_digits() == "7890"
        assert account.get_type() == "account"

    def test_account_to_dict(self):
        """
        Test the `to_dict` method.
        """
        status = Status(status=StatusEnum.OK, reason="Active", message="process ok")
        account = Account(
            bankCode="001", bankName="Test Bank", accountType="Savings", accountNumber="1234567890", status=status
        )

        expected_dict = {
            "status": status.to_dict(),
            "bankCode": "001",
            "bankName": "Test Bank",
            "accountType": "Savings",
            "accountNumber": "1234567890",
        }

        assert account.to_dict() == expected_dict

    def test_account_to_dict_without_status(self):
        """
        Test the `to_dict` method when status is not set.
        """
        account = Account(bankCode="001", bankName="Test Bank", accountType="Savings", accountNumber="1234567890")

        expected_dict = {
            "status": None,
            "bankCode": "001",
            "bankName": "Test Bank",
            "accountType": "Savings",
            "accountNumber": "1234567890",
        }

        assert account.to_dict() == expected_dict

    def test_account_get_type(self):
        """
        Test the `get_type` method.
        """
        account = Account(bankCode="001", bankName="Test Bank", accountType="Savings", accountNumber="1234567890")

        assert account.get_type() == "account"

    def test_account_last_digits(self):
        """
        Test the `last_digits` method.
        """
        account = Account(bankCode="001", bankName="Test Bank", accountType="Savings", accountNumber="1234567890")

        assert account.last_digits() == "7890"

    def test_account_last_digits_empty(self):
        """
        Test the `last_digits` method when account number is empty.
        """
        account = Account(bankCode="001", bankName="Test Bank", accountType="Savings", accountNumber="")

        assert account.last_digits() == ""
