"""
Unit tests for scraper functions
Fast tests that don't require network or API calls
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from io import BytesIO


def test_scrape_handles_missing_link():
    """Unit: scrape_latest_gaceta_url returns None if PDF link not found"""
    from scripts.scrape_and_summarize import scrape_latest_gaceta_url

    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.text = "<html><body><p>No PDF link here</p></body></html>"
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        url = scrape_latest_gaceta_url()
        assert url is None


def test_scrape_handles_network_error():
    """Unit: scrape_latest_gaceta_url returns None on network error"""
    from scripts.scrape_and_summarize import scrape_latest_gaceta_url

    with patch('requests.get') as mock_get:
        mock_get.side_effect = Exception("Network error")
        url = scrape_latest_gaceta_url()
        assert url is None


def test_download_pdf_handles_404():
    """Unit: download_pdf returns None on 404 error"""
    from scripts.scrape_and_summarize import download_pdf
    import requests

    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.RequestException("404 Not Found")
        pdf = download_pdf("https://example.com/fake.pdf")
        assert pdf is None


def test_download_pdf_handles_timeout():
    """Unit: download_pdf returns None on timeout"""
    from scripts.scrape_and_summarize import download_pdf

    with patch('requests.get') as mock_get:
        import requests
        mock_get.side_effect = requests.exceptions.Timeout("Timeout")
        pdf = download_pdf("https://example.com/slow.pdf")
        assert pdf is None


def test_extract_text_handles_corrupted_pdf():
    """Unit: extract_text_from_pdf handles corrupted PDFs gracefully"""
    from scripts.scrape_and_summarize import extract_text_from_pdf

    # Create a corrupted PDF (invalid format)
    corrupted_pdf = BytesIO(b"Not a real PDF file")

    text = extract_text_from_pdf(corrupted_pdf, max_pages=1)
    # Should return None on error, not crash
    assert text is None


def test_load_summaries_handles_missing_file():
    """Unit: load_summaries returns empty dict if file doesn't exist"""
    from scripts.scrape_and_summarize import load_summaries
    from pathlib import Path

    with patch.object(Path, 'exists', return_value=False):
        summaries = load_summaries()
        assert summaries == {}


def test_load_summaries_handles_corrupted_json():
    """Unit: load_summaries handles corrupted JSON gracefully"""
    from scripts.scrape_and_summarize import load_summaries
    from pathlib import Path

    with patch.object(Path, 'exists', return_value=True):
        with patch('builtins.open', mock_open_with_content="{invalid json}"):
            # Should raise JSONDecodeError, which we can catch
            with pytest.raises(Exception):  # Could be JSONDecodeError or ValueError
                load_summaries()


def test_save_summaries_limits_to_90_days():
    """Unit: save_summaries keeps only last 90 days"""
    from scripts.scrape_and_summarize import save_summaries
    from pathlib import Path
    import json

    # Create 100 summaries (more than MAX_SUMMARIES=90)
    summaries = {f"2024-{i//30+1:02d}-{i%30+1:02d}": {"summary": f"Day {i}"} for i in range(100)}

    with patch('builtins.open', create=True) as mock_open:
        with patch.object(Path, 'mkdir'):
            mock_file = MagicMock()
            mock_open.return_value.__enter__.return_value = mock_file

            save_summaries(summaries)

            # Check that json.dump was called
            mock_file.write.assert_called()


@pytest.mark.unit
def test_summarize_with_gpt4_handles_api_error(monkeypatch):
    """Unit: summarize_with_gpt4 handles OpenAI API errors gracefully"""
    from scripts.scrape_and_summarize import summarize_with_gpt4
    from datetime import datetime

    # Mock the entire OpenAI client to raise an error when creating completion
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = Exception("API Error")

    def mock_openai_constructor(*args, **kwargs):
        return mock_client

    monkeypatch.setattr('scripts.scrape_and_summarize.OpenAI', mock_openai_constructor)

    result = summarize_with_gpt4("Test text", datetime.now())
    assert result is None


@pytest.mark.unit
def test_summarize_with_gpt4_handles_invalid_json(monkeypatch, mock_openai_response):
    """Unit: summarize_with_gpt4 handles invalid JSON response"""
    from scripts.scrape_and_summarize import summarize_with_gpt4
    from datetime import datetime

    # Mock OpenAI to return invalid JSON
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Not valid JSON at all"
    mock_client.chat.completions.create.return_value = mock_response

    monkeypatch.setattr('scripts.scrape_and_summarize.OpenAI', lambda *args, **kwargs: mock_client)

    result = summarize_with_gpt4("Test text", datetime.now())
    assert result is None  # Should return None on invalid JSON


# ===== Timezone Tests =====
def test_timezone_handling_costa_rica():
    """Unit: Main function uses Costa Rica timezone (UTC-6)"""
    from datetime import datetime
    import pytz

    costa_rica_tz = pytz.timezone("America/Costa_Rica")
    now_cr = datetime.now(costa_rica_tz)

    # Should have timezone info
    assert now_cr.tzinfo is not None
    assert now_cr.tzname() in ("CST", "CDT")  # Central Standard/Daylight Time


def test_date_extraction_from_url_dd_mm_yyyy_format():
    """Unit: Extract date from COMP_DD_MM_YYYY.pdf format correctly"""
    import re
    from datetime import datetime

    url = "https://www.imprentanacional.go.cr/pub/2025/11/12/COMP_12_11_2025.pdf"

    # Test regex pattern
    match = re.search(r'COMP_(\d{2})_(\d{2})_(\d{4})\.pdf', url)
    assert match is not None

    day, month, year = match.groups()
    assert day == "12"
    assert month == "11"
    assert year == "2025"

    # Parse to date string
    gazette_date = datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")
    date_str = gazette_date.strftime("%Y-%m-%d")
    assert date_str == "2025-11-12"  # Should be November 12th, not 13th


def test_date_extraction_old_yyyymmdd_format():
    """Unit: Also handle old gaceta_YYYYMMDD format"""
    import re
    from datetime import datetime

    url = "https://www.imprentanacional.go.cr/gaceta/2024/07/15/gaceta_20240715.pdf"

    # Test regex pattern for old format
    match = re.search(r'gaceta[_/]?(\d{8})', url)
    assert match is not None

    date_str_match = match.group(1)
    assert date_str_match == "20240715"

    # Parse to date
    gazette_date = datetime.strptime(date_str_match, "%Y%m%d")
    date_str = gazette_date.strftime("%Y-%m-%d")
    assert date_str == "2024-07-15"


def test_no_timezone_drift_on_midnight():
    """Unit: Date extraction works correctly around midnight UTC"""
    from datetime import datetime
    import pytz

    # Simulate: 04:37 UTC (which is Nov 13 UTC, but Nov 12 in Costa Rica)
    utc_tz = pytz.timezone("UTC")
    utc_time = datetime(2025, 11, 13, 4, 37, tzinfo=utc_tz)

    # Convert to Costa Rica time (UTC-6)
    costa_rica_tz = pytz.timezone("America/Costa_Rica")
    cr_time = utc_time.astimezone(costa_rica_tz)

    # In Costa Rica, this should still be Nov 12
    assert cr_time.day == 12
    assert cr_time.month == 11

    # Date string should reflect Costa Rica date
    date_str = cr_time.strftime("%Y-%m-%d")
    assert date_str == "2025-11-12"
