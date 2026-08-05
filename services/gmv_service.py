import logging

from browser.browser_manager import BrowserManager
from browser.tiktok_page import TikTokSampleRequestPage
from browser.creator_search_page import CreatorSearchPage
from sheet.gmv_sheet_service import GMVSheetService
from parser.gmv_parser import parse_gmv, parse_sales
from config import GMV_THRESHOLD, SALES_THRESHOLD
from config import TIKTOK_CREATOR_SEARCH_URL


class GMVService:
    def run(self):
        logging.info("Chức năng: Tìm kiếm GMV của KOL")

        sheet = GMVSheetService()
        rows = sheet.get_rows_to_process()

        logging.info(f"Tổng số dòng cần xử lý: {len(rows)}")

        browser = BrowserManager()

        success_count = 0
        qualified_count = 0
        rejected_count = 0
        failed_count = 0

        try:
            page = browser.connect(TIKTOK_CREATOR_SEARCH_URL)
            logging.info("Đã attach Chrome thành công")

            tiktok = TikTokSampleRequestPage(page)
            creator = CreatorSearchPage(page)

            tiktok.wait_until_ready()

            for index, item in enumerate(rows, start=1):
                logging.info(
                    f"[{index}/{len(rows)}] Đang xử lý KOC: {item['koc']}"
                )

                try:
                    tiktok.search_koc(item["koc"])
                    tiktok.select_creator_koc(item["koc"])

                    metrics = creator.read_metrics()

                    gmv_text = metrics["gmv_text"]
                    sales_text = metrics["sales_text"]

                    gmv_value, gmv_hidden = parse_gmv(gmv_text)
                    sales_value = parse_sales(sales_text)

                    result = ""

                    if not gmv_hidden and gmv_value is not None:
                        if gmv_value > GMV_THRESHOLD:
                            result = gmv_text

                    else:
                        if sales_value > SALES_THRESHOLD:
                            result = f"{sales_value} SMBR"

                    if result:
                        sheet.update_result(
                            item["row"],
                            result
                        )

                        qualified_count += 1

                        logging.info(
                            f"Đạt điều kiện - {result}"
                        )

                    else:
                        sheet.clear_result(item["row"])

                        rejected_count += 1

                        logging.info(
                            "Không đạt điều kiện"
                        )

                    success_count += 1

                except Exception as e:
                    failed_count += 1

                    logging.error(
                        f"KOC lỗi: {item['koc']} - {e}"
                    )

                    continue

            logging.info("========================================")
            logging.info("KẾT THÚC PHIÊN CHẠY GMV")
            logging.info(f"Tổng KOC: {len(rows)}")
            logging.info(f"Xử lý thành công: {success_count}")
            logging.info(f"Đạt điều kiện: {qualified_count}")
            logging.info(f"Không đạt: {rejected_count}")
            logging.info(f"Lỗi: {failed_count}")

        finally:
            browser.close()