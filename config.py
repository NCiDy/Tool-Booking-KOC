from pathlib import Path

# =========================
# Google Sheets
# =========================

GOOGLE_CREDENTIALS = Path("credentials.json")

SPREADSHEET_ID = "1w25cXttV2tZ2RNIwvu6QYI4Kq9kAN3VHkxCgv2iV2jQ"
WORKSHEET_NAME = "KOC TỔNG "

# =========================
# Sheet Configuration
# =========================

START_ROW = 4

COL_KOC = "B"
COL_STATUS = "D"
COL_PRODUCT = "H"
COL_VIDEO_LINK = "R"

TARGET_STATUS = "ĐÃ NHẬN MẪU"

# =========================
# Logging
# =========================

LOG_DIR = Path("logs")
REPORT_DIR = Path("reports")

# =========================
# Browser
# =========================

CDP_URL = "http://127.0.0.1:9222"

TIKTOK_SAMPLE_REQUEST_URL = "https://affiliate.tiktok.com/product/sample-request"