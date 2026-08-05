from playwright.sync_api import sync_playwright
from config import CDP_URL, TIKTOK_SAMPLE_REQUEST_URL


class BrowserManager:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def connect(self, target_url=TIKTOK_SAMPLE_REQUEST_URL):
        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.connect_over_cdp(CDP_URL)

        contexts = self.browser.contexts
        if not contexts:
            raise Exception("Không tìm thấy Chrome context")

        self.context = contexts[0]

        for page in self.context.pages:
            url = page.url
            if target_url in url:
                self.page = page
                self.page.bring_to_front()
                return self.page

        raise Exception(
            f"Không tìm thấy tab TikTok: {target_url}"
        )

    def close(self):
        if self.playwright:
            self.playwright.stop()