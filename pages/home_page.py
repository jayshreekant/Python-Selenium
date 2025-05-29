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
