from playwright.sync_api import Page, expect, Locator, TimeoutError

class BasePage:
    """Lớp cha chứa các hành động Playwright cơ bản, kế thừa cho mọi Page Object."""

    def __init__(self, page: Page):
        self.page = page

    def _visit(self, url: str):
        """Điều hướng tới URL được chỉ định."""
        print(f"[BasePage] Navigate to: {url}")
        self.page.goto(url, wait_until="domcontentloaded")

    def _get_locator(self, locator: str) -> Locator:
        """Trả về đối tượng Locator từ chuỗi selector."""
        return self.page.locator(locator)
    
    def _get_by_role(self,role:str) --> Role:
        return self.page.get_by_role(role)

    def _click(self, locator: str, name: str = ""):
        """Thực hiện click với xử lý lỗi và ghi log."""
        try:
            print(f"[Click] {name or locator}")
            element = self._get_locator(locator)
            expect(element).to_be_visible()
            element.click()
        except Exception as e:
            print(f"[ERROR] Unable to click to {locator}: {type(e).__name__} - {e}")
            raise

    def _fill(self, locator: str, text: str, name: str = ""):
        """Điền dữ liệu vào ô input."""
        print(f"[Fill] '{text}' into {name or locator}")
        self._get_locator(locator).fill(text)

    def _select_item_from_ddl(self,locator:str,search:str,item:str,index: int = 1):
        """Click vô ô, điền dữ liệu, nhấn ENTER"""

        ddl = self._get_locator(locator)
        ddl.click()

        # Tìm ô search và nhập giá trị
        search_box = self._get_by_role(search).nth(index)
        search_box.fill(item)
        search_box.press("Enter")


    # page.locator(PICKUP_LOCATION_DROPDOWN).click() # Click để mở dropdown
    #     if warehouse_data.location == "Yes":
    #         page.locator(PICKUP_LOCATION_OPTION_YES).click()
    #     else:
    #         page.locator(PICKUP_LOCATION_OPTION_NO).click()

    def select_from_custom_dropdown(self, dropdown_locator: str, option_text: str):
        """
        Mở một dropdown tùy chỉnh (ví dụ: Select2) và chọn một tùy chọn dựa trên text.
        
        Args:
            dropdown_locator (str): Locator của phần tử hiển thị dropdown (ví dụ: container).
            option_text (str): Text của tùy chọn cần chọn.
        """
        self.page.locator(dropdown_locator).click() # Click để mở dropdown
        
        # Giả định cấu trúc options là li trong ul có ID là kết quả của dropdown_locator + '-results'
        # Ví dụ: nếu dropdown_locator là '#select2-id-container', thì results là '#select2-id-results'
        # Cần điều chỉnh nếu cấu trúc HTML khác
        dropdown_id = dropdown_locator.split('-container')[0].replace('#select2-', '')
        results_list_id = f"select2-{dropdown_id}-results"
        
        option_locator = f"//ul[@id='{results_list_id}']/li[text()='{option_text}']"
        self.page.locator(option_locator).click()

    def _select(self,locator,locator1, locator2,option:str,name:str=""):
        print(f"[Select] '{option}' into {name or locator}")
        self._get_locator(locator).click()
        if option =="Yes":
            self._get_locator(locator1).click()
        else:
            self._get_locator(locator2).click()

    def _assert_text_visible(self, locator: str, text: str):
        """Kiểm tra văn bản mong đợi hiển thị trên giao diện."""
        print(f"[Assert] Check '{text}' exists")
        expect(self._get_locator(locator)).to_contain_text(text)