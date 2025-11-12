#!/usr/bin/env python3
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌟 End-to-End Gazette Scraper Test - Government Website Integration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Description:
    Simple, focused end-to-end test validating the complete Costa Rica government
    website scraping pipeline. Tests PDF discovery, download, storage, and database
    persistence without complex mocking or extensive setup requirements.

🏗️ Test Architecture:
    ```
    ┌─────────────────┐   validates   ┌──────────────────┐
    │  Test Setup     │ ─────────────▶│  Website Access  │
    │  (Temp DB)      │               │  (Live Request)  │
    └─────────────────┘               └──────────────────┘
            │                                   │
            │ creates temp env                  │ scrapes PDF link
            ▼                                   ▼
    ┌─────────────────┐               ┌──────────────────┐
    │ Isolated DB     │               │   PDF Download   │
    │ (Test Schema)   │               │  (Binary Data)   │
    └─────────────────┘               └──────────────────┘
            │                                   │
            │ validates storage                 │ saves to temp dir
            ▼                                   ▼
    ┌─────────────────┐               ┌──────────────────┐
    │ Database Record │◀──────────────│  File System     │
    │ (Persistence)   │               │  (Temp Storage)  │
    └─────────────────┘               └──────────────────┘
    ```

🧪 Test Strategy:
    • Live Integration: Tests against actual government website
    • Minimal Dependencies: Uses existing scraping infrastructure
    • Temporary Isolation: Creates test database and directories
    • Real Data Validation: Verifies actual PDF content and metadata
    • Complete Pipeline: End-to-end workflow from scrape to storage

🔒 Security Considerations:
    ⚠️  MEDIUM: Network requests to government site (respects robots.txt)
    ⚠️  LOW: Temporary file creation in system directories
    ⚠️  LOW: Test database isolation prevents production data corruption

Author: GacetaChat Team | Version: 1.0.0 | Last Updated: 2024-12-19
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import os
import shutil
import tempfile
from datetime import datetime
from unittest.mock import patch

import pytest
import pytz
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import the functions we want to test
from download_gaceta import download_daily_gaceta, download_pdf, save_pdf_to_db
from models import Base, GacetaPDF


