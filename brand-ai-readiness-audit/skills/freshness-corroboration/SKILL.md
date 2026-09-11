---
name: freshness-corroboration
description: Audits semantic structured data, knowledge graph grounding, entity disambiguation, and citation extractability for AI search engines. Extracts Schema.org JSON-LD, Microdata, and OpenGraph tags, detects missing sameAs links (Wikidata, Crunchbase) that cause LLM hallucinations and entity collision, and scores machine quotation readiness across key brand claims. Use when diagnosing why AI assistants misrepresent brand facts or fail to quote sources.
license: MIT
allowed-tools:
  - python
  - bash
  - web_fetch
---

# Freshness & Corroboration Audit Skill (Knowledge & Citations)

## When to use
Use this skill when auditing a website for semantic structured data (JSON-LD), entity disambiguation, Knowledge Graph anchoring (`sameAs` links), factual freshness, and machine citation extractability.

## Inputs
- `url` *(string, required)*: The target website URL or domain.
- `crawled_pages` *(list of objects, optional)*: List of crawled page dictionaries containing HTML, URLs, and headers.

## Procedure
1. **Schema.org Structured Data Extraction**:
   - Extract and validate all `<script type="application/ld+json">`, Microdata, and RDFa elements across crawled pages.
   - Verify presence of critical entity types: `Organization`, `Product`, `Offer`, `FAQPage`, `Article`, `BreadcrumbList`.
   - Flag pages missing structured data as **`high`** severity.
2. **Entity Disambiguation & `sameAs` Knowledge Graph Anchoring**:
   - Inspect `Organization` schema for `sameAs` array linking to Wikidata (`wikidata.org/wiki/Q...`), Wikipedia, Crunchbase, and verified social profiles.
   - Detect entity ambiguity where common brand names risk LLM hallucination or mistaken identity.
   - Flag missing `sameAs` entity links as **`high`** severity.
3. **Citation Readiness & Atomic Claim Density**:
   - Compute atomic quote density across paragraphs (declarative subject-verb-object factual assertions).
   - Detect critical data locked inside non-text elements (raster images without alt text, canvas widgets, untranscribed PDFs).
   - Flag ungrounded or unverifiable claims.
4. **OpenGraph & Social Meta Verification**:
   - Validate `og:title`, `og:description`, `og:image`, `og:url`, and `twitter:card`.

## Output
Emits a list of normalized findings:

```json
[
  {
    "id": "KNOW-001",
    "title": "Missing Schema.org JSON-LD structured data",
    "severity": "high",
    "category": "structured_data",
    "skill": "freshness-corroboration",
    "location": "https://example.com/pricing",
    "evidence": "Pricing page contains 0 JSON-LD or Microdata blocks, preventing AI assistants from extracting verified tiers.",
    "suggested_action": {
      "summary": "Inject Product and Offer JSON-LD schema with currency, price, and availability properties.",
      "priority": "high"
    }
  },
  {
    "id": "KNOW-002",
    "title": "No Wikidata or Knowledge Graph entity disambiguation (sameAs)",
    "severity": "high",
    "category": "identity",
    "skill": "freshness-corroboration",
    "location": "https://example.com",
    "evidence": "Organization schema lacks sameAs properties linking to Wikidata (QID), risking LLM entity confusion.",
    "suggested_action": {
      "summary": "Add sameAs array containing Wikidata, Crunchbase, and LinkedIn URLs to Organization JSON-LD.",
      "priority": "high"
    }
  }
]
```

## References
- Schema Types Guide: [`references/schema_types_guide.md`](file:///c:/Users/Krish%20Bhandari/OneDrive/Documents/Adobe_26/skills/freshness-corroboration/references/schema_types_guide.md)
- Citation Heuristics: [`references/citation_heuristics.md`](file:///c:/Users/Krish%20Bhandari/OneDrive/Documents/Adobe_26/skills/freshness-corroboration/references/citation_heuristics.md)
- Check Catalog: [`references/checks.md`](file:///c:/Users/Krish%20Bhandari/OneDrive/Documents/Adobe_26/skills/freshness-corroboration/references/checks.md)

## Scripts
- Consistency & Knowledge Engine: [`scripts/consistency.py`](file:///c:/Users/Krish%20Bhandari/OneDrive/Documents/Adobe_26/skills/freshness-corroboration/scripts/consistency.py)
