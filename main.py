import logging
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

    logging.info("Đọc dữ liệu")
    rows = sheet.get_rows_to_process()

    logging.info(f"Tổng số dòng cần xử lý: {len(rows)}")

    for i, item in enumerate(rows, start=1):
        logging.info(
            f"[{i}/{len(rows)}] Row {item['row']} - {item['koc']} | {item['product']}"
        )


if __name__ == "__main__":
    main()