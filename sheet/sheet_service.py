import gspread
from google.oauth2.service_account import Credentials
from config import COL_VIDEO_LINK
import re
from gspread.utils import a1_to_rowcol

from config import (
    GOOGLE_CREDENTIALS,
    SPREADSHEET_ID,
    WORKSHEET_NAME,
    START_ROW,
    COL_KOC,
    COL_STATUS,
    COL_PRODUCT,
    COL_VIDEO_LINK,
    TARGET_STATUS,
)


class SheetService:
    def __init__(self):
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]

        credentials = Credentials.from_service_account_file(
            GOOGLE_CREDENTIALS,
            scopes=scopes,
        )

        client = gspread.authorize(credentials)

        self.sheet = client.open_by_key(SPREADSHEET_ID).worksheet(WORKSHEET_NAME)

    @staticmethod
    def col_to_index(col: str) -> int:
        result = 0
        for c in col.upper():
            result = result * 26 + ord(c) - ord("A") + 1
        return result

    def get_rows_to_process(self):
        values = self.sheet.get_all_values()

        koc_col = self.col_to_index(COL_KOC) - 1
        status_col = self.col_to_index(COL_STATUS) - 1
        product_col = self.col_to_index(COL_PRODUCT) - 1
        video_col = self.col_to_index(COL_VIDEO_LINK) - 1

        rows = []

        for row_number in range(START_ROW, len(values) + 1):
            row = values[row_number - 1]

            def get_value(index):
                return row[index].strip() if index < len(row) else ""

            koc = get_value(koc_col)
            status = get_value(status_col)

            if not koc:
                continue

            if status != TARGET_STATUS:
                continue

            rows.append(
                {
                    "row": row_number,
                    "koc": koc,
                    "status": status,
                    "product": get_value(product_col),
                    "video_link": get_value(video_col),
                }
            )

        return rows

    def update_video_links(self, row_number: int, text: str):
        row, col = a1_to_rowcol(f"{COL_VIDEO_LINK}{row_number}")

        # Tìm tất cả URL trong nội dung
        url_pattern = re.compile(r"https://www\.tiktok\.com/\S+")

        text_format_runs = []

        for match in url_pattern.finditer(text):
            # Reset format từ đầu dòng
            line_start = text.rfind("\n", 0, match.start()) + 1

            text_format_runs.append(
                {
                    "startIndex": line_start,
                    "format": {}
                }
            )

            # Bắt đầu hyperlink đúng từ URL
            text_format_runs.append(
                {
                    "startIndex": match.start(),
                    "format": {
                        "link": {
                            "uri": match.group()
                        }
                    }
                }
            )

        request = {
            "updateCells": {
                "range": {
                    "sheetId": self.sheet.id,
                    "startRowIndex": row - 1,
                    "endRowIndex": row,
                    "startColumnIndex": col - 1,
                    "endColumnIndex": col,
                },
                "rows": [
                    {
                        "values": [
                            {
                                "userEnteredValue": {
                                    "stringValue": text
                                },
                                "textFormatRuns": text_format_runs,
                            }
                        ]
                    }
                ],
                "fields": "userEnteredValue,textFormatRuns",
            }
        }

        self.sheet.spreadsheet.batch_update(
            {
                "requests": [request]
            }
        )