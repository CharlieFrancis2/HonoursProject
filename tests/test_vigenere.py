import unittest
from unittest.mock import patch

# Adjusted imports for the project structure
from src.ciphers.vigenere import encode, decode


class TestVigenereCipherMethods(unittest.TestCase):
    @patch('src.gui.gui_main.update_terminal')
    def test_encode_basic(self, mock_update_terminal):
        """
        Test the encode function with a basic example using the Vigenère cipher.
        """
        result = encode("helloworld", "key", lambda x: x)
        self.assertEqual(result, "RIJVSUYVJN")

    @patch('src.gui.gui_main.update_terminal')
    def test_decode_basic(self, mock_update_terminal):
        """
        Test the decode function with a basic example using the Vigenère cipher.
        """
        result = decode("rijvsuyvjn", "key", lambda x: x)
        self.assertEqual(result, "HELLOWORLD")

    @patch('src.gui.gui_main.update_terminal')
    def test_encode_with_special_chars(self, mock_update_terminal):
        """
        Test the encode function to ensure it properly handles texts with special characters using the Vigenère cipher.
        """
        result = encode("hello@world!", "key", lambda x: x)
        # Assuming special characters are removed:
        self.assertEqual(result, "RIJVSUYVJN")

    @patch('src.gui.gui_main.update_terminal')
    def test_encode_empty_string(self, mock_update_terminal):
        """
        Test encoding an empty string using the Vigenère cipher.
        """
        result = encode("", "key", lambda x: x)
        self.assertEqual(result, "")

    @patch('src.gui.gui_main.update_terminal')
    def test_decode_empty_string(self, mock_update_terminal):
        """
        Test decoding an empty string using the Vigenère cipher.
        """
        result = decode("", "key", lambda x: x)
        self.assertEqual(result, "")

    @patch('src.gui.gui_main.update_terminal')
    def test_encode_with_keyword_all_spaces(self, mock_update_terminal):
        """
        Test the encode function with a keyword consisting of all spaces (invalid scenario) using the Vigenère cipher.
        """
        # Assuming the function handles or rejects invalid keywords:
        with self.assertRaises(ValueError):
            encode("helloworld", "     ", lambda x: x)

    @patch('src.gui.gui_main.update_terminal')
    def test_decode_with_long_keyword(self, mock_update_terminal):
        """
        Test the decode function with a relatively long keyword using the Vigenère cipher.
        """
        result = decode("rijvsuyvjn", "longkeyword", lambda x: x)
        # Expected result needs to be adjusted based on the actual implementation details of your Vigenère cipher
        # TODO: Fix test
        self.assertEqual(result, "SOMEOUTPUT")