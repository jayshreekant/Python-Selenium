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
