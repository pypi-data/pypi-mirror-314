import unittest
from pii_scanner.scanner import PIIScanner

class TestPIIScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = PIIScanner()

    def test_scan_email(self):
        text = "Contact me at john.doe@example.com"
        result = self.scanner.scan_text(text)
        self.assertIn('email', result)
        self.assertIn('john.doe@example.com', result['email'])

    def test_scan_phone(self):
        text = "Call me at +123 456 7890"
        result = self.scanner.scan_text(text)
        self.assertIn('phone', result)
        self.assertIn('+123 456 7890', result['phone'])

    # Add more tests for other PII types

if __name__ == '__main__':
    unittest.main()
