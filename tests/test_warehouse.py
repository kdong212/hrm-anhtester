import sys
import os
import pytest
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from playwright.sync_api import Page
# from pages.login_page import LoginPage
from pages.home_page import HomePage
from data.warehouse_data import WarehouseData
from pages.warehouse_page import WarehousePage

# @pytest.fixture
# def test_logged_in_page(page: Page):
#        # --- PHẦN 1: SETUP --- Fixture to login and return HOMEPAGE, along with Teardown logout
#     print("\n[Setup] Login ...")
#     login_page = LoginPage(page)

#     with open("config/credentials.json") as f:
#         creds = json.load(f)

#     valid = creds["valid_user"]
#     HomePage = login_page.login(valid["username"], valid["password"])
#     HomePage.assert_login_successful()
#     print("[Setup] Done login")

#     # --- PHẦN 2: YIELD ---
#     yield page

#     # --- PHẦN 3: TEARDOWN ---
#     print("\n[Fixture Teardown] Logging out ...")
#     # login_page = HomePage.logout()
#     # login_page.assert_logout_successful()
#     print("[Fixture Teardown] Done logout")

def test_add_warehouse_successful(test_logged_in_page):
    # assert test_logged_in_page is not None
    warehouse_data = WarehouseData()
    home_page = test_logged_in_page
    warehouse_page = home_page.go_to_warehouse_page()
    warehouse_page.click_add_new_button()
    warehouse_page.fill_warehouse_details(warehouse_data)
    warehouse_page.save_warehouse()
    
    warehouse_page.verify_warehouse_in_list(warehouse_data)

    print(f"Warehouse '{warehouse_data.name}' đã được thêm và hiển thị đúng trong danh sách.")
