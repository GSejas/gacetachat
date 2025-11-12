# GacetaChat Tests

Comprehensive test suite for the serverless alpha.

## Quick Start

```bash
# Install test dependencies
uv pip install pytest pytest-mock pytest-cov

# Run all tests (excludes expensive OpenAI tests)
pytest

# Run only unit tests (fastest)
pytest tests/ -m unit

# Run integration tests (requires network)
pytest tests/ -m integration

# Run Streamlit app tests
pytest test_demo_simple.py -v

# Run expensive tests manually (costs ~$0.01-0.05)
pytest tests/ -m expensive
```

## Test Structure

```
tests/
├── __init__.py
├── conftest.py                  # Fixtures (mock OpenAI, etc.)
├── test_scraper_unit.py         # Unit tests (fast, no network)
├── test_scraper_integration.py  # Integration tests (network required)
└── README.md                    # This file

test_demo_simple.py              # Streamlit app tests (root level)
pytest.ini                       # pytest configuration
```

## Test Categories

### Unit Tests (`-m unit`)
- Fast (<1 second each)
- No network or API calls
- Mock all external dependencies
- Test individual functions in isolation

### Integration Tests (`-m integration`)
- Require network access
- Test scraper → PDF download → text extraction
- Use mocked OpenAI (free!)
- Take 10-30 seconds per test

### Expensive Tests (`-m expensive`)
- Call real OpenAI API (costs money!)
- Only run manually or on main branch CI
- Cost: ~$0.01-0.05 per run

### Smoke Tests (`-m smoke`)
- Basic "does it work at all?" checks
- Run these first when debugging

## Coverage

```bash
# Generate HTML coverage report
pytest tests/ test_demo_simple.py --cov=scripts --cov=demo_simple --cov-report=html

# View report
open htmlcov/index.html  # macOS/Linux
start htmlcov/index.html  # Windows
```

## Troubleshooting

### Tests fail with "Module not found"
```bash
# Make sure you're in the project root
cd /path/to/gacetachat

# Install dependencies
uv pip install -r requirements.txt
uv pip install pytest pytest-mock
```

### Integration tests timeout
```bash
# Increase timeout or skip integration tests
pytest tests/ -m "not integration"
```

### Expensive tests run when they shouldn't
```bash
# Verify pytest.ini has the right marker config
pytest tests/ -v  # Should NOT run expensive tests by default
```

## CI/CD

Tests run automatically on:
- Push to `master` or `main` branch
- Pull requests
- Manual workflow trigger

See [.github/workflows/test.yml](../.github/workflows/test.yml) for details.

Expensive tests only run on `master`/`main` branch to save costs.

## Cost Breakdown

| Test Type | Cost per Run | Run Frequency | Monthly Cost |
|-----------|--------------|---------------|--------------|
| Unit | $0.00 | Every commit | $0 |
| Integration | $0.00 | Every commit | $0 |
| Streamlit | $0.00 | Every commit | $0 |
| Expensive | $0.01-0.05 | Main branch only | ~$3/month |

**Total**: ~$3/month if you merge to main 60 times/month.

## Writing New Tests

### Example: Unit Test
```python
# tests/test_my_feature.py
import pytest

def test_my_function():
    from scripts.scrape_and_summarize import my_function
    result = my_function("input")
    assert result == "expected"
```

### Example: Integration Test
```python
@pytest.mark.integration
def test_full_flow():
    # Test with real network calls
    from scripts.scrape_and_summarize import scrape_latest_gaceta_url
    url = scrape_latest_gaceta_url()
    assert url is not None
```

### Example: Expensive Test
```python
@pytest.mark.expensive
def test_with_real_openai():
    # Costs money - only run manually
    from scripts.scrape_and_summarize import summarize_with_gpt4
    result = summarize_with_gpt4("test", datetime.now())
    assert result is not None
```

## Best Practices

1. **Use fixtures** from `conftest.py` to avoid repetition
2. **Mock OpenAI** unless testing AI quality (save costs!)
3. **Keep unit tests fast** (<1 second each)
4. **Use descriptive test names** (`test_scraper_handles_404` not `test_1`)
5. **One assertion per test** when possible
6. **Test edge cases** (404s, timeouts, corrupted data)

## Questions?

See [docs/TEST_ARCHITECTURE.md](../docs/TEST_ARCHITECTURE.md) for full architecture details.
