from datetime import datetime
import unittest

from checkout.entities.status import Status
from checkout.enums.status_enum import StatusEnum


class StatusTest(unittest.TestCase):

    def test_initialization(self):
        """
        Test the initialization of a Status object.
        """
        status = Status(
            status=StatusEnum.OK, reason="All good", message="Operation successful", date="2024-11-25T12:00:00"
        )
        self.assertEqual(status.status, StatusEnum.OK)
        self.assertEqual(status.reason, "All good")
        self.assertEqual(status.message, "Operation successful")
        self.assertEqual(status.date, "2024-11-25T12:00:00")

    def test_default_date(self):
        """
        Test the default date generation.
        """
        status = Status(status=StatusEnum.OK, reason="All good")
        self.assertIsNotNone(status.date)
        self.assertTrue(datetime.fromisoformat(status.date))

    def test_is_successful(self):
        """
        Test the is_successful method.
        """
        status = Status(status=StatusEnum.OK, reason="Success")
        self.assertTrue(status.is_successful())

    def test_is_approved(self):
        """
        Test the is_approved method.
        """
        status = Status(status=StatusEnum.APPROVED, reason="Approved")
        self.assertTrue(status.is_approved())

    def test_is_rejected(self):
        """
        Test the is_rejected method.
        """
        status = Status(status=StatusEnum.REJECTED, reason="Rejected")
        self.assertTrue(status.is_rejected())

    def test_is_error(self):
        """
        Test the is_error method.
        """
        status = Status(status=StatusEnum.ERROR, reason="Error occurred")
        self.assertTrue(status.is_error())

    def test_quick_method(self):
        """
        Test the quick class method.
        """
        quick_status = Status.quick(
            status=StatusEnum.OK, reason="Quick init", message="Quick message", date="2024-11-25T12:00:00"
        )
        self.assertIsInstance(quick_status, Status)
        self.assertEqual(quick_status.status, StatusEnum.OK)
        self.assertEqual(quick_status.reason, "Quick init")
        self.assertEqual(quick_status.message, "Quick message")
        self.assertEqual(quick_status.date, "2024-11-25T12:00:00")

    def test_to_dict(self):
        """
        Test the to_dict method.
        """
        status = Status(
            status=StatusEnum.OK, reason="All good", message="Everything is fine", date="2024-11-25T12:00:00"
        )
        expected_dict = {
            "status": StatusEnum.OK.value,
            "reason": "All good",
            "message": "Everything is fine",
            "date": "2024-11-25T12:00:00",
        }
        self.assertEqual(status.to_dict(), expected_dict)
