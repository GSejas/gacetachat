# Multi-Language Support Strategy

## Overview

GacetaChat targets Spanish-speaking Costa Ricans first, but multi-language support increases impact and accessibility for:
- International researchers
- Foreign investors
- Regional partners (Central America)
- English-speaking Costa Ricans

## Recommended Architecture: Hybrid Approach

### Phase 1: Spanish Only (Current - Alpha)
- All summaries in Spanish
- Source PDFs are Spanish
- Target audience: Costa Rican NGOs, journalists, citizens

### Phase 2: Add English (Beta - 3 months)
- Generate English summaries during scraping
- Use GPT-4 to translate during AI generation
- Minimal cost increase (~30% more tokens)

### Phase 3: On-Demand Translation (6 months)
- Portuguese, French, other languages
- Translate from Spanish on first request
- Cache translations for future users

## Implementation Details

### Scraper Changes (Phase 2)

**Current prompt:**
```python
prompt = f"""Eres un asistente experto en resumir documentos legales de Costa Rica.
...
Responde en español...
"""
```

**Multi-language prompt:**
```python
prompt = f"""You are an expert at summarizing Costa Rican legal documents.

Generate summaries in both Spanish and English.

Input: La Gaceta text in Spanish
Output: JSON with both languages

{{
  "es": {{
    "summary": "Resumen en español...",
    "bullets": [...]
  }},
  "en": {{
    "summary": "Summary in English...",
    "bullets": [...]
  }}
}}
"""
```

**Cost impact:**
- Current: ~4,500 tokens/day
- With English: ~6,000 tokens/day (+33%)
- Annual cost increase: $0.60/year ($2.00 → $2.60)

### Demo Changes

**Add language selector:**
```python
# demo_simple.py
import streamlit as st

# Language selector in sidebar
lang = st.sidebar.selectbox(
    "🌐 Idioma / Language",
    options=["es", "en"],
    format_func=lambda x: {"es": "🇨🇷 Español", "en": "🇺🇸 English"}[x]
)

# Display summary in selected language
if lang in day_data:
    summary = day_data[lang]
else:
    summary = day_data["es"]  # Fallback to Spanish
```

**UI Text Translation:**
```python
# translations.py
TRANSLATIONS = {
    "es": {
        "title": "GacetaChat - Resumen Diario",
        "summary": "Resumen",
        "key_points": "Puntos Clave",
        "topics": "Temas"
    },
    "en": {
        "title": "GacetaChat - Daily Summary",
        "summary": "Summary",
        "key_points": "Key Points",
        "topics": "Topics"
    }
}

def t(key, lang="es"):
    return TRANSLATIONS[lang].get(key, TRANSLATIONS["es"][key])
```

### Data Structure

**Current (Spanish only):**
```json
{
  "2025-11-12": {
    "summary": "La Gaceta presenta...",
    "bullets": [...],
    "topics": ["Legal", "Salud"]
  }
}
```

**Phase 2 (Spanish + English):**
```json
{
  "2025-11-12": {
    "es": {
      "summary": "La Gaceta presenta...",
      "bullets": [...],
      "topics": ["Legal", "Salud"]
    },
    "en": {
      "summary": "The Official Gazette presents...",
      "bullets": [...],
      "topics": ["Legal", "Health"]
    },
    "header_image": "header_images/2025-11-12.jpg",
    "pdf_url": "...",
    "generated_at": "..."
  }
}
```

**Phase 3 (On-demand translation):**
```json
{
  "2025-11-12": {
    "es": {...},
    "en": {...},
    "translations": {
      "pt": {...},  // Cached translation
      "fr": {...}   // Cached translation
    }
  }
}
```

## Translation Quality

### Option A: GPT-4 Translation (Recommended)
- Use same model for consistency
- Prompt: "Translate this summary while preserving legal terminology"
- Cost: ~$0.001 per translation
- Quality: Excellent for legal/formal text

### Option B: Dedicated Translation API
- DeepL: $5-25/month
- Google Translate API: $20/million characters
- Quality: Good, but may miss legal nuances

**Recommendation:** Stick with GPT for translations (consistency + quality).

## User Language Detection

### Method 1: Browser Locale (Automatic)
```python
# Streamlit detects browser language
import streamlit as st

# Not directly supported in Streamlit, but can use JavaScript
st.components.v1.html("""
<script>
const lang = navigator.language || navigator.userLanguage;
window.parent.postMessage({type: 'language', value: lang.split('-')[0]}, '*');
</script>
""")
```

### Method 2: Manual Selector (Recommended for MVP)
```python
# Simple, reliable, gives user control
lang = st.sidebar.selectbox("🌐 Language", ["es", "en"])
```

### Method 3: URL Parameter
```
https://gacetachat.app/?lang=en
https://gacetachat.app/?lang=es
```

## SEO Considerations

For multi-language support, consider:
- Separate URLs per language: `/es/`, `/en/`
- `hreflang` tags for Google
- Translated meta descriptions

