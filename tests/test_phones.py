import unittest
from censoror import censor_phones

class TestPhoneCensoring(unittest.TestCase):
    def test_phone_censoring(self):
        # Define a sample input containing phone numbers
        data = "Contact us at (800) 353 4940 or 9876543210"
        # Call the phone censoring function
        censored_data, phones_list = censor_phones(data)
        # Check if phone numbers were censored
        self.assertNotEqual(censored_data, data, "Phone numbers were not censored.")
        # Check if the phone numbers list is not empty
        self.assertTrue(phones_list, "No phone numbers were found.")

if __name__ == '__main__':
    unittest.main()
