#!/usr/bin/env python3
"""
GacetaChat Daily Scraper - Serverless Alpha
Scrapes La Gaceta, summarizes with GPT-4o, saves to JSON

Cost: ~$2-5 per day (OpenAI API)
Runtime: ~2-5 minutes per day
"""

import os
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path
import pypdf
from io import BytesIO
from openai import OpenAI
from bs4 import BeautifulSoup

# Configuration
DATA_DIR = Path(__file__).parent.parent / "data"
SUMMARIES_FILE = DATA_DIR / "summaries.json"
MAX_SUMMARIES = 90  # Keep last 90 days
GACETA_BASE_URL = "https://www.imprentanacional.go.cr"


def scrape_latest_gaceta_url():
    """
    Scrape La Gaceta homepage to find today's PDF link dynamically.
    More reliable than hardcoded URL patterns (based on V1 logic).
    """
    print("🔍 Scraping La Gaceta homepage for latest PDF...")
    try:
        response = requests.get(f"{GACETA_BASE_URL}/gaceta/", timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        anchor = soup.select_one("#ctl00_PdfGacetaDescargarHyperLink")

        if anchor and anchor.get("href"):
            pdf_path = anchor["href"]
            full_url = f"{GACETA_BASE_URL}{pdf_path}" if pdf_path.startswith("/") else pdf_path
            print(f"✅ Found PDF URL: {full_url}")
            return full_url
        else:
            print("❌ Could not find PDF link on homepage")
            return None
    except Exception as e:
        print(f"❌ Failed to scrape homepage: {e}")
        return None


def download_pdf(url):
    """Download PDF from URL, return bytes"""
    print(f"📥 Downloading: {url}")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return BytesIO(response.content)
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to download: {e}")
        return None


def extract_text_from_pdf(pdf_bytes, max_pages=50):
    """Extract text from PDF with page tracking (limit to first 50 pages to save costs)"""
    print("📄 Extracting text from PDF...")
    try:
        reader = pypdf.PdfReader(pdf_bytes)
        total_pages = len(reader.pages)
        pages_to_read = min(max_pages, total_pages)

        # Extract text with page markers for reference
        text_with_pages = ""
        for i in range(pages_to_read):
            page = reader.pages[i]
            page_num = i + 1  # 1-indexed for humans
            text_with_pages += f"\n[PÁGINA {page_num}]\n"
            text_with_pages += page.extract_text() + "\n"

        print(f"✅ Extracted {len(text_with_pages)} characters from {pages_to_read}/{total_pages} pages")
        return text_with_pages
    except Exception as e:
        print(f"❌ Failed to extract text: {e}")
        return None


def summarize_with_gpt4(text, date):
    """Use GPT-4o to create a 5-bullet summary with page references"""
    print("🤖 Generating summary with GPT-4o...")

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Prompt version for tracking and reproducibility
    PROMPT_VERSION = "2.0.0"  # Semver: major.minor.patch

    prompt = f"""Eres un asistente experto en resumir documentos legales de Costa Rica.

A continuación está el texto de La Gaceta Oficial de Costa Rica del {date.strftime('%d de %B, %Y')}.

El texto incluye marcadores de página en formato [PÁGINA N]. DEBES incluir estas referencias en tu resumen.

Tu tarea:
1. Lee el documento completo
2. Identifica los 5 cambios, decisiones o anuncios más importantes
3. Crea un resumen de 5 puntos en español claro y simple
4. Cada punto debe tener un emoji relevante al inicio
5. IMPORTANTE: Para cada punto, incluye las páginas donde aparece la información
6. Identifica 3-5 temas principales (ej: Legal, Fiscal, Salud, Educación, Ambiente)

Formato de respuesta (JSON):
{{
  "summary": "Breve resumen general en 1-2 oraciones",
  "bullets": [
    {{
      "icon": "⚖️",
      "text": "Descripción del cambio legal o decisión",
      "pages": [1, 2]
    }},
    {{
      "icon": "💰",
      "text": "Descripción del cambio fiscal",
      "pages": [5]
    }},
    ...
  ],
  "topics": ["Legal", "Fiscal", "Salud", ...]
}}

IMPORTANTE: El campo "pages" debe ser un array de números de página donde encontraste la información.

Texto de La Gaceta:
{text[:15000]}

Responde SOLO con el JSON, sin texto adicional."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Cost-effective option (~$0.15 per 1M input tokens)
            messages=[
                {"role": "system", "content": "Eres un experto en resumir documentos legales oficiales de Costa Rica."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # Lower temperature for more factual summaries
            max_completion_tokens=1000  # Updated API parameter name
        )

        result = response.choices[0].message.content.strip()

        # Clean markdown code blocks if present
        if result.startswith("```json"):
            result = result[7:]
        if result.startswith("```"):
            result = result[3:]
        if result.endswith("```"):
            result = result[:-3]

        result = result.strip()

        summary_data = json.loads(result)

        # Add metadata for transparency and reproducibility
        summary_data["prompt_version"] = PROMPT_VERSION
        summary_data["model"] = "gpt-5-mini"

        # Track API usage for cost monitoring
        usage = response.usage
        cost_input = (usage.prompt_tokens / 1_000_000) * 0.25  # $0.25 per 1M input tokens
        cost_output = (usage.completion_tokens / 1_000_000) * 2.00  # $2.00 per 1M output tokens
        summary_data["api_cost_usd"] = round(cost_input + cost_output, 4)
        summary_data["tokens"] = {
            "input": usage.prompt_tokens,
            "output": usage.completion_tokens,
            "total": usage.total_tokens
        }

        print(f"✅ Summary generated: {len(summary_data['bullets'])} bullets (prompt v{PROMPT_VERSION})")
        print(f"💰 Cost: ${summary_data['api_cost_usd']:.4f} | Tokens: {usage.total_tokens}")
        return summary_data

    except Exception as e:
        print(f"❌ Failed to generate summary: {e}")
        return None


def load_summaries():
    """Load existing summaries from JSON"""
    if SUMMARIES_FILE.exists():
        with open(SUMMARIES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_summaries(summaries):
    """Save summaries to JSON"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Keep only last 90 days
    if len(summaries) > MAX_SUMMARIES:
        sorted_dates = sorted(summaries.keys(), reverse=True)
        summaries = {date: summaries[date] for date in sorted_dates[:MAX_SUMMARIES]}

    with open(SUMMARIES_FILE, 'w', encoding='utf-8') as f:
        json.dump(summaries, f, ensure_ascii=False, indent=2)

    print(f"💾 Saved summaries to {SUMMARIES_FILE}")


def main():
    """Main scraper function"""
    print("=" * 60)
    print("GacetaChat Daily Scraper - Alpha")
    print("=" * 60)

    today = datetime.now()
    summaries = load_summaries()

    # First, try scraping homepage for latest PDF (most reliable)
    print("\n🌐 Method 1: Scraping homepage for latest PDF...")
    url = scrape_latest_gaceta_url()

    if url:
        pdf_bytes = download_pdf(url)
        if pdf_bytes:
            # Extract date from URL
            # URL formats:
            # - https://www.imprentanacional.go.cr/pub/2025/11/12/COMP_12_11_2025.pdf (DD_MM_YYYY)
            # - Old: .../gaceta/2024/07/15/gaceta_20240715.pdf (YYYYMMDD)
            try:
                import re
                # Try new format: COMP_DD_MM_YYYY.pdf
                match = re.search(r'COMP_(\d{2})_(\d{2})_(\d{4})\.pdf', url)
                if match:
                    day, month, year = match.groups()
                    gazette_date = datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")
                    date_str = gazette_date.strftime("%Y-%m-%d")
                    print(f"📅 Extracted date from filename: {date_str}")
                else:
                    # Try old format: gaceta_YYYYMMDD
                    match = re.search(r'gaceta[_/]?(\d{8})', url)
                    if match:
                        gazette_date = datetime.strptime(match.group(1), "%Y%m%d")
                        date_str = gazette_date.strftime("%Y-%m-%d")
                        print(f"📅 Extracted date from filename: {date_str}")
                    else:
                        # Fallback to today's date
                        date_str = today.strftime("%Y-%m-%d")
                        print(f"⚠️ Could not extract date from URL, using today: {date_str}")
            except Exception as e:
                date_str = today.strftime("%Y-%m-%d")
                print(f"⚠️ Date extraction failed ({e}), using today: {date_str}")

            print(f"📅 Detected date: {date_str}")

            if date_str in summaries:
                print(f"✅ Summary already exists for {date_str}")
            else:
                # Process this PDF
                text = extract_text_from_pdf(pdf_bytes)
                if text and len(text) >= 1000:
                    summary_data = summarize_with_gpt4(text, datetime.strptime(date_str, "%Y-%m-%d"))
                    if summary_data:
                        summary_data["date"] = date_str
                        summary_data["pdf_url"] = url
                        summary_data["generated_at"] = datetime.now().isoformat()
                        summaries[date_str] = summary_data
                        save_summaries(summaries)

                        print(f"\n✅ SUCCESS! Summary for {date_str} saved")
                        print(f"   Summary: {summary_data['summary']}")
                        print(f"   Bullets: {len(summary_data['bullets'])}")
                        print(f"   Topics: {', '.join(summary_data['topics'])}")

                        print("\n" + "=" * 60)
                        print(f"✨ Scraper finished. Total summaries: {len(summaries)}")
                        print("=" * 60)
                        return  # Success!

    # Fallback: Try recent dates with URL pattern (if homepage scraping failed)
    print("\n🔄 Method 2: Trying recent dates with URL pattern...")
    for offset in range(3):
        date = today - timedelta(days=offset)
        date_str = date.strftime("%Y-%m-%d")

        print(f"\n📅 Trying date: {date_str}")

        if date_str in summaries:
            print(f"✅ Summary already exists for {date_str}")
            continue

        # Construct URL from date
        url = f"{GACETA_BASE_URL}/gaceta/{date.year}/{date.month:02d}/{date.day:02d}/gaceta_{date.year}{date.month:02d}{date.day:02d}.pdf"
        pdf_bytes = download_pdf(url)

        if pdf_bytes is None:
            print(f"⏩ Skipping {date_str} - PDF not available")
            continue

        # Extract text
        text = extract_text_from_pdf(pdf_bytes)
        if text is None or len(text) < 1000:
            print(f"⏩ Skipping {date_str} - Text extraction failed or too short")
            continue

        # Generate summary
        summary_data = summarize_with_gpt4(text, date)
        if summary_data is None:
            print(f"❌ Failed to generate summary for {date_str}")
            continue

        # Add metadata
        summary_data["date"] = date_str
        summary_data["pdf_url"] = url
        summary_data["generated_at"] = datetime.now().isoformat()

        # Save to summaries
        summaries[date_str] = summary_data
        save_summaries(summaries)

        print(f"\n✅ SUCCESS! Summary for {date_str} saved")
        print(f"   Summary: {summary_data['summary']}")
        print(f"   Bullets: {len(summary_data['bullets'])}")
        print(f"   Topics: {', '.join(summary_data['topics'])}")

        # Only process one day per run to save costs
        break

    print("\n" + "=" * 60)
    print(f"✨ Scraper finished. Total summaries: {len(summaries)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
