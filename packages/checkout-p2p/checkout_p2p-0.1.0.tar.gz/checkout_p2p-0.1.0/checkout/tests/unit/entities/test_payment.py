import unittest

from checkout.entities.amount import Amount
from checkout.entities.discount import Discount
from checkout.entities.item import Item
from checkout.entities.payment import Payment
from checkout.entities.payment_modifier import PaymentModifier
from checkout.entities.person import Person


class PaymentTest(unittest.TestCase):

    def test_payment_initialization(self):
        """
        Test the initialization of a Payment object with default values.
        """
        payment = Payment(reference="REF001")
        assert payment.reference == "REF001"
        assert payment.description == ""
        assert payment.amount is None
        assert payment.allowPartial is False
        assert payment.shipping is None
        assert payment.items == []
        assert payment.recurring is None
        assert payment.payment is None
        assert payment.discount is None
        assert payment.subscribe is False
        assert payment.agreement is None
        assert payment.agreementType == ""
        assert payment.modifiers == []

    def test_payment_initialization_with_values(self):
        """
        Test the initialization of a Payment object with provided values.
        """
        amount = Amount(currency="USD", total=100.0)
        discount = Discount(code="DISC10", type="PERCENTAGE", amount=10.0, base=100.0)
        shipping = Person(document="123456789", name="John", surname="Doe")
        items = [Item(sku="ITEM001", name="Test Item", qty="1", price="50.0")]
        modifiers = [PaymentModifier(type="FEDERAL_GOVERNMENT", code="MOD001")]

        payment = Payment(
            reference="REF001",
            description="Test Payment",
            amount=amount,
            allowPartial=True,
            shipping=shipping,
            items=items,
            discount=discount,
            subscribe=True,
            agreement=123,
            agreementType="TYPE001",
            modifiers=modifiers,
        )

        assert payment.reference == "REF001"
        assert payment.description == "Test Payment"
        assert payment.amount == amount
        assert payment.allowPartial is True
        assert payment.shipping == shipping
        assert payment.items == items
        assert payment.discount == discount
        assert payment.subscribe is True
        assert payment.agreement == 123
        assert payment.agreementType == "TYPE001"
        assert payment.modifiers == modifiers

    def test_set_items(self):
        """
        Test setting items in the Payment object.
        """
        payment = Payment(reference="REF001")
        items = [{"sku": "ITEM001", "name": "Test Item", "qty": "1", "price": "50.0"}]
        payment.set_items(items)

        assert len(payment.items) == 1
        assert payment.items[0].sku == "ITEM001"

    def test_items_to_array(self):
        """
        Test converting items to an array of dictionaries.
        """
        payment = Payment(reference="REF001")
        items = [{"sku": "ITEM001", "name": "Test Item", "qty": "1", "price": "50.0"}]
        payment.set_items(items)

        items_array = payment.items_to_array()
        assert len(items_array) == 1
        assert items_array[0]["sku"] == "ITEM001"

    def test_set_modifiers(self):
        """
        Test setting modifiers in the Payment object.
        """
        payment = Payment(reference="REF001")
        modifiers = [{"type": "CUSTOM_TYPE", "code": "MOD123"}]
        payment.set_modifiers(modifiers)

        assert len(payment.modifiers) == 1
        assert payment.modifiers[0].type == "CUSTOM_TYPE"

    def test_modifiers_to_array(self):
        """
        Test converting modifiers to an array of dictionaries.
        """
        payment = Payment(reference="REF001")
        modifiers = [{"type": "CUSTOM_TYPE", "code": "MOD123"}]
        payment.set_modifiers(modifiers)

        modifiers_array = payment.modifiers_to_array()
        assert len(modifiers_array) == 1
        assert modifiers_array[0]["type"] == "CUSTOM_TYPE"

    def test_to_dict(self):
        """
        Test converting the Payment object to a dictionary.
        """
        amount = Amount(currency="USD", total=100.0)
        discount = Discount(code="DISC10", type="PERCENTAGE", amount=10.0, base=100.0)
        shipping = Person(document="123456789", name="John", surname="Doe")
        items = [Item(sku="ITEM001", name="Test Item", qty="1", price="50.0")]
        modifiers = [PaymentModifier(type="FEDERAL_GOVERNMENT", code="MOD001")]

        payment = Payment(
            reference="REF001",
            description="Test Payment",
            amount=amount,
            shipping=shipping,
            items=items,
            discount=discount,
            modifiers=modifiers,
        )

        payment_dict = payment.to_dict()
        assert payment_dict["reference"] == "REF001"
        assert payment_dict["amount"]["currency"] == "USD"
        assert payment_dict["shipping"]["name"] == "John"
        assert payment_dict["items"][0]["sku"] == "ITEM001"
        assert payment_dict["discount"]["code"] == "DISC10"
        assert payment_dict["modifiers"][0]["type"] == "FEDERAL_GOVERNMENT"
