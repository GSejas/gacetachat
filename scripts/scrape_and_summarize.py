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
import PyPDF2
from io import BytesIO
from openai import OpenAI

# Configuration
DATA_DIR = Path(__file__).parent.parent / "data"
SUMMARIES_FILE = DATA_DIR / "summaries.json"
MAX_SUMMARIES = 90  # Keep last 90 days

# La Gaceta URL pattern
# Example: https://www.imprentanacional.go.cr/gaceta/2024/07/15/gaceta_20240715.pdf
GACETA_URL_TEMPLATE = "https://www.imprentanacional.go.cr/gaceta/{year}/{month:02d}/{day:02d}/gaceta_{year}{month:02d}{day:02d}.pdf"


def get_gaceta_url(date):
    """Generate La Gaceta PDF URL for a given date"""
    return GACETA_URL_TEMPLATE.format(
        year=date.year,
        month=date.month,
        day=date.day
    )


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
    """Extract text from PDF (limit to first 50 pages to save costs)"""
    print("📄 Extracting text from PDF...")
    try:
        reader = PyPDF2.PdfReader(pdf_bytes)
        total_pages = len(reader.pages)
        pages_to_read = min(max_pages, total_pages)

        text = ""
        for i in range(pages_to_read):
            page = reader.pages[i]
            text += page.extract_text() + "\n"

        print(f"✅ Extracted {len(text)} characters from {pages_to_read}/{total_pages} pages")
        return text
    except Exception as e:
        print(f"❌ Failed to extract text: {e}")
        return None


def summarize_with_gpt4(text, date):
    """Use GPT-4o to create a 5-bullet summary"""
    print("🤖 Generating summary with GPT-4o...")

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    prompt = f"""Eres un asistente experto en resumir documentos legales de Costa Rica.

A continuación está el texto de La Gaceta Oficial de Costa Rica del {date.strftime('%d de %B, %Y')}.

Tu tarea:
1. Lee el documento completo
2. Identifica los 5 cambios, decisiones o anuncios más importantes
3. Crea un resumen de 5 puntos en español claro y simple
4. Cada punto debe tener un emoji relevante al inicio
5. Identifica 3-5 temas principales (ej: Legal, Fiscal, Salud, Educación, Ambiente)

Formato de respuesta (JSON):
{{
  "summary": "Breve resumen general en 1-2 oraciones",
  "bullets": [
    {{"icon": "⚖️", "text": "Descripción del cambio legal o decisión"}},
    {{"icon": "💰", "text": "Descripción del cambio fiscal"}},
    ...
  ],
  "topics": ["Legal", "Fiscal", "Salud", ...]
}}

Texto de La Gaceta:
{text[:15000]}

Responde SOLO con el JSON, sin texto adicional."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # More cost-effective than gpt-4-turbo
            messages=[
                {"role": "system", "content": "Eres un experto en resumir documentos legales oficiales de Costa Rica."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # Lower temperature for more factual summaries
            max_tokens=1000
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

        print(f"✅ Summary generated: {len(summary_data['bullets'])} bullets")
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

    # Try today's date
    today = datetime.now()
    date = today

    # La Gaceta is sometimes published with 1-2 day delay, so try today and yesterday
    for offset in range(3):
        date = today - timedelta(days=offset)
        date_str = date.strftime("%Y-%m-%d")

        print(f"\n📅 Trying date: {date_str}")

        # Check if we already have this summary
        summaries = load_summaries()
        if date_str in summaries:
            print(f"✅ Summary already exists for {date_str}")
            continue

        # Download PDF
        url = get_gaceta_url(date)
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
