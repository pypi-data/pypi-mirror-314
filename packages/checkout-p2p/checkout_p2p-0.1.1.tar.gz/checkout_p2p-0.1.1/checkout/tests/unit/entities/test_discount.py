import unittest

from checkout.entities.discount import Discount


class TestDiscount(unittest.TestCase):

    def test_discount_initialization(self):
        discount = Discount(code="DISCOUNT2023", type="Percentage", amount=50.0, base=200.0, percent=25.0)

        self.assertEqual(discount.code, "DISCOUNT2023")
        self.assertEqual(discount.type, "Percentage")
        self.assertEqual(discount.amount, 50.0)
        self.assertEqual(discount.base, 200.0)
        self.assertEqual(discount.percent, 25.0)

    def test_discount_to_dict(self):
        expected_dict = {"code": "DISCOUNT2023", "type": "Percentage", "amount": 50.0, "base": 200.0, "percent": 25.0}

        discount = Discount.model_validate(expected_dict)

        self.assertEqual(discount.to_dict(), expected_dict)

    def test_discount_missing_field(self):
        """
        Test that an error is raised when required fields are missing.
        """
        with self.assertRaises(ValueError):
            Discount(type="Percentage", amount=50.0, base=200.0)

    def test_discount_field_types(self):
        """
        Test that an error is raised when field types are incorrect.
        For example, if 'amount' is a string instead of a float.
        """
        with self.assertRaises(ValueError):
            Discount(code="DISCOUNT2023", type="Percentage", amount="fifty", base=200.0, percent=25.0)
