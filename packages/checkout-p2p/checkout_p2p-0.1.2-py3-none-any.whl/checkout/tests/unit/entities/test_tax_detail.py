import unittest

from pydantic import ValidationError

from checkout.entities.tax_detail import TaxDetail


class TaxtDetailTest(unittest.TestCase):

    def test_initialization(self):
        """
        Test the initialization of a TaxDetail object.
        """
        tax_detail = TaxDetail(kind="VAT", amount=100.0, base=500.0)

        self.assertEqual(tax_detail.kind, "VAT")
        self.assertEqual(tax_detail.amount, 100.0)
        self.assertEqual(tax_detail.base, 500.0)

    def test_to_dict(self):
        """
        Test the to_dict method of TaxDetail.
        """
        tax_detail = TaxDetail(kind="VAT", amount=100.0, base=500.0)

        expected_dict = {
            "kind": "VAT",
            "amount": 100.0,
            "base": 500.0,
        }

        self.assertEqual(tax_detail.to_dict(), expected_dict)

    def test_to_dict_without_base(self):
        """
        Test the to_dict method when base is not provided.
        """
        tax_detail = TaxDetail(kind="VAT", amount=100.0)

        expected_dict = {"amount": 100, "base": None, "kind": "VAT"}

        self.assertEqual(tax_detail.to_dict(), expected_dict)

    def test_missing_required_fields(self):
        """
        Test that missing required fields raise a validation error.
        """
        with self.assertRaises(ValidationError):
            TaxDetail(amount=100.0)
