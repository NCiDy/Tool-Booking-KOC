from playwright.sync_api import Page
import logging


class TikTokSampleRequestPage:
    def __init__(self, page: Page):
        self.page = page

    def wait_until_ready(self):
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(1000)

    def search_koc(self, koc_name: str):
        logging.info(f"Tìm kiếm KOC: {koc_name}")

        search_input = self.page.locator(
            "input[data-tid='m4b_input_search']"
        )

        search_input.wait_for(state="visible", timeout=10000)

        search_input.click()

        # Xóa nội dung cũ
        search_input.fill("")
        # Nhập tên KOC
        search_input.fill(koc_name)
        # Chờ dropdown hiển thị
        self.page.wait_for_timeout(1500)

    def select_koc(self, koc_name: str):
        logging.info(f"Chọn KOC: {koc_name}")

        # Chờ dropdown xuất hiện
        dropdown = self.page.locator("div[data-tid='m4b_dropdown_menu']")
        dropdown.wait_for(state="visible", timeout=10000)

        # Chọn item có đúng username
        koc_item = dropdown.locator(
            f"div[data-tid='m4b_dropdown_menu_item']:has(span.text-brand-10:has-text('{koc_name}'))"
        ).first

        koc_item.wait_for(state="visible", timeout=10000)

        koc_item.click()

        self.page.wait_for_timeout(1500)

        logging.info("Đã chọn đúng KOC")

    def open_history(self):
        logging.info("Mở popup Lịch sử")

        history_button = self.page.locator(
            "div[data-e2e='d26e4665-f69b-79ec'] img.cursor-pointer"
        ).first

        history_button.wait_for(state="visible", timeout=10000)

        history_button.click()

        logging.info("Đã click nút Lịch sử")

         # Chờ panel lịch sử xuất hiện
        self.verify_history_opened()

    def verify_history_opened(self):
        logging.info("Kiểm tra popup Lịch sử")

        history_panel = self.page.locator(
            "tr.core-table-expand-content div.prod-group-by-creator-list__SubTableWrap-eMtloh"
        ).first

        history_panel.wait_for(state="visible", timeout=10000)

        logging.info("Xác nhận popup Lịch sử đã mở")