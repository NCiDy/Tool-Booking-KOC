import logging
import random

from playwright.sync_api import Locator, Page


class CreatorSearchPage:
    def __init__(self, page: Page):
        self.page = page

    def read_metrics(self):
        first_row = self.get_creator_rows().first
        first_row.wait_for(state="visible", timeout=10000)

        return self.read_metrics_from_row(first_row)

    def get_creator_rows(self) -> Locator:
        table_body = self.page.locator("tbody").first
        table_body.wait_for(state="visible", timeout=20000)

        rows = table_body.locator("tr")
        rows.first.wait_for(state="visible", timeout=20000)

        return rows

    def read_username_from_row(self, row: Locator) -> str:
        return row.locator(
            "span.text-body-m-medium"
        ).first.inner_text().strip()

    def read_metrics_from_row(self, row: Locator):
        logging.info("Đọc GMV và Số món bán ra")

        gmv_text = row.locator(
            "td:nth-child(4) span"
        ).first.inner_text().strip()

        sales_text = row.locator(
            "td:nth-child(5) span"
        ).first.inner_text().strip()

        # Category
        try:
            category_text = row.locator(
                "svg.alliance-icon-Bag + span span.text-overflow-single"
            ).first.inner_text().strip()

        except Exception:
            category_text = ""


        logging.info(f"GMV: {gmv_text}")
        logging.info(f"Số món bán ra: {sales_text}")
        logging.info(f"Category: {category_text}")

        return {
            "gmv_text": gmv_text,
            "sales_text": sales_text,
            "category_text": category_text,
        }

    def scroll_to_load_more(self):
        rows = self.get_creator_rows()
        last_row = rows.nth(rows.count() - 1)

        last_row.scroll_into_view_if_needed()
        last_row.evaluate(
            """
            element => {
                let parent = element.parentElement;

                while (parent) {
                    const style = window.getComputedStyle(parent);
                    const canScroll = /(auto|scroll)/.test(style.overflowY)
                        && parent.scrollHeight > parent.clientHeight;

                    if (canScroll) {
                        parent.scrollTop = parent.scrollHeight;
                        return;
                    }

                    parent = parent.parentElement;
                }

                window.scrollTo(0, document.body.scrollHeight);
            }
            """
        )

        delay = random.randint(3000, 5000)
        logging.info(
            f"Đã tới cuối danh sách, chờ {delay / 1000:.1f}s để tải thêm KOC"
        )
        self.page.wait_for_timeout(delay)
