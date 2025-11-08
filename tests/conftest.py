import pytest

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from utils.config_reader import ConfigReader
import logging

logger = logging.getLogger(__name__)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(scope="session")
def browser():
    """Browser fixture - khởi tạo browser cho toàn bộ test session"""
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=False,  # Set True để chạy headless
            slow_mo=50      # Slow down cho dễ observe
        )
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def context(browser: Browser):
    """Browser context fixture - tạo context mới cho mỗi test"""
    context = browser.new_context(
        viewport={"width": 960, "height": 540},
        locale="vi-VN"
    )
    yield context
    context.close()

@pytest.fixture(scope="function")
def page(context: BrowserContext):
    """Page fixture - tạo page mới cho mỗi test"""
    page = context.new_page()
    yield page
    page.close()

@pytest.fixture(scope="session")
def test_credentials():
    """Load test credentials from JSON"""
    logger.info("Loading test credentials from JSON")
    return ConfigReader.get_credentials()

@pytest.fixture(scope="session")
def base_url():
    """Get base URL from config"""
    return ConfigReader.get_base_url()