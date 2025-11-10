from playwright.sync_api import sync_playwright
from playwright.sync_api import expect,Page

from pages.base_page import BasePage
from pages.warehouse_page import WarehousePage

class HomePage(BasePage):
    WELCOME_MESSAGE = "//h6[@class='m-b-5' and contains(text(),'Welcome')]"

    LOGOUT_BUTTON = "a.btn.btn-smb.btn-outline-primary.rounded-pill[href='https://hrm.anhtester.com/erp/system-logout']"

    def __init__(self, page: Page):
        self.page = page

    def go_to_warehouse_page(self):
        # print("[Action] Navigating to Warehouse Page...")
        # self.page.click(self.menu_warehouse)
        # self.page.wait_for_url("**/warehouse")
        # return WarehousePage(self.page)    
        WAREHOUSE_URL ="https://hrm.anhtester.com/erp/warehouse-list"
        self._visit(WAREHOUSE_URL)
        return WarehousePage(self.page)

    def assert_login_successful(self):
        """Xác minh đăng nhập thành công."""
        welcome_locator = self._get_locator(self.WELCOME_MESSAGE)
        expect(welcome_locator).to_be_visible()
        expect(welcome_locator).to_contain_text("Welcome")

    def logout(self):
        self._click(self.LOGOUT_BUTTON)
        from pages.login_page import LoginPage
        return LoginPage(self.page)    

    