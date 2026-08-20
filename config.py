from pathlib import Path

# =========================
# Google Sheets
# =========================

GOOGLE_CREDENTIALS = Path("credentials.json")
EXISTING_KOC_FILE = Path("existing_kocs.txt")

SPREADSHEET_ID = "1w25cXttV2tZ2RNIwvu6QYI4Kq9kAN3VHkxCgv2iV2jQ"
WORKSHEET_NAME = "KOC TỔNG "
WORKSHEET_GMV = "KOC_GMV"
WORKSHEET_KOC_DATA = "KOC_DATA"

GMV_THRESHOLD = 120_000_000
SALES_THRESHOLD = 2000
# =========================
# Sheet Configuration
# =========================

START_ROW = 4

COL_KOC = "B"
COL_CATEGORY = "C"
COL_STATUS = "D"
COL_RESULT = "E"
COL_PRODUCT = "H"
COL_VIDEO_LINK = "R"
TARGET_STATUS = "ĐÃ NHẬN MẪU"

# False = lấy toàn bộ video
# True = chỉ lấy video trong khoảng ngày


FILTER_BY_DATE = True


START_DATE = "11/08/2026"
END_DATE = "17/08/2026"
# =========================
# Logging
# =========================

LOG_DIR = Path("logs")
REPORT_DIR = Path("reports")

# =========================
# Browser
# =========================

CDP_URL = "http://127.0.0.1:9222"

TIKTOK_SAMPLE_REQUEST_URL = "https://affiliate.tiktok.com/affiliate/sample/sample-request"

TIKTOK_CREATOR_SEARCH_URL = "https://affiliate.tiktok.com/affiliate/creator"