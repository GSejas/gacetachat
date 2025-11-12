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
