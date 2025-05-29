# Python Selenium Testing Framework

A comprehensive, production-ready Selenium testing framework built with Python, featuring Page Object Model, multi-browser support, and advanced testing capabilities.

## 🚀 Features

- **Page Object Model (POM)** - Clean separation of page logic and test logic
- **Multi-Browser Support** - Chrome, Firefox, Edge with automatic driver management
- **Cross-Platform** - Works on Windows, macOS, and Linux
- **Parallel Execution** - Run tests in parallel for faster execution
- **Smart Waits** - Intelligent explicit waits with custom timeouts
- **Screenshot on Failure** - Automatic screenshots when tests fail
- **Comprehensive Logging** - Detailed logs with timestamps
- **HTML Reports** - Beautiful test reports with pytest-html
- **Environment Configuration** - Flexible configuration via environment variables
- **CI/CD Ready** - Designed for continuous integration pipelines
- **Shadow DOM Support** - Handle modern web components
- **Database Ready** - Built-in database connectivity support

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Writing Tests](#writing-tests)
- [Running Tests](#running-tests)
- [Advanced Features](#advanced-features)
- [Best Practices](#best-practices)
- [Contributing](#contributing)
- [License](#license)

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/selenium-framework.git
   cd selenium-framework
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation**
   ```bash
   pytest --version
   ```

## 🚀 Quick Start

1. **Run sample tests**
   ```bash
   pytest tests/ -v
   ```

2. **Generate HTML report**
   ```bash
   pytest tests/ -v --html=reports/report.html --self-contained-html
   ```

3. **Run in headless mode**
   ```bash
   HEADLESS=true pytest tests/ -v
   ```

## 📁 Project Structure

```
selenium-framework/
├── config/
│   └── config.py              # Configuration management
├── utils/
│   ├── driver_factory.py      # WebDriver factory
│   └── base_driver.py         # Base driver operations
├── pages/
│   ├── base_page.py           # Base page class
│   ├── login_page.py          # Login page object
│   └── home_page.py           # Home page object
├── tests/
│   ├── test_login.py          # Login tests
│   └── test_home.py           # Home page tests
├── test_base/
│   └── base_test.py           # Base test class
├── test_data/
│   └── test_users.json        # Test data files
├── screenshots/               # Test failure screenshots
├── reports/                   # Test reports
├── logs/                      # Test execution logs
├── conftest.py               # pytest configuration
├── requirements.txt          # Project dependencies
└── README.md                 # This file
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Base configuration
BASE_URL=https://your-app.com
BROWSER=chrome
HEADLESS=false

# Timeouts (seconds)
IMPLICIT_WAIT=10
EXPLICIT_WAIT=20
PAGE_LOAD_TIMEOUT=30

# Test settings
SCREENSHOT_ON_FAILURE=true
LOG_LEVEL=INFO

# Database (optional)
DB_HOST=localhost
DB_PORT=3306
DB_USER=testuser
DB_PASSWORD=testpass
```

### Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `BASE_URL` | `https://example.com` | Application base URL |
| `BROWSER` | `chrome` | Browser choice (chrome, firefox, edge) |
| `HEADLESS` | `false` | Run browser in headless mode |
| `IMPLICIT_WAIT` | `10` | Implicit wait timeout in seconds |
| `EXPLICIT_WAIT` | `20` | Explicit wait timeout in seconds |
| `PAGE_LOAD_TIMEOUT` | `30` | Page load timeout in seconds |
| `SCREENSHOT_ON_FAILURE` | `true` | Take screenshot on test failure |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |

## ✍️ Writing Tests

### Creating a Page Object

```python
from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class ProductPage(BasePage):
    # Locators
    PRODUCT_TITLE = (By.H1, "product-title")
    ADD_TO_CART_BTN = (By.ID, "add-to-cart")
    PRICE_ELEMENT = (By.CLASS_NAME, "price")
    
    def __init__(self, driver, config):
        super().__init__(driver, config)
        self.url = f"{config.BASE_URL}/products"
    
    def get_product_title(self):
        return self.base_driver.get_element_text(*self.PRODUCT_TITLE)
    
    def add_to_cart(self):
        self.base_driver.click_element(*self.ADD_TO_CART_BTN)
        return self
    
    def get_price(self):
        return self.base_driver.get_element_text(*self.PRICE_ELEMENT)
```

### Creating a Test

```python
from test_base.base_test import BaseTest
import pytest

class TestProduct(BaseTest):
    
    def test_product_display(self):
        """Test product information is displayed correctly"""
        self.product_page.open()
        
        # Verify product title
        title = self.product_page.get_product_title()
        assert title is not None
        assert len(title) > 0
        
        # Verify price is displayed
        price = self.product_page.get_price()
        assert "$" in price
    
    @pytest.mark.smoke
    def test_add_to_cart(self):
        """Test adding product to cart"""
        self.product_page.open()
        self.product_page.add_to_cart()
        
        # Verify success message or cart update
        # Add your assertions here
```

## 🏃‍♂️ Running Tests

### Basic Commands

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_login.py -v

# Run specific test method
pytest tests/test_login.py::TestLogin::test_successful_login -v

# Run tests with markers
pytest -m smoke -v

# Run tests in parallel
pytest tests/ -n 4 -v
```

### Browser Options

```bash
# Chrome (default)
pytest tests/ -v

# Firefox
BROWSER=firefox pytest tests/ -v

# Edge
BROWSER=edge pytest tests/ -v

# Headless mode
HEADLESS=true pytest tests/ -v
```

### Reporting Options

```bash
# HTML report
pytest tests/ -v --html=reports/report.html --self-contained-html

# JUnit XML report
pytest tests/ -v --junitxml=reports/junit.xml

# Allure report
pytest tests/ -v --alluredir=reports/allure-results
allure serve reports/allure-results
```

### Advanced Options

```bash
# Stop on first failure
pytest tests/ -x

# Show local variables in tracebacks
pytest tests/ -l

# Increase verbosity
pytest tests/ -vv

# Run only failed tests from last run
pytest tests/ --lf

# Run tests that failed or passed (but didn't fail) last time
pytest tests/ --ff
```

## 🔧 Advanced Features

### Custom Waits

```python
# Wait for element to be clickable
element = self.base_driver.wait_for_clickable(By.ID, "submit-btn")

# Wait for element to be visible
element = self.base_driver.wait_for_visible(By.CLASS_NAME, "success-msg")

# Wait for element to disappear
self.base_driver.wait_for_invisible(By.ID, "loading-spinner")
```

### JavaScript Execution

```python
# Execute JavaScript
result = self.base_driver.execute_javascript("return document.title;")

# Scroll to element
element = self.base_driver.find_element(By.ID, "footer")
self.base_driver.scroll_to_element(element)
```

### Screenshots

```python
# Manual screenshot
screenshot_path = self.take_screenshot("custom_screenshot")

# Automatic on failure (configured in base_test.py)
```

### Parallel Execution

```bash
# Install pytest-xdist
pip install pytest-xdist

# Run tests in parallel
pytest tests/ -n auto  # Auto-detect CPU cores
pytest tests/ -n 4     # Use 4 workers
```

### Database Integration

```python
# In your test
def test_user_data(self):
    # Test creates user in application
    self.registration_page.register_user("testuser", "password")
    
    # Verify in database
    db_user = self.database.get_user_by_username("testuser")
    assert db_user is not None
    assert db_user.username == "testuser"
```

## 🎯 Best Practices

### Page Objects

- **Single Responsibility**: Each page object should represent one page or component
- **Return Self**: Methods that perform actions should return `self` for method chaining
- **Descriptive Names**: Use clear, descriptive method names
- **Locator Constants**: Define locators as class constants

```python
# Good
def login(self, username, password):
    self.enter_username(username)
    self.enter_password(password)
    self.click_login_button()
    return self

# Method chaining
self.login_page.login("user", "pass").verify_successful_login()
```

### Test Organization

- **Arrange-Act-Assert**: Structure tests clearly
- **One Assertion Per Concept**: Focus each test on one specific behavior
- **Descriptive Test Names**: Test names should describe what they test
- **Use Fixtures**: Share common setup using pytest fixtures

```python
def test_should_display_error_when_login_with_invalid_credentials(self):
    # Arrange
    invalid_username = "invalid_user"
    invalid_password = "wrong_password"
    
    # Act
    self.login_page.login(invalid_username, invalid_password)
    
    # Assert
    assert self.login_page.is_error_displayed()
    assert "invalid credentials" in self.login_page.get_error_message().lower()
```

### Error Handling

- Always use explicit waits instead of `time.sleep()`
- Implement proper exception handling
- Take screenshots on failures
- Provide meaningful error messages

### Performance

- Use headless mode for CI/CD
- Implement smart waits
- Minimize browser interactions
- Use parallel execution for large test suites

## 🔄 CI/CD Integration

### GitHub Actions Example

```yaml
name: Selenium Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        HEADLESS=true pytest tests/ -v --html=reports/report.html
      env:
        BASE_URL: ${{ secrets.BASE_URL }}
    
    - name: Upload test results
      uses: actions/upload-artifact@v2
      if: always()
      with:
        name: test-results
        path: reports/
```

### Jenkins Pipeline

```groovy
pipeline {
    agent any
    
    environment {
        HEADLESS = 'true'
        BASE_URL = 'https://staging.example.com'
    }
    
    stages {
        stage('Setup') {
            steps {
                sh 'python -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }
        
        stage('Test') {
            steps {
                sh '. venv/bin/activate && pytest tests/ -v --junitxml=reports/junit.xml'
            }
        }
    }
    
    post {
        always {
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: 'report.html',
                reportName: 'Test Report'
            ])
        }
    }
}
```

## 🐛 Troubleshooting

### Common Issues

1. **WebDriver not found**
   ```bash
   # Solution: webdriver-manager handles this automatically
   pip install webdriver-manager
   ```

2. **Element not found**
   ```python
   # Use explicit waits instead of implicit waits
   element = self.base_driver.wait_for_visible(By.ID, "element-id", timeout=30)
   ```

3. **Stale element reference**
   ```python
   # Re-find the element instead of storing it
   def click_submit(self):
       self.base_driver.click_element(*self.SUBMIT_BUTTON)
   ```

4. **Tests failing in headless mode**
   ```python
   # Add window size for headless mode
   options.add_argument("--window-size=1920,1080")
   ```

### Debug Mode

```bash
# Run with debug information
pytest tests/ -v -s --tb=long

# Run single test with maximum verbosity
pytest tests/test_login.py::test_login -vv -s
```

## 📊 Test Reports

The framework generates multiple types of reports:

- **HTML Reports**: Visual test results with screenshots
- **JUnit XML**: For CI/CD integration
- **Logs**: Detailed execution logs with timestamps
- **Screenshots**: Automatic capture on test failures

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run linting
flake8 .

# Run type checking
mypy .

# Run security checks
bandit -r .
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Selenium WebDriver](https://selenium.dev/) - Web automation framework
- [pytest](https://pytest.org/) - Testing framework
- [webdriver-manager](https://github.com/SergeyPirogov/webdriver_manager) - Automatic driver management

## 📞 Support

- Create an issue for bug reports or feature requests
- Check existing issues before creating new ones
- Provide detailed information including error messages and environment details

---

**Happy Testing! 🎉**
