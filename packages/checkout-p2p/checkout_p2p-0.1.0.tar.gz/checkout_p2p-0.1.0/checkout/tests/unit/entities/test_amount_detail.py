import unittest

from checkout.entities.amount_detail import AmountDetail


class AmountDetailTest(unittest.TestCase):

    def test_amount_detail_initialization(self):
        amount_detil = AmountDetail(kind="test_kind", amount=10.0)

        assert amount_detil.kind == "test_kind"
        assert amount_detil.amount == 10.0

    def test_amount_detail_to_dict(self):
        expected_dict = {"kind": "test_kind", "amount": 10.0}
        amount_detil = AmountDetail.model_validate(expected_dict)

        assert amount_detil.to_dict() == expected_dict
