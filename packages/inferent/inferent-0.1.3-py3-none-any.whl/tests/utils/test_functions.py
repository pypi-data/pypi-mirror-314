import unittest
from unittest.mock import patch
import logging
import time
from src.inferent.utils import (
    retry,
)  # Adjust the import based on your module name


class TestRetryDecorator(unittest.TestCase):

    @patch("src.inferent.utils.functions.logging.error")
    @patch("src.inferent.utils.functions.time.sleep")
    def test_retry_success(self, mock_sleep, mock_logging):
        """Test that the function succeeds on the first attempt."""

        @retry(retry_num=3, retry_sleep_sec=1)
        def success_function():
            return "success"

        result = success_function()

        self.assertEqual(result, "success")
        self.assertEqual(mock_logging.call_count, 0)  # No errors logged
        mock_sleep.assert_not_called()  # Sleep should not be called

    @patch("src.inferent.utils.functions.logging.error")
    @patch("src.inferent.utils.functions.time.sleep")
    def test_retry_failure(self, mock_sleep, mock_logging):
        """Test that the function fails after retries."""

        @retry(retry_num=3, retry_sleep_sec=1)
        def failing_function():
            raise ValueError("An error occurred")

        with self.assertRaisesRegex(Exception, "Exceed max retry.*") as context:
            failing_function()

        self.assertIn("Exceed max retry num: 3 failed", str(context.exception))
        self.assertEqual(
            mock_logging.call_count, 10
        )  # 3 errors for retries + 1 final failure
        mock_sleep.assert_called_with(1)  # Sleep should be called with 1 second

        # Verify that the error messages were logged
        self.assertIn(
            "Trying attempt %s of %s.",
            [call[0][0] for call in mock_logging.call_args_list],
        )

    @patch("src.inferent.utils.functions.logging.error")
    @patch("src.inferent.utils.functions.time.sleep")
    def test_retry_partial_success(self, mock_sleep, mock_logging):
        """Test that the function succeeds after one or more failures."""

        attempt = 0

        @retry(retry_num=3, retry_sleep_sec=1)
        def partial_success_function():
            nonlocal attempt
            attempt += 1
            if attempt < 3:
                raise ValueError("An error occurred")
            return "success"

        result = partial_success_function()

        self.assertEqual(result, "success")
        self.assertEqual(
            mock_logging.call_count, 6
        )  # Should log errors for 2 failures
        self.assertEqual(
            mock_sleep.call_count, 2
        )  # Sleep should be called twice


if __name__ == "__main__":
    unittest.main()
