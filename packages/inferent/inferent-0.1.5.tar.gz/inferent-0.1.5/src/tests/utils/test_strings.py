import unittest

from src.inferent.utils.strings import ct


class TestStringMethods(unittest.TestCase):

    def test_ct(self):
        ### edge cases
        self.assertEqual(ct(None), "")
        self.assertEqual(ct(""), "")

        ### encoding
        self.assertEqual(ct("foo\xfc"), "foo")  # Non UTF8
        self.assertEqual(ct("foo\u0627"), "foo")  # UTF8, non-ascii
        self.assertEqual(ct("f$oo, bar"), "foo bar")  # punctuation
        self.assertEqual(ct("FOO BAR"), "foo bar")  # lowercase
        self.assertEqual(ct("  foo  bar   "), "foo  bar")  # strip

    def test_empty_string(self):
        """Test that an empty string returns an empty string."""
        result = ct("")
        self.assertEqual(result, "")

    def test_no_punctuation(self):
        """Test a string with no punctuation."""
        result = ct("Hello World")
        self.assertEqual(result, "hello world")

    def test_with_punctuation(self):
        """Test a string with punctuation."""
        result = ct("Hello, World!")
        self.assertEqual(result, "hello world")

    def test_with_numbers(self):
        """Test a string containing numbers."""
        result = ct("Hello World 123!")
        self.assertEqual(result, "hello world 123")

    def test_lowercase(self):
        """Test that the output is in lowercase."""
        result = ct("HeLLo WoRLD!")
        self.assertEqual(result, "hello world")

    def test_strip_whitespace(self):
        """Test that leading and trailing whitespace is stripped."""
        result = ct("   Hello World!   ")
        self.assertEqual(result, "hello world")

    def test_replace_characters(self):
        """Test that specific characters can be replaced."""
        result = ct("Hello World!", replace="o")
        self.assertEqual(result, "hell wrld")

    def test_remove_punctuation_false(self):
        """Test that punctuation is retained when remove_punctuation is False."""
        result = ct("Hello, World!", remove_punctuation=False)
        self.assertEqual(result, "hello, world!")

    def test_no_lowercase(self):
        """Test that the output is unchanged if lower is False."""
        result = ct("Hello World", lower=False)
        self.assertEqual(result, "Hello World")

    def test_no_strip(self):
        """Test that whitespace is not stripped if strip is False."""
        result = ct("   Hello World!   ", strip=False)
        self.assertEqual(result, "   hello world   ")


if __name__ == "__main__":
    unittest.main()
