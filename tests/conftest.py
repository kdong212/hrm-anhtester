# import pytest

# import sys
# import os


# from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
# from utils.config_reader import ConfigReader
# import logging

# logger = logging.getLogger(__name__)
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# @pytest.fixture(scope="session")
# def browser():
#     """Browser fixture - khởi tạo browser cho toàn bộ test session"""
#     with sync_playwright() as playwright:
#         browser = playwright.chromium.launch(
#             headless=False,  # Set True để chạy headless
#             slow_mo=50      # Slow down cho dễ observe
#         )
#         yield browser
#         browser.close()

# @pytest.fixture(scope="function")
# def context(browser: Browser):
#     """Browser context fixture - tạo context mới cho mỗi test"""
#     context = browser.new_context(
#         viewport={"width": 960, "height": 540},
#         locale="vi-VN"
#     )
#     yield context
#     context.close()

# @pytest.fixture(scope="function")
# def page(context: BrowserContext):
#     """Page fixture - tạo page mới cho mỗi test"""
#     page = context.new_page()
#     yield page
#     page.close()

# @pytest.fixture(scope="session")
# def test_credentials():
#     """Load test credentials from JSON"""
#     logger.info("Loading test credentials from JSON")
#     return ConfigReader.get_credentials()

# @pytest.fixture(scope="session")
# def base_url():
#     """Get base URL from config"""
#     return ConfigReader.get_base_url()

# import pytest
# from playwright.sync_api import Page
# import json, os,sys

# # sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from pages.home_page import HomePage
# from pages.login_page import LoginPage

# SESSION_FILE = "storage/auth.json"

# @pytest.fixture
# def test_logged_in_page(page: Page):
#     print("\n[Setup] Checking saved session...")
#     if os.path.exists(SESSION_FILE):
#         print("[Setup] Found existing session, using it.")
#         # page.context.add_cookies(json.load(open(SESSION_FILE)))
#         context = page.context
#         context.close()  # đóng context hiện tại
#         new_context = context.browser.new_context(storage_state=SESSION_FILE)
#         page = new_context.new_page()

#         URL = "https://hrm.anhtester.com/erp/login"
#         page.goto(URL)
#         yield HomePage(page)
#         return

#     print("[Setup] No session found, logging in...")
#     login_page = LoginPage(page)
#     with open("config/credentials.json") as f:
#         creds = json.load(f)
#     valid = creds["valid_user"]

#     home_page = login_page.login(valid["username"], valid["password"])
#     home_page.assert_login_successful()

#     # Lưu session
#     page.context.storage_state(path=SESSION_FILE)
#     yield home_page

#     # Teardown
#     print("[Teardown] Logging out...")
#     login_page = home_page.logout()
#     login_page.assert_logout_successful()


import os
import json
import pytest
from playwright.sync_api import Browser
from pages.login_page import LoginPage
from pages.home_page import HomePage

SESSION_FILE = "storage/auth.json"
BASE_URL = "https://hrm.anhtester.com/erp"  # ⚠️ đổi theo dự án bạn



def safe_new_context(browser: Browser, storage_state_path: str):
    """Tạo context an toàn: nếu session file lỗi, tạo context trống."""
    if not os.path.exists(storage_state_path) or os.path.getsize(storage_state_path) == 0:
        print(f"[WARN] No valid session file found at {storage_state_path}")
        return browser.new_context()

    try:
        with open(storage_state_path) as f:
            json.load(f)  # test xem JSON có hợp lệ không
        return browser.new_context(storage_state=storage_state_path)
    except Exception as e:
        print(f"[WARN] Invalid storage_state file, ignoring: {e}")
        return browser.new_context()
    
@pytest.fixture   
def test_logged_in_page(browser: Browser):
    """Tự động login nếu chưa có session, lưu lại để debug lần sau."""

    # --- Nếu có session, thử dùng ---
    if os.path.exists(SESSION_FILE) and os.path.getsize(SESSION_FILE) > 0:
        print(f"[Setup] Trying existing session: {SESSION_FILE}")
        context = safe_new_context(browser, SESSION_FILE)
        page = context.new_page()
        page.goto(f"{BASE_URL}/home")
        try:
            LOGOUT_BUTTON = "a.btn.btn-smb.btn-outline-primary.rounded-pill[href='https://hrm.anhtester.com/erp/system-logout']"
            page.wait_for_selector(LOGOUT_BUTTON, timeout=5000)
            print("[Setup] Reuse session successful ✅")
            yield HomePage(page)
            context.close()
            return
        except Exception:
            print("[WARN] Old session invalid ❌ — will login again.")
            context.close()

    # --- Nếu chưa có session hợp lệ: login lại ---
    print("[Setup] Logging in to create new session...")
    context = browser.new_context()
    page = context.new_page()
    page.goto(f"{BASE_URL}/login")

    # login
    login_page = LoginPage(page)
    with open("config/credentials.json") as f:
        creds = json.load(f)
    valid = creds["valid_user"]

    home_page = login_page.login(valid["username"], valid["password"])
    home_page.assert_login_successful()

    # ✅ Lưu lại session mới
    os.makedirs("storage", exist_ok=True)
    context.storage_state(path=SESSION_FILE)
    print(f"[Setup] Saved new session → {SESSION_FILE}")

    yield home_page

    # Teardown
    context.close()
    print("[Teardown] Context closed ✅")    


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, playwright):
    """
    Cho phép hiển thị browser khi debug
    """
    return {**browser_context_args, "viewport": {"width": 960, "height": 540},"headless": False,}

# @pytest.fixture(scope="session")
# def storage_state_path():
#     """Đường dẫn lưu session"""
#     os.makedirs("storage", exist_ok=True)
#     return SESSION_FILE

# @pytest.fixture(scope="session")
# def ensure_login(browser: Browser, storage_state_path):
#     """
#     Fixture login một lần, lưu lại session (auth.json)
#     Dùng cho debug hoặc chạy test nhiều file
#     """
#     if os.path.exists(storage_state_path):
#         print(f"[Setup] Using existing session from {storage_state_path}")
#         return storage_state_path

#     print("[Setup] No session found → performing login...")
#     context = browser.new_context()
#     page = context.new_page()
#     page.goto(f"{BASE_URL}/login")

#     login_page = LoginPage(page)
#     with open("config/credentials.json") as f:
#         creds = json.load(f)
#         valid = creds["valid_user"]

#     home_page = login_page.login(valid["username"], valid["password"])
#     home_page.assert_login_successful()
#     print("[Setup] Done login")

#     print(f"[Setup] Saving session to {storage_state_path}")
#     context.storage_state(path=storage_state_path)
#     context.close()
#     return storage_state_path


# @pytest.fixture
# def test_logged_in_page(browser: Browser, ensure_login, storage_state_path):
#     """
#     Fixture chính cho test:
#     - Load lại session nếu có
#     - Dùng được cả khi debug
#     """
#     context = safe_new_context(browser, SESSION_FILE)

#     page = context.new_page()
#     page.goto(f"{BASE_URL}/erp/desk")
#     LOGOUT_BUTTON = "a.btn.btn-smb.btn-outline-primary.rounded-pill[href='https://hrm.anhtester.com/erp/system-logout']"
#     page.wait_for_selector(LOGOUT_BUTTON,"3000")
#     # page.wait_for_url(f"{BASE_URL}/erp/desk")

#     yield HomePage(page)

#     context.close()

