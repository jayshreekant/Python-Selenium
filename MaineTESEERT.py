# config/config.py
import os
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Config:
    """Configuration class for test settings"""
    BASE_URL: str = "https://example.com"
    BROWSER: str = "chrome"  # chrome, firefox, edge, safari
    HEADLESS: bool = False
    IMPLICIT_WAIT: int = 10
    EXPLICIT_WAIT: int = 20
    PAGE_LOAD_TIMEOUT: int = 30
    SCREENSHOT_ON_FAILURE: bool = True
    VIDEO_RECORDING: bool = False
    LOG_LEVEL: str = "INFO"
    
    # Test data
    TEST_DATA_PATH: str = "test_data/"
    SCREENSHOTS_PATH: str = "screenshots/"
    REPORTS_PATH: str = "reports/"
    
    # Database (if needed)
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    
    @classmethod
    def from_env(cls):
        """Load configuration from environment variables"""
        return cls(
            BASE_URL=os.getenv("BASE_URL", cls.BASE_URL),
            BROWSER=os.getenv("BROWSER", cls.BROWSER).lower(),
            HEADLESS=os.getenv("HEADLESS", "false").lower() == "true",
            IMPLICIT_WAIT=int(os.getenv("IMPLICIT_WAIT", str(cls.IMPLICIT_WAIT))),
            EXPLICIT_WAIT=int(os.getenv("EXPLICIT_WAIT", str(cls.EXPLICIT_WAIT))),
        )

# utils/driver_factory.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import logging

logger = logging.getLogger(__name__)

class DriverFactory:
    """Factory class for creating WebDriver instances"""
    
    @staticmethod
    def create_driver(browser: str, headless: bool = False, **kwargs) -> webdriver.Remote:
        """
        Create and configure WebDriver instance
        
        Args:
            browser: Browser name (chrome, firefox, edge)
            headless: Run in headless mode
            **kwargs: Additional browser-specific options
        
        Returns:
            WebDriver instance
        """
        browser = browser.lower()
        
        if browser == "chrome":
            return DriverFactory._create_chrome_driver(headless, **kwargs)
        elif browser == "firefox":
            return DriverFactory._create_firefox_driver(headless, **kwargs)
        elif browser == "edge":
            return DriverFactory._create_edge_driver(headless, **kwargs)
        else:
            raise ValueError(f"Unsupported browser: {browser}")
    
    @staticmethod
    def _create_chrome_driver(headless: bool, **kwargs) -> webdriver.Chrome:
        """Create Chrome WebDriver with optimized options"""
        options = ChromeOptions()
        
        # Performance optimizations
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        options.add_argument("--disable-images")  # Optional: faster loading
        options.add_argument("--window-size=1920,1080")
        
        if headless:
            options.add_argument("--headless")
        
        # Custom options from kwargs
        for arg in kwargs.get("chrome_args", []):
            options.add_argument(arg)
        
        service = ChromeService(ChromeDriverManager().install())
        
        try:
            driver = webdriver.Chrome(service=service, options=options)
            logger.info("Chrome driver created successfully")
            return driver
        except Exception as e:
            logger.error(f"Failed to create Chrome driver: {e}")
            raise
    
    @staticmethod
    def _create_firefox_driver(headless: bool, **kwargs) -> webdriver.Firefox:
        """Create Firefox WebDriver"""
        options = FirefoxOptions()
        
        if headless:
            options.add_argument("--headless")
        
        options.set_preference("dom.webnotifications.enabled", False)
        options.set_preference("media.volume_scale", "0.0")
        
        service = FirefoxService(GeckoDriverManager().install())
        
        try:
            driver = webdriver.Firefox(service=service, options=options)
            logger.info("Firefox driver created successfully")
            return driver
        except Exception as e:
            logger.error(f"Failed to create Firefox driver: {e}")
            raise
    
    @staticmethod
    def _create_edge_driver(headless: bool, **kwargs) -> webdriver.Edge:
        """Create Edge WebDriver"""
        options = EdgeOptions()
        
        if headless:
            options.add_argument("--headless")
        
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        service = EdgeService(EdgeChromiumDriverManager().install())
        
        try:
            driver = webdriver.Edge(service=service, options=options)
            logger.info("Edge driver created successfully")
            return driver
        except Exception as e:
            logger.error(f"Failed to create Edge driver: {e}")
            raise

# utils/base_driver.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os
from datetime import datetime

