from sheet.sheet_service import SheetService
from config import (
    START_ROW,
    TARGET_STATUS,
    WORKSHEET_GMV,
    COL_RESULT,
    COL_CATEGORY,
)


class GMVSheetService(SheetService):
    def __init__(self, worksheet_name=WORKSHEET_GMV):
        super().__init__()

        # Đổi worksheet trong cùng spreadsheet
        self.sheet = self.sheet.spreadsheet.worksheet(
            worksheet_name
        )

    def get_rows_to_process(self):
        values = self.sheet.get_all_values()

        rows = []

        for row_number in range(START_ROW, len(values) + 1):
            row = values[row_number - 1]

            koc = row[1].strip() if len(row) > 1 else ""
            status = row[3].strip() if len(row) > 3 else ""

            if not koc:
                continue

            if status != TARGET_STATUS:
                continue

            rows.append(
                {
                    "row": row_number,
                    "koc": koc,
                }
            )

        return rows

    def update_result(self, row: int, value: str):
        self.sheet.update(
            f"{COL_RESULT}{row}",
            [[value]]
        )

    def clear_result(self, row: int):
        self.sheet.update(
            f"{COL_RESULT}{row}",
            [[""]]
        )

    def update_category(self, row: int, value: str):
        self.sheet.update(
            f"{COL_CATEGORY}{row}",
            [[value]]
        )

    def clear_category(self, row: int):
        self.sheet.update(
            f"{COL_CATEGORY}{row}",
            [[""]]
        )
