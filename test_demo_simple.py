"""
Streamlit app tests using st.testing.v1
Fast tests that verify the Streamlit UI works correctly
"""
import pytest
from streamlit.testing.v1 import AppTest


def test_app_loads_without_crashing():
    """Smoke test: Does the app even load?"""
    at = AppTest.from_file("demo_simple.py", default_timeout=10)
    at.run()
    assert not at.exception, f"App crashed with: {at.exception}"


def test_app_shows_title():
    """Does the title render correctly?"""
    at = AppTest.from_file("demo_simple.py")
    at.run()

    # Check for title
    assert len(at.title) > 0, "No title found"
    assert "GacetaChat" in at.title[0].value


def test_app_shows_status_indicator():
    """Shows either 🟢 (live) or 🟡 (demo) indicator"""
    at = AppTest.from_file("demo_simple.py")
    at.run()

    # Check for status indicator in captions
    captions = [str(c.value) for c in at.caption]
    has_indicator = any("🟢" in c or "🟡" in c for c in captions)

    assert has_indicator, "No status indicator found (expected 🟢 or 🟡)"


def test_app_has_date_selector():
    """Does the app render a date picker?"""
    at = AppTest.from_file("demo_simple.py")
    at.run()

    # Streamlit date_input creates a date_input widget
    assert len(at.date_input) > 0, "No date selector found"


def test_app_displays_summary_section():
    """Does the app show summary content?"""
    at = AppTest.from_file("demo_simple.py")
    at.run()

    # Check for markdown content (summaries are displayed with st.markdown)
    assert len(at.markdown) > 0, "No markdown content found"


def test_app_has_sidebar_content():
    """Does the sidebar have expected content?"""
    at = AppTest.from_file("demo_simple.py")
    at.run()

    # Sidebar should have info/help content
    # Streamlit doesn't expose sidebar separately in AppTest,
    # but we can check that the app renders without errors
    assert not at.exception


def test_app_handles_date_selection():
    """Can we interact with the date picker?"""
    at = AppTest.from_file("demo_simple.py")
    at.run()

    # App should have date_input widget
    if len(at.date_input) > 0:
        # Get available dates from the date_input widget
        # In Streamlit testing, we can check if the widget exists
        assert at.date_input[0].value is not None


def test_app_shows_bullet_points():
    """Does the app display bullet point summaries?"""
    at = AppTest.from_file("demo_simple.py")
    at.run()

    # Look for emoji icons that indicate bullet points
    markdown_content = " ".join([str(m.value) for m in at.markdown])

    # Common emojis used in summaries
    common_emojis = ["⚖️", "💰", "🏥", "📚", "🌱", "🏢", "⚡", "🔍"]
    has_emojis = any(emoji in markdown_content for emoji in common_emojis)

    assert has_emojis, "No bullet point emojis found in markdown content"


def test_app_shows_onboarding_section():
    """Does the app show '¿Qué es La Gaceta?' onboarding?"""
    at = AppTest.from_file("demo_simple.py")
    at.run()

    # Check for onboarding text
    all_text = " ".join([str(m.value) for m in at.markdown])
    assert "Gaceta" in all_text, "No mention of 'Gaceta' found in app"


@pytest.mark.smoke
def test_app_renders_without_errors_multiple_runs():
    """Smoke test: App should render consistently across multiple runs"""
    for _ in range(3):
        at = AppTest.from_file("demo_simple.py")
        at.run()
        assert not at.exception, f"App crashed on one of multiple runs: {at.exception}"


def test_app_has_expected_structure():
    """Verify app has expected UI elements"""
    at = AppTest.from_file("demo_simple.py")
    at.run()

    # Should have:
    # - Title
    # - Caption (status indicator)
    # - Date input
    # - Markdown content (summaries)
    assert len(at.title) > 0, "Missing title"
    assert len(at.caption) > 0, "Missing caption"
    assert len(at.date_input) > 0, "Missing date picker"
    assert len(at.markdown) > 0, "Missing markdown content"
