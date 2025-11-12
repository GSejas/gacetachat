# GacetaChat Screenshots

This directory contains screenshots of the GacetaChat demo for documentation purposes.

## Manual Capture

Take screenshots of:
- **homepage.png** - Main view with daily summary
- **date-navigation.png** - Date picker in action
- **onboarding.png** - Onboarding experience expanded
- **mobile-view.png** - Mobile responsive view

## Automated Capture with Playwright

### Option 1: Using Playwright MCP Server (Recommended)

If Claude Code has Playwright MCP server enabled:

```bash
# Just ask Claude to capture screenshots!
# Claude will use the mcp__playwright tools automatically
```

### Option 2: Using Python Script

```bash
# Install dependencies
pip install playwright pillow
playwright install chromium

# Run the script
python scripts/capture_screenshots.py
```

The script will:
1. Launch headless Chromium browser
2. Navigate to https://gacetachat.streamlit.app/
3. Capture desktop screenshots (1280x720)
4. Capture mobile screenshots (375x812)
5. Optimize images for web
6. Save to this directory

## Screenshot Guidelines

- **Format**: PNG (optimized)
- **Desktop size**: 1280x720 @ 2x (Retina)
- **Mobile size**: 375x812 @ 2x (iPhone)
- **Max file size**: ~300KB per image
- **Naming**: Lowercase with hyphens (e.g., `mobile-view.png`)

## Current Screenshots

| Screenshot | Description | Status |
|------------|-------------|--------|
| `homepage.png` | Main summary view | ⏳ Pending |
| `date-navigation.png` | Date picker UI | ⏳ Pending |
| `onboarding.png` | Onboarding expanded | ⏳ Pending |
| `mobile-view.png` | Mobile responsive | ⏳ Pending |

## Adding New Screenshots

1. Capture the screenshot
2. Optimize with `python scripts/capture_screenshots.py` or manually
3. Add to this README
4. Reference in main README.md
5. Commit and push

---

*These screenshots showcase the Streamlit demo prototype, not the final MVP which will be built with Next.js + FastAPI.*
