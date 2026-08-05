import logging
from playwright.sync_api import Page


class CreatorSearchPage:
    def __init__(self, page: Page):
        self.page = page

    def read_metrics(self):
        logging.info("Đọc GMV và Số món bán ra")

        table_body = self.page.locator("tbody").first
        table_body.wait_for(state="visible", timeout=10000)

        first_row = table_body.locator("tr").first
        first_row.wait_for(state="visible", timeout=10000)

        gmv_text = first_row.locator(
            "td:nth-child(4) span"
        ).first.inner_text().strip()

        sales_text = first_row.locator(
            "td:nth-child(5) span"
        ).first.inner_text().strip()

        logging.info(f"GMV: {gmv_text}")
        logging.info(f"Số món bán ra: {sales_text}")

        return {
            "gmv_text": gmv_text,
            "sales_text": sales_text,
        }