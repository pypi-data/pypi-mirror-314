import unittest

from checkout.entities.status import Status
from checkout.entities.transaction import Transaction
from checkout.enums.status_enum import StatusEnum
from checkout.messages.responses.reverse import ReverseResponse


class ReverseResponseTest(unittest.TestCase):

    def test_initialization_with_all_fields(self):
        """
        Test the initialization of ReverseResponse with all fields provided.
        """
        status = Status(status=StatusEnum.OK, reason="Reversal successful")
        transaction = Transaction(
            reference="REF001",
            internal_reference="INT001",
            payment_method="CreditCard",
            payment_method_name="Visa",
            issuer_name="Bank A",
            authorization="AUTH001",
            receipt="REC001",
            franchise="VISA",
            refunded=True,
        )

        reverse_response = ReverseResponse(
            status=status,
            payment=transaction,
        )

        self.assertIsInstance(reverse_response.status, Status)
        self.assertIsInstance(reverse_response.payment, Transaction)
        self.assertEqual(reverse_response.status.reason, "Reversal successful")
        self.assertEqual(reverse_response.payment.reference, "REF001")

    def test_initialization_with_no_fields(self):
        """
        Test the initialization of ReverseResponse with no fields provided.
        """
        reverse_response = ReverseResponse()

        self.assertIsNone(reverse_response.status)
        self.assertIsNone(reverse_response.payment)

    def test_to_dict_with_all_fields(self):
        """
        Test the to_dict method when all fields are provided.
        """
        status = Status(status=StatusEnum.OK, reason="Reversal successful")
        transaction = Transaction(
            reference="REF001",
            internal_reference="INT001",
            payment_method="CreditCard",
            payment_method_name="Visa",
            issuer_name="Bank A",
            authorization="AUTH001",
            receipt="REC001",
            franchise="VISA",
            refunded=True,
        )

        reverse_response = ReverseResponse(
            status=status,
            payment=transaction,
        )

        expected_dict = {
            "status": status.to_dict(),
            "payment": transaction.to_dict(),
        }

        self.assertEqual(reverse_response.to_dict(), expected_dict)

    def test_to_dict_with_no_fields(self):
        """
        Test the to_dict method when no fields are provided.
        """
        reverse_response = ReverseResponse()

        expected_dict = {
            "status": None,
            "payment": None,
        }

        self.assertEqual(reverse_response.to_dict(), expected_dict)

    def test_to_dict_with_partial_fields(self):
        """
        Test the to_dict method when only one field is provided.
        """
        status = Status(status=StatusEnum.ERROR, reason="Reversal failed")

        reverse_response = ReverseResponse(
            status=status,
        )

        expected_dict = {
            "status": status.to_dict(),
            "payment": None,
        }

        self.assertEqual(reverse_response.to_dict(), expected_dict)
