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
