import logging
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
import re
from constants.product_labels import PRODUCT_LABELS
from datetime import datetime
from config import FILTER_BY_DATE, START_DATE, END_DATE

class HistoryPanel:
    def __init__(self, page: Page):
        self.page = page

    def get_product_rows(self):
        rows = self.page.locator(
            'div[class*="ProdGroupByCreatorItemWrap"]'
        )

        rows.first.wait_for(
            state="visible",
            timeout=10000
        )

        count = rows.count()

        logging.info(
            f"Tìm thấy {count} dòng sản phẩm"
        )

        return rows

    def process_products(self):
        rows = self.get_product_rows()
        count = rows.count()

        all_products = []

        for i in range(count):
            row = rows.nth(i)

            product_name = row.locator(
                'span[data-e2e="5810fc19-8066-252a"]'
            ).first.inner_text().strip()

            product_name = product_name.split("#", 1)[0].strip()
            product_name = PRODUCT_LABELS.get(product_name, product_name)

            action_items = row.locator(
                'div[data-e2e="e197794d-b324-d3da"]'
            )

            target_action = None

            for j in range(action_items.count()):
                item = action_items.nth(j)

                if item.inner_text().strip() == "Xem nội dung":
                    target_action = item
                    break

            if target_action is None:
                logging.info(
                    f"[{product_name}] Không có action 'Xem nội dung', bỏ qua"
                )
                continue

            logging.info(f"[{product_name}] Mở popup video")

            target_action.click()

            videos = self.process_video_popup(product_name)

            all_products.append(
                {
                    "product": product_name,
                    "videos": videos,
                }
            )

            logging.info(
                f"[{product_name}] Thu thập {len(videos)} video"
            )

        return all_products

    def _parse_date(self, date_str: str):
        try:
            return datetime.strptime(date_str, "%d/%m/%Y")
        except Exception:
            return None


    def _should_collect_video(self, publish_date: str):
        """
        Trả về:
        - "collect": lấy link
        - "skip": bỏ qua (quá mới)
        - "break": dừng duyệt (đã cũ hơn START_DATE)
        """

        if not FILTER_BY_DATE:
            return "collect"

        day = self._parse_date(publish_date)
        start = self._parse_date(START_DATE)
        end = self._parse_date(END_DATE)

        if day is None or start is None or end is None:
            return "collect"

        if day > end:
            return "skip"

        if start <= day <= end:
            return "collect"

        return "break"

    def process_video_popup(self, product_name: str):
        logging.info(f"[{product_name}] Chờ video cards xuất hiện")
        # Chờ video card đầu tiên xuất hiện
        video_blocks = self.page.locator(
            "div[class*='video-card__StyledVideoCard']"
        )

        count = 0
        for _ in range(15):
            count = video_blocks.count()
            if count > 0:
                break
            self.page.wait_for_timeout(200)

        logging.info(f"[{product_name}] Tìm thấy {count} video")

        results = []

        # NẾU COUNT > 0 THÌ MỚI CHẠY VÒNG LẶP
        for i in range(count):
            block = video_blocks.nth(i)

            # ===== LẤY NGÀY PHÁT HÀNH =====
            try:
                publish_text = block.locator(
                    "div.text-body-s-regular.text-neutral-text3"
                ).first.inner_text()

                publish_date = publish_text.replace(
                    "Thời gian phát hành:",
                    ""
                ).strip()

            except Exception:
                publish_date = ""
                logging.warning(
                    f"[{product_name}] Video {i+1}/{count} - Không lấy được ngày"
                )

            logging.info(
                f"[{product_name}] Video {i+1}/{count} - Ngày: {publish_date}"
            )

            action = self._should_collect_video(publish_date)

            if action == "skip":
                logging.info(
                    f"[{product_name}] Bỏ qua video ngày {publish_date} (quá mới)"
                )
                continue

            if action == "break":
                logging.info(
                    f"[{product_name}] Dừng duyệt tại video ngày {publish_date} (đã cũ hơn khoảng cần lấy)"
                )
                break

            # ===== MỞ VIDEO TRÊN TIKTOK =====
            video_button = block.locator(
                "button:has-text('Xem video trên TikTok')"
            ).first

            try:
                with self.page.context.expect_page(timeout=10000) as page_info:
                    video_button.click()

                video_page = page_info.value

                video_url = ""

                # Lấy URL TikTok ngay khi nó xuất hiện
                for _ in range(25):  # tối đa ~5 giây
                    current_url = video_page.url

                    if "tiktok.com/@" in current_url and "/video/" in current_url:
                        video_url = current_url
                        break

                    self.page.wait_for_timeout(200)

                 # Nếu đã lấy được URL TikTok thì chờ thêm để ổn định
                if video_url:
                    self.page.wait_for_timeout(3000)  
                    final_url = video_page.url    
                    if (
                        "tiktok.com/@" in final_url
                        and "/video/" in final_url
                    ):
                        video_url = final_url    

                # Nếu không lấy được URL TikTok thì mới báo lỗi
                if not video_url:
                    logging.warning(
                        f"[{product_name}] Video {i+1}/{count} - Không lấy được URL TikTok"
                    )

                    results.append(
                        {
                            "publish_date": publish_date,
                            "url": "Không lấy được link",
                        }
                    )

                    video_page.close()
                    continue

                logging.info(f"[{product_name}] URL: {video_url}")

                results.append(
                    {
                        "publish_date": publish_date,
                        "url": video_url,
                    }
                )

                video_page.close()

            except Exception as e:
                logging.error(
                    f"[{product_name}] Không lấy được link video {i+1}: {e}"
                )

                results.append(
                    {
                        "publish_date": publish_date,
                        "url": "Không lấy được link",
                    }
                )

        # ===== ĐÓNG POPUP VIDEO =====
        ok_button = self.page.locator("button[data-e2e='3a07bec0-c901-5e60']").first

        try:
            ok_button.wait_for(state="attached",timeout=5000)

            ok_button.click()

            logging.info(f"[{product_name}] Đã đóng popup video")

        except Exception:
            logging.warning(f"[{product_name}] Không tìm thấy nút đóng popup")

        return results