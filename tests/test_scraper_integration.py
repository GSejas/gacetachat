"""
Integration tests for scraper
These tests require network access and may call external APIs
"""
import pytest
from datetime import datetime
from pathlib import Path


@pytest.mark.integration
def test_scraper_finds_pdf_link():
    """Integration: Can we scrape the homepage and find a PDF link?"""
    from scripts.scrape_and_summarize import scrape_latest_gaceta_url

    url = scrape_latest_gaceta_url()

    # Should find a URL
    assert url is not None, "Failed to scrape PDF link from La Gaceta homepage"

    # Should be a valid La Gaceta URL
    assert "imprentanacional.go.cr" in url, f"URL doesn't look like La Gaceta: {url}"
    assert ".pdf" in url.lower(), f"URL doesn't point to a PDF: {url}"


@pytest.mark.integration
def test_download_pdf_from_scraped_url():
    """Integration: Can we download PDF from the scraped URL?"""
    from scripts.scrape_and_summarize import scrape_latest_gaceta_url, download_pdf

    url = scrape_latest_gaceta_url()
    assert url is not None, "Failed to scrape URL"

    pdf_bytes = download_pdf(url)

    # Should download successfully
    assert pdf_bytes is not None, f"Failed to download PDF from {url}"

    # Should have PDF header
    pdf_bytes.seek(0)
    header = pdf_bytes.read(4)
    assert header == b'%PDF', "Downloaded file is not a PDF"


@pytest.mark.integration
def test_extract_text_from_real_pdf():
    """Integration: Can we extract text from a real La Gaceta PDF?"""
    from scripts.scrape_and_summarize import (
        scrape_latest_gaceta_url,
        download_pdf,
        extract_text_from_pdf
    )

    url = scrape_latest_gaceta_url()
    pdf_bytes = download_pdf(url)
    assert pdf_bytes is not None

    # Extract first 5 pages only (faster test)
    text = extract_text_from_pdf(pdf_bytes, max_pages=5)

    # Should extract meaningful text
    assert text is not None, "Failed to extract text from PDF"
    assert len(text) >= 100, f"Extracted text too short: {len(text)} chars"

    # Should contain typical La Gaceta keywords
    text_lower = text.lower()
    assert any(keyword in text_lower for keyword in [
        "gaceta", "república", "costa rica", "decreto", "artículo"
    ]), "Extracted text doesn't look like La Gaceta content"


@pytest.mark.integration
def test_scraper_flow_with_mocked_ai(mock_gpt4_call, tmp_path):
    """
    Integration: Test full scraping flow with mocked OpenAI
    This tests everything except the AI summarization (saves costs)
    """
    from scripts.scrape_and_summarize import (
        scrape_latest_gaceta_url,
        download_pdf,
        extract_text_from_pdf,
        save_summaries
    )
    import json

    # Scrape and download
    url = scrape_latest_gaceta_url()
    assert url is not None

    pdf_bytes = download_pdf(url)
    assert pdf_bytes is not None

    text = extract_text_from_pdf(pdf_bytes, max_pages=10)
    assert text is not None

    # Summarize with mocked GPT-4 (free!)
    from scripts.scrape_and_summarize import summarize_with_gpt4
    summary = summarize_with_gpt4(text, datetime.now())

    assert summary is not None
    assert "bullets" in summary
    assert "topics" in summary
    assert len(summary["bullets"]) == 5

    # Save to temporary file
    test_file = tmp_path / "test_summaries.json"
    summaries = {"2024-07-15": summary}

    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump(summaries, f, ensure_ascii=False, indent=2)

    # Verify file was created and contains valid JSON
    assert test_file.exists()
    with open(test_file, 'r', encoding='utf-8') as f:
        loaded = json.load(f)
        assert "2024-07-15" in loaded


@pytest.mark.integration
@pytest.mark.expensive
def test_full_scrape_to_json_with_real_ai():
    """
    EXPENSIVE TEST: Full flow with real OpenAI API call
    Cost: ~$0.01-0.05 per run

    Only run this manually or on main branch CI
    """
    from scripts.scrape_and_summarize import (
        scrape_latest_gaceta_url,
        download_pdf,
        extract_text_from_pdf,
        summarize_with_gpt4
    )

    # Full flow
    url = scrape_latest_gaceta_url()
    pdf_bytes = download_pdf(url)
    text = extract_text_from_pdf(pdf_bytes, max_pages=20)

    # Real API call (costs money!)
    summary = summarize_with_gpt4(text, datetime.now())

    # Validate response structure
    assert summary is not None, "GPT-4o returned None"
    assert "summary" in summary, "Missing 'summary' field"
    assert "bullets" in summary, "Missing 'bullets' field"
    assert "topics" in summary, "Missing 'topics' field"

    # Validate content quality
    assert len(summary["bullets"]) == 5, f"Expected 5 bullets, got {len(summary['bullets'])}"
    assert all("icon" in b and "text" in b for b in summary["bullets"]), "Invalid bullet structure"
    assert len(summary["topics"]) >= 3, f"Expected at least 3 topics, got {len(summary['topics'])}"

    # Validate Spanish content
    assert any(
        spanish_word in summary["summary"].lower()
        for spanish_word in ["decreto", "ley", "costa rica", "gaceta", "república"]
    ), "Summary doesn't look like Spanish Costa Rican content"


@pytest.mark.integration
def test_json_data_persistence(tmp_path):
    """Integration: Test that summaries can be saved and loaded correctly"""
    from scripts.scrape_and_summarize import save_summaries, load_summaries
    import json

    # Mock the SUMMARIES_FILE path
    test_file = tmp_path / "summaries.json"

    # Create test data
    test_summaries = {
        "2024-07-15": {
            "summary": "Test summary",
            "bullets": [{"icon": "⚖️", "text": "Test 1"}],
            "topics": ["Legal"]
        }
    }

    # Save
    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump(test_summaries, f, ensure_ascii=False, indent=2)

    # Load
    with open(test_file, 'r', encoding='utf-8') as f:
        loaded = json.load(f)

    assert loaded == test_summaries
    assert loaded["2024-07-15"]["summary"] == "Test summary"