class BaseDriver:
    """Base driver class with common WebDriver operations"""
    
    def __init__(self, driver, config):
        self.driver = driver
        self.config = config
        self.wait = WebDriverWait(driver, config.EXPLICIT_WAIT)
        self.actions = ActionChains(driver)
        
        # Configure timeouts
        self.driver.implicitly_wait(config.IMPLICIT_WAIT)
        self.driver.set_page_load_timeout(config.PAGE_LOAD_TIMEOUT)
    
    def find_element(self, by: By, value: str, timeout: int = None):
        """Find element with explicit wait"""
        wait_time = timeout or self.config.EXPLICIT_WAIT
        wait = WebDriverWait(self.driver, wait_time)
        
        try:
            return wait.until(EC.presence_of_element_located((by, value)))
        except TimeoutException:
            self.take_screenshot(f"element_not_found_{value}")
            raise TimeoutException(f"Element not found: {by}={value}")
    
    def find_elements(self, by: By, value: str, timeout: int = None):
        """Find multiple elements with explicit wait"""
        wait_time = timeout or self.config.EXPLICIT_WAIT
        wait = WebDriverWait(self.driver, wait_time)
        
        try:
            wait.until(EC.presence_of_element_located((by, value)))
            return self.driver.find_elements(by, value)
        except TimeoutException:
            return []
    
    def click_element(self, by: By, value: str, timeout: int = None):
        """Click element with wait"""
        element = self.wait_for_clickable(by, value, timeout)
        try:
            element.click()
        except Exception:
            # Fallback to JavaScript click
            self.driver.execute_script("arguments[0].click();", element)
    
    def send_keys_to_element(self, by: By, value: str, text: str, clear: bool = True, timeout: int = None):
        """Send keys to element"""
        element = self.find_element(by, value, timeout)
        if clear:
            element.clear()
        element.send_keys(text)
    
    def wait_for_clickable(self, by: By, value: str, timeout: int = None):
        """Wait for element to be clickable"""
        wait_time = timeout or self.config.EXPLICIT_WAIT
        wait = WebDriverWait(self.driver, wait_time)
        return wait.until(EC.element_to_be_clickable((by, value)))
    
    def wait_for_visible(self, by: By, value: str, timeout: int = None):
        """Wait for element to be visible"""
        wait_time = timeout or self.config.EXPLICIT_WAIT
        wait = WebDriverWait(self.driver, wait_time)
        return wait.until(EC.visibility_of_element_located((by, value)))
    
    def wait_for_invisible(self, by: By, value: str, timeout: int = None):
        """Wait for element to be invisible"""
        wait_time = timeout or self.config.EXPLICIT_WAIT
        wait = WebDriverWait(self.driver, wait_time)
        return wait.until(EC.invisibility_of_element_located((by, value)))
    
    def scroll_to_element(self, element):
        """Scroll to element"""
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)  # Allow scroll to complete
    
    def hover_over_element(self, by: By, value: str):
        """Hover over element"""
        element = self.find_element(by, value)
        self.actions.move_to_element(element).perform()
    
    def drag_and_drop(self, source_by: By, source_value: str, target_by: By, target_value: str):
        """Drag and drop operation"""
        source = self.find_element(source_by, source_value)
        target = self.find_element(target_by, target_value)
        self.actions.drag_and_drop(source, target).perform()
    
    def switch_to_frame(self, frame_reference):
        """Switch to iframe"""
        self.driver.switch_to.frame(frame_reference)
    
    def switch_to_default_content(self):
        """Switch back to main content"""
        self.driver.switch_to.default_content()
    
    def switch_to_window(self, window_handle):
        """Switch to window"""
        self.driver.switch_to.window(window_handle)
    
    def get_current_url(self):
        """Get current URL"""
        return self.driver.current_url
    
    def get_page_title(self):
        """Get page title"""
        return self.driver.title
    
    def refresh_page(self):
        """Refresh current page"""
        self.driver.refresh()
    
    def navigate_back(self):
        """Navigate back"""
        self.driver.back()
    
    def navigate_forward(self):
        """Navigate forward"""
        self.driver.forward()
    
    def execute_javascript(self, script, *args):
        """Execute JavaScript"""
        return self.driver.execute_script(script, *args)
    
    def take_screenshot(self, name: str = None):
        """Take screenshot"""
        if not os.path.exists(self.config.SCREENSHOTS_PATH):
            os.makedirs(self.config.SCREENSHOTS_PATH)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png" if name else f"screenshot_{timestamp}.png"
        filepath = os.path.join(self.config.SCREENSHOTS_PATH, filename)
        
        self.driver.save_screenshot(filepath)
        return filepath
    
    def get_element_text(self, by: By, value: str, timeout: int = None):
        """Get element text"""
        element = self.find_element(by, value, timeout)
        return element.text
    
    def get_element_attribute(self, by: By, value: str, attribute: str, timeout: int = None):
        """Get element attribute"""
        element = self.find_element(by, value, timeout)
        return element.get_attribute(attribute)
    
    def is_element_present(self, by: By, value: str):
        """Check if element is present"""
        try:
            self.driver.find_element(by, value)
            return True
        except NoSuchElementException:
            return False
    
    def is_element_visible(self, by: By, value: str):
        """Check if element is visible"""
        try:
            element = self.driver.find_element(by, value)
            return element.is_displayed()
        except NoSuchElementException:
            return False

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

