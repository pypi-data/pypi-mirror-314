import unittest

from checkout.entities.item import Item


class ItemTest(unittest.TestCase):

    def test_item_initialization(self):
        """
        Test the initialization of the Item class.
        """
        item = Item(sku="ITEM001", name="Test Item", category="Category A", qty="2", price="10.00", tax="1.20")

        self.assertEqual(item.sku, "ITEM001")
        self.assertEqual(item.name, "Test Item")
        self.assertEqual(item.category, "Category A")
        self.assertEqual(item.qty, "2")
        self.assertEqual(item.price, "10.00")
        self.assertEqual(item.tax, "1.20")

    def test_item_to_dict(self):
        """
        Test the `to_dict` method.
        """
        item = Item(sku="ITEM001", name="Test Item", category="Category A", qty="2", price="10.00", tax="1.20")

        expected_dict = {
            "sku": "ITEM001",
            "name": "Test Item",
            "category": "Category A",
            "qty": "2",
            "price": "10.00",
            "tax": "1.20",
        }

        self.assertEqual(item.to_dict(), expected_dict)

    def test_item_to_dict_with_defaults(self):
        """
        Test the `to_dict` method with default values.
        """
        item = Item()

        expected_dict = {
            "sku": "",
            "name": "",
            "category": "",
            "qty": "",
            "price": "",
            "tax": "",
        }

        self.assertEqual(item.to_dict(), expected_dict)

    def test_item_partial_initialization(self):
        """
        Test partial initialization of the Item class.
        """
        item = Item(sku="ITEM001", price="10.00")

        self.assertEqual(item.sku, "ITEM001")
        self.assertEqual(item.name, "")
        self.assertEqual(item.category, "")
        self.assertEqual(item.qty, "")
        self.assertEqual(item.price, "10.00")
        self.assertEqual(item.tax, "")
