# TikTok Booking Assistant

Automation tool for **TikTok Shop Affiliate creator management**, including **video report collection** and **creator GMV screening**, with direct integration to **Google Sheets**.

---

## Overview

TikTok Booking Assistant automates repetitive creator management workflows inside **TikTok Shop Affiliate**.

The tool connects to an already logged-in Chrome browser through **Chrome DevTools Protocol (CDP)** and provides two independent automation modules:

1. **Creator Video Collector** – Collect TikTok video reports from creator sample-request history.
2. **Creator GMV Scanner** – Evaluate creators based on GMV and sales performance.

Both modules export structured results directly into **Google Sheets**.

---

## Features

### Video Collection Module

* Connect to an existing Chrome session (no repeated login)
* Search creators automatically
* Open creator history panel
* Collect all promoted products
* Collect all TikTok videos for each product
* Extract publish dates
* Extract TikTok video URLs
* Custom product name mapping
* Optional weekly date filtering
* Export formatted reports to Google Sheets
* Clickable TikTok hyperlinks inside Google Sheets cells

### GMV Screening Module

* Search creators automatically
* Select the correct creator from multiple search results
* Extract creator GMV
* Extract sales volume (Số món bán ra)
* Evaluate creators based on GMV threshold
* Handle hidden GMV values (1M₫+)
* Fallback evaluation using sales volume
* Automatically update Google Sheets with qualified creators
* Overwrite previous daily GMV results

### System Features

* Session logging
* Error recovery
* Continue processing after failures
* Google Sheets integration
* Modular architecture
* Chrome CDP connection
* Automatic report generation

---

## Project Structure

```text
tiktok_booking_assistant/
│
├── browser/
│   ├── browser_manager.py
│   ├── tiktok_page.py
│   ├── history_panel.py
│   └── creator_search_page.py
│
├── sheet/
│   ├── sheet_service.py
│   └── gmv_sheet_service.py
│
├── parser/
│   ├── video_formatter.py
│   └── gmv_parser.py
│
├── services/
│   └── gmv_service.py
│
├── constants/
│   └── product_labels.py
│
├── logs/
├── reports/
│
├── config.py
├── main.py
├── requirements.txt
└── README.md
```

---

## Requirements

* Python 3.12+
* Google Chrome
* Google Service Account
* Google Sheets API enabled
* Playwright

---

## Installation

### Clone the repository

```bash
git clone https://github.com/NCiDy/Tool-Booking-KOC
cd tiktok_booking_assistant
```

### Create virtual environment

```bash
python -m venv .venv
```

### Activate virtual environment

Windows

```bash
.venv\\Scripts\\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Install Playwright browsers

```bash
playwright install
```

---

## Google Sheets Setup

1. Create a Google Cloud project.
2. Enable **Google Sheets API**.
3. Create a **Service Account**.
4. Download the JSON credentials.
5. Place the file in the project root:

```text
credentials.json
```

6. Share the target Google Sheet with the Service Account email.

---

## Chrome Setup

Launch Chrome with remote debugging enabled.

Windows

```bash
"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" ^
--remote-debugging-port=9222 ^
--user-data-dir="C:\\ChromeDebug"
```

Verify CDP connection:

```text
http://127.0.0.1:9222/json/version
```

---

## Configuration

Edit **config.py**.

### Google Sheets

```python
SPREADSHEET_ID = "YOUR_SPREADSHEET_ID"

WORKSHEET_NAME = "KOC TỔNG"

WORKSHEET_GMV = "KOC_GMV"
```

### Sheet Columns

```python
START_ROW = 4

COL_KOC = "B"

COL_STATUS = "D"

COL_RESULT = "E"

COL_PRODUCT = "H"

COL_VIDEO_LINK = "R"
```

### Status Filter

```python
TARGET_STATUS = "ĐÃ NHẬN MẪU"
```

### GMV Evaluation

```python
GMV_THRESHOLD = 120_000_000

SALES_THRESHOLD = 2000
```

### TikTok URLs

```python
TIKTOK_SAMPLE_REQUEST_URL = "https://affiliate.tiktok.com/product/sample-request"

TIKTOK_CREATOR_SEARCH_URL = "https://affiliate.tiktok.com/connection/creator"
```

### Date Filtering

Export all videos

```python
FILTER_BY_DATE = False
```

Export weekly reports

```python
FILTER_BY_DATE = True

START_DATE = "01/08/2026"

END_DATE = "07/08/2026"
```

---

## Product Label Mapping

Edit:

```text
constants/product_labels.py
```

Example:

```python
PRODUCT_LABELS = {
    "Long product name": "SKU30",
}
```

---

## Running

Start the application:

```bash
python main.py
```

The tool displays a menu:

```text
=== TikTok Booking Assistant ===

1. Tìm kiếm GMV của KOL

2. Lấy link video của các KOL
```

---

## Video Report Output

Example Google Sheets cell:

```text
SKU30: Chuối Sấy 1: https://www.tiktok.com/@/video/766111...

SKU30: Chuối Sấy 2: https://www.tiktok.com/@/video/766222...

Nui: Snack 1: https://www.tiktok.com/@/video/766333...
```

Each TikTok URL is automatically exported as a **clickable hyperlink**.

---

## GMV Evaluation Logic

The tool evaluates creators in the following order:

### GMV Visible

If:

```text
GMV > 120,000,000 VND
```

Result:

```text
250Tr ₫
```

is written into the GMV column.

### GMV Hidden

If:

```text
GMV = 1M₫+
```

then the tool evaluates:

```text
Sales Volume > 2000
```

Result:

```text
25400 SMBR
```

is written into the GMV column.

If neither condition is met, the result cell is cleared.

---

## Video Collection Workflow

1. Read target creators from Google Sheets
2. Filter by **ĐÃ NHẬN MẪU**
3. Search creator
4. Open creator history
5. Collect products
6. Collect videos
7. Extract publish date
8. Extract TikTok URL
9. Apply product label mapping
10. Apply optional date filtering
11. Export to Google Sheets

---

## GMV Screening Workflow

1. Read target creators from **KOC_GMV**
2. Search creator
3. Select the correct creator
4. Read GMV
5. Evaluate GMV threshold
6. If GMV is hidden, evaluate sales volume
7. Update Google Sheets
8. Continue processing remaining creators

---

## Branch Strategy

```text
main

└── develop

    ├── feature/video-collector

    ├── feature/date-filter

    ├── feature/google-sheet-hyperlink

    └── feature/gmv-search
```

---

## Current Status

### Video Module

* Google Sheets integration
* Chrome CDP connection
* Creator search
* History panel automation
* Product collection
* Video collection
* Publish date extraction
* TikTok URL extraction
* Product label mapping
* Weekly date filtering
* Hyperlink export

### GMV Module

* Creator search
* Multi-result username matching
* GMV extraction
* Sales volume extraction
* GMV threshold evaluation
* Hidden GMV handling
* SMBR evaluation
* Daily overwrite updates

### System

* Session logging
* Error recovery
* Processing statistics
* Automatic report generation

---

## Author

Personal automation project for **TikTok KOC booking and creator screening workflow automation**.
