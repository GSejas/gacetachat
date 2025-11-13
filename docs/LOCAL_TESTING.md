# Local Testing Guide

## Testing Header Image Generation Locally

### Prerequisites

1. **Install Python dependencies:**
```bash
# Option 1: Using uv (recommended)
uv pip install -r requirements-scraper.txt

# Option 2: Using pip
pip install -r requirements-scraper.txt
```

2. **Install system dependency (poppler):**

**macOS:**
```bash
brew install poppler
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y poppler-utils
```

**Windows:**
1. Download poppler from: https://github.com/oschwartz10612/poppler-windows/releases/
2. Extract to `C:\Program Files\poppler`
3. Add `C:\Program Files\poppler\Library\bin` to PATH

**Verify installation:**
```bash
# Should show version info
pdftoppm -v
```

3. **Set OpenAI API key:**
```bash
# Create .env file
echo "OPENAI_API_KEY=your_key_here" > .env

# Or export directly
export OPENAI_API_KEY=your_key_here  # macOS/Linux
set OPENAI_API_KEY=your_key_here     # Windows CMD
$env:OPENAI_API_KEY="your_key_here"  # Windows PowerShell
```

### Run the Scraper

```bash
# From project root
python scripts/scrape_and_summarize.py
```

### Expected Output

```
============================================================
GacetaChat Daily Scraper - Alpha
============================================================

🌐 Method 1: Scraping homepage for latest PDF...
🔍 Scraping La Gaceta homepage for latest PDF...
✅ Found PDF URL: https://www.imprentanacional.go.cr/pub/2025/11/12/COMP_12_11_2025.pdf
📥 Downloading: https://www.imprentanacional.go.cr/pub/2025/11/12/COMP_12_11_2025.pdf
📅 Extracted date from filename: 2025-11-12
📅 Detected date: 2025-11-12
🎨 Creating header image from PDF...
✅ Header image saved: 2025-11-12.jpg (87.3 KB)
📄 Extracting text from PDF...
✅ Extracted 45231 characters from 50/156 pages
🤖 Generating summary with GPT-4o...
✅ Summary generated: 5 bullets (prompt v2.0.0)
💰 Cost: $0.0018 | Tokens: 4719

✅ SUCCESS! Summary for 2025-11-12 saved
   Summary: La Gaceta Oficial del 12 de noviembre...
   Bullets: 5
   Topics: Legal, Salud, Economía, Competencia
   Header: header_images/2025-11-12.jpg

============================================================
✨ Scraper finished. Total summaries: 2
============================================================
```

### Check Generated Files

**Header image:**
```bash
# Should exist
ls data/header_images/2025-11-12.jpg

# Check size (should be 50-150 KB)
du -h data/header_images/2025-11-12.jpg
```

**Updated JSON:**
```bash
# Check summaries.json includes header_image field
cat data/summaries.json | grep -A 5 "header_image"
```

**View the image:**
```bash
# macOS
open data/header_images/2025-11-12.jpg

# Linux
xdg-open data/header_images/2025-11-12.jpg

# Windows
start data/header_images/2025-11-12.jpg
```

### Test the Demo

```bash
# Run Streamlit demo locally
uv run demo_simple.py
# Or: streamlit run demo_simple.py
```

Visit http://localhost:8501 and check:
1. Header image displays at top
2. Image is darkened (not bright white)
3. Caption shows "La Gaceta Oficial"
4. Full width display

### Testing Without OpenAI API Key

If you just want to test image generation without AI summary:

**Create test script:**
```python
# test_header_image.py
from pathlib import Path
from io import BytesIO
import requests
from pdf2image import convert_from_bytes
from PIL import ImageEnhance

# Download sample PDF
url = "https://www.imprentanacional.go.cr/pub/2025/11/12/COMP_12_11_2025.pdf"
response = requests.get(url)
pdf_bytes = BytesIO(response.content)

# Convert first page
images = convert_from_bytes(pdf_bytes.read(), first_page=1, last_page=1, dpi=150)

# Crop and darken
page_image = images[0]
width, height = page_image.size
header = page_image.crop((0, 0, width, height // 2))

enhancer_brightness = ImageEnhance.Brightness(header)
darkened = enhancer_brightness.enhance(0.6)

enhancer_contrast = ImageEnhance.Contrast(darkened)
final = enhancer_contrast.enhance(1.1)

# Save
output = Path("test_header.jpg")
final.save(output, "JPEG", quality=85, optimize=True)
print(f"✅ Test image saved: {output} ({output.stat().st_size / 1024:.1f} KB)")
```

