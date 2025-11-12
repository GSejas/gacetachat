# Quick Test Guide

## Install & Run Tests (5 minutes)

```bash
# 1. Install test dependencies
uv pip install pytest pytest-mock pytest-cov

# 2. Run all tests (auto-skips expensive tests)
pytest -v

# 3. See results
# ✅ = passed | ❌ = failed | ⏩ = skipped
```

## What Just Ran?

**26 tests total**:
- ✅ 10 unit tests (fast, no network)
- ✅ 5 integration tests (network required)
- ✅ 11 Streamlit app tests
- ⏩ 1 expensive test (skipped by default)

**Time**: ~30-60 seconds
**Cost**: $0.00 (expensive tests skipped)

## Common Commands

```bash
# Fast unit tests only (2 seconds)
pytest tests/ -m unit

# Integration tests (30 seconds)
pytest tests/ -m integration

# Streamlit app tests (5 seconds)
pytest test_demo_simple.py

# Run expensive test manually (costs ~$0.03)
pytest tests/ -m expensive

# Coverage report
pytest --cov=scripts --cov-report=term-missing
```

## Understanding Test Results

```bash
tests/test_scraper_unit.py::test_scrape_handles_missing_link PASSED      [ 6%]
tests/test_scraper_unit.py::test_scrape_handles_network_error PASSED     [13%]
```

- `PASSED` ✅ = Test succeeded
- `FAILED` ❌ = Test found a bug (fix it!)
- `SKIPPED` ⏩ = Test marked as expensive/slow
- `[13%]` = Progress (13% of tests complete)

## If Tests Fail

### Import Errors
```bash
uv pip install requests beautifulsoup4 pypdf streamlit openai
```

### Network Errors (integration tests)
```bash
# Skip integration tests if offline
pytest tests/ -m "not integration"
```

### All Tests Fail
```bash
# Check Python version (needs 3.11+)
python --version

# Reinstall dependencies
uv pip install -r requirements.txt
```

## CI/CD (Automatic)

Tests run automatically when you:
- Push to GitHub
- Open a pull request
- Merge to main/master

See results in GitHub Actions tab.

## More Info

- **Full docs**: [docs/TEST_ARCHITECTURE.md](docs/TEST_ARCHITECTURE.md)
- **Test README**: [tests/README.md](tests/README.md)
- **Summary**: [TESTING_SUMMARY.md](TESTING_SUMMARY.md)

---

**TL;DR**: Run `pytest -v` and see green checkmarks ✅
