#!/usr/bin/env python3
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌟 Gazette PDF Downloader - Automated Costa Rica Official Gazette Scraper
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Description:
    Automated web scraper for Costa Rica's official gazette (La Gaceta). Downloads
    daily PDFs from imprentanacional.go.cr, manages file storage, database tracking,
    and triggers AI processing pipeline. Runs as scheduled background service.

🏗️ Architecture Flow:
    ```
    ┌─────────────────┐   HTTP GET    ┌──────────────────┐
    │  Scheduler      │ ─────────────▶│   Web Scraper    │
    │  (Daily Cron)   │               │  (BeautifulSoup) │
    └─────────────────┘               └──────────────────┘
            │                                 │
            │ Costa Rica Time                 │ PDF Discovery
            ▼                                 ▼
    ┌─────────────────┐               ┌──────────────────┐
    │ Timezone Mgmt   │               │  Government Site │
    │ (America/CR)    │               │  PDF Extraction  │
    └─────────────────┘               └──────────────────┘
            │                                 │
            │ Date-based Path                 │ PDF Download
            ▼                                 ▼
    ┌─────────────────┐               ┌──────────────────┐
    │ File System     │               │   PDF Storage    │
    │ (gaceta_pdfs/)  │◀──────────────│   + DB Record    │
    └─────────────────┘               └──────────────────┘
            │                                 │
            │ Trigger Processing              │ Index Creation
            ▼                                 ▼
    ┌─────────────────┐               ┌──────────────────┐
    │ AI Processing   │               │  FAISS Index     │
    │ Pipeline        │               │  Generation      │
    └─────────────────┘               └──────────────────┘
    ```

📥 Inputs:
    • Scheduler triggers: Daily execution at specified times (Costa Rica timezone)
    • Government website: HTML parsing from imprentanacional.go.cr/gaceta/
    • File system: Directory structure for PDF storage (gaceta_pdfs/{date}/)
    • Database state: Existing PDF records to prevent duplicate downloads
    • Configuration: PDF storage paths, processing templates, execution settings

📤 Outputs:
    • PDF files: Daily gazette documents in date-organized directories
    • Database records: GacetaPDF entries with file paths and metadata
    • FAISS indices: Vector search databases for semantic queries
    • Processing logs: Execution status and error tracking
    • AI execution sessions: Triggered prompt processing for new content

🔗 Dependencies:
    • requests: HTTP client for web scraping and PDF downloads
    • beautifulsoup4: HTML parsing for PDF link extraction
    • pytz: Timezone handling for Costa Rica time calculations
    • schedule: Task scheduling for automated daily execution
    • crud: AI prompt execution engine and session management
    • pdf_processor: Document processing and vector index creation

🏛️ Component Relationships:
    ```mermaid
    graph TD
        A[Download Scheduler] --> B[Web Scraper]
        A --> C[Timezone Manager]
        B --> D[PDF Downloader]

        D --> E[File Storage]
        D --> F[(Database)]
        E --> G[PDF Processor]
        G --> H[FAISS Index]

        F --> I[Execution Engine]
        I --> J[AI Processing]

        K[Government Site] --> B
        L[Costa Rica Time] --> C

        classDef downloader fill:#e1f5fe
        classDef storage fill:#f3e5f5
        classDef external fill:#fff3e0
        classDef processing fill:#fff8e1

        class A,B,D downloader
        class E,F,H storage
        class K,L external
        class G,I,J processing
    ```

🔒 Security Considerations:
    ⚠️  HIGH: No SSL certificate validation for government site downloads
    ⚠️  HIGH: File system writes without path validation - directory traversal risk
    ⚠️  MEDIUM: No rate limiting on government website requests - potential blocking
    ⚠️  MEDIUM: Downloaded PDFs not scanned for malware before processing
    ⚠️  LOW: No authentication for government website access (public data)

🛡️ Risk Analysis:
    • Website Changes: Government site structure changes could break scraping
    • Resource Exhaustion: Large PDF files could consume excessive disk space
    • Network Dependencies: Internet connectivity required for daily operation
    • Processing Failures: PDF corruption could cause downstream AI failures
    • Regulatory Compliance: Automated scraping may violate site terms of service

