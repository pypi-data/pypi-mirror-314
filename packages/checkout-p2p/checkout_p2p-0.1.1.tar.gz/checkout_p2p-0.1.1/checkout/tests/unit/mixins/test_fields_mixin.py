import unittest

from checkout.entities.name_value_pair import NameValuePair
from checkout.mixins.fields_mixin import FieldsMixin


class FieldsMixinTest(unittest.TestCase):

    def test_get_fields(self):
        """
        Test retrieving the fields list.
        """
        mixin = FieldsMixin()
        mixin.fields = [NameValuePair(keyword="key1", value="value1")]
        fields = mixin.get_fields()
        self.assertEqual(len(fields), 1)
        self.assertEqual(fields[0].keyword, "key1")
        self.assertEqual(fields[0].value, "value1")

    def test_set_fields_with_dict(self):
        """
        Test setting fields with a dictionary containing an 'item' key.
        """
        mixin = FieldsMixin()
        fields_data = {"item": [{"keyword": "key1", "value": "value1"}, {"keyword": "key2", "value": "value2"}]}
        mixin.set_fields(fields_data)
        self.assertEqual(len(mixin.fields), 2)
        self.assertEqual(mixin.fields[0].keyword, "key1")
        self.assertEqual(mixin.fields[1].keyword, "key2")

    def test_set_fields_with_list(self):
        """
        Test setting fields with a list of dictionaries.
        """
        mixin = FieldsMixin()
        fields_data = [{"keyword": "key1", "value": "value1"}, {"keyword": "key2", "value": "value2"}]
        mixin.set_fields(fields_data)
        self.assertEqual(len(mixin.fields), 2)
        self.assertEqual(mixin.fields[0].keyword, "key1")
        self.assertEqual(mixin.fields[1].value, "value2")

    def test_fields_to_array(self):
        """
        Test converting fields to a list of dictionaries.
        """
        mixin = FieldsMixin()
        mixin.fields = [
            NameValuePair(keyword="key1", value="value1"),
            NameValuePair(keyword="key2", value="value2"),
        ]
        result = mixin.fields_to_array()
        expected = [
            {"keyword": "key1", "value": "value1", "displayOn": "none"},
            {"keyword": "key2", "value": "value2", "displayOn": "none"},
        ]
        self.assertEqual(result, expected)

    def test_fields_to_key_value(self):
        """
        Test converting fields to a key-value dictionary.
        """
        mixin = FieldsMixin()
        mixin.fields = [
            NameValuePair(keyword="key1", value="value1"),
            NameValuePair(keyword="key2", value="value2"),
        ]
        result = mixin.fields_to_key_value()
        expected = {"key1": "value1", "key2": "value2"}
        self.assertEqual(result, expected)

    def test_add_field_with_dict(self):
        """
        Test adding a field using a dictionary.
        """
        mixin = FieldsMixin()
        field_data = {"keyword": "key1", "value": "value1"}
        mixin.add_field(field_data)
        self.assertEqual(len(mixin.fields), 1)
        self.assertEqual(mixin.fields[0].keyword, "key1")
        self.assertEqual(mixin.fields[0].value, "value1")

    def test_add_field_with_name_value_pair(self):
        """
        Test adding a field using a NameValuePair instance.
        """
        mixin = FieldsMixin()
        nvp = NameValuePair(keyword="key1", value="value1")
        mixin.add_field(nvp)
        self.assertEqual(len(mixin.fields), 2)
        self.assertEqual(mixin.fields[0].keyword, "key1")
        self.assertEqual(mixin.fields[0].value, "value1")

    def test_set_fields_with_item_key(self):
        """
        Test setting fields when the input is a dictionary with an 'item' key.
        """
        fields_data = {"item": [{"keyword": "key1", "value": "value1"}, {"keyword": "key2", "value": "value2"}]}

        mixin = FieldsMixin()
        mixin.set_fields(fields_data)
        self.assertEqual(len(mixin.fields), 2)

        self.assertEqual(mixin.fields[0].keyword, "key1")
        self.assertEqual(mixin.fields[1].keyword, "key2")

    def test_fields_to_key_value_with_non_name_value_pair(self):
        """
        Test fields_to_key_value skips non-NameValuePair objects.
        """
        mixin = FieldsMixin()
        mixin.fields = [NameValuePair(keyword="key1", value="value1"), "invalid_field"]
        result = mixin.fields_to_key_value()
        expected = {"key1": "value1"}
        self.assertEqual(result, expected)
