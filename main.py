import logging
from parser.video_formatter import build_video_text
from browser.browser_manager import BrowserManager
from browser.tiktok_page import TikTokSampleRequestPage
from sheet.sheet_service import SheetService
from browser.history_panel import HistoryPanel
from reports.report_service import ReportService
from services.gmv_service import GMVService
from pathlib import Path
from datetime import datetime

log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

log_file = log_dir / datetime.now().strftime("run_%Y-%m-%d_%H-%M.log")

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)


def main():
    logging.info("Khởi động TikTok Booking Assistant")

    start_time = datetime.now()
    sheet = SheetService()
    rows = sheet.get_rows_to_process()
    report = ReportService()
    report.total_kocs = len(rows)

    logging.info(f"Tổng số dòng cần xử lý: {len(rows)}")

    browser = BrowserManager()

    try:
        page = browser.connect()

        logging.info("Đã attach Chrome thành công")

        tiktok = TikTokSampleRequestPage(page)

        tiktok.wait_until_ready()

        failed_kocs = []
        success_count = 0

        for index, item in enumerate(rows, start=1):
            logging.info(
                f"[{index}/{len(rows)}] Đang xử lý KOC: {item['koc']}"
            )

            try:
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
                video_count = sum(
                    len(product.get("videos", []))
                    for product in products
                )

                report.add_success(
                    product_count=len(products),
                    video_count=video_count,
                )

                success_count += 1

                logging.info(
                    f"Đã ghi {len(products)} sản phẩm vào Google Sheets"
                )

                logging.info(f"Hoàn thành: {item['koc']}")

            except Exception as e:
                logging.error(
                    f"KOC lỗi: {item['koc']} - {e}"
                )

                failed_kocs.append(
                    {
                        "koc": item["koc"],
                        "row": item["row"],
                        "error": str(e),
                    }
                )
                report.add_failed(
                    koc=item["koc"],
                    row=item["row"],
                    error=str(e),
                )

                continue

        end_time = datetime.now()
        duration = end_time - start_time  

        report_path = report.save()
        logging.info(
            f"Đã tạo report: {report_path}"
        )
        logging.info("========================================")
        logging.info("KẾT THÚC PHIÊN CHẠY")
        logging.info(f"Tổng KOC: {len(rows)}")
        logging.info(f"Thành công: {success_count}")
        logging.info(f"Thất bại: {len(failed_kocs)}")
        logging.info(f"Thời gian chạy: {duration}")

        if failed_kocs:
            logging.info("Danh sách KOC thất bại:")

            for failed in failed_kocs:
                logging.info(
                    f"- {failed['koc']} (dòng {failed['row']}): {failed['error']}"
                )    
        logging.info(f"Log file: {log_file}")
        
    finally:
        browser.close()

def run_gmv_service():
    service = GMVService()
    service.run()

if __name__ == "__main__":
    
    print()
    print("=== TikTok Booking Assistant ===")
    print("1. Tìm kiếm GMV của KOL")
    print("2. Lấy link video của các KOL")
    print()

    choice = input("Chọn chức năng (1/2): ").strip()

    if choice == "1":
        run_gmv_service()

    elif choice == "2":
        main()

    else:
        print("Lựa chọn không hợp lệ.")