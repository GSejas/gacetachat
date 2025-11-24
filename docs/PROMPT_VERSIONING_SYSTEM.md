# Prompt Versioning & Multi-Variant System

## Overview

System for running multiple prompt variants simultaneously with review/approval workflow for testing, experimentation, and content adaptation.

## Use Cases

1. **A/B Testing** - Test new prompt versions before replacing production
2. **Content Adaptation** - Different prompts for Twitter, email, web, etc.
3. **Experimentation** - Try different styles/formats without breaking production
4. **Quality Control** - Review/approve variants before publishing
5. **Historical Tracking** - Audit which prompts were used when

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Daily Scraper Workflow                    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  1. Prompt Registry (configs/prompts.yaml)                   │
│     - prompt_web_v3.0.0 (PRODUCTION, auto-approve)          │
│     - prompt_twitter_v1.0.0 (EXPERIMENTAL, needs review)    │
│     - prompt_email_v1.0.0 (EXPERIMENTAL, needs review)      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  2. Execute All Active Prompts                               │
│     → For each prompt variant:                               │
│       - Generate summary with GPT-4o                         │
│       - Save to data/variants/{date}/{variant_id}.json      │
│       - Mark with status: draft/pending/approved            │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  3. Review/Approval Workflow                                 │
│     → PRODUCTION prompts: auto-approve → summaries.json     │
│     → EXPERIMENTAL prompts: save to variants/ for review    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  4. Manual Review Tool (CLI or Web UI)                       │
│     → Compare variants side-by-side                          │
│     → Approve/reject/edit variants                           │
│     → Promote experimental → production                      │
└─────────────────────────────────────────────────────────────┘
```

## Prompt Registry Format

**File:** `configs/prompts.yaml`

```yaml
prompts:
  # Production prompt (auto-published to summaries.json)
  - id: web_v3.0.0
    name: "Web Bilingual (ES/EN)"
    status: production
    auto_approve: true
    format: bilingual_web
    description: "Standard bilingual summary for web demo"
    cost_per_run: 0.03

  # Experimental Twitter variant
  - id: twitter_v1.0.0
    name: "Twitter Thread (ES only)"
    status: experimental
    auto_approve: false
    format: twitter_thread
    description: "Short bullets optimized for Twitter threads (280 chars)"
    cost_per_run: 0.02
    prompt_template: |
      You are creating Twitter-optimized summaries...
      Each bullet must be ≤280 characters...

  # Experimental email variant
  - id: email_v1.0.0
    name: "Email Newsletter (ES/EN)"
    status: experimental
    auto_approve: false
    format: email_newsletter
    description: "Longer explanations for email subscribers"
    cost_per_run: 0.04
    prompt_template: |
      You are writing for email newsletter subscribers...
      Include context and explanations...

# Approval workflow settings
review:
  require_manual_approval_for:
    - experimental
    - testing

  auto_approve_for:
    - production

  reviewers:
    - email: contact@gacetachat.cr
      notify_on_new_variants: true
```

## Data Storage Structure

```
data/
├── summaries.json              # Production summaries (web demo)
├── variants/                   # All prompt variant outputs
│   └── 2024-07-15/
│       ├── web_v3.0.0.json            # Auto-approved (copied to summaries.json)
│       ├── twitter_v1.0.0.json        # Pending review
│       ├── email_v1.0.0.json          # Pending review
│       └── metadata.json              # Execution metadata
└── approved/                   # Approved variants by format
    ├── twitter/
    │   └── 2024-07-15.json
    └── email/
        └── 2024-07-15.json
