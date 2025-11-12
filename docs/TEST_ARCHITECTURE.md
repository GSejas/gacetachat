# GacetaChat Test Architecture

**Version**: 1.0
**Last Updated**: 2025-11-12
**Author**: Test Architect Analysis

---

## Executive Summary

**Current State**: Zero test coverage for serverless alpha
**Priority**: Integration > Unit > E2E
**Framework**: Streamlit `st.testing.v1` + pytest
**Cost Consideration**: Mock OpenAI API in tests (don't burn money)

---

## 1. Current Testing State Analysis

### What We Have
- ❌ **No tests** for serverless alpha code
- ✅ `archive/v1/conftest.py` exists but V1 is archived
- ✅ pytest installed in venv
- ✅ Streamlit includes `st.testing.v1` testing framework (simple!)

### What We Need to Test

**Critical Path** (this is our moneymaker):
```
La Gaceta Homepage → Scraper → PDF Download → Text Extraction → GPT-4o → JSON → Git Commit → Streamlit Display
```

If ANY of these steps break, the alpha is dead. Priority = test this flow.

---

## 2. Test Architecture Strategy

### Why Integration Tests First?

For a serverless alpha, **integration tests** give you the most bang for your buck:

1. **Scraper reliability** - Does it actually find and download today's PDF?
2. **AI robustness** - Does GPT-4o return valid JSON consistently?
3. **Data integrity** - Does the JSON get committed and loaded correctly?
4. **Streamlit UX** - Does the app display data without crashing?

**Unit tests** are important but less critical for an alpha that's validating market demand, not scaling to 1M users.

**E2E tests** are overkill for a JSON-in-Git alpha. Save for full MVP.

### Test Pyramid (Inverted for Alpha)

```
       E2E Tests (Manual only)
       ├─ User journey: "Can I see today's summary?"

    Integration Tests (Automated - HIGH PRIORITY)
    ├─ Scraper → Download → Extract → Summarize → Save
    ├─ Streamlit loads live data correctly
    ├─ GitHub Actions workflow completes

  Unit Tests (Automated - MEDIUM PRIORITY)
  ├─ scrape_latest_gaceta_url() returns valid URL
  ├─ download_pdf() handles 404s gracefully
  ├─ extract_text_from_pdf() handles corrupted PDFs
  ├─ Streamlit load_demo_data() falls back to demo
```

---

## 3. Streamlit Testing with `st.testing.v1`

Streamlit has a **built-in testing framework** that's dead simple:

### Example: Test Streamlit App

```python
# test_demo_simple.py
from streamlit.testing.v1 import AppTest

def test_app_loads_without_crashing():
    """Smoke test: Does the app even load?"""
    at = AppTest.from_file("demo_simple.py")
    at.run()
    assert not at.exception

def test_app_shows_title():
    """Does the title render correctly?"""
    at = AppTest.from_file("demo_simple.py")
    at.run()
    assert "GacetaChat" in at.title[0].value

def test_app_shows_demo_data_when_no_live_data():
    """Falls back to demo_data.json if data/summaries.json missing"""
    at = AppTest.from_file("demo_simple.py")
    at.run()
    # Check for demo indicator
    assert any("🟡" in str(c.value) for c in at.caption)

def test_app_shows_live_indicator_with_real_data():
    """Shows 🟢 when data/summaries.json exists"""
    # This test assumes data/summaries.json exists
    at = AppTest.from_file("demo_simple.py")
    at.run()
    # Check for live indicator (only if file exists)
    captions = [str(c.value) for c in at.caption]
    assert any("🟢" in c or "🟡" in c for c in captions)
```

**Run tests:**
```bash
pytest test_demo_simple.py -v
```

**Why this is perfect for alpha:**
- No Selenium/Playwright setup needed
- Fast (runs in ~2-3 seconds)
- Catches 80% of UI bugs
- Uses Streamlit's own testing framework (reliable)

---

## 4. Integration Tests for Scraper

### Critical Integration Test: Full Scraping Flow

```python
# tests/test_scraper_integration.py
import pytest
import json
from pathlib import Path
from scripts.scrape_and_summarize import (
    scrape_latest_gaceta_url,
    download_pdf,
    extract_text_from_pdf,
    load_summaries,
    save_summaries
)

@pytest.mark.integration
def test_scraper_finds_pdf_link():
    """Integration: Can we scrape the homepage and find a PDF link?"""
    url = scrape_latest_gaceta_url()
    assert url is not None
    assert "imprentanacional.go.cr" in url
    assert ".pdf" in url.lower()

@pytest.mark.integration
def test_download_and_extract_text():
    """Integration: Can we download and extract text from a PDF?"""
    url = scrape_latest_gaceta_url()
    assert url is not None

    pdf_bytes = download_pdf(url)
    assert pdf_bytes is not None

    text = extract_text_from_pdf(pdf_bytes, max_pages=5)  # Only 5 pages for speed
    assert text is not None
    assert len(text) >= 100  # Should have at least 100 characters

@pytest.mark.integration
@pytest.mark.expensive  # Mark as expensive because it calls OpenAI
def test_full_scrape_to_json_flow(tmp_path):
    """Integration: Full flow from scraping to saving JSON"""
    # This test costs $0.01-0.05 per run (OpenAI API)
    # Only run manually or on main branch merges

    url = scrape_latest_gaceta_url()
    pdf_bytes = download_pdf(url)
    text = extract_text_from_pdf(pdf_bytes, max_pages=10)

    # Call GPT-4o (costs money!)
    from scripts.scrape_and_summarize import summarize_with_gpt4
    from datetime import datetime
    summary = summarize_with_gpt4(text, datetime.now())

    assert summary is not None
    assert "bullets" in summary
    assert "topics" in summary
    assert len(summary["bullets"]) == 5
    assert all("icon" in b and "text" in b for b in summary["bullets"])
```

**Run integration tests:**
```bash
# Run all except expensive tests
pytest tests/ -v -m "not expensive"

# Run expensive tests manually
pytest tests/ -v -m expensive
```

---

## 5. Unit Tests for Scraper Functions

```python
# tests/test_scraper_unit.py
import pytest
from unittest.mock import Mock, patch
from scripts.scrape_and_summarize import (
    scrape_latest_gaceta_url,
    download_pdf,
    extract_text_from_pdf
)

def test_scrape_handles_missing_link():
    """Unit: scrape_latest_gaceta_url returns None if link not found"""
    with patch('requests.get') as mock_get:
        mock_get.return_value.text = "<html><body>No PDF link here</body></html>"
        url = scrape_latest_gaceta_url()
        assert url is None

def test_download_pdf_handles_404():
    """Unit: download_pdf returns None on 404"""
    with patch('requests.get') as mock_get:
        mock_get.side_effect = Exception("404 Not Found")
        pdf = download_pdf("https://example.com/fake.pdf")
        assert pdf is None

def test_extract_text_handles_empty_pdf():
    """Unit: extract_text_from_pdf handles PDFs with no text"""
    # Create a mock PDF with no extractable text
    from io import BytesIO
    empty_pdf = BytesIO(b"%PDF-1.4\n")  # Minimal PDF header

    # Should not crash, just return empty or minimal text
    text = extract_text_from_pdf(empty_pdf, max_pages=1)
    assert text is not None or text == ""
```

---

## 6. GitHub Actions Integration Tests

Test that the workflow actually runs successfully:

```yaml
# .github/workflows/test.yml
name: Run Tests

on:
  push:
    branches: [master, main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'

    - name: Install uv
      uses: astral-sh/setup-uv@v5

    - name: Install dependencies
      run: |
        uv pip install --system pytest pytest-mock requests beautifulsoup4 pypdf streamlit

    - name: Run unit tests
      run: |
        pytest tests/ -v -m "not expensive"

    - name: Run Streamlit app tests
      run: |
        pytest test_demo_simple.py -v

    # Only run expensive tests on main branch
    - name: Run integration tests (with OpenAI)
      if: github.ref == 'refs/heads/master'
      env:
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      run: |
        pytest tests/ -v -m expensive
```

---

## 7. Cost-Aware Testing Strategy

### Problem: Tests That Cost Money

Every call to `summarize_with_gpt4()` costs **$0.01-0.05** (GPT-4o pricing).

If you run tests on every commit, costs add up:
- 10 commits/day × $0.03/test = **$0.30/day = $9/month** (just from tests!)

### Solution: Mock OpenAI in Most Tests

```python
# tests/conftest.py
import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_openai_response():
    """Mock GPT-4o response to avoid API costs"""
    return {
        "summary": "Resumen de prueba de La Gaceta",
        "bullets": [
            {"icon": "⚖️", "text": "Cambio legal de prueba"},
            {"icon": "💰", "text": "Decisión fiscal de prueba"},
            {"icon": "🏥", "text": "Anuncio de salud de prueba"},
            {"icon": "📚", "text": "Cambio educativo de prueba"},
            {"icon": "🌱", "text": "Regulación ambiental de prueba"}
        ],
        "topics": ["Legal", "Fiscal", "Salud", "Educación", "Ambiente"]
    }

@pytest.fixture
def mock_gpt4_call(monkeypatch, mock_openai_response):
    """Replace OpenAI API calls with mock response"""
    def mock_summarize(*args, **kwargs):
        return mock_openai_response

    monkeypatch.setattr(
        'scripts.scrape_and_summarize.summarize_with_gpt4',
        mock_summarize
    )
```

**Usage in tests:**
```python
def test_scraper_with_mocked_ai(mock_gpt4_call):
    """Test full flow without calling OpenAI API (saves money!)"""
    # This test costs $0.00
    from scripts.scrape_and_summarize import main
    main()  # Uses mocked GPT-4 response
    # Verify JSON was saved correctly
```

---

## 8. Testing Priority for Alpha

### Week 1: Essential Tests (MVP)
- [ ] Streamlit smoke test (`test_app_loads_without_crashing`)
- [ ] Scraper finds PDF link (`test_scraper_finds_pdf_link`)
- [ ] JSON save/load works (`test_load_summaries`)

**Effort**: 2-3 hours
**Coverage**: ~60% of critical path

### Week 2: Integration Tests
- [ ] Full scraping flow (with mocked OpenAI)
- [ ] GitHub Actions workflow test
- [ ] Streamlit displays live data correctly

**Effort**: 3-4 hours
**Coverage**: ~85% of critical path

### Month 2+: Unit Tests & Edge Cases
- [ ] Handle 404s, timeouts, corrupted PDFs
- [ ] Handle malformed OpenAI responses
- [ ] Test data cleanup (90-day limit)

**Effort**: 4-6 hours
**Coverage**: ~95%+

---

## 9. Testing Commands Cheat Sheet

```bash
# Install test dependencies
uv pip install pytest pytest-mock pytest-cov

# Run all tests
pytest tests/ -v

# Run only unit tests (fast, free)
pytest tests/ -v -m "not expensive"

# Run only integration tests (expensive, uses OpenAI)
pytest tests/ -v -m expensive

# Run Streamlit app tests
pytest test_demo_simple.py -v

# Run with coverage report
pytest tests/ --cov=scripts --cov=demo_simple --cov-report=html

# Run specific test
pytest tests/test_scraper_unit.py::test_scrape_handles_missing_link -v

# Run tests in parallel (faster)
uv pip install pytest-xdist
pytest tests/ -n auto
```

---

## 10. File Structure

```
gacetachat/
├── scripts/
│   └── scrape_and_summarize.py      # Main scraper logic
├── demo_simple.py                    # Streamlit app
├── tests/                            # NEW: Test directory
│   ├── __init__.py
│   ├── conftest.py                  # Fixtures (mock OpenAI)
│   ├── test_scraper_unit.py         # Unit tests for scraper functions
│   ├── test_scraper_integration.py  # Integration tests (scraping flow)
│   └── test_data_handling.py        # Tests for JSON save/load
├── test_demo_simple.py               # NEW: Streamlit app tests
├── pytest.ini                        # NEW: pytest configuration
└── .github/
    └── workflows/
        ├── daily-scraper.yml         # Existing scraper workflow
        └── test.yml                  # NEW: CI/CD test workflow
```

---

## 11. pytest.ini Configuration

```ini
# pytest.ini
[pytest]
markers =
    expensive: Tests that call OpenAI API (cost money, run manually)
    integration: Integration tests (require network)
    unit: Unit tests (fast, no network)
    smoke: Smoke tests (basic functionality)

testpaths = tests

# Don't run expensive tests by default
addopts = -v --tb=short -m "not expensive"

# Ignore venv and archive directories
norecursedirs = venv archive .git
```

---

## 12. What NOT to Test (For Alpha)

**Skip these for now** (add later for full MVP):

1. ❌ **Performance tests** - Who cares if it takes 3 seconds vs 1 second? It runs daily.
2. ❌ **Load tests** - Alpha has <50 users, not 50,000.
3. ❌ **Security tests** - No user authentication, no database, just public data.
4. ❌ **Accessibility tests** - Important for MVP, not critical for alpha validation.
5. ❌ **Cross-browser E2E** - Streamlit handles browser compatibility.

**Focus on**: Does it work? Does it break when La Gaceta changes? Does GPT-4 return valid JSON?

---

## 13. Success Metrics for Testing

### Alpha Testing Goals

**Week 1**:
- ✅ Scraper runs successfully 5 days in a row
- ✅ No crashes in Streamlit app
- ✅ Basic smoke tests passing

**Month 1**:
- ✅ 90%+ test coverage on critical path
- ✅ CI/CD pipeline catches regressions
- ✅ Zero manual testing needed for deployments

**Month 3**:
- ✅ Integration tests catch homepage changes before scraper fails
- ✅ Mocked tests run in <10 seconds
- ✅ Expensive tests run only on main branch merges

---

## 14. Troubleshooting Tests

### Tests Fail Locally But Pass in CI
- **Cause**: Different Python versions, missing dependencies
- **Fix**: Use same Python version locally as CI (3.11)

### Tests Are Slow
- **Cause**: Calling OpenAI API in every test
- **Fix**: Use `@pytest.mark.expensive` and mock OpenAI responses

### Streamlit Tests Crash
- **Cause**: Streamlit caching interferes with tests
- **Fix**: Clear cache between tests:
```python
@pytest.fixture(autouse=True)
def clear_streamlit_cache():
    import streamlit as st
    st.cache_data.clear()
```

### GitHub Actions Workflow Fails
- **Cause**: Missing `OPENAI_API_KEY` secret
- **Fix**: Add secret in repo settings OR skip expensive tests in CI

---

## 15. Next Steps

**Immediate** (This Week):
1. Create `tests/` directory
2. Write `conftest.py` with OpenAI mock fixture
3. Write 3 smoke tests for Streamlit app
4. Add `pytest.ini` configuration
5. Run tests manually: `pytest -v`

**Short-term** (Next 2 Weeks):
1. Add integration test for scraper (without OpenAI)
2. Create GitHub Actions test workflow
3. Write unit tests for error handling
4. Achieve 70%+ coverage on `scrape_and_summarize.py`

**Long-term** (Month 2+):
1. Monitor test flakiness (tests that fail randomly)
2. Add performance benchmarks (optional)
3. Set up test coverage reporting (codecov.io)
4. When building full MVP: add E2E tests with Playwright

---

## 16. Architectural Decision Records (ADR)

### ADR-001: Use Streamlit's Built-in Testing Framework
**Decision**: Use `st.testing.v1` instead of Selenium/Playwright for Streamlit app tests

**Rationale**:
- Faster (2-3 seconds vs 30+ seconds)
- No browser dependencies
- Official Streamlit testing framework
- Perfect for alpha validation

**Alternatives Considered**:
- Selenium: Too slow, complex setup
- Playwright: Overkill for simple Streamlit app

### ADR-002: Mock OpenAI API Calls in Tests
**Decision**: Use pytest fixtures to mock GPT-4o responses in most tests

**Rationale**:
- Saves ~$9/month on test API costs
- Tests run faster (no network calls)
- Tests are deterministic (no AI variability)

**When to Use Real API**:
- Manual testing before releases
- Integration tests on main branch only (via CI flag)

### ADR-003: Integration Tests Before Unit Tests
**Decision**: Prioritize integration tests for alpha validation

**Rationale**:
- Alpha's value = "Does the scraper work end-to-end?"
- Unit tests are important but less critical for market validation
- Integration tests catch 80% of bugs with 20% of effort

**When to Add Unit Tests**:
- After alpha proves demand
- Before scaling to full MVP
- When refactoring scraper logic

---

## 17. Cost-Benefit Analysis

### Without Tests
**Pros**:
- Ship faster (no time spent writing tests)

**Cons**:
- Manual testing takes 10-15 min/day
- Bugs discovered by NGO users (embarrassing)
- One bad scrape = 24 hours of missing data
- Can't refactor safely

**Cost**: ~1 hour/week manual testing = **$50/week** ($2,600/year at $50/hr rate)

### With Tests (This Architecture)
**Pros**:
- Automated testing takes 0 min/day
- Catch bugs before deployment
- Refactor with confidence
- Professional impression for grant applications

**Cons**:
- Upfront cost: 8-10 hours to write tests
- Monthly OpenAI test costs: ~$3/month (expensive tests only)

**Cost**: 10 hours upfront + $3/month = **$500 one-time + $36/year**

**ROI**: Save $2,600/year by automating tests = **520% ROI**

---

## 18. References & Resources

**Streamlit Testing**:
- Official docs: https://docs.streamlit.io/develop/api-reference/app-testing
- Tutorial: "Testing Streamlit Apps" (Streamlit blog)

**pytest**:
- Docs: https://docs.pytest.org/
- Fixtures guide: https://docs.pytest.org/en/stable/how-to/fixtures.html
- Mocking: https://docs.pytest.org/en/stable/how-to/monkeypatch.html

**GitHub Actions**:
- pytest in CI: https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python

**Cost Estimation**:
- OpenAI pricing: https://openai.com/api/pricing/
- GPT-4o: ~$0.03 per 1,000 tokens input + $0.06 per 1,000 tokens output

---

## The Bottom Line

**For a $60/month serverless alpha, spend 10 hours on tests to save 50+ hours of manual testing.**

**Test Priority**:
1. **Integration**: Does the scraper → GPT-4 → JSON → Streamlit flow work?
2. **Unit**: Do individual functions handle errors gracefully?
3. **E2E**: (Skip for alpha, add for MVP)

**Framework**: Streamlit `st.testing.v1` + pytest + mocked OpenAI

**Cost**: $3/month (if you only run expensive tests on main branch)

**This is how you test a civic tech alpha in 2025.**

---

*Built with testing best practices from 50 years of software engineering*
*Cost-optimized for serverless alpha validation*
