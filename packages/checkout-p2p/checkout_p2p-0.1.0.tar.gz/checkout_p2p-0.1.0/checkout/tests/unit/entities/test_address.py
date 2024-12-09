import unittest

from checkout.entities.address import Address


class AddressTest(unittest.TestCase):

    def test_address_initialization(self):
        """
        Test the initialization of the Address object.
        """
        address = Address(
            street="123 Main St",
            city="Test City",
            state="Test State",
            postalCode="12345",
            country="Test Country",
            phone="123-456-7890",
        )

        assert address.street == "123 Main St"
        assert address.city == "Test City"
        assert address.state == "Test State"
        assert address.postalCode == "12345"
        assert address.country == "Test Country"
        assert address.phone == "123-456-7890"

    def test_address_to_dict(self):
        """
        Test the `to_dict` method.
        """
        address = Address(
            street="123 Main St",
            city="Test City",
            state="Test State",
            postalCode="12345",
            country="Test Country",
            phone="123-456-7890",
        )

        expected_dict = {
            "street": "123 Main St",
            "city": "Test City",
            "state": "Test State",
            "postalCode": "12345",
            "country": "Test Country",
            "phone": "123-456-7890",
        }

        assert address.to_dict() == expected_dict

    def test_address_to_dict_partial(self):
        """
        Test the `to_dict` method when only partial data is provided.
        """
        address = Address(street="123 Main St", city="Test City")

        expected_dict = {
            "street": "123 Main St",
            "city": "Test City",
            "state": "",
            "postalCode": "",
            "country": "",
            "phone": "",
        }

        assert address.to_dict() == expected_dict

    def test_address_default_values(self):
        """
        Test that the Address class initializes fields with default values when not provided.
        """
        address = Address()

        assert address.street == ""
        assert address.city == ""
        assert address.state == ""
        assert address.postalCode == ""
        assert address.country == ""
        assert address.phone == ""

    def test_address_empty_to_dict(self):
        """
        Test the `to_dict` method when all fields have default values.
        """
        address = Address()

        expected_dict = {"street": "", "city": "", "state": "", "postalCode": "", "country": "", "phone": ""}

        assert address.to_dict() == expected_dict
