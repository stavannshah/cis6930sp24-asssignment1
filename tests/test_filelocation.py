import unittest
import os

class TestFileExistence(unittest.TestCase):
    def test_file_exists(self):
        # Specify the path to the file you want to check
        file_path = 'raw1.txt'
        # Check if the file exists at the specified path
        self.assertTrue(os.path.exists(file_path), f"The file {file_path} does not exist")

if __name__ == '_main_':
   unittest.main()

