import unittest

from checkout.entities.payment_modifier import PaymentModifier


class PaymentModifierTest(unittest.TestCase):

    def test_initialization(self):
        """
        Test initialization of PaymentModifier with default values.
        """
        modifier = PaymentModifier()
        assert modifier.type is None
        assert modifier.code is None
        assert modifier.additional == {}

    def test_initialization_with_values(self):
        """
        Test initialization of PaymentModifier with provided values.
        """
        modifier = PaymentModifier(type="CUSTOM_TYPE", code="MOD123", additional={"key": "value"})
        assert modifier.type == "CUSTOM_TYPE"
        assert modifier.code == "MOD123"
        assert modifier.additional == {"key": "value"}

    def test_set_type(self):
        """
        Test setting the type of PaymentModifier.
        """
        modifier = PaymentModifier()
        modifier.set_type("FEDERAL_GOVERNMENT")
        assert modifier.type == "FEDERAL_GOVERNMENT"

    def test_set_code(self):
        """
        Test setting the code of PaymentModifier.
        """
        modifier = PaymentModifier()
        modifier.set_code("CODE123")
        assert modifier.code == "CODE123"

    def test_get_additional(self):
        """
        Test retrieving additional data by key.
        """
        modifier = PaymentModifier(additional={"key1": "value1", "key2": "value2"})
        assert modifier.get_additional("key1") == "value1"
        assert modifier.get_additional("key3", "default") == "default"

    def test_get_additional_entire_dict(self):
        """
        Test retrieving the entire additional data dictionary.
        """
        additional_data = {"key1": "value1", "key2": "value2"}
        modifier = PaymentModifier(additional=additional_data)
        assert modifier.get_additional() == additional_data

    def test_set_additional(self):
        """
        Test setting additional data.
        """
        modifier = PaymentModifier()
        modifier.set_additional({"key1": "value1", "key2": "value2"})
        assert modifier.additional == {"key1": "value1", "key2": "value2"}

    def test_merge_additional(self):
        """
        Test merging additional data with new data.
        """
        modifier = PaymentModifier(additional={"key1": "value1"})
        modifier.merge_additional({"key2": "value2"})
        assert modifier.additional == {"key1": "value1", "key2": "value2"}

    def test_to_dict(self):
        """
        Test converting PaymentModifier to a dictionary.
        """
        modifier = PaymentModifier(type="CUSTOM_TYPE", code="MOD123", additional={"key": "value"})
        expected_dict = {
            "type": "CUSTOM_TYPE",
            "code": "MOD123",
            "additional": {"key": "value"},
        }
        assert modifier.to_dict() == expected_dict