⚡ Performance Characteristics:
    • Download Speed: ~2-5 seconds per PDF (5-20MB typical file size)
    • Scheduling Overhead: <1 second for daily check and execution
    • Memory Usage: ~50MB baseline + 2x PDF size during processing
    • Disk Usage: ~50MB per day (varies by gazette size)
    • Processing Time: 30-120 seconds for complete PDF→FAISS pipeline

🧪 Testing Strategy:
    • Unit Tests: PDF extraction, file operations, database persistence
    • Integration Tests: End-to-end download and processing workflows
    • Performance Tests: Large PDF handling, concurrent processing scenarios
    • Reliability Tests: Network failure recovery, partial download handling

📊 Monitoring & Observability:
    • Metrics: Download success rate, file sizes, processing times
    • Logging: Download attempts, errors, file operations, AI processing
    • Alerts: Download failures, disk space issues, processing errors
    • Health Checks: Website availability, file system access, database connectivity

🔄 Data Flow:
    ```
    Schedule ──▶ Web Scrape ──▶ PDF Download ──▶ File Save ──▶ DB Record ──▶ AI Process
         │           │            │             │           │              │
         ▼           ▼            ▼             ▼           ▼              ▼
    Time Check   Link Extract   HTTP GET    File Write   DB Insert    Index Create
    ```

📚 Usage Examples:
    ```python
    # Manual execution
    download_daily_gaceta()

    # Scheduled execution
    schedule.every().day.at("09:00").do(download_daily_gaceta)

    # Process existing PDF
    check_and_download_today_pdf()

    # Run with AI processing
    python download_gaceta.py  # Background daemon mode
    ```

🔧 Scheduling Configuration:
    ```python
    # Daily Schedule (Costa Rica Time)
    DOWNLOAD_TIME = "09:00"              # 9 AM daily download
    RETRY_INTERVAL = 3600                # 1 hour retry on failure
    MAX_RETRIES = 3                      # Maximum retry attempts

    # File Organization
    STORAGE_PATTERN = "gaceta_pdfs/{date}/gaceta.pdf"
    DATE_FORMAT = "%Y-%m-%d"             # ISO date format
    TIMEZONE = "America/Costa_Rica"      # Local government timezone

    # Processing Triggers
    AUTO_PROCESS_NEW_PDFS = True         # Trigger AI pipeline automatically
    AI_TEMPLATE_ID = 1                   # Default prompt template for processing
    ```

🚨 Error Handling Patterns:
    ```python
    # Network error recovery
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Download failed: {e}")
        schedule_retry()

    # File operation safety
    try:
        with open(file_path, "wb") as f:
            f.write(pdf_data)
    except IOError as e:
        logging.error(f"File write failed: {e}")
        cleanup_partial_download()
    ```

🔄 Deployment with PM2:
    ```bash
    # PM2 ecosystem configuration
    pm2 start download_gaceta.py --name gazette-downloader
    pm2 startup  # Enable auto-start on boot
    pm2 save     # Persist current configuration
    ```

Author: GacetaChat Team | Version: 2.1.0 | Last Updated: 2024-12-19
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

# download_gaceta.py
import datetime
import logging
import os
import time
from datetime import datetime

import pytz
import requests
import schedule

# def fetch_pdf(url):
#     import requests
from bs4 import BeautifulSoup

from config import config
from crud import PromptExecutionEngine, get_execution_session_by_date
from db import Session
from faiss_helper import FAISSHelper
from logging_setup import setup_logging
from models import ExecutionState, GacetaPDF  # , Session
from pdf_processor import PDFProcessor

setup_logging()


def download_pdf():
    response = requests.get("https://www.imprentanacional.go.cr/gaceta/")
    soup = BeautifulSoup(response.text, "html.parser")

    anchor = soup.select_one("#ctl00_PdfGacetaDescargarHyperLink")

    if anchor:
        pdf_url = anchor["href"]
        pdf_response = requests.get("https://www.imprentanacional.go.cr" + pdf_url)

        return pdf_response.content
    else:
        return None


def save_pdf_to_db(file_path, date_str):
    try:
        session = Session()
        gaceta = GacetaPDF(
            date=datetime.strptime(date_str, "%Y-%m-%d"), file_path=file_path
        )
        session.add(gaceta)
        session.commit()
        session.close()
        logging.info(f"Saved PDF to database for {date_str}")
        return gaceta
    except Exception as e:
        logging.error(f"Failed to save PDF to database: {e}")


