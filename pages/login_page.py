from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import logging
logger = logging.getLogger(__name__)
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
