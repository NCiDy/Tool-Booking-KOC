import logging

from browser.browser_manager import BrowserManager
from sheet.sheet_service import SheetService

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%H:%M:%S",
)


def main():
    logging.info("Khởi động TikTok Booking Assistant")

    logging.info("Kết nối Google Sheets")
    sheet = SheetService()

    rows = sheet.get_rows_to_process()

    logging.info(f"Tổng số dòng cần xử lý: {len(rows)}")

    logging.info("Kết nối Chrome (CDP)")

    browser = BrowserManager()

    try:
        page = browser.connect()

        logging.info("Đã attach thành công vào tab TikTok Shop Affiliate")

        logging.info(f"URL hiện tại: {page.url}")

    finally:
        browser.close()


if __name__ == "__main__":
    main()