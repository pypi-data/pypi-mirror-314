import unittest

from checkout.entities.amount_base import AmountBase
from checkout.entities.amount_conversion import AmountConversion


class AmountConversionTest(unittest.TestCase):

    def test_amoun_conversion_initialization(self):
        to_amount = AmountBase(currency="COP", total=4000)
        from_amount = AmountBase(currency="USD", total=11)

        amount_conversion = AmountConversion(
            fromAmount=from_amount,
            toAmount=to_amount,
            factor=0.01,
        )

        assert amount_conversion.fromAmount == from_amount
        assert amount_conversion.toAmount == to_amount
        assert amount_conversion.factor == 0.01

    def test_amount_conversion_set_amount_base(self):
        amount_conversion = AmountConversion()
        amount_conversion.set_amount_base({"currency": "COP", "total": 1000})

        assert amount_conversion.toAmount.currency == "COP"
        assert amount_conversion.toAmount.total == 1000.0
        assert amount_conversion.fromAmount.currency == "COP"
        assert amount_conversion.fromAmount.total == 1000.0
        assert amount_conversion.factor == 1

    def test_amount_conversion_to_dict(self):

        amount_conversion = AmountConversion(
            fromAmount=AmountBase(currency="COP", total=4000),
            toAmount=AmountBase(currency="USD", total=11),
            factor=0.01,
        )

        assert amount_conversion.to_dict() == {
            "fromAmount": {"currency": "COP", "total": 4000.0},
            "toAmount": {"currency": "USD", "total": 11.0},
            "factor": 0.01,
        }
