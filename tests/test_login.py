from test_base.base_test import BaseTest
from pages.base_page import BasePage
import logging
logger = logging.getLogger(__name__)

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