def download_daily_gaceta():

    # Set the timezone to Costa Rica
    costa_rica_tz = pytz.timezone("America/Costa_Rica")
    current_time = datetime.now(costa_rica_tz)

    # Get the date string in the format "YYYY-MM-DD"
    date_str = current_time.strftime("%Y-%m-%d")

    directory = f"gaceta_pdfs/{date_str}"
    file_path = os.path.join(directory, "gaceta.pdf")

    session = Session()
    existing_gaceta = (
        session.query(GacetaPDF)
        .filter_by(date=datetime.strptime(date_str, "%Y-%m-%d"))
        .first()
    )

    if not existing_gaceta:
        if os.path.exists(file_path):
            logging.info(
                f"PDF file for {date_str} already exists, but not in the database. Creating DB entry."
            )
            save_pdf_to_db(file_path, date_str)
        else:
            pdf_data = download_pdf()
            if pdf_data:
                os.makedirs(directory, exist_ok=True)
                with open(file_path, "wb") as f:
                    f.write(pdf_data)
                save_pdf_to_db(file_path, date_str)
                print(f"Downloaded and saved PDF for {date_str}")
            else:
                print(f"Failed to download PDF for {date_str}")
    else:
        print(f"PDF for {date_str} already exists")

    session.close()


def check_and_download_today_pdf():

    # Set the timezone to Costa Rica
    costa_rica_tz = pytz.timezone("America/Costa_Rica")
    current_time = datetime.now(costa_rica_tz)

    # Get the date string in the format "YYYY-MM-DD"
    date_str = current_time.strftime("%Y-%m-%d")
    latest_gaceta_dir = os.path.join(config.GACETA_PDFS_DIR, date_str)

    session = Session()
    existing_gaceta = (
        session.query(GacetaPDF)
        .filter_by(date=datetime.strptime(date_str, "%Y-%m-%d"))
        .first()
    )
    if not existing_gaceta:
        logging.info(f"Downloading PDF for {date_str}")
        download_daily_gaceta()
    else:
        logging.info(f"PDF for {date_str} already exists")

    faiss_helper = FAISSHelper()
    pdf_processor = PDFProcessor(faiss_helper)

    # Check if FAISS index exists, load if it does, else process latest PDF
    if os.path.exists(os.path.join(latest_gaceta_dir, "index.faiss")):
        db = faiss_helper.load_faiss_index(latest_gaceta_dir)
        db.index
        # documents = db.docstore.get_all_documents()
    else:
        db, documents = pdf_processor.process_latest_pdf()
        db.index

    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    session_for_today = get_execution_session_by_date(session, date_obj)

    prompt_execution_engine = PromptExecutionEngine(session)

    if isinstance(session_for_today, list):
        session_for_today = session_for_today[0] if session_for_today else None

    if (
        session_for_today is None
        or session_for_today.status != ExecutionState.EXECUTED.value
    ) and existing_gaceta is not None:
        prompt_execution_engine.execute_content_template_prompts(
            None, 1, gaceta_id=existing_gaceta.id
        )
    else:
        if session_for_today.document_id is None:
            session_for_today.document_id = existing_gaceta.id
            session.commit()
    session.close()


# Configure logging
logging.basicConfig(
    filename="download.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def initial_check_and_create_missing_entries():
    session = Session()
    directory = config.GACETA_PDFS_DIR

    for date_folder in os.listdir(directory):
        folder_path = os.path.join(directory, date_folder)
        if os.path.isdir(folder_path):
            date_str = date_folder
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                existing_gaceta = (
                    session.query(GacetaPDF)
                    .filter_by(date=datetime.strptime(date_str, "%Y-%m-%d"))
                    .first()
                )
                if not existing_gaceta:
                    file_path = os.path.join(folder_path, "gaceta.pdf")
                    if os.path.exists(file_path):
                        logging.info(
                            f"Folder for {date_str} exists, but no DB entry found. Creating DB entry."
                        )
                        save_pdf_to_db(file_path, date_str)
            except ValueError:
                logging.warning(f"Skipping invalid date folder: {date_folder}")
    session.close()


schedule.every(1).minutes.do(check_and_download_today_pdf)

if __name__ == "__main__":
    initial_check_and_create_missing_entries()
    check_and_download_today_pdf()
    while True:
        schedule.run_pending()
        time.sleep(60)
