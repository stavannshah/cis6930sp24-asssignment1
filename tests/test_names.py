import unittest
from censoror import censor_names

class TestNameCensoring(unittest.TestCase):
    def test_name_censoring(self):
        # Define a sample input containing names
        data = "Harshit Lohaan"
        # Call the name censoring function
        censored_data, names_list = censor_names(data)
        # Check if names were censored
        self.assertNotEqual(censored_data, data, "Names were not censored.")
        # Check if the names list is not empty
        self.assertTrue(names_list, "No names were found.")

if __name__ == '__main__':
    unittest.main()
