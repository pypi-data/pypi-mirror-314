import unittest

from checkout.entities.status import Status
from checkout.enums.status_enum import StatusEnum
from checkout.messages.responses.redirect import RedirectResponse


class RedirectResponseTest(unittest.TestCase):

    def test_initialization_with_all_fields(self):
        """
        Test the initialization of RedirectResponse with all fields provided.
        """
        status = Status(status=StatusEnum.OK, reason="Approved")
        redirect_response = RedirectResponse(
            requestId="12345",
            process_url="https://example.com/session",
            status=status,
        )

        self.assertEqual(redirect_response.request_id, "12345")
        self.assertEqual(redirect_response.process_url, "https://example.com/session")
        self.assertIsInstance(redirect_response.status, Status)
        self.assertTrue(redirect_response.is_successful())

    def test_initialization_with_partial_fields(self):
        """
        Test the initialization of RedirectResponse with only required fields.
        """
        status = Status(status=StatusEnum.REJECTED, reason="Declined")
        redirect_response = RedirectResponse(
            requestId="67890",
            process_url="https://example.com/session",
            status=status,
        )

        self.assertEqual(redirect_response.request_id, "67890")
        self.assertEqual(redirect_response.process_url, "https://example.com/session")
        self.assertFalse(redirect_response.is_successful())

    def test_to_dict(self):
        """
        Test the to_dict method for RedirectResponse.
        """
        status = Status(status=StatusEnum.OK, reason="Approved")
        redirect_response = RedirectResponse(
            requestId="12345",
            process_url="https://example.com/session",
            status=status,
        )

        expected_dict = {
            "requestId": "12345",
            "processUrl": "https://example.com/session",
            "status": status.to_dict(),
        }

        self.assertEqual(redirect_response.to_dict(), expected_dict)

    def test_is_successful_with_no_status(self):
        """
        Test is_successful method when status is None.
        """
        redirect_response = RedirectResponse(
            requestId="12345",
            process_url="https://example.com/session",
            status=None,
        )

        self.assertFalse(redirect_response.is_successful())
