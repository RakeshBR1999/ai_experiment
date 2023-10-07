# tests/test_mymodule.py
import unittest
from model import my_function

class TestMyModule(unittest.TestCase):
    def test_my_function(self):
        # Test cases for my_function
        self.assertEqual(my_function(2,3), 5)
        # Add more test cases here

if __name__ == '__main__':
    unittest.main()
