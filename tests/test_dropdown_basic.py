import sys, os
from pathlib import Path

# ✅ Thêm project root vào sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from pages.ware_page import WarePage
from playwright.sync_api import sync_playwright
def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 👀 mở UI thật
        page = browser.new_page()

        # đường dẫn động đến file warehouse.html
        html_path = Path(__file__).parent.parent / "sources" / "warehouse.html"
        file_url = html_path.resolve().as_uri()

        print(f"Opening: {file_url}")
        page.goto(file_url)

        

        ware_page = WarePage(page)
        country_name = "Australia"
        ware_page.select_country(country_name)

        input("Nhấn Enter để đóng browser...")
if __name__ == "__main__":
    main()