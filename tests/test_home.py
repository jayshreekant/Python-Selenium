from test_base.base_test import BaseTest
import logging
logger = logging.getLogger(__name__)

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
