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
