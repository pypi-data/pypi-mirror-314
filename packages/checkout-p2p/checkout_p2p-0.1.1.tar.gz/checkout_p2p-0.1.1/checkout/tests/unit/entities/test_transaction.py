import unittest

from checkout.entities.amount_conversion import AmountConversion
from checkout.entities.discount import Discount
from checkout.entities.name_value_pair import NameValuePair
from checkout.entities.status import Status
from checkout.entities.transaction import Transaction
from checkout.enums.status_enum import StatusEnum


class TransactionTest(unittest.TestCase):

    def test_initialization(self):
        """
        Test initialization of Transaction with minimal data.
        """
        transaction = Transaction(reference="test_ref")
        self.assertEqual(transaction.reference, "test_ref")
        self.assertEqual(transaction.internal_reference, "")
        self.assertEqual(transaction.payment_method, "")
        self.assertIsNone(transaction.amount)
        self.assertIsNone(transaction.status)
        self.assertFalse(transaction.refunded)
        self.assertEqual(transaction.processor_fields, [])

    def test_is_successful(self):
        """
        Test is_successful method with different status values.
        """
        transaction = Transaction(reference="test_ref", status=Status(status=StatusEnum.ERROR, reason="XX"))
        self.assertFalse(transaction.is_successful())

        transaction.status.status = StatusEnum.OK
        self.assertTrue(transaction.is_successful())

    def test_is_approved(self):
        """
        Test is_approved method with different status values.
        """
        transaction = Transaction(reference="test_ref", status=Status(status=StatusEnum.APPROVED, reason="00"))
        self.assertTrue(transaction.is_approved())

        transaction.status.status = StatusEnum.REJECTED
        self.assertFalse(transaction.is_approved())

    def test_set_processor_fields(self):
        """
        Test setting processor fields from a list of dictionaries.
        """
        data = [{"keyword": "key1", "value": "value1"}, {"keyword": "key2", "value": "value2"}]
        transaction = Transaction(reference="test_ref")
        transaction.set_processor_fields(data)

        self.assertEqual(len(transaction.processor_fields), 2)
        self.assertEqual(transaction.processor_fields[0].keyword, "key1")
        self.assertEqual(transaction.processor_fields[0].value, "value1")
        self.assertEqual(transaction.processor_fields[1].keyword, "key2")
        self.assertEqual(transaction.processor_fields[1].value, "value2")

    def test_processor_fields_to_array(self):
        """
        Test conversion of processor fields to a list of dictionaries.
        """
        data = [NameValuePair(keyword="key1", value="value1"), NameValuePair(keyword="key2", value="value2")]
        transaction = Transaction(reference="test_ref", processor_fields=data)
        result = transaction.processor_fields_to_array()

        expected = [
            {"keyword": "key1", "value": "value1", "displayOn": "none"},
            {"keyword": "key2", "value": "value2", "displayOn": "none"},
        ]
        self.assertEqual(result, expected)

    def test_set_processor_fields_with_item_key(self):
        """
        Test set_processor_fields with a dictionary containing an 'item' key.
        """

        processor_fields_data = {
            "item": [
                {"keyword": "key1", "value": "value1"},
                {"keyword": "key2", "value": "value2"},
            ]
        }

        transaction = Transaction(reference="testReference")

        transaction.set_processor_fields(processor_fields_data)

        self.assertEqual(len(transaction.processor_fields), 2)
        self.assertEqual(transaction.processor_fields[0].keyword, "key1")
        self.assertEqual(transaction.processor_fields[0].value, "value1")
        self.assertEqual(transaction.processor_fields[1].keyword, "key2")
        self.assertEqual(transaction.processor_fields[1].value, "value2")

    def test_additional_data(self):
        """
        Test parsing processor fields as a key-value dictionary.
        """
        data = [NameValuePair(keyword="key1", value="value1"), NameValuePair(keyword="key2", value="value2")]
        transaction = Transaction(reference="test_ref", processor_fields=data)
        additional_data = transaction.additional_data()

        expected = {
            "key1": "value1",
            "key2": "value2",
        }
        self.assertEqual(additional_data, expected)

    def test_to_dict(self):
        """
        Test conversion of Transaction object to a dictionary.
        """
        status = Status(status=StatusEnum.APPROVED, reason="Test reason")
        amount = AmountConversion(currency="USD", total=100.0)
        discount = Discount(code="DISCOUNT1", type="PERCENT", amount=10.0, base=100.0)
        processor_fields = [
            NameValuePair(keyword="key1", value="value1"),
            NameValuePair(keyword="key2", value="value2"),
        ]

        transaction = Transaction(
            reference="test_ref",
            internal_reference="internal_ref",
            payment_method="card",
            payment_method_name="Credit Card",
            issuer_name="Test Bank",
            amount=amount,
            authorization="12345",
            receipt="54321",
            franchise="VISA",
            refunded=True,
            discount=discount,
            processor_fields=processor_fields,
            status=status,
        )

        result = transaction.to_dict()

        expected = {
            "status": status.to_dict(),
            "internalReference": "internal_ref",
            "paymentMethod": "card",
            "paymentMethodName": "Credit Card",
            "issuerName": "Test Bank",
            "amount": amount.to_dict(),
            "authorization": "12345",
            "reference": "test_ref",
            "receipt": "54321",
            "franchise": "VISA",
            "refunded": True,
            "discount": discount.to_dict(),
            "processorFields": [
                {"keyword": "key1", "value": "value1", "displayOn": "none"},
                {"keyword": "key2", "value": "value2", "displayOn": "none"},
            ],
        }
        self.assertEqual(result, expected)
