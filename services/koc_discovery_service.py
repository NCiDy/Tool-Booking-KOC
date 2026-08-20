import logging

from browser.browser_manager import BrowserManager
from browser.creator_search_page import CreatorSearchPage
from config import EXISTING_KOC_FILE, TIKTOK_CREATOR_SEARCH_URL
from services.gmv_service import evaluate_metrics
from sheet.koc_data_sheet_service import KOCDataSheetService
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

class KOCDiscoveryService:
    @staticmethod
    def normalize_username(username: str) -> str:
        return username.strip().casefold()

    def load_existing_kocs(self) -> set[str]:
        if not EXISTING_KOC_FILE.exists():
            EXISTING_KOC_FILE.touch()
            return set()

        with EXISTING_KOC_FILE.open("r", encoding="utf-8") as file:
            return {
                self.normalize_username(line)
                for line in file
                if line.strip()
            }

    @staticmethod
    def append_existing_koc(username: str):
        needs_newline = False

        if EXISTING_KOC_FILE.exists() and EXISTING_KOC_FILE.stat().st_size > 0:
            with EXISTING_KOC_FILE.open("rb") as file:
                file.seek(-1, 2)
                needs_newline = file.read(1) not in (b"\n", b"\r")

        with EXISTING_KOC_FILE.open("a", encoding="utf-8") as file:
            if needs_newline:
                file.write("\n")

            file.write(f"{username}\n")

    def run(self):
        logging.info("Chức năng: Lấy KOC trực tiếp từ danh sách TikTok")

        existing_kocs = self.load_existing_kocs()
        seen_on_web = set()

        logging.info(
            f"Đã tải {len(existing_kocs)} username từ existing_kocs.txt vào Set"
        )

        sheet = KOCDataSheetService()
        browser = BrowserManager()

        scanned_count = 0
        written_count = 0
        duplicate_count = 0
        failed_count = 0

        try:
            page = browser.connect(TIKTOK_CREATOR_SEARCH_URL)
            logging.info("Đã attach Chrome thành công")

            creator = CreatorSearchPage(page)

            while True:
                rows = creator.get_creator_rows()
                row_count = rows.count()

                for index in range(row_count):
                    row = rows.nth(index)

                    try:
                        username = creator.read_username_from_row(row)
                        normalized_username = self.normalize_username(username)

                        if not normalized_username:
                            continue

                        if normalized_username in seen_on_web:
                            continue

                        seen_on_web.add(normalized_username)
                        scanned_count += 1

                        logging.info(
                            f"[{scanned_count}] Đang kiểm tra KOC: {username}"
                        )

                        if normalized_username in existing_kocs:
                            duplicate_count += 1
                            logging.info(
                                f"Bỏ qua KOC đã tồn tại: {username}"
                            )
                            continue

                        metrics = creator.read_metrics_from_row(row)
                        result = evaluate_metrics(
                            metrics["gmv_text"],
                            metrics["sales_text"],
                        )

                        if not result:
                            logging.info(
                                f"KOC không đạt điều kiện: {username}. Dừng quét."
                            )
                            self.log_summary(
                                scanned_count,
                                written_count,
                                duplicate_count,
                                failed_count,
                            )
                            return

                        target_row = sheet.get_next_empty_row()
                        category_text = metrics.get("category_text", "")

                        sheet.update_category(target_row, category_text)
                        sheet.update_result(target_row, result)
                        sheet.update_koc(target_row, username)

                        existing_kocs.add(normalized_username)
                        self.append_existing_koc(username)
                        written_count += 1

                        logging.info(
                            f"Đã ghi dòng {target_row}: {username} | "
                            f"{category_text} | {result}"
                        )

                    except Exception as error:
                        failed_count += 1
                        logging.error(
                            f"KOC lỗi tại vị trí {index + 1}: {error}"
                        )

                creator.scroll_to_load_more()

                try:
                    loaded_rows = creator.get_creator_rows()

                except PlaywrightTimeoutError:
                    logging.warning(
                        "TikTok chưa tải lại danh sách sau khi scroll. "
                        "Không tìm thấy KOC mới, dừng quét an toàn."
                    )
                    break

                has_new_creator = False

                for index in range(loaded_rows.count()):
                    try:
                        username = creator.read_username_from_row(
                            loaded_rows.nth(index)
                        )
                        normalized_username = self.normalize_username(username)

                        if normalized_username not in seen_on_web:
                            has_new_creator = True
                            break

                    except Exception:
                        continue

                if not has_new_creator:
                    logging.info("TikTok không còn tải thêm KOC mới. Dừng quét.")
                    break

            self.log_summary(
                scanned_count,
                written_count,
                duplicate_count,
                failed_count,
            )

        finally:
            browser.close()

    @staticmethod
    def log_summary(
        scanned_count: int,
        written_count: int,
        duplicate_count: int,
        failed_count: int,
    ):
        logging.info("========================================")
        logging.info("KẾT THÚC PHIÊN QUÉT KOC TỪ TIKTOK")
        logging.info(f"Đã quét: {scanned_count}")
        logging.info(f"Đã ghi Sheet: {written_count}")
        logging.info(f"Trùng đã bỏ qua: {duplicate_count}")
        logging.info(f"Lỗi: {failed_count}")
