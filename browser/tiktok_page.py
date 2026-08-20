from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
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

        try:
            # Chờ dropdown xuất hiện
            dropdown = self.page.locator(
                "div[data-tid='m4b_dropdown_menu']"
            )

            dropdown.wait_for(
                state="visible",
                timeout=3000
            )

            # Chọn item có đúng username
            koc_item = dropdown.locator(
                f"div[data-tid='m4b_dropdown_menu_item']:has(span.text-brand-10:has-text('{koc_name}'))"
            ).first

            koc_item.wait_for(
                state="visible",
                timeout=3000
            )

            koc_item.click()

            self.page.wait_for_timeout(1500)

            logging.info("Đã chọn đúng KOC")

        except PlaywrightTimeoutError:
            raise Exception(
                f"Không tìm thấy KOC: {koc_name}"
            )


    def select_creator_koc(self, koc_name: str):
        logging.info(f"Chọn KOC Creator: {koc_name}")

        try:
            dropdown = self.page.locator(
                "div[data-tid='m4b_dropdown_menu']"
            )

            dropdown.wait_for(
                state="visible",
                timeout=10000
            )

            items = dropdown.locator(
                "div[data-tid='m4b_dropdown_menu_item']"
            )

            count = items.count()

            if count == 0:
                raise Exception(f"Không tìm thấy KOC: {koc_name}")

            # Chỉ có 1 kết quả → click luôn
            if count == 1:
                items.first.click()
                self.page.wait_for_timeout(1500)
                logging.info("Đã chọn KOC Creator (1 kết quả)")
                return

            # Có từ 2 kết quả trở lên → so khớp chính xác username
            for i in range(count):
                item = items.nth(i)

                username = item.locator(
                    "span[data-e2e='c56dc287-a320-2ef6']"
                ).first.inner_text().strip()

                logging.info(f"Kết quả {i+1}: {username}")

                if username == koc_name:
                    item.click()
                    self.page.wait_for_timeout(1500)
                    logging.info(
                        "Đã chọn đúng KOC Creator theo username"
                    )
                    return

            raise Exception(f"Không tìm thấy KOC: {koc_name}")

        except PlaywrightTimeoutError:
            raise Exception(f"Không tìm thấy KOC: {koc_name}")

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
        history_item = self.page.locator(
            'div[class*="ProdGroupByCreatorItemWrap"]'
        ).first

        history_item.wait_for(
            state="visible",
            timeout=10000
        )

        logging.info("Xác nhận popup Lịch sử đã mở")