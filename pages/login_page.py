from playwright.sync_api import sync_playwright
from playwright.sync_api import expect

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Đại diện cho trang đăng nhập của hệ thống."""

    # Locators (được định nghĩa như hằng số)
    URL = "https://hrm.anhtester.com/erp/login"
    
    USERNAME_FIELD = "#iusername"
    PASSWORD_FIELD = "#ipassword"
    LOGIN_BUTTON = ".btn.btn-primary.mt-2.ladda-button"

    SUCCESS_MESSAGE = "h2:has-text('Logged In Successfully.')"
    ERROR_MESSAGE = ".alert-danger"
    WELCOME_MESSAGE = "//h6[contains(text(), 'Welcome')]"

    # Business Actions
    def goto(self):
        """Điều hướng tới trang Login."""
        self._visit(self.URL)

    def login(self, username, password):
        """Thực hiện nghiệp vụ đăng nhập."""
        self.goto()
        self._fill(self.USERNAME_FIELD, username, name="Username")
        self._fill(self.PASSWORD_FIELD, password, name="Password")
        self._click(self.LOGIN_BUTTON, name="Login Button")
        from pages.home_page import HomePage
        try:
            self.page.locator(self.WELCOME_MESSAGE).is_visible()
            return HomePage(self.page)
        except TimeoutError:
            # Nếu không thấy giỏ hàng, kiểm tra lỗi đăng nhập
            if self.page.locator(self.ERROR_MESSAGE).is_visible():
                raise Exception("Login failed: Sai tên đăng nhập hoặc mật khẩu.")
            else:
                raise Exception("Login failed: Không xác định được trạng thái sau đăng nhập.")

    def assert_error_message_visible(self, expected_text):
        """Kiểm tra thông báo lỗi đăng nhập hiển thị đúng."""
        self._assert_text_visible(self.ERROR_MESSAGE, expected_text)

    def assert_logout_successful(self):
        expect(self.page).to_have_url(self.URL)


    
    