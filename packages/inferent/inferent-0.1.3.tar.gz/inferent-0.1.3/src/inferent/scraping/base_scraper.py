"""A base selenium webscraper."""

import binascii
import logging
import os
import shutil
from typing import Callable, Optional, Type

from parsel import Selector
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from .utils import css_cond

CACHE_DIR = "base_scraper_cache"


class BaseScraper:
    """
    A base class for web scraping using Selenium.

    Attributes:
        logger (logging.Logger): Logger for the scraper.
        driver (webdriver.Chrome): Selenium WebDriver instance.
    """

    def __init__(self) -> None:
        """Initialize the BaseScraper"""
        self.logger = logging.getLogger("BaseScraper")
        self.driver = self.init_driver()

    def init_driver(self) -> webdriver.Chrome:
        """
        Initialize the Selenium WebDriver with Chrome options.

        Returns:
            webdriver.Chrome: A configured Chrome WebDriver instance.
        """
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")  # Linux only
        chrome_options.add_argument("--headless")
        chrome_options.add_argument(
            "--enable-features=NetworkService,NetworkServiceInProcess"
        )
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--proxy-server='direct://'")
        chrome_options.add_argument("--proxy-bypass-list=*")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--ignore-certificate-errors")

        return webdriver.Chrome(options=chrome_options)

    def get_selector(self) -> Selector:
        """
        Get a Parsel Selector for the current page source.

        Returns:
            Selector: A Parsel Selector object for the current page source.
        """
        return Selector(text=self.driver.page_source)

    def get_selector_from_cache(
        self,
        url: Optional[str],
        wait_cond: Optional[Callable[["WebDriver"], bool]] = None,
    ) -> Selector:
        """Gets selector from cache if exists, otherwise calls get()"""
        filepath = os.path.join(CACHE_DIR, binascii.hexlify(url))
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf8") as f:
                contents = f.read()
                return Selector(text=contents)
        else:
            return self.get(url, wait_cond=wait_cond, cache=True)

    def get(
        self,
        url: str,
        wait_cond: Optional[Callable[["WebDriver"], bool]] = None,
        wait_time: int = 100,
        cache: bool = False,
    ) -> None:
        """
        Load a webpage and optionally wait for a specific text in the title.

        Args:
            url (str): The URL of the webpage to load.
            title_text (Optional[str]): Text to wait for in the page title.
        """
        self.driver.get(url)
        if wait_cond is not None:
            WebDriverWait(self.driver, wait_time).until(wait_cond)
        if cache:
            self.cache(url, self.driver.page_source)
        return self.get_selector()

    def cache(self, url: str, contents: str):
        """Cache url with contents"""
        os.makedirs(CACHE_DIR, exist_ok=True)
        filepath = os.path.join(CACHE_DIR, binascii.hexlify(url))
        with open(filepath, "w", encoding="utf8") as f:
            f.write(contents)

    def click(self, el: "WebElement") -> None:
        """Clicks an element"""
        ActionChains(self.driver).move_to_element(el).click().perform()

    def click_xpath(self, xpath: str) -> bool:
        """
        Click on an element specified by the XPath if not already selected.

        Args:
            xpath (str): The XPath of the element to click.

        Returns:
            bool: True if the element was clicked, False otherwise.
        """
        try:
            el = self.driver.find_element(By.XPATH, xpath)
            if el is not None:
                classes = el.get_attribute("class").split(" ")
                if "selected" not in classes:
                    self.click(el)
                else:
                    self.logger.info("Element already selected.")
                return True
        except NoSuchElementException:
            self.logger.info("Element not found with the given XPath.")

        return False

    def css_wait(
        self, css_sel: str, time: int = 30
    ) -> webdriver.remote.webelement.WebElement:
        """
        Wait until a CSS element is located.

        Args:
            selector (str): The CSS selector of the element to locate.
            time (int): Maximum wait time in seconds. Default is 30.

        Returns:
            WebElement: The located WebElement.
        """
        return WebDriverWait(self.driver, time).until(css_cond(css_sel))

    def element_exists(self, by: By, tag: str) -> bool:
        """
        Check if an element exists by its tag and locator strategy.

        Args:
            by (By): The locator strategy to use.
            tag (str): The tag or identifier to locate the element.

        Returns:
            bool: True if the element exists, False otherwise.
        """
        try:
            self.driver.find_element(by, tag)
            return True
        except NoSuchElementException:
            return False

    def __enter__(self) -> "BaseScraper":
        """
        Enter the runtime context related to this object.

        Returns:
            BaseScraper: The scraper instance.
        """
        return self

    def __exit__(
        self,
        exctype: Optional[Type["BaseException"]],
        excinst: Optional["BaseException"],
        exctb: Optional["TracebackType"],
    ) -> bool:
        """
        Exit the runtime context related to this object.

        Args:
            exc_type: The exception type.
            exc_value: The exception value.
            traceback: The traceback object.
        """
        self.driver.quit()

        # flush cache
        if os.path.exists(CACHE_DIR):
            shutil.rmtree(CACHE_DIR)

        return False
