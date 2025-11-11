from playwright.sync_api import expect,Page,sync_playwright

from pages.base_page import BasePage


class WarePage(BasePage):
        



        

    COUNTRY_DROPDOWN_DISPLAY = "#select2-country-k1-container" # Locator cho phần tử hiển thị giá trị được chọn
    COUNTRY_SEARCH_INPUT = "span.select2-search.select2-search--dropdown > input" # Giả định input search khi dropdown mở
    COUNTRY_OPTIONS_LIST = "ul.select2-results__options li" # Locator cho các option trong dropdown sau khi mở

    COUNTRY_NAME = "Australia"
    def __init__(self, page: Page):
        self.page = page

        
    def select_country(self,country_name):
        # self.page.click(self.COUNTRY_DROPDOWN_DISPLAY)
        # self.page.wait_for_selector(self.COUNTRY_OPTIONS_LIST)
        #     # self.page.fill(self.COUNTRY_SEARCH_INPUT,country_name)
        # try:
        #     search_locator = self.page.locator(self.COUNTRY_SEARCH_INPUT)
        #     if search_locator.count() > 0:
        #         print("[select_country] Found search input inside dropdown — filling it")
        #         search_locator.fill(country_name)
        #                 # small wait để nội dung lọc xuất hiện
        #         self.page.wait_for_timeout(200)
        #         self.page.keyboard.press("Enter")
        # except Exception as e:
        #             # không phải lỗi fatal nếu không có ô search
        #             print(f"[select_country] No search input or failed to fill: {e}")
        # expect(self.page.locator(self.COUNTRY_DROPDOWN_DISPLAY)).to_contain_text(country_name)
        

        # self.page.get_by_text(country_name, exact=True).click()

        # expect(self.page.locator(self.COUNTRY_DROPDOWN_DISPLAY)).to_contain_text(country_name)
        # print(f"[select_country] SUCCESS: selected '{country_name}'")
        # ✅ 1. Click vào dropdown "Country"
        self.page.locator("span.select2-selection__rendered", has_text="Country").click()

        # ✅ 2. Nhập hoặc chọn giá trị "Vietnam"
        self.page.locator(".select2-search__field").fill(country_name)

        # ✅ 3. Click chọn item từ list hiển thị
        self.page.locator(".select2-results__option", has_text=country_name).click()

        # ✅ 4. Kiểm tra giá trị hiển thị
        expect(self.page.locator("span.select2-selection__rendered")).to_have_text("Vietnam")
        
        

        