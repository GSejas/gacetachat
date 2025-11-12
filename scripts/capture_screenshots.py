#!/usr/bin/env python3
"""
Automated screenshot capture for GacetaChat demo using Playwright.

Usage:
    python scripts/capture_screenshots.py

This script will:
1. Navigate to the live Streamlit demo
2. Capture screenshots of key pages/states
3. Save them to docs/screenshots/
4. Optimize images for web

Requirements:
    pip install playwright pillow
    playwright install chromium
"""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from datetime import datetime

# Configuration
DEMO_URL = "https://gacetachat.streamlit.app/"
SCREENSHOTS_DIR = Path(__file__).parent.parent / "docs" / "screenshots"
VIEWPORT_DESKTOP = {"width": 1280, "height": 720}
VIEWPORT_MOBILE = {"width": 375, "height": 812}


async def capture_screenshots():
    """Capture all screenshots for the demo"""

    # Ensure screenshots directory exists
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=True)

        # Desktop screenshots
        print("📸 Capturing desktop screenshots...")
        context = await browser.new_context(
            viewport=VIEWPORT_DESKTOP,
            device_scale_factor=2  # Retina quality
        )
        page = await context.new_page()

        # Navigate to demo
        print(f"   → Loading {DEMO_URL}")
        await page.goto(DEMO_URL, wait_until="networkidle")
        await page.wait_for_timeout(3000)  # Let Streamlit fully render

        # Screenshot 1: Homepage with onboarding expanded
        print("   → Capturing onboarding view...")
        await page.screenshot(
            path=SCREENSHOTS_DIR / "onboarding.png",
            full_page=False
        )

        # Screenshot 2: Collapse onboarding, show main content
        print("   → Capturing homepage...")
        # Try to collapse the expander
        try:
            expander = page.locator("summary:has-text('¿Qué es La Gaceta Oficial?')")
            if await expander.is_visible():
                await expander.click()
                await page.wait_for_timeout(500)
        except:
            pass

        await page.screenshot(
            path=SCREENSHOTS_DIR / "homepage.png",
            full_page=False
        )

        # Screenshot 3: Date navigation expanded
        print("   → Capturing date navigation...")
        try:
            date_expander = page.locator("summary:has-text('Seleccionar otra fecha')")
            if await date_expander.is_visible():
                await date_expander.click()
                await page.wait_for_timeout(500)
        except:
            pass

        await page.screenshot(
            path=SCREENSHOTS_DIR / "date-navigation.png",
            full_page=False
        )

        await context.close()

        # Mobile screenshots
        print("📱 Capturing mobile screenshots...")
        mobile_context = await browser.new_context(
            viewport=VIEWPORT_MOBILE,
            device_scale_factor=2,
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15"
        )
        mobile_page = await mobile_context.new_page()

        await mobile_page.goto(DEMO_URL, wait_until="networkidle")
        await mobile_page.wait_for_timeout(3000)

        print("   → Capturing mobile view...")
        await mobile_page.screenshot(
            path=SCREENSHOTS_DIR / "mobile-view.png",
            full_page=True
        )

        await mobile_context.close()
        await browser.close()

    print(f"\n✅ Screenshots saved to {SCREENSHOTS_DIR}")
    print("\n📋 Captured screenshots:")
    for screenshot in sorted(SCREENSHOTS_DIR.glob("*.png")):
        size_kb = screenshot.stat().st_size / 1024
        print(f"   • {screenshot.name} ({size_kb:.1f} KB)")


async def optimize_screenshots():
    """Optimize screenshots for web using Pillow"""
    try:
        from PIL import Image

        print("\n🔧 Optimizing screenshots...")
        for screenshot in SCREENSHOTS_DIR.glob("*.png"):
            img = Image.open(screenshot)

            # Optimize PNG
            img.save(
                screenshot,
                optimize=True,
                quality=85
            )

            size_kb = screenshot.stat().st_size / 1024
            print(f"   ✓ {screenshot.name} optimized ({size_kb:.1f} KB)")

        print("✅ All screenshots optimized!")

    except ImportError:
        print("\n⚠️  Pillow not installed. Skipping optimization.")
        print("   Install with: pip install pillow")


async def main():
    """Main entry point"""
    print("=" * 60)
    print("GacetaChat Screenshot Capture Tool")
    print("=" * 60)
    print(f"Target: {DEMO_URL}")
    print(f"Output: {SCREENSHOTS_DIR}")
    print("=" * 60)

    await capture_screenshots()
    await optimize_screenshots()

    print("\n" + "=" * 60)
    print("✨ Done! Screenshots ready for README.md")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
