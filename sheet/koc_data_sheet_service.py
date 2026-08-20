from config import COL_KOC, START_ROW, WORKSHEET_KOC_DATA
from sheet.gmv_sheet_service import GMVSheetService


class KOCDataSheetService(GMVSheetService):
    def __init__(self):
        super().__init__(WORKSHEET_KOC_DATA)

        koc_column = self.col_to_index(COL_KOC)
        values = self.sheet.col_values(koc_column)

        self.occupied_rows = {
            row_number
            for row_number, value in enumerate(values, start=1)
            if row_number >= START_ROW and value.strip()
        }
        self.next_row = START_ROW

    def get_next_empty_row(self) -> int:
        while self.next_row in self.occupied_rows:
            self.next_row += 1

        return self.next_row

    def update_koc(self, row: int, username: str):
        self.sheet.update(
            f"{COL_KOC}{row}",
            [[username]],
        )

        self.occupied_rows.add(row)
        self.next_row = row + 1
