from playwright.sync_api import sync_playwright
from playwright.sync_api import expect,Page

from pages.base_page import BasePage

class HomePage(BasePage):
    WELCOME_MESSAGE = "//h6[@class='m-b-5' and contains(text(),'Welcome')]"

    LOGOUT_BUTTON = "a.btn.btn-smb.btn-outline-primary.rounded-pill[href='https://hrm.anhtester.com/erp/system-logout']"

    def __init__(self, page: Page):
        self.page = page

    def assert_login_successful(self):
        """Xác minh đăng nhập thành công."""
        welcome_locator = self._get_locator(self.WELCOME_MESSAGE)
        expect(welcome_locator).to_be_visible()
        expect(welcome_locator).to_contain_text("Welcome")

    def logout(self):
        self._click(self.LOGOUT_BUTTON)
        from pages.login_page import LoginPage
        return LoginPage(self.page)    

    