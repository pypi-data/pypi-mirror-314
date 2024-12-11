import unittest
from unittest.mock import MagicMock, patch, ANY, mock_open

import pandas as pd

from src.inferent.scraping.utils import (
    _load_checkpoint,
    _save_checkpoint,
    _flush_checkpoint,
    checkpoint_scrape,
    title_cond,
)


class TestCheckpointFunctions(unittest.TestCase):

    @patch("src.inferent.scraping.utils.os.makedirs")
    @patch("src.inferent.scraping.utils.os.path.exists")
    @patch("src.inferent.scraping.utils.open", new_callable=mock_open)
    @patch("src.inferent.scraping.utils.json.load")
    @patch("src.inferent.scraping.utils.pd.read_csv")
    def test_load_checkpoint(
        self,
        mock_read_csv,
        mock_json_load,
        mock_file,
        mock_exists,
        mock_makedirs,
    ):
        # Test loading existing dict data
        mock_exists.return_value = True
        mock_json_load.side_effect = [["item1", "item2"], {"key": "value"}]
        result = _load_checkpoint("test", "dict")
        self.assertEqual(result, (["item1", "item2"], {"key": "value"}))

        # Test loading existing DataFrame
        mock_exists.reset_mock()
        mock_exists.return_value = True
        mock_json_load.reset_mock(side_effect=True)
        mock_json_load.return_value = ["item1", "item2"]
        mock_read_csv.return_value = pd.DataFrame({"col": [1, 2, 3]})
        result = _load_checkpoint("test", "df")
        self.assertEqual(result[0], ["item1", "item2"])
        pd.testing.assert_frame_equal(
            result[1], pd.DataFrame({"col": [1, 2, 3]})
        )

        # Test loading non-existing data
        mock_exists.reset_mock()
        mock_exists.return_value = False
        result = _load_checkpoint("test", "list")
        self.assertEqual(result, ([], []))

        # Test unsupported datatype
        with self.assertRaises(ValueError):
            _load_checkpoint("test", "unsupported")

    @patch("src.inferent.scraping.utils.os.makedirs")
    @patch("src.inferent.scraping.utils.open", new_callable=mock_open)
    @patch("src.inferent.scraping.utils.json.dump")
    def test_save_checkpoint(self, mock_json_dump, mock_file, mock_makedirs):
        _save_checkpoint("test", ["item1", "item2"], {"key": "value"})
        mock_json_dump.assert_any_call(["item1", "item2"], mock_file())
        mock_json_dump.assert_any_call({"key": "value"}, mock_file())

    @patch("src.inferent.scraping.utils.os.path.exists")
    @patch("src.inferent.scraping.utils.shutil.rmtree")
    def test_flush_checkpoint(self, mock_rmtree, mock_exists):
        mock_exists.return_value = True
        _flush_checkpoint("test")
        mock_rmtree.assert_called_once_with("test_checkpoint")

    @patch("src.inferent.scraping.utils._load_checkpoint")
    @patch("src.inferent.scraping.utils._save_checkpoint")
    @patch("src.inferent.scraping.utils._flush_checkpoint")
    def test_checkpoint_scrape(self, mock_flush, mock_save, mock_load):
        mock_load.return_value = ([], [])
        mock_callback = MagicMock(return_value=[1, 2, 3])
        result = checkpoint_scrape(
            "test", ["item1", "item2"], mock_callback, "list", 1
        )
        self.assertEqual(result, [1, 2, 3, 1, 2, 3])
        self.assertEqual(mock_save.call_count, 2)
        mock_flush.assert_called_once()

    @patch("src.inferent.scraping.utils.EC")
    def test_title_cond(self, mock_ec):
        title_cond("foo")
        mock_ec.title_contains.assert_called_once_with("foo")


if __name__ == "__main__":
    unittest.main()
