from playwright.sync_api import sync_playwright
from playwright.sync_api import expect,Page
import random
from faker import Faker
from pages.base_page import BasePage
from data.warehouse_data import WarehouseData

fake = Faker()

class WarehousePage(BasePage):
    WAREHOUSE_URL ="https://hrm.anhtester.com/erp/warehouse-list"

    ADD_NEW_BUTTON = "role=link[name='Add New']"

    WAREHOUSE_NAME_INPUT = "role=textbox[name='Warehouse Name']"
    CONTACT_NUMBER_INPUT = "div.card-body > div.row > div:nth-child(2) input[type='text']" # Cần cụ thể hơn cho input field
    PICKUP_LOCATION_DROPDOWN = "#select2-pickup_location-9l-container" # Locator cho phần tử hiển thị giá trị được chọn
    PICKUP_LOCATION_OPTION_YES = "//ul[@id='select2-pickup_location-9l-results']/li[text()='Yes']" # Giả định cấu trúc options
    PICKUP_LOCATION_OPTION_NO = "//ul[@id='select2-pickup_location-9l-results']/li[text()='No']" # Giả định cấu trúc options

    COUNTRY_DROPDOWN_DISPLAY = "#select2-country-k1-container" # Locator cho phần tử hiển thị giá trị được chọn
    COUNTRY_SEARCH_INPUT = "span.select2-search.select2-search--dropdown > input" # Giả định input search khi dropdown mở
    COUNTRY_OPTIONS_LIST = "ul.select2-results__options li" # Locator cho các option trong dropdown sau khi mở

    ADDRESS_INPUT = "role=textbox[name='Address']"
    # ADDRESS2_INPUT: Bạn chưa cung cấp locator. Thêm vào đây nếu có.
    CITY_INPUT = "role=textbox[name='City']"
    STATE_INPUT = "role=textbox[name='State / Province']"
    POSTAL_CODE_INPUT = "role=textbox[name='Zip Code / Postal Code']"
    SAVE_BUTTON = ".btn.btn-primary.ladda-button"

    SUCCESS_MESSAGE = "text='Warehouse added'" # Giả định text của thông báo thành công
    WAREHOUSE_LIST_TABLE = "#xin_table" # Locator cho bảng chứa danh sách warehouse

    # def __init__(self, page: Page):
    #     self.page = page

    # def __init__(self, location_option=None, country_name=None):
        # self.name = f"WH_{fake.company()}_{fake.random_int(min=1000, max=9999)}"
        # self.contact_number = fake.phone_number()
        # # 'Yes' cho Pickup, 'No' cho Drop Off. Điều chỉnh nếu logic thực tế khác.
        # self.location = location_option if location_option is not None else random.choice(["Yes", "No"])
        # self.country = country_name # Sẽ được gán sau khi lấy từ dropdown
        # self.address = fake.street_address()
        # self.address2 = fake.secondary_address() # Bạn chưa cung cấp locator cho Address 2, tạm thời bỏ qua hoặc thêm nếu có.
        # self.city = fake.city()
        # self.state = fake.state() # Bạn chưa cung cấp locator cho State, tạm thời bỏ qua hoặc thêm nếu có.
        # self.postal_code = fake.postcode() # Bạn chưa cung cấp locator cho Postal Code, tạm thời bỏ qua hoặc thêm nếu có.

    def navigate_to_warehouse_list(self):
        self._visit(self.WAREHOUSE_URL)

    def click_add_new_button(self):
        self._click(self.ADD_NEW_BUTTON)

    def add_warehouse_record(self,warehouse_data: WarehouseData):
        
        # page.goto("https://hrm.anhtester.com/login")
        # page.fill("input[name='email']", "admin_example")
        # page.fill("input[name='password']", "123456")
        # page.click("button[type='submit']")
        # expect(page.locator("text='Welcome'")).to_be_visible() # Xác nhận đăng nhập thành công

    # Điều hướng đến trang thêm Warehouse
        self.navigate_to_warehouse_list()
        #----------------------------- update by going to submenu later
        self.click_add_new_button()

    # --- Step 1: Tạo dữ liệu ngẫu nhiên ---
        # warehouse_data = WarehouseData()

        # --- Step 2, 3: Điền tên và số liên lạc ---
        # self.goto()
        # self._fill(self.USERNAME_FIELD, username, name="Username")
        # self._fill(self.PASSWORD_FIELD, password, name="Password")
        # self._click(self.LOGIN_BUTTON, name="Login Button")
        # from pages.home_page import HomePage
        # try:
        #     self.page.locator(self.WELCOME_MESSAGE).is_visible()
        #     return HomePage(self.page)
        # except TimeoutError:
        #     # Nếu không thấy giỏ hàng, kiểm tra lỗi đăng nhập
        #     if self.page.locator(self.ERROR_MESSAGE).is_visible():
        #         raise Exception("Login failed: Sai tên đăng nhập hoặc mật khẩu.")
        #     else:
        #         raise Exception("Login failed: Không xác định được trạng thái sau đăng nhập.")
            
        self._fill(self.WAREHOUSE_NAME_INPUT,warehouse_data.name)
        self._fill(self.CONTACT_NUMBER_INPUT,warehouse_data.contact_number)

        

        # --- Step 4: Chọn Location (Pickup/Drop off) --

        # page.locator(PICKUP_LOCATION_DROPDOWN).click() # Click để mở dropdown
        # if warehouse_data.location == "Yes":
        #     page.locator(PICKUP_LOCATION_OPTION_YES).click()
        # else:
        #     page.locator(PICKUP_LOCATION_OPTION_NO).click()

        self.select_from_custom_dropdown(self.PICKUP_LOCATION_DROPDOWN_DISPLAY, warehouse_data.location)

        # Logic chọn Country (vẫn giữ ở đây vì phức tạp hơn với search input)
        self.page.locator(self.COUNTRY_DROPDOWN_DISPLAY).click()
        self.page.wait_for_selector(self.COUNTRY_OPTIONS_LIST)
        
        country_elements = self.page.locator(self.COUNTRY_OPTIONS_LIST).all()
        all_countries = [elem.text_content().strip() for elem in country_elements if elem.text_content().strip() != '']
        selected_country = random.choice(all_countries)
        warehouse_data.country = selected_country
        
        self.page.fill(self.COUNTRY_SEARCH_INPUT, selected_country)
        # Locator này cần chính xác để click vào option đã search
        self.page.locator(f"//ul[contains(@id, 'select2-country') and contains(@id, '-results')]/li[text()='{selected_country}']").click()
        
        self.page.fill(self.ADDRESS_INPUT, warehouse_data.address)
        self.page.fill(self.CITY_INPUT, warehouse_data.city)
        self.page.fill(self.STATE_INPUT, warehouse_data.state)
        self.page.fill(self.POSTAL_CODE_INPUT, warehouse_data.postal_code)

        # --- Step 9: Click Save ---
        # page.click(SAVE_BUTTON)

        # # --- Expected Result 1: Xác minh thông báo thành công ---
        # expect(page.locator(SUCCESS_MESSAGE)).to_be_visible()
        # print("Thông báo 'Warehouse added' đã hiển thị.")

        # # --- Expected Result 2: Xác minh record mới trong danh sách ---
        # # Chuyển hướng về trang danh sách (nếu cần) hoặc đợi danh sách cập nhật
        # # page.goto("URL_TO_WAREHOUSE_LIST") # Nếu sau khi save không tự chuyển

        # # Tìm hàng trong bảng có chứa tên warehouse vừa tạo
        # # Cần một locator đủ mạnh để tìm hàng chứa text cụ thể
        # new_record_row = page.locator(f"{WAREHOUSE_LIST_TABLE} >> text={warehouse_data.name}")
        # expect(new_record_row).to_be_visible()

        # # Xác minh các cột khác trong hàng đó
        # # Điều này yêu cầu bạn biết cấu trúc cột của bảng (ví dụ: cột thứ mấy là Tên, SĐT, Thành phố,...)
        # # Giả định thứ tự các cột (có thể cần điều chỉnh): Tên, SĐT, Thành phố, Quốc gia, Added By
        # expect(new_record_row.locator("td:nth-child(1)")).to_contain_text(warehouse_data.name)
        # expect(new_record_row.locator("td:nth-child(2)")).to_contain_text(warehouse_data.contact_number)
        # expect(new_record_row.locator("td:nth-child(3)")).to_contain_text(warehouse_data.city)
        # expect(new_record_row.locator("td:nth-child(4)")).to_contain_text(warehouse_data.country)
        # expect(new_record_row.locator("td:nth-child(5)")).to_contain_text("admin_example") # Giả định user logged là admin_example

        # print(f"Warehouse '{warehouse_data.name}' đã được thêm và hiển thị đúng trong danh sách.")



    def save_warehouse(self):
        self.page.click(self.SAVE_BUTTON)
        expect(self.page.locator(self.SUCCESS_MESSAGE)).to_be_visible()

    def verify_warehouse_in_list(self, warehouse_data):
        new_record_row = self.page.locator(f"{self.WAREHOUSE_LIST_TABLE} >> text={warehouse_data.name}")
        expect(new_record_row).to_be_visible()

        expect(new_record_row.locator("td:nth-child(1)")).to_contain_text(warehouse_data.name)
        expect(new_record_row.locator("td:nth-child(2)")).to_contain_text(warehouse_data.contact_number)
        expect(new_record_row.locator("td:nth-child(3)")).to_contain_text(warehouse_data.city)
        expect(new_record_row.locator("td:nth-child(4)")).to_contain_text(warehouse_data.country)
        expect(new_record_row.locator("td:nth-child(5)")).to_contain_text("admin_example") # Giả định user logged