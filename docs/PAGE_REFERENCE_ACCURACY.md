# Page Reference Accuracy Analysis

## Current Problem

**Critical Issue:** We're only sending the first 15,000 characters (~3-5 pages) to GPT, but asking it to summarize the entire document (50-200 pages) with accurate page references.

### Evidence

```python
# scripts/scrape_and_summarize.py:216
prompt = f"""...
La Gaceta text:
{text[:15000]}  # ⚠️ TRUNCATED TO 15K CHARS
"""
```

**La Gaceta Stats:**
- Typical size: 50-200 pages
- Characters per page: ~3,000-5,000
- First 15k chars: ~3-5 pages only
- **Coverage: <10% of document**

### What This Means

1. **GPT only sees pages 1-5** - The bulk of the document (pages 6-200) is never analyzed
2. **Page references are guesses** - GPT infers pages from limited context
3. **Important items missed** - Major decisions on page 50+ never surface
4. **Hallucination risk** - GPT may cite pages it never read

### Verification

Looking at actual data (`data/summaries.json`):

```json
{
  "2025-11-13": {
    "bullets": [
      {"text": "...", "pages": [2]},   // ✅ Within first 15k
      {"text": "...", "pages": [3]},   // ✅ Within first 15k
      {"text": "...", "pages": [4]},   // ⚠️ Likely within 15k
      {"text": "...", "pages": [3]},   // ✅ Within first 15k
      {"text": "...", "pages": [3]}    // ✅ Within first 15k
    ]
  }
}
```

**Observation:** All page references are pages 2-4, which aligns with the 15k character limit. This suggests:
- ✅ Page references are accurate **for the content GPT actually saw**
- ❌ But we're missing 95% of the document
- ❌ Page 50+ content is completely ignored

##root Cause

**Trade-off made in v1 prototype:**
- **Goal:** Keep costs low (<$5/day)
- **Decision:** Truncate to 15k chars to fit within GPT context window cheaply
- **Consequence:** Analyzing only first few pages

### Cost Constraint

**GPT-4o-mini Pricing:**
- Input: $0.25 per 1M tokens
- Output: $2.00 per 1M tokens

**Full document analysis:**
- 200 pages × 3,500 chars/page = 700,000 chars
- ~175,000 tokens input
- Cost: $0.04/day × 365 = **$14.60/year**

**Current truncated analysis:**
- 15,000 chars = ~3,750 tokens
- Cost: $0.001/day × 365 = **$0.36/year**

**Savings by truncating: $14.24/year**

## Solutions

### Option 1: Send Full Document (Simple, Accurate)

**Approach:**
```python
# Remove truncation
prompt = f"""...
La Gaceta text:
{text}  # Full document, no truncation
"""
```

**Pros:**
- ✅ Accurate page references
- ✅ Complete coverage
- ✅ Simple implementation

**Cons:**
- ❌ Higher cost: +$14/year
- ❌ May hit context limits (200k tokens for GPT-4o-mini)
- ❌ Slower processing

**Cost Analysis:**
- Current: $0.36/year
- Full doc: $14.60/year
- **Increase: +$14.24/year** (still cheap!)

**Recommendation:** ✅ **Do this.** $14/year is negligible for accurate analysis.

---

### Option 2: Map-Reduce Summarization (Complex, Scalable)

**Approach:**
1. **Chunk** document into 20-page segments
2. **Map:** Summarize each chunk independently
3. **Reduce:** Combine chunk summaries into final 5 bullets
4. **Track** page references through the pipeline

```python
def analyze_full_document_map_reduce(text):
    # Split into chunks
    chunks = chunk_document(text, pages_per_chunk=20)

    # Map: Summarize each chunk
    chunk_summaries = []
    for i, chunk in enumerate(chunks):
        summary = summarize_chunk(chunk, chunk_id=i)
        chunk_summaries.append(summary)

    # Reduce: Combine into top 5
    final_summary = reduce_summaries(chunk_summaries, top_k=5)

    return final_summary
```

**Pros:**
- ✅ Handles documents of any size
- ✅ Accurate page references (tracked through chunks)
- ✅ Parallelizable (faster)

**Cons:**
- ❌ Complex implementation
- ❌ Higher cost: 2x API calls (map + reduce)
- ❌ Risk of missing cross-chunk context

**Cost Analysis:**
- Map phase: 10 chunks × $0.01 = $0.10/day
- Reduce phase: $0.01/day
- **Total: $40/year** (3x more than full-doc)

---

### Option 3: Embedding + RAG (Advanced, Overkill)

**Approach:**
1. **Embed** all pages using text-embedding-3-small
2. **Index** embeddings in vector DB (Chroma, FAISS)
3. **Retrieve** top-K relevant sections per topic
4. **Summarize** only relevant sections

**Pros:**
- ✅ Extremely accurate page references
- ✅ Can answer specific queries (future feature)
- ✅ Reusable embeddings for search

**Cons:**
- ❌ Very complex infrastructure
- ❌ Higher costs (embeddings + storage)
- ❌ Overkill for daily summaries

**Cost Analysis:**
- Embeddings: 200 pages × $0.0001 = $0.02/day = $7.30/year
- Summarization: $0.01/day = $3.65/year
- **Total: ~$11/year**

---

### Option 4: Smart Chunking with Importance Scoring (Hybrid)

