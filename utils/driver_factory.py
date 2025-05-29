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