class TestGazetteScraper:
    """
    End-to-end test for Costa Rica government gazette scraping.

    Tests the complete pipeline:
    1. Website accessibility and HTML parsing
    2. PDF link discovery and extraction
    3. PDF download and content validation
    4. File system storage operations
    5. Database persistence and retrieval
    """

    @pytest.fixture(autouse=True)
    def setup_test_environment(self):
        """Set up isolated test environment with temporary database and directories."""
        # Create temporary database for testing
        self.test_db_path = tempfile.mktemp(suffix=".db")
        self.test_engine = create_engine(f"sqlite:///{self.test_db_path}")
        Base.metadata.create_all(self.test_engine)

        # Create test session
        TestSession = sessionmaker(bind=self.test_engine)
        self.test_session = TestSession()

        # Create temporary directory for PDF storage
        self.temp_dir = tempfile.mkdtemp(prefix="gaceta_test_")

        # Mock the database session to use our test database
        self.db_patcher = patch("download_gaceta.Session")
        self.mock_session = self.db_patcher.start()
        self.mock_session.return_value = self.test_session

        # Mock the config to use our temporary directory
        self.config_patcher = patch("download_gaceta.config")
        self.mock_config = self.config_patcher.start()
        self.mock_config.GACETA_PDFS_DIR = self.temp_dir

        yield  # This is where the test runs

        # Cleanup (equivalent to tearDown)
        self.test_session.close()
        self.db_patcher.stop()
        self.config_patcher.stop()

        # Remove temporary database
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

        # Remove temporary directory
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_government_website_accessibility(self):
        """Test that the Costa Rica government gazette website is accessible."""
        try:
            response = requests.get(
                "https://www.imprentanacional.go.cr/gaceta/", timeout=10
            )
            assert (
                response.status_code == 200
            ), "Government website should be accessible"
            assert (
                "gaceta" in response.text.lower()
            ), "Response should contain gazette content"
            print("✅ Government website is accessible")
        except requests.RequestException as e:
            pytest.fail(f"❌ Failed to access government website: {e}")

    def test_pdf_link_discovery(self):
        """Test that PDF download link can be discovered from the website."""
        try:
            response = requests.get(
                "https://www.imprentanacional.go.cr/gaceta/", timeout=10
            )
            soup = BeautifulSoup(response.text, "html.parser")

            # Look for the PDF download link using the selector from download_gaceta.py
            anchor = soup.select_one("#ctl00_PdfGacetaDescargarHyperLink")

            assert anchor is not None, "PDF download link should be found on the page"
            assert "href" in anchor.attrs, "PDF link should have href attribute"

            pdf_url = anchor["href"]
            assert pdf_url.endswith(".pdf"), "Link should point to a PDF file"
            print(f"✅ PDF link discovered: {pdf_url}")

        except Exception as e:
            pytest.fail(f"❌ Failed to discover PDF link: {e}")

    def test_pdf_download_functionality(self):
        """Test the actual PDF download from the government website."""
        try:
            pdf_data = download_pdf()

            # Validate that we got PDF data
            assert pdf_data is not None, "PDF data should not be None"
            assert len(pdf_data) > 1000, "PDF data should be substantial (>1KB)"

            # Validate PDF header (PDF files start with %PDF)
            assert pdf_data.startswith(
                b"%PDF"
            ), "Downloaded data should be a valid PDF file"

            print(f"✅ PDF downloaded successfully: {len(pdf_data):,} bytes")

        except Exception as e:
            pytest.fail(f"❌ Failed to download PDF: {e}")

    def test_file_storage_operations(self):
        """Test PDF file storage in the correct directory structure."""
        try:
            # Download PDF data
            pdf_data = download_pdf()
            assert pdf_data is not None, "Need valid PDF data for storage test"

            # Create date-based directory structure
            costa_rica_tz = pytz.timezone("America/Costa_Rica")
            current_time = datetime.now(costa_rica_tz)
            date_str = current_time.strftime("%Y-%m-%d")

            directory = os.path.join(self.temp_dir, date_str)
            file_path = os.path.join(directory, "gaceta.pdf")

            # Save the PDF file
            os.makedirs(directory, exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(pdf_data)

            # Validate file storage
            assert os.path.exists(file_path), "PDF file should be saved to disk"
            assert (
                os.path.getsize(file_path) > 1000
            ), "Saved PDF should have substantial size"

            # Validate file content
            with open(file_path, "rb") as f:
                saved_data = f.read()
            assert pdf_data == saved_data, "Saved PDF should match downloaded data"

            print(f"✅ PDF stored successfully at: {file_path}")

        except Exception as e:
            pytest.fail(f"❌ Failed to store PDF file: {e}")

    def test_database_persistence(self):
        """Test that PDF metadata is correctly saved to the database."""
        try:
            # Create test data
            costa_rica_tz = pytz.timezone("America/Costa_Rica")
            current_time = datetime.now(costa_rica_tz)
            date_str = current_time.strftime("%Y-%m-%d")
            test_file_path = f"{self.temp_dir}/{date_str}/gaceta.pdf"

            # Save to database using the function under test
            gaceta_record = save_pdf_to_db(test_file_path, date_str)

            # Validate database record creation
            assert gaceta_record is not None, "Database record should be created"
            assert gaceta_record.file_path == test_file_path, "File path should match"

            # Validate database persistence
            saved_record = (
                self.test_session.query(GacetaPDF)
                .filter_by(file_path=test_file_path)
                .first()
            )
            assert (
                saved_record is not None
            ), "Record should be retrievable from database"
            assert (
                saved_record.file_path == test_file_path
            ), "Retrieved file path should match"

            print(
                f"✅ Database record created: ID={saved_record.id}, Date={saved_record.date}"
            )

        except Exception as e:
            pytest.fail(f"❌ Failed to save to database: {e}")

    def test_complete_end_to_end_workflow(self):
        """
        Test the complete end-to-end workflow:
        Website scraping → PDF download → File storage → Database persistence
        """
        try:
            print("\n🚀 Running complete end-to-end gazette scraping test...")

            # Step 1: Verify we can access the government website
            response = requests.get(
                "https://www.imprentanacional.go.cr/gaceta/", timeout=10
            )
            assert response.status_code == 200
            print("   ✅ Government website accessible")

            # Step 2: Verify we can find the PDF link
            soup = BeautifulSoup(response.text, "html.parser")
            anchor = soup.select_one("#ctl00_PdfGacetaDescargarHyperLink")
            assert anchor is not None
            print("   ✅ PDF download link discovered")

            # Step 3: Download the actual PDF
            pdf_data = download_pdf()
            assert pdf_data is not None
            assert pdf_data.startswith(b"%PDF")
            print(f"   ✅ PDF downloaded: {len(pdf_data):,} bytes")

            # Step 4: Test the complete daily download function
            # This will create directories, save files, and update database
            with patch("download_gaceta.datetime") as mock_datetime:
                # Mock the current time to ensure consistent test behavior
                costa_rica_tz = pytz.timezone("America/Costa_Rica")
                fixed_time = datetime(2024, 12, 19, 10, 0, 0, tzinfo=costa_rica_tz)
                mock_datetime.now.return_value = fixed_time
                mock_datetime.strptime.side_effect = datetime.strptime

                # Run the complete download function
                download_daily_gaceta()

                # Verify file was created
                expected_dir = os.path.join(self.temp_dir, "2024-12-19")
                expected_file = os.path.join(expected_dir, "gaceta.pdf")

                assert os.path.exists(expected_file), "PDF file should be created"
                print(f"   ✅ File saved: {expected_file}")

                # Verify database record was created
                saved_record = self.test_session.query(GacetaPDF).first()
                assert saved_record is not None, "Database record should be created"
                assert saved_record.file_path == expected_file
                print(f"   ✅ Database record created: ID={saved_record.id}")

            print("🎉 End-to-end test completed successfully!")

        except Exception as e:
            pytest.fail(f"❌ End-to-end test failed: {e}")

    def test_duplicate_download_prevention(self):
        """Test that duplicate downloads are properly prevented."""
        try:
            # Create initial database record
            costa_rica_tz = pytz.timezone("America/Costa_Rica")
            test_date = datetime(2024, 12, 19, tzinfo=costa_rica_tz)
            test_file_path = f"{self.temp_dir}/2024-12-19/gaceta.pdf"

            initial_record = GacetaPDF(date=test_date, file_path=test_file_path)
            self.test_session.add(initial_record)
            self.test_session.commit()

            # Mock datetime to return our test date
            with patch("download_gaceta.datetime") as mock_datetime:
                mock_datetime.now.return_value = test_date
                mock_datetime.strptime.side_effect = datetime.strptime

                # Count initial records
                initial_count = self.test_session.query(GacetaPDF).count()

                # Run download function - should detect existing record
                download_daily_gaceta()

                # Verify no duplicate record was created
                final_count = self.test_session.query(GacetaPDF).count()
                assert (
                    initial_count == final_count
                ), "Should not create duplicate records"

            print("✅ Duplicate download prevention working correctly")

        except Exception as e:
            pytest.fail(f"❌ Duplicate prevention test failed: {e}")


def run_focused_scraper_test():
    """
    Run a focused test suite for government website scraping.

    This function provides a simple entry point for running just the
    essential scraping tests without the full test suite.
    """
    print("🔍 Running focused gazette scraper tests...")
    print("=" * 60)

    # Create a test instance and manually set up the environment
    test_instance = TestGazetteScraper()

    # Manually setup the test environment (since we're not using pytest runner)
    test_instance.test_db_path = tempfile.mktemp(suffix=".db")
    test_instance.test_engine = create_engine(f"sqlite:///{test_instance.test_db_path}")
    Base.metadata.create_all(test_instance.test_engine)

    TestSession = sessionmaker(bind=test_instance.test_engine)
    test_instance.test_session = TestSession()

    test_instance.temp_dir = tempfile.mkdtemp(prefix="gaceta_test_")

    test_instance.db_patcher = patch("download_gaceta.Session")
    test_instance.mock_session = test_instance.db_patcher.start()
    test_instance.mock_session.return_value = test_instance.test_session

    test_instance.config_patcher = patch("download_gaceta.config")
    test_instance.mock_config = test_instance.config_patcher.start()
    test_instance.mock_config.GACETA_PDFS_DIR = test_instance.temp_dir

    try:
        print("\n1. Testing government website accessibility...")
        test_instance.test_government_website_accessibility()

        print("\n2. Testing PDF link discovery...")
        test_instance.test_pdf_link_discovery()

        print("\n3. Testing PDF download functionality...")
        test_instance.test_pdf_download_functionality()

        print("\n4. Running complete end-to-end workflow test...")
        test_instance.test_complete_end_to_end_workflow()

        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED! Government website scraping is working correctly.")

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        raise
    finally:
        # Manual cleanup
        test_instance.test_session.close()
        test_instance.db_patcher.stop()
        test_instance.config_patcher.stop()

        if os.path.exists(test_instance.test_db_path):
            os.remove(test_instance.test_db_path)

        if os.path.exists(test_instance.temp_dir):
            shutil.rmtree(test_instance.temp_dir)


# Pytest markers for test organization
pytestmark = [
    pytest.mark.integration,
    pytest.mark.slow,  # These tests make real network requests
]


if __name__ == "__main__":
    # Option 1: Run focused tests (recommended for quick validation)
    print("Choose test mode:")
    print("1. Focused tests (quick validation)")
    print("2. Full pytest suite (comprehensive)")

    choice = input("\nEnter choice (1 or 2, default=1): ").strip() or "1"

    if choice == "1":
        run_focused_scraper_test()
    else:
        # Option 2: Run full pytest suite
        import subprocess
        import sys

        # Run pytest with verbose output
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                __file__,
                "-v",
                "--tb=short",
                "-s",  # Don't capture print statements
            ]
        )
        sys.exit(result.returncode)
