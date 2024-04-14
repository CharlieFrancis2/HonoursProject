import unittest
from unittest.mock import patch

# Adjusted imports for the project structure
from src.ciphers.caesar import encode, decode


class TestCipherMethods(unittest.TestCase):
    # @patch('src.analysis.utility.prepare_text', return_value="HELLOWORLD")
    @patch('src.gui.gui_main.update_terminal')
    def test_encode_basic(self, mock_update_terminal):
        """
        Test the encode function with a basic example.
        """
        result = encode("hello world", 3, lambda x: x)
        self.assertEqual(result, "KHOORZRUOG")

    # @patch('src.analysis.utility.prepare_text', return_value="HELLOWORLD")
    @patch('src.gui.gui_main.update_terminal')
    def test_decode_basic(self, mock_update_terminal):
        """
        Test the decode function with a basic example.
        """
        result = decode("khoor zruog", 3, lambda x: x)
        self.assertEqual(result, "HELLOWORLD")

    # @patch('src.analysis.utility.prepare_text', return_value="HELLOWORLD")
    @patch('src.gui.gui_main.update_terminal')
    def test_encode_with_special_chars(self, mock_update_terminal):
        """
        Test the encode function to ensure it properly handles texts with special characters.
        """
        result = encode("hello@world!", 3, lambda x: x)
        self.assertEqual(result, "KHOORZRUOG")

    # @patch('src.analysis.utility.prepare_text', return_value="HELLOWORLD")
    @patch('src.gui.gui_main.update_terminal')
    def test_decode_with_flag(self, mock_update_terminal):
        """
        Test the decode function with the flag parameter set to True to ensure the callback is used.
        """
        # Call the decode function with flag=True
        result = decode("KHOOR@ZRUOG!", 3, mock_update_terminal)

        # Check the result of decoding
        self.assertEqual(result, "HELLOWORLD")

        # Assert that the callback was called
        mock_update_terminal.assert_called()

    @patch('src.gui.gui_main.update_terminal')
    def test_encode_zero_key(self, mock_update_terminal):
        """
        Test encoding with a key of 0, expecting no change to the input text.
        """
        result = encode("hello world", 0, lambda x: x)
        self.assertEqual(result, "HELLOWORLD")

    @patch('src.gui.gui_main.update_terminal')
    def test_decode_zero_key(self, mock_update_terminal):
        """
        Test decoding with a key of 0, expecting no change to the input text.
        """
        result = decode("hello world", 0, lambda x: x)
        self.assertEqual(result, "HELLOWORLD")

    @patch('src.gui.gui_main.update_terminal')
    def test_encode_negative_key(self, mock_update_terminal):
        """
        Test encoding with a negative key.
        """
        result = encode("hello world", -3, lambda x: x)
        # Assuming your cipher correctly handles negative shifts:
        self.assertEqual(result, "EBIILTLOIA")

    @patch('src.gui.gui_main.update_terminal')
    def test_decode_large_key(self, mock_update_terminal):
        """
        Test decoding with a key larger than 26.
        """
        result = decode("khoor zruog", 29, lambda x: x)  # 29 % 26 is effectively 3
        self.assertEqual(result, "HELLOWORLD")

    @patch('src.gui.gui_main.update_terminal')
    def test_encode_empty_string(self, mock_update_terminal):
        """
        Test encoding an empty string.
        """
        result = encode("", 3, lambda x: x)
        self.assertEqual(result, "")

    @patch('src.gui.gui_main.update_terminal')
    def test_decode_empty_string(self, mock_update_terminal):
        """
        Test decoding an empty string.
        """
        result = decode("", 3, lambda x: x)
        self.assertEqual(result, "")

    @patch('src.gui.gui_main.update_terminal')
    def test_encode_non_english_chars(self, mock_update_terminal):
        """
        Test encoding with non-English characters.
        """
        result = encode("héllo wörld", 3, lambda x: x)
        # Assuming non-English chars are either removed by prepare_text or handled in some way:
        self.assertNotEqual(result, "KHOORZRUOG")  # Adjust assertion based on your handling


if __name__ == '__main__':
    unittest.main()
