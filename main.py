import logging
from parser.video_formatter import build_video_text
from browser.browser_manager import BrowserManager
from browser.tiktok_page import TikTokSampleRequestPage
from sheet.sheet_service import SheetService
from browser.history_panel import HistoryPanel

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%H:%M:%S",
)


def main():
    logging.info("Khởi động TikTok Booking Assistant")

    sheet = SheetService()
    rows = sheet.get_rows_to_process()

    logging.info(f"Tổng số dòng cần xử lý: {len(rows)}")

    browser = BrowserManager()

    try:
        page = browser.connect()

        logging.info("Đã attach Chrome thành công")

        tiktok = TikTokSampleRequestPage(page)

        tiktok.wait_until_ready()

        for index, item in enumerate(rows, start=1):
            logging.info(
                f"[{index}/{len(rows)}] Đang xử lý KOC: {item['koc']}"
            )

            tiktok.search_koc(item["koc"])
            tiktok.select_koc(item["koc"])

            tiktok.open_history()
            panel = HistoryPanel(page)
            products = panel.process_products()

            video_text = build_video_text(products)

            sheet.update_video_links(
                item["row"],
                video_text
            )
            logging.info(
                f"Đã ghi {len(products)} sản phẩm vào Google Sheets"
            )
            tiktok.verify_history_opened()

            logging.info(f"Hoàn thành: {item['koc']}")

    finally:
        browser.close()


if __name__ == "__main__":
    main()