# test_base/base_test.py
import pytest
import logging
from config.config import Config
from utils.driver_factory import DriverFactory
from pages.base_page import BasePage
from pages.login_page import LoginPage
from pages.home_page import HomePage

logger = logging.getLogger(__name__)

class BaseTest:
    """Base test class with setup and teardown"""
    
    @pytest.fixture(autouse=True)
    def setup(self, request):
        """Setup method for each test"""
        # Load configuration
        self.config = Config.from_env()
        
        # Create driver
        self.driver = DriverFactory.create_driver(
            browser=self.config.BROWSER,
            headless=self.config.HEADLESS
        )
        
        # Initialize page objects
        self.login_page = LoginPage(self.driver, self.config)
        self.home_page = HomePage(self.driver, self.config)
        
        logger.info(f"Starting test: {request.node.name}")
        
        yield
        
        # Teardown
        if self.config.SCREENSHOT_ON_FAILURE and hasattr(request.node, "rep_call") and request.node.rep_call.failed:
            self.take_screenshot(f"FAILED_{request.node.name}")
        
        self.driver.quit()
        logger.info(f"Finished test: {request.node.name}")
    
    def take_screenshot(self, name: str):
        """Take screenshot"""
        return BasePage(self.driver, self.config).take_screenshot(name)
    
    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        """Hook to capture test results"""
        outcome = yield
        rep = outcome.get_result()
        setattr(item, "rep_" + rep.when, rep)
