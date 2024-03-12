import unittest
from censoror import censor_dates

class TestDateCensoring(unittest.TestCase):
    def test_date_censoring(self):
        # Define a sample input containing dates
        data = "Meet on 2024/03/15 at 8:00 AM"
        # Call the date censoring function
        censored_data, dates_list = censor_dates(data)
        # Check if dates were censored
        self.assertNotEqual(censored_data, data, "Dates were not censored.")
        # Check if the dates list is not empty
        self.assertTrue(dates_list, "No dates were found.")

if __name__ == '__main__':
    unittest.main()