**Approach:**
1. **Scan** full document to identify section headers
2. **Score** each section by importance (title keywords, length)
3. **Select** top 50% of sections
4. **Summarize** selected sections only

**Pros:**
- ✅ Better than truncation
- ✅ Lower cost than full-doc
- ✅ Focuses on important content

**Cons:**
- ❌ May miss important content in "unimportant" sections
- ❌ Complex heuristics needed

**Cost Analysis:**
- ~50% of full document
- **~$7/year**

---

## Recommendation: Option 1 (Send Full Document)

**Rationale:**
1. **Cost is negligible** - $14/year is 0.05% of a $30k grant budget
2. **Simplest implementation** - Remove truncation, done
3. **Accurate page references** - No guessing or hallucination
4. **Complete coverage** - Don't miss page 150 policy changes

### Implementation

```python
def summarize_with_gpt4(text, date):
    """Use GPT-4o to create bilingual summary with accurate page references"""

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Calculate document stats
    estimated_tokens = len(text) // 4
    print(f"📊 Document size: {len(text):,} chars (~{estimated_tokens:,} tokens)")

    # Check context window (GPT-4o-mini supports 128k tokens)
    if estimated_tokens > 120000:
        print("⚠️ Document exceeds 120k tokens, will be truncated")
        # Fall back to map-reduce or chunking
        return summarize_with_chunking(text, date)

    prompt = f"""You are an expert at summarizing Costa Rican legal documents.

Below is the FULL text from La Gaceta Oficial de Costa Rica from {date.strftime('%B %d, %Y')}.

The text includes page markers in the format [PÁGINA N]. You MUST include these page references.

IMPORTANT: Read the ENTIRE document. Do not focus only on the first few pages.

Your task:
1. Read the FULL document (all pages)
2. Identify the 5 most important items across ALL pages
3. For each item, include accurate page numbers

La Gaceta text (FULL DOCUMENT):
{text}  # ✅ No truncation

Respond ONLY with JSON..."""

    # ... rest of implementation
```

### Migration Steps

1. **Update `summarize_with_gpt4()` function** - Remove `[:15000]` truncation
2. **Add context window check** - Handle documents >120k tokens
3. **Test with recent Gaceta** - Verify page references span full document
4. **Monitor costs** - Should increase from $0.001/day to ~$0.04/day
5. **Update documentation** - Note improved accuracy

### Expected Outcomes

**Before (Truncated):**
```json
{
  "bullets": [
    {"text": "Item 1", "pages": [2]},    // ✅ Accurate
    {"text": "Item 2", "pages": [3]},    // ✅ Accurate
    {"text": "Item 3", "pages": [4]},    // ✅ Accurate
    {"text": "Item 4", "pages": [3]},    // ✅ Accurate
    {"text": "Item 5", "pages": [2]}     // ✅ Accurate
  ]
}
// ❌ But missing pages 5-200!
```

**After (Full Document):**
```json
{
  "bullets": [
    {"text": "Major policy change", "pages": [15, 16]},   // ✅ Now visible
    {"text": "New regulation", "pages": [45]},            // ✅ Now visible
    {"text": "Budget allocation", "pages": [78, 79]},     // ✅ Now visible
    {"text": "Environmental decree", "pages": [102]},     // ✅ Now visible
    {"text": "Labor law update", "pages": [134]}          // ✅ Now visible
  ]
}
// ✅ Full document coverage!
```

## Verification Strategy

### Post-Implementation Testing

1. **Manual spot-check** - Download PDF, verify page references match content
2. **Statistical analysis** - Page distribution should be ~uniform across document
3. **Confidence scoring** - Ask GPT to rate confidence in page references (1-10)
4. **Human review** - Sample 10 summaries/month, verify accuracy

### Automated Quality Checks

```python
def verify_page_references(summary, pdf_text):
    """Verify that page references are accurate"""

    for bullet in summary["bullets"]:
        text_snippet = bullet["text"]
        claimed_pages = bullet["pages"]

        # Extract text from claimed pages
        page_texts = extract_pages(pdf_text, claimed_pages)

        # Check if bullet content appears on claimed pages
        found = any(fuzzy_match(text_snippet, page) for page in page_texts)

        if not found:
            print(f"⚠️ Page reference mismatch: '{text_snippet}' not found on pages {claimed_pages}")
            return False

    return True
```

## Cost-Benefit Analysis

### Current System (Truncated)
- **Coverage:** ~5% of document
- **Page accuracy:** High (for pages seen)
- **Completeness:** Low (missing 95%)
- **Cost:** $0.36/year
- **Grant risk:** High (incomplete analysis)

### Proposed System (Full Document)
- **Coverage:** 100% of document
- **Page accuracy:** High
- **Completeness:** High
- **Cost:** $14.60/year
- **Grant risk:** Low (professional quality)

**ROI:** Spending +$14/year to properly analyze a critical government document is a no-brainer for a $30k grant-funded project.

## Next Steps

1. **Implement Option 1** (remove truncation)
2. **Test with 3 recent Gacetas**
3. **Manually verify page references**
4. **Monitor API costs for 1 week**
5. **If costs acceptable, deploy to production**

**Timeline:** 2 hours to implement + 1 week to validate

**Decision:** Recommend implementing immediately. The current truncation is a quality issue that undermines the entire project's credibility.
