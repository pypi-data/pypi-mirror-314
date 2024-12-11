"""Tests for base_scraper.py."""

import unittest
from unittest.mock import MagicMock, patch, ANY

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from src.inferent.scraping.base_scraper import BaseScraper
from src.inferent.scraping.utils import title_cond


class TestBaseScraper(unittest.TestCase):
    """Tests for base_scraper.py"""

    @patch("logging.getLogger")
    @patch("src.inferent.scraping.BaseScraper.init_driver")
    def setUp(self, mock_init_driver, mock_logger):
        self.mock_driver = MagicMock()
        mock_init_driver.return_value = self.mock_driver
        self.mock_logger = MagicMock()
        mock_logger.return_value = self.mock_logger
        self.scraper = BaseScraper()

    @patch("selenium.webdriver.Chrome", autospec=True)
    def test_init_driver(self, mock_Chrome):
        self.scraper.init_driver()
        mock_Chrome.assert_called_once_with(options=ANY)

    def test_get_selector(self):
        self.mock_driver.page_source = (
            "<html><body><div>Hello World</div></body></html>"
        )
        selector = self.scraper.get_selector()
        self.assertEqual(selector.css("div::text").get(), "Hello World")

    @patch("selenium.webdriver.support.ui.WebDriverWait.until", autospec=True)
    def test_get(self, mock_until):
        self.mock_driver.page_source = "asdf"
        self.scraper.get(
            "http://example.com", wait_cond=title_cond("Example Domain")
        )
        self.mock_driver.get.assert_called_once_with("http://example.com")
        mock_until.assert_called()

    @patch("selenium.webdriver.ActionChains.move_to_element", autospec=True)
    def test_click(self, mock_move_to_element):
        self.scraper.click("foo")
        mock_move_to_element.assert_called_once_with(ANY, "foo")
        mock_move_to_element.return_value.click().perform.assert_called_once_with()

    def test_click_xpath_not_found(self):
        self.mock_driver.find_element.side_effect = NoSuchElementException
        result = self.scraper.click_xpath("//button")
        self.assertFalse(result)

    @patch("selenium.webdriver.ActionChains.move_to_element", autospec=True)
    def test_click_xpath_found_no_selected(self, mock_move_to_element):
        mock_element = MagicMock()
        mock_element.get_attribute.return_value = "foo bar"
        self.mock_driver.find_element.return_value = mock_element
        result = self.scraper.click_xpath("//button")
        self.assertTrue(result)
        mock_element.get_attribute.assert_called_once_with("class")
        mock_move_to_element.assert_called()

    @patch("selenium.webdriver.ActionChains.move_to_element", autospec=True)
    def test_click_xpath_found_selected(self, mock_move_to_element):
        mock_element = MagicMock()
        mock_element.get_attribute.return_value = "foo selected"
        self.mock_driver.find_element.return_value = mock_element
        result = self.scraper.click_xpath("//button")
        self.assertTrue(result)
        mock_element.get_attribute.assert_called_once_with("class")
        self.assertFalse(mock_move_to_element.called)
        self.mock_logger.info.assert_called_once_with(
            "Element already selected."
        )

    def test_css_wait(self):
        mock_element = MagicMock()
        self.mock_driver.find_element.return_value = mock_element
        self.scraper.css_wait("div")
        self.mock_driver.find_element.assert_called_once_with(
            By.CSS_SELECTOR, "div"
        )

    def test_element_exists(self):
        self.mock_driver.find_element.return_value = MagicMock()
        exists = self.scraper.element_exists(By.CSS_SELECTOR, "div")
        self.assertTrue(exists)

        self.mock_driver.find_element.side_effect = NoSuchElementException
        exists = self.scraper.element_exists(By.CSS_SELECTOR, "div")
        self.assertFalse(exists)


if __name__ == "__main__":
    unittest.main()
