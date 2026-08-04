# TikTok Booking Assistant

Automation tool for collecting TikTok creator sample-request videos and exporting video reports to Google Sheets.

## Overview

TikTok Booking Assistant automates the manual workflow of checking creator video submissions in **TikTok Shop Affiliate – Sample Request** and exporting structured video reports to **Google Sheets**.

The tool connects to an already logged-in Chrome browser via **Chrome DevTools Protocol (CDP)**, collects creator video data, formats the report, and writes the results directly into Google Sheets.

## Features

* Connect to an existing Chrome session (no repeated login)
* Search creators automatically
* Open creator history panel
* Collect all products for each creator
* Collect all TikTok videos for each product
* Extract:

  * Product name
  * Publish date
  * TikTok video URL
* Custom product name mapping
* Weekly date filtering
* Export formatted reports to Google Sheets
* Clickable TikTok hyperlinks directly inside report cells

## Project Structure

```text
tiktok_booking_assistant/
│
├── browser/                # Playwright browser automation
│   ├── browser_manager.py
│   ├── tiktok_page.py
│   └── history_panel.py
│
├── sheet/                  # Google Sheets integration
│   └── sheet_service.py
│
├── parser/                 # Report formatting and parsing
│   └── video_formatter.py
│
├── constants/              # Static mappings
│   └── product_labels.py
│
├── credentials/            # Google service account credentials
│
├── logs/
├── reports/
│
├── config.py               # Runtime configuration
├── main.py
├── requirements.txt
└── README.md
```

## Requirements

* Python 3.12+
* Google Chrome
* Google Service Account
* Google Sheets API enabled
* Playwright browsers installed

## Installation

### 1. Clone repository

```bash
git clone https://github.com/NCiDy/Tool-Booking-KOC
cd tiktok_booking_assistant
```

### 2. Create virtual environment

```bash
python -m venv .venv
```

Activate:

**Windows**

```bash
.venv\\Scripts\\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright browsers

```bash
playwright install
```

## Google Sheets Setup

1. Create a Google Cloud project.
2. Enable **Google Sheets API**.
3. Create a **Service Account**.
4. Download the JSON credentials.
5. Place the file inside:

```text
credentials/service_account.json
```

6. Share the target Google Sheet with the Service Account email.

## Chrome Setup

Launch Chrome with remote debugging enabled.

**Windows**

```bash
"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" ^
--remote-debugging-port=9222 ^
--user-data-dir="C:\\ChromeDebug"
```

Verify:

```text
http://127.0.0.1:9222/json/version
```

## Configuration

Edit `config.py`.

### Google Sheets

```python
SPREADSHEET_ID = "YOUR_SPREADSHEET_ID"
WORKSHEET_NAME = "KOC TỔNG"
```

### Target columns

```python
START_ROW = 4

COL_KOC = "B"
COL_STATUS = "D"
COL_PRODUCT = "H"
COL_VIDEO_LINK = "R"
```

### Status filter

```python
TARGET_STATUS = "ĐÃ NHẬN MẪU"
```

### Date filter

Export **all videos**:

```python
FILTER_BY_DATE = False
```

Export a **weekly report**:

```python
FILTER_BY_DATE = True

START_DATE = "05/08/2026"
END_DATE = "11/08/2026"
```

## Product Name Mapping

Edit:

```text
constants/product_labels.py
```

Example:

```python
PRODUCT_LABELS = {
    'Long product name here': 'Short Name',
}
```

## Running

```bash
python main.py
```

## Output Format

Google Sheets cell:

```text
Nui 1 (31/07/2026): https://www.tiktok.com/@/video/766111...
Nui 2 (29/07/2026): https://www.tiktok.com/@/video/766222...

Khoai lang 1 (25/07/2026): https://www.tiktok.com/@/video/766333...
```

Each TikTok URL is automatically converted into a **clickable hyperlink** inside the same cell.

## Workflow

1. Read target KOCs from Google Sheets.
2. Filter by **ĐÃ NHẬN MẪU**.
3. Search creator.
4. Open creator history.
5. Collect products.
6. Collect videos.
7. Extract publish date and TikTok URL.
8. Apply product label mapping.
9. Apply optional date filtering.
10. Export report to Google Sheets.

## Branch Strategy

```text
main
└── develop
    ├── feature/video-collector
    ├── feature/date-filter
    └── feature/google-sheet-hyperlink
```

## Current Status

Implemented:

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
* Clickable hyperlinks in Google Sheets

## Author

Personal automation project for TikTok KOC booking workflow automation.