```

## Updated Scraper Workflow

**File:** `scripts/scrape_and_summarize_multi.py`

```python
def run_multi_prompt_workflow(date, pdf_text):
    """Execute all active prompts and save variants"""

    # Load prompt registry
    prompts = load_prompt_registry("configs/prompts.yaml")

    results = {}

    for prompt_config in prompts:
        if prompt_config["status"] not in ["production", "experimental"]:
            continue  # Skip disabled/archived prompts

        print(f"🤖 Running prompt: {prompt_config['name']} ({prompt_config['id']})")

        # Generate summary with this prompt variant
        result = execute_prompt(
            prompt_id=prompt_config["id"],
            prompt_template=prompt_config.get("prompt_template", DEFAULT_TEMPLATE),
            pdf_text=pdf_text,
            date=date
        )

        # Add metadata
        result["prompt_metadata"] = {
            "prompt_id": prompt_config["id"],
            "prompt_name": prompt_config["name"],
            "status": prompt_config["status"],
            "generated_at": datetime.now().isoformat(),
            "cost_estimate": prompt_config["cost_per_run"]
        }

        # Save variant
        variant_path = save_variant(date, prompt_config["id"], result)

        # Auto-approve production prompts
        if prompt_config.get("auto_approve", False):
            approve_variant(date, prompt_config["id"], auto=True)
            print(f"✅ Auto-approved: {prompt_config['id']}")
        else:
            print(f"⏳ Pending review: {variant_path}")

        results[prompt_config["id"]] = result

    return results
```

## Review/Approval CLI Tool

**File:** `scripts/review_variants.py`

```python
#!/usr/bin/env python3
"""
Interactive tool to review and approve prompt variants.

Usage:
    python scripts/review_variants.py --date 2024-07-15
    python scripts/review_variants.py --date today
    python scripts/review_variants.py --compare twitter_v1.0.0 twitter_v1.1.0
"""

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

@click.command()
@click.option("--date", default="today", help="Date to review (YYYY-MM-DD or 'today')")
@click.option("--compare", multiple=True, help="Compare specific variants")
def review_variants(date, compare):
    """Review and approve/reject prompt variants"""

    if date == "today":
        date = datetime.now().strftime("%Y-%m-%d")

    # Load pending variants
    variants = load_pending_variants(date)

    if not variants:
        console.print(f"[green]✅ No pending variants for {date}[/green]")
        return

    # Display variants side-by-side
    for variant_id, variant_data in variants.items():
        console.print(Panel(
            format_variant_preview(variant_data),
            title=f"📋 {variant_id}",
            border_style="blue"
        ))

        # Prompt for action
        action = click.prompt(
            "Action?",
            type=click.Choice(["approve", "reject", "edit", "skip"]),
            default="skip"
        )

        if action == "approve":
            approve_variant(date, variant_id)
            console.print(f"[green]✅ Approved {variant_id}[/green]")
        elif action == "reject":
            reason = click.prompt("Rejection reason")
            reject_variant(date, variant_id, reason)
            console.print(f"[red]❌ Rejected {variant_id}[/red]")
        elif action == "edit":
            edited = edit_variant_interactive(variant_data)
            save_variant(date, variant_id, edited)
            approve_variant(date, variant_id)
            console.print(f"[yellow]✏️ Edited and approved {variant_id}[/yellow]")

def approve_variant(date, variant_id, auto=False):
    """Move variant to approved/ and update summaries.json"""

    variant_data = load_variant(date, variant_id)

    # Determine output format
    format_type = variant_data["prompt_metadata"].get("format", "web")

    if format_type == "bilingual_web":
        # Copy to main summaries.json
        update_summaries_json(date, variant_data)
    else:
        # Save to format-specific approved folder
        approved_path = f"data/approved/{format_type}/{date}.json"
        save_json(approved_path, variant_data)

    # Update metadata
    variant_data["approval_metadata"] = {
        "approved_at": datetime.now().isoformat(),
        "approved_by": "auto" if auto else os.environ.get("USER", "manual"),
        "status": "approved"
    }

    save_variant(date, variant_id, variant_data)
```

## Cost Analysis

### Current System (Single Prompt)
- **1 prompt/day** × $0.03/run = **$10.95/year**

### Multi-Prompt System (3 variants)
- **Production (web)**: 1/day × $0.03 = $10.95/year
- **Experimental (twitter)**: 1/day × $0.02 = $7.30/year (only while testing)
- **Experimental (email)**: 1/day × $0.04 = $14.60/year (only while testing)
- **Total during testing**: $32.85/year
- **Total after settling**: $10.95/year (just production)

**Cost Control:**
- Only run experimental prompts when actively testing
- Archive/disable after validation
- Set daily budget limits in code

## Review Workflow Options

### Option 1: CLI Review (Recommended for Alpha)
```bash
# Daily: Review pending variants
python scripts/review_variants.py --date today

