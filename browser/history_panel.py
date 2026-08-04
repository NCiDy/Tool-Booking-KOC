import logging
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
import re


class HistoryPanel:
    def __init__(self, page: Page):
        self.page = page

    def get_product_rows(self):
        panel = self.page.locator(
            "tr.core-table-expand-content div[class*='SubTableWrap']"
        ).first
        panel.wait_for(state="visible", timeout=10000)

        # Product items là các div, không phải tr — match theo phần class ổn định
        rows = panel.locator(
            'div[role="list"] > div[class*="ProdGroupByCreatorItemWrap"]'
        )
        count = rows.count()
        logging.info(f"Tìm thấy {count} dòng sản phẩm")
        return rows

    def process_products(self):
        rows = self.get_product_rows()
        count = rows.count()

        for i in range(count):
            row = rows.nth(i)

            # Tên sản phẩm - đúng selector theo cấu trúc thật
            product_name = row.locator(
                'div[class*="text-14"][class*="leading-20"][class*="truncate"]'
            ).first.inner_text().strip()

            # Các hành động là div.cursor-pointer chứa span text, không phải <button>
            action_items = row.locator('div[data-e2e="e197794d-b324-d3da"]')
            action_count = action_items.count()

            target_action = None
            for j in range(action_count):
                item = action_items.nth(j)
                text = item.inner_text().strip()
                if text == "Xem nội dung":
                    target_action = item
                    break

            if target_action is None:
                logging.info(f"[{product_name}] Không có action 'Xem nội dung', bỏ qua")
                continue

            # Kiểm tra action có bị disable không (class opacity-50 cursor-not-allowed)
            class_attr = target_action.get_attribute("class") or ""
            if "cursor-not-allowed" in class_attr:
                logging.info(f"[{product_name}] Action bị disable, bỏ qua")
                continue

            logging.info(f"[{product_name}] Mở popup video")

            with self.page.expect_response(lambda r: True, timeout=10000):
                target_action.click()

            videos = self.process_video_popup(product_name)
            logging.info(
                f"[{product_name}] Thu thập {len(videos)} video"
            )

    def process_video_popup(self, product_name: str):
        logging.info(f"[{product_name}] Chờ video cards xuất hiện")

        # Chờ video card đầu tiên xuất hiện
        video_blocks = self.page.locator(
            "div[class*='video-card__StyledVideoCard']"
        )

        video_blocks.first.wait_for(state="attached", timeout=10000)

        count = video_blocks.count()

        logging.info(f"[{product_name}] Tìm thấy {count} video")

        results = []

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

            # ===== MỞ VIDEO TRÊN TIKTOK =====
            video_button = block.locator(
                "button:has-text('Xem video trên TikTok')"
            ).first

            try:
                with self.page.context.expect_page(timeout=10000) as page_info:
                    video_button.click()

                video_page = page_info.value

                # Chỉ chờ rất ngắn để URL được gán
                for _ in range(10):  # tối đa ~2 giây
                    video_url = video_page.url
                    if video_url and video_url != "about:blank":
                        break
                    self.page.wait_for_timeout(200)

                video_url = video_page.url

                match = re.search(r"/video/(\d+)", video_url)
                video_id = match.group(1) if match else ""

                logging.info(f"[{product_name}] URL: {video_url}")

                results.append({
                    "publish_date": publish_date,
                    "url": video_url,
                    "video_id": video_id,
                })

                video_page.close()

            except Exception as e:
                logging.error(f"[{product_name}] Không lấy được link video {i+1}: {e}")

                results.append({
                    "publish_date": publish_date,
                    "url": "Không lấy được link",
                    "video_id": "",
                })

        # ===== ĐÓNG POPUP VIDEO =====
        ok_button = self.page.locator(
            "button[data-e2e='3a07bec0-c901-5e60']"
        ).first

        ok_button.wait_for(state="attached", timeout=5000)

        ok_button.click()

        logging.info(
            f"[{product_name}] Đã đóng popup video"
        )

        return results