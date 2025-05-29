# pages/base_page.py
from utils.base_driver import BaseDriver
from selenium.webdriver.common.by import By
import logging

logger = logging.getLogger(__name__)

class BasePage:
    """Base page class for Page Object Model"""
    
    def __init__(self, driver, config):
        self.driver = driver
        self.config = config
        self.base_driver = BaseDriver(driver, config)
        self.url = config.BASE_URL
    
    def open(self, url: str = None):
        """Open page"""
        page_url = url or self.url
        logger.info(f"Opening URL: {page_url}")
        self.driver.get(page_url)
        return self
    
    def get_title(self):
        """Get page title"""
        return self.base_driver.get_page_title()
    
    def get_current_url(self):
        """Get current URL"""
        return self.base_driver.get_current_url()
    
    def wait_for_page_load(self, timeout: int = None):
        """Wait for page to load completely"""
        wait_time = timeout or self.config.EXPLICIT_WAIT
        self.base_driver.wait.until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
    
    def take_screenshot(self, name: str = None):
        """Take screenshot"""
        return self.base_driver.take_screenshot(name or self.__class__.__name__)
