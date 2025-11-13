# Header Images

This directory contains darkened header images extracted from the first page of each day's La Gaceta PDF.

## Purpose

- **Visual authenticity** - Shows the actual government document
- **Trust signal** - Demonstrates this is real La Gaceta data
- **Visual distinction** - Each day looks different
- **Design element** - Professional header for summaries

## Technical Details

- **Source:** First page of daily La Gaceta PDF
- **Crop:** Top half only (header area)
- **Processing:** 40% darkening + slight contrast boost
- **Format:** JPEG, quality 85
- **Size:** ~50-150 KB per image
- **DPI:** 150 (balance of quality/size)

## Generation

Images are generated automatically by `scripts/scrape_and_summarize.py` during the daily scraping process:

1. Download PDF
2. Convert first page to image (pdf2image)
3. Crop to top half
4. Darken 40% + boost contrast 10%
5. Save as JPEG (optimized)
6. Reference in summaries.json

## Display

The demo (`demo_simple.py`) displays these images at the top of each day's summary if available.

## File Naming

Format: `YYYY-MM-DD.jpg`

Examples:
- `2025-11-12.jpg`
- `2025-11-13.jpg`

## Dependencies

- `pdf2image` (Python package)
- `Pillow` (PIL for image processing)
- `poppler-utils` (system package, required by pdf2image)

## Maintenance

- Images are kept for 90 days (same as summaries)
- Old images are automatically removed when summaries are pruned
- Total storage: ~5-15 MB for 90 days of images

## Fallback

If image generation fails (missing dependencies, PDF issues):
- Scraper continues without error
- Summary is still generated
- Demo works fine without header image

---

**Note:** Images are committed to git so the demo can display them on Streamlit Cloud. If repo size becomes an issue, consider hosting images separately (S3, Cloudflare R2, etc.).
