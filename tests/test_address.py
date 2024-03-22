import unittest
from censoror import censor_addresses

class TestAddressCensoring(unittest.TestCase):
    def test_address_censoring(self):
        # Define a sample input containing an address
        data = "660 Parrington Oval, Norman, OK 73019"
        # Call the address censoring function
        censored_data, address_list = censor_address(data)
        # Check if the address was censored
        self.assertNotEqual(censored_data, data, "Address was not censored.")
        # Check if the address list is not empty
        self.assertTrue(address_list, "No addresses were found.")

if __name__ == '__main__':
    unittest.main()