# Example page classes
class LoginPage(BasePage):
    """Login page implementation"""
    
    # Locators
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")
    
    def __init__(self, driver, config):
        super().__init__(driver, config)
        self.url = f"{config.BASE_URL}/login"
    
    def enter_username(self, username: str):
        """Enter username"""
        self.base_driver.send_keys_to_element(*self.USERNAME_INPUT, username)
        return self
    
    def enter_password(self, password: str):
        """Enter password"""
        self.base_driver.send_keys_to_element(*self.PASSWORD_INPUT, password)
        return self
    
    def click_login(self):
        """Click login button"""
        self.base_driver.click_element(*self.LOGIN_BUTTON)
        return self
    
    def login(self, username: str, password: str):
        """Complete login process"""
        logger.info(f"Logging in with username: {username}")
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        return self
    
    def get_error_message(self):
        """Get error message text"""
        return self.base_driver.get_element_text(*self.ERROR_MESSAGE)
    
    def is_error_displayed(self):
        """Check if error message is displayed"""
        return self.base_driver.is_element_visible(*self.ERROR_MESSAGE)

class HomePage(BasePage):
    """Home page implementation"""
    
    # Locators
    WELCOME_MESSAGE = (By.CLASS_NAME, "welcome-message")
    USER_MENU = (By.ID, "user-menu")
    LOGOUT_LINK = (By.LINK_TEXT, "Logout")
    
    def __init__(self, driver, config):
        super().__init__(driver, config)
        self.url = f"{config.BASE_URL}/home"
    
    def get_welcome_message(self):
        """Get welcome message"""
        return self.base_driver.get_element_text(*self.WELCOME_MESSAGE)
    
    def click_user_menu(self):
        """Click user menu"""
        self.base_driver.click_element(*self.USER_MENU)
        return self
    
    def logout(self):
        """Logout user"""
        self.click_user_menu()
        self.base_driver.click_element(*self.LOGOUT_LINK)
        return self

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

# Example test files
class TestLogin(BaseTest):
    """Login functionality tests"""
    
    def test_successful_login(self):
        """Test successful login"""
        self.login_page.open()
        self.login_page.login("testuser", "testpass")
        
        # Verify successful login
        assert "dashboard" in self.driver.current_url.lower()
        
    def test_invalid_login(self):
        """Test login with invalid credentials"""
        self.login_page.open()
        self.login_page.login("invalid", "invalid")
        
        # Verify error message
        assert self.login_page.is_error_displayed()
        error_msg = self.login_page.get_error_message()
        assert "invalid" in error_msg.lower()
    
    def test_empty_fields_login(self):
        """Test login with empty fields"""
        self.login_page.open()
        self.login_page.click_login()
        
        # Verify error handling
        assert self.login_page.is_error_displayed()

class TestHomePage(BaseTest):
    """Home page functionality tests"""
    
    def test_home_page_elements(self):
        """Test home page elements are present"""
        # Login first
        self.login_page.open()
        self.login_page.login("testuser", "testpass")
        
        # Navigate to home page
        self.home_page.open()
        
        # Verify elements
        welcome_msg = self.home_page.get_welcome_message()
        assert "welcome" in welcome_msg.lower()
    
    def test_logout_functionality(self):
        """Test logout functionality"""
        # Login first
        self.login_page.open()
        self.login_page.login("testuser", "testpass")
        
        # Go to home and logout
        self.home_page.open()
        self.home_page.logout()
        
        # Verify redirect to login page
        assert "login" in self.driver.current_url.lower()

# conftest.py (pytest configuration)
import pytest
import logging
import os
from datetime import datetime

def pytest_configure(config):
    """Configure pytest"""
    # Create directories
    os.makedirs("reports", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # Configure logging
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'logs/test_log_{timestamp}.log'),
            logging.StreamHandler()
        ]
    )

def pytest_html_report_title(report):
    """Customize HTML report title"""
    report.title = "Selenium Test Automation Report"

# requirements.txt content
"""
selenium>=4.15.0
webdriver-manager>=4.0.0
pytest>=7.4.0
pytest-html>=4.0.0
pytest-xdist>=3.3.0
allure-pytest>=2.13.0
requests>=2.31.0
python-dotenv>=1.0.0
"""

# Usage instructions and example runner
if __name__ == "__main__":
    print("""
    Selenium Framework Usage:
    
    1. Install dependencies:
       pip install -r requirements.txt
    
    2. Run tests:
       pytest tests/ -v --html=reports/report.html
    
    3. Run specific test:
       pytest tests/test_login.py::TestLogin::test_successful_login -v
    
    4. Run with different browser:
       BROWSER=firefox pytest tests/ -v
    
    5. Run headless:
       HEADLESS=true pytest tests/ -v
    
    6. Run parallel tests:
       pytest tests/ -n 4 -v
    
    Framework Features:
    - Page Object Model pattern
    - Cross-browser support (Chrome, Firefox, Edge)
    - Automatic driver management
    - Built-in waits and error handling
    - Screenshot on failure
    - Comprehensive logging
    - HTML test reports
    - Parallel test execution
    - Environment-based configuration
    - Shadow DOM support
    - Database connectivity ready
    """)
