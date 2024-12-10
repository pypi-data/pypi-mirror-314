import unittest
from easy_datetime import to_unix

class TestEasyDateTime(unittest.TestCase):
    def test_standard_format(self):
        self.assertEqual(to_unix("2021-01-01"), 1609459200)
        
    def test_slash_format(self):
        self.assertEqual(to_unix("2021/01/01"), 1609459200)
        
    def test_american_format(self):
        self.assertEqual(to_unix("01-01-2021"), 1609459200)
        
    def test_short_format(self):
        self.assertEqual(to_unix("1-01-2021"), 1609459200)
        
    def test_invalid_format(self):
        with self.assertRaises(ValueError):
            to_unix("invalid-date")

if __name__ == '__main__':
    unittest.main()