**Run:**
```bash
python test_header_image.py
```

### Troubleshooting

#### Error: "pdf2image not found"
```bash
pip install pdf2image
```

#### Error: "Unable to find pdftoppm"
Poppler not installed or not in PATH. See installation instructions above.

#### Error: "PIL not found"
```bash
pip install Pillow
```

#### Image too large (>200 KB)
- Check DPI (should be 150, not 300)
- Check JPEG quality (should be 85, not 100)
- Check if full page instead of cropped half

#### Image not displaying in demo
```bash
# Check file exists
ls data/header_images/2025-11-12.jpg

# Check JSON has correct path
grep "header_image" data/summaries.json

# Check path in demo
python -c "from pathlib import Path; print(Path('data/header_images/2025-11-12.jpg').exists())"
```

#### Image too dark / too light
Edit `scripts/scrape_and_summarize.py`:
```python
# Line ~101: Adjust brightness (0.6 = 60%)
darkened = enhancer_brightness.enhance(0.6)  # Try 0.5-0.7

# Line ~104: Adjust contrast (1.1 = 110%)
final_image = enhancer_contrast.enhance(1.1)  # Try 1.0-1.2
```

### Testing Fallback Behavior

**Test without poppler (should gracefully skip image):**
```bash
# Temporarily rename poppler
which pdftoppm  # Note the path
sudo mv /usr/bin/pdftoppm /usr/bin/pdftoppm.bak

# Run scraper
python scripts/scrape_and_summarize.py

# Should see: "⚠️ pdf2image or PIL not installed - skipping header image"
# But scraper should still complete successfully

# Restore poppler
sudo mv /usr/bin/pdftoppm.bak /usr/bin/pdftoppm
```

### Performance Testing

```bash
# Time the scraper
time python scripts/scrape_and_summarize.py
```

**Expected times:**
- PDF download: 5-10 seconds
- Header image: 2-5 seconds
- Text extraction: 1-2 seconds
- AI summary: 3-8 seconds
- **Total: 15-30 seconds**

### Manual Testing Checklist

- [ ] Poppler installed (`pdftoppm -v` works)
- [ ] Python dependencies installed
- [ ] OpenAI API key set
- [ ] Scraper runs without errors
- [ ] Header image created in `data/header_images/`
- [ ] Image size 50-150 KB
- [ ] JSON includes `header_image` field
- [ ] Demo displays image correctly
- [ ] Image is darkened (not bright white)
- [ ] Fallback works (scraper runs without poppler)

### Continuous Testing

**Run scraper on demand:**
```bash
# Clear existing summary for today to force regeneration
python -c "import json; d = json.load(open('data/summaries.json')); d.pop('2025-11-12', None); json.dump(d, open('data/summaries.json', 'w'), indent=2)"

# Run scraper again
python scripts/scrape_and_summarize.py
```

**Test different dates:**
```python
# Modify scraper to test specific date
# In scrape_and_summarize.py, change URL pattern
```

---

## Quick Test Commands

**Full test:**
```bash
# Install dependencies
uv pip install -r requirements-scraper.txt

# Verify poppler
pdftoppm -v

# Set API key
export OPENAI_API_KEY=your_key

# Run scraper
python scripts/scrape_and_summarize.py

# Check output
ls -lh data/header_images/
open data/header_images/*.jpg

# Run demo
uv run demo_simple.py
```

**Fast test (image only):**
```python
# test_image_quick.py
from scripts.scrape_and_summarize import create_header_image, download_pdf
from io import BytesIO

url = "https://www.imprentanacional.go.cr/pub/2025/11/12/COMP_12_11_2025.pdf"
pdf_bytes = download_pdf(url)
result = create_header_image(pdf_bytes, "test")
print(f"Result: {result}")
```

---

**Last Updated:** 2025-11-12
**Status:** Ready for local testing
**Time to test:** ~5 minutes (first time), ~30 seconds (subsequent)
