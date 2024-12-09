import unittest

from checkout.entities.amount import Amount
from checkout.entities.amount_detail import AmountDetail
from checkout.entities.tax_detail import TaxDetail


class AmountTest(unittest.TestCase):

    def test_amount_initialization(self):
        """
        Test initializing the Amount class with default values.
        """
        amount = Amount(total=100.0, currency="COP")

        assert amount.total == 100.0
        assert amount.currency == "COP"
        assert amount.taxes == []
        assert amount.details == []
        assert amount.tip is None
        assert amount.insurance is None

    def test_set_taxes(self):
        """
        Test setting taxes using a mix of dictionaries and `TaxDetail` instances.
        """
        tax_data = [
            {"kind": "VAT", "amount": 10.0},
            TaxDetail(kind="SERVICE", amount=5.0),
        ]

        amount = Amount(total=100.0, currency="COP")
        amount.set_taxes(tax_data)

        assert len(amount.taxes) == 2
        assert amount.taxes[0].kind == "VAT"
        assert amount.taxes[0].amount == 10.0
        assert amount.taxes[1].kind == "SERVICE"
        assert amount.taxes[1].amount == 5.0

    def test_set_details(self):
        """
        Test setting details using a mix of dictionaries and `AmountDetail` instances.
        """
        details_data = [
            {"kind": "FEE", "amount": 3.0},
            AmountDetail(kind="DISCOUNT", amount=2.0),
        ]

        amount = Amount(total=100.0, currency="COP")
        amount.set_details(details_data)

        assert len(amount.details) == 2
        assert amount.details[0].kind == "FEE"
        assert amount.details[0].amount == 3.0
        assert amount.details[1].kind == "DISCOUNT"
        assert amount.details[1].amount == 2.0

    def test_taxes_to_dict(self):
        """
        Test converting taxes to an array of dictionaries.
        """
        tax_data = [
            {"kind": "VAT", "amount": 10.0},
            TaxDetail(kind="SERVICE", amount=5.0),
        ]

        amount = Amount(total=100.0, currency="COP")
        amount.set_taxes(tax_data)

        taxes_dict = amount.taxes_to_dict()
        assert len(taxes_dict) == 2
        assert taxes_dict[0] == {"amount": 10.0, "base": None, "kind": "VAT"}
        assert taxes_dict[1] == {"amount": 5.0, "base": None, "kind": "SERVICE"}

    def test_details_to_dict(self):
        """
        Test converting details to an array of dictionaries.
        """
        details_data = [
            {"kind": "FEE", "amount": 3.0},
            AmountDetail(kind="DISCOUNT", amount=2.0),
        ]

        amount = Amount(total=100.0, currency="COP")
        amount.set_details(details_data)

        details_array = amount.details_to_dict()
        assert len(details_array) == 2
        assert details_array[0] == {"kind": "FEE", "amount": 3.0}
        assert details_array[1] == {"kind": "DISCOUNT", "amount": 2.0}

    def test_to_dict(self):
        """
        Test converting the Amount object to a dictionary including taxes and details.
        """
        tax_data = [
            {"kind": "VAT", "amount": 10.0},
            TaxDetail(kind="SERVICE", amount=5.0),
        ]
        details_data = [
            {"kind": "FEE", "amount": 3.0},
            AmountDetail(kind="DISCOUNT", amount=2.0),
        ]

        amount = Amount(total=100.0, currency="COP", tip=15.0, insurance=20.0)
        amount.set_taxes(tax_data)
        amount.set_details(details_data)

        amount_dict = amount.to_dict()
        expected_dict = {
            "currency": "COP",
            "total": 100.0,
            "taxes": [{"kind": "VAT", "amount": 10.0, "base": None}, {"kind": "SERVICE", "amount": 5.0, "base": None}],
            "details": [{"kind": "FEE", "amount": 3.0}, {"kind": "DISCOUNT", "amount": 2.0}],
            "tip": 15.0,
            "insurance": 20.0,
        }

        assert amount_dict == expected_dict