# Compare two prompt versions
python scripts/review_variants.py --compare twitter_v1.0.0 twitter_v1.1.0
```

### Option 2: Web Dashboard (Future v2.0)
- Streamlit admin panel
- Side-by-side variant comparison
- One-click approve/reject
- Analytics on prompt performance

### Option 3: Email Review (Simple)
- Email daily digest of pending variants
- Reply with "approve twitter_v1.0.0" to approve
- GitHub Issues integration for discussion

## Migration Path

### Phase 1: Add Registry (Week 1)
1. Create `configs/prompts.yaml`
2. Register current prompt as `web_v3.0.0` (production, auto-approve)
3. Update scraper to read registry
4. No behavior change - just infrastructure

### Phase 2: Add Variants (Week 2)
1. Create Twitter prompt variant
2. Run both prompts daily
3. Store in `data/variants/`
4. Manual review via file inspection

### Phase 3: Review Tool (Week 3)
1. Build CLI review tool
2. Implement approve/reject workflow
3. Add comparison features

### Phase 4: Automation (Week 4)
1. Email notifications for pending reviews
2. Auto-publish approved variants
3. Analytics dashboard

## Example: Twitter Prompt Variant

```yaml
- id: twitter_v1.0.0
  name: "Twitter Thread"
  status: experimental
  format: twitter_thread
  auto_approve: false
  prompt_template: |
    You are creating a Twitter thread about La Gaceta Oficial de Costa Rica.

    Rules:
    - First tweet: Hook (max 280 chars)
    - 5 tweets: Key points (max 280 chars each)
    - Each tweet must be standalone
    - Use emojis strategically
    - Include hashtags: #CostaRica #LaGaceta

    Output JSON:
    {
      "thread": [
        {"tweet_num": 1, "text": "🇨🇷 La Gaceta de hoy trae..."},
        {"tweet_num": 2, "text": "⚖️ ..."},
        ...
      ]
    }
```

## Security & Quality Controls

1. **Cost Limits**
   ```python
   MAX_DAILY_COST = 0.50  # $0.50/day
   if sum(variant.cost for variant in variants) > MAX_DAILY_COST:
       send_alert("Daily cost limit exceeded")
   ```

2. **Quality Checks**
   ```python
   def validate_variant(variant):
       """Basic quality checks before saving"""
       assert len(variant["bullets"]) == 5
       assert all(len(b["text"]) > 10 for b in variant["bullets"])
       assert "summary" in variant
   ```

3. **Rollback**
   ```python
   # If bad variant approved, rollback
   python scripts/review_variants.py --rollback twitter_v1.0.0 --date 2024-07-15
   ```

## Recommendations

**For GacetaChat Alpha:**

1. **Start Simple** - Implement prompt registry first (Phase 1)
2. **Add Twitter variant** - Test content adaptation (Phase 2)
3. **Manual review** - File-based review for first 2 weeks
4. **Build CLI tool** - Once workflow is validated (Phase 3)

**Benefits:**
- ✅ Test new prompts without breaking production
- ✅ A/B test for quality improvements
- ✅ Adapt content for different channels (Twitter, email, WhatsApp)
- ✅ Historical tracking of what prompts were used
- ✅ Quality control before publishing

**Risks:**
- ⚠️ Higher costs during testing ($33/year vs $11/year)
- ⚠️ More complexity to maintain
- ⚠️ Need discipline to review variants daily

## Next Steps

Want me to implement:

1. **Quick start** - Just the prompt registry + variants storage?
2. **Full system** - Registry + variants + review CLI?
3. **Twitter-specific** - Just add Twitter prompt variant to test?

Let me know which approach fits your timeline!
