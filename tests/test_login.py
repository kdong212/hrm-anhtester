import sys
import os
import pytest
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.home_page import HomePage

@pytest.fixture
def test_logged_in_page(page: Page):
       # --- PHẦN 1: SETUP --- Fixture to login and return HOMEPAGE, along with Teardown logout
    print("\n[Setup] Login ...")
    login_page = LoginPage(page)

    with open("config/credentials.json") as f:
        creds = json.load(f)

    valid = creds["valid_user"]
    HomePage = login_page.login(valid["username"], valid["password"])
    HomePage.assert_login_successful()
    print("[Setup] Done login")

    # --- PHẦN 2: YIELD ---
    yield HomePage

    # --- PHẦN 3: TEARDOWN ---
    print("\n[Fixture Teardown] Logging out ...")
    login_page = HomePage.logout()
    login_page.assert_logout_successful()
    print("[Fixture Teardown] Done logout")

def test_successful_login_standard_user(test_logged_in_page):
    assert test_logged_in_page is not None