Example:
```html
<link rel="alternate" hreflang="es" href="https://gacetachat.app/es/" />
<link rel="alternate" hreflang="en" href="https://gacetachat.app/en/" />
```

## Migration Path

### Phase 1 → Phase 2 (Add English)

**Step 1: Update scraper**
```python
# Modify summarize_with_gpt4() to request both languages
# Update JSON structure to {"es": {...}, "en": {...}}
```

**Step 2: Migrate existing data**
```python
# Migration script
for date, summary in summaries.items():
    if "es" not in summary:  # Old format
        summaries[date] = {
            "es": summary,
            "en": None  # Will be generated later
        }
```

**Step 3: Backfill English**
```python
# Optional: Generate English for past 90 days
for date, data in summaries.items():
    if data["en"] is None:
        data["en"] = translate_summary(data["es"], "en")
```

**Step 4: Update demo**
```python
# Add language selector
# Update display logic
```

### Phase 2 → Phase 3 (On-demand translation)

**Add translation caching:**
```python
def get_translation(summary_es, target_lang):
    # Check cache first
    cache_key = f"{date}_{target_lang}"
    if cache_key in translations:
        return translations[cache_key]

    # Generate translation
    translation = translate_with_gpt(summary_es, target_lang)

    # Save to cache
    translations[cache_key] = translation
    return translation
```

## Cost Analysis

### Current (Spanish only)
- **Daily:** ~$0.006 (4,500 tokens × $0.00125/1k)
- **Annual:** $2.19

### Phase 2 (Spanish + English)
- **Daily:** ~$0.008 (6,000 tokens × $0.00125/1k)
- **Annual:** $2.92
- **Increase:** +33% or $0.73/year

### Phase 3 (+ 3 on-demand languages)
- **Daily:** $0.008 (English pre-generated)
- **On-demand:** $0.001 per translation per language
- **Annual (assuming 10 requests/day):** $2.92 + $3.65 = $6.57
- **Still incredibly cheap!**

## Target Languages (Priority Order)

1. **Spanish (es)** - Primary, source of truth
2. **English (en)** - International access, researchers, investors
3. **Portuguese (pt)** - Regional (Brazil, Portugal)
4. **French (fr)** - International organizations, diplomats
5. **Mandarin (zh)** - Investors, trade relations

## Technical Requirements

### Scraper
- Modify `summarize_with_gpt4()` to request multiple languages
- Update JSON structure
- Add language field to metadata

### Demo
- Add language selector (sidebar)
- Load appropriate language
- Translate UI elements
- Handle missing translations (fallback to Spanish)

### API (Future)
```
GET /api/summaries/2025-11-12?lang=en
GET /api/summaries/2025-11-12?lang=es
GET /api/summaries/latest?lang=pt
```

## Accessibility Benefits

- **Hearing impaired:** Can read in native language
- **Non-Spanish speakers:** Access to Costa Rican government info
- **Researchers:** English abstracts for academic work
- **International NGOs:** Monitor Costa Rica in their language

## Grant Opportunities

Multi-language support strengthens applications:
- **Mozilla Foundation:** Accessibility focus
- **Google.org:** Global impact
- **OpenAI:** AI for good (translation democratizes access)

## Implementation Timeline

### Phase 2 (English) - 1 week
- Day 1-2: Update scraper prompt
- Day 3-4: Migrate existing data
- Day 5: Update demo UI
- Day 6: Testing
- Day 7: Deploy

### Phase 3 (On-demand) - 2 weeks
- Week 1: Build translation cache system
- Week 2: Add UI for language selection, testing

## Code Example: Minimal Implementation

**scraper update:**
```python
# scripts/scrape_and_summarize.py
prompt = f"""Generate summaries in both Spanish and English...

{{
  "es": {{...}},
  "en": {{...}}
}}
"""

response = client.chat.completions.create(...)
summary_data = json.loads(response.choices[0].message.content)

# summary_data now has both "es" and "en" keys
```

**demo update:**
```python
# demo_simple.py
lang = st.sidebar.selectbox("Language", ["es", "en"])

if day_data:
    # Get summary in selected language (fallback to Spanish)
    summary = day_data.get(lang, day_data.get("es"))

    st.write(summary["summary"])
    for bullet in summary["bullets"]:
        st.markdown(f"{bullet['icon']} {bullet['text']}")
```

That's it! Minimal changes, big impact.

## Recommendation

**For Alpha:** Keep Spanish only (current)
**For Beta (after funding):** Add English during scraping
**For Production:** On-demand translation for other languages

**Cost impact:** Negligible ($0.73/year for English)
**Development time:** 1 week for English support
**Impact:** Significantly broadens audience and grant opportunities

---

**Status:** Planned for Phase 2 (Beta)
**Priority:** Medium (after MVP launch)
**Cost:** ~$3-7/year for 5 languages
**Complexity:** Low (GPT handles translation)
