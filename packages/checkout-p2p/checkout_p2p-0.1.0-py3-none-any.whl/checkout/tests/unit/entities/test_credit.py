import unittest

from checkout.entities.credit import Credit


class TestCredit(unittest.TestCase):

    def test_credit_initialization(self):
        """
        Test that the Credit object initializes correctly with all fields.
        """
        credit = Credit(code="CREDIT123", type="Personal", groupCode="GRP001", installment=12)

        self.assertEqual(credit.code, "CREDIT123")
        self.assertEqual(credit.type, "Personal")
        self.assertEqual(credit.groupCode, "GRP001")
        self.assertEqual(credit.installment, 12)

    def test_credit_to_dict(self):
        """
        Test the `to_dict` method.
        """
        expected_dict = {
            "code": "CREDIT123",
            "type": "Personal",
            "groupCode": "GRP001",
            "installment": 12,
        }

        credit = Credit.model_validate(expected_dict)

        self.assertEqual(credit.to_dict(), expected_dict)

    def test_credit_missing_field(self):
        """
        Test that the Credit object raises a validation error when required fields are missing.
        """
        with self.assertRaises(ValueError):
            Credit(type="Personal", groupCode="GRP001", installment=12)

    def test_credit_field_types(self):
        """
        Test that the Credit object enforces the correct types for fields.
        """
        with self.assertRaises(ValueError):
            Credit(
                code="CREDIT123",
                type="Personal",
                groupCode="GRP001",
                installment="twelve",
            )
