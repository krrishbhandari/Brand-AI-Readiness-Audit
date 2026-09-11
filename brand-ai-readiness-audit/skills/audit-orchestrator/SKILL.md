---
name: audit-orchestrator
description: Master entrypoint skill for the Brand AI-Readiness Audit Marketplace. Accepts a website URL or domain, orchestrates specialized sub-skills (crawl-render-audit, freshness-corroboration, engagement-audit), deduplicates findings, calculates severity metrics, synthesizes proactive improvements, and emits the standardized JSON audit report. Use when diagnosing why a brand is invisible in AI assistants or suffering high bounce rates from referred visitors.
license: MIT
allowed-tools:
  - python
  - bash
  - web_fetch
---

# Audit Orchestrator Skill (Master Entrypoint)

## When to use
Invoke this skill whenever a general AI agent or human auditor needs to run a comprehensive, evidence-backed Brand AI-Readiness Audit on any website URL or domain. This skill is the single designated entrypoint (`entrypoint: true` in `marketplace.json`) for the marketplace.

## Inputs
- `url` *(string, required)*: The target website URL (e.g. `https://example.com`) or bare domain (`example.com`).
- `max_pages` *(integer, optional, default: 20)*: Maximum number of internal pages to crawl during the audit.
- `max_depth` *(integer, optional, default: 2)*: Maximum link traversal depth from the root URL.
- `timeout` *(integer, optional, default: 10)*: Request timeout in seconds per page fetch.
- `user_agent` *(string, optional, default: "BrandAuditBot/1.0 (AI-Readiness-Audit)")*: HTTP User-Agent header.

## Procedure
1. **Input Normalization & Sanity Checks**: Validate the input URL, ensure canonical `https://` protocol, resolve the root hostname, and verify target availability.
2. **Sub-Skill Dispatch & Execution**:
   - Invoke `crawl-render-audit` to inspect `robots.txt` AI crawler permissions (`GPTBot`, `ClaudeBot`, `PerplexityBot`), `/llms.txt` presence, sitemaps, and SSR vs. CSR JavaScript render locks.
   - Invoke `freshness-corroboration` to parse Schema.org JSON-LD, extract entity disambiguation (`sameAs` Wikidata/Crunchbase links), audit citation snippet density, and identify ungrounded claims.
   - Invoke `engagement-audit` to measure above-the-fold value proposition clarity, calculate Flesch-Kincaid readability, evaluate signal-to-noise ratio, and detect trust/conversion friction.
3. **Deduplication & Normalization**:
   - Merge findings across all skills.
   - Remove duplicate or overlapping issues using deterministic hashing (`category + title + location`).
   - Standardize finding identifiers (`DISC-xxx`, `KNOW-xxx`, `ENG-xxx`, `PROACT-xxx`).
4. **Severity Matrix & Impact Scoring**:
   - Categorize severities strictly into `critical`, `high`, `medium`, `low`, or `info`.
   - Calculate the composite `ai_readiness_score` (0-100) using the rubric deduction weights in `references/severity_matrix.md`.
5. **Proactive Strategic Recommendations**:
   - Synthesize beyond-problem proactive recommendations (e.g. drop-in `/llms.txt` template, unified Schema `@graph` tree, atomic quotation formatting).
6. **Schema Validation & Output Generation**:
   - Validate report against `references/audit_schema.json`.
   - Emit the standardized JSON report.

## Output
Emits a structured JSON audit report conforming strictly to the required schema:

```json
{
  "site": "example.com",
  "audited_at": "2026-09-06T00:30:00Z",
  "summary": {
    "total_findings": 4,
    "critical": 1,
    "high": 2,
    "medium": 1,
    "low": 0,
    "ai_readiness_score": 58
  },
  "findings": [
    {
      "id": "DISC-001",
      "title": "AI crawlers blocked in robots.txt",
      "severity": "critical",
      "evidence": "robots.txt explicitly disallows User-Agent: GPTBot, ClaudeBot, and PerplexityBot from /.",
      "suggested_action": {
        "summary": "Update robots.txt to grant allow rules for conversational AI search engines.",
        "priority": "critical"
      }
    }
  ],
  "proactive_recommendations": []
}
```

## References
- Schema Definition: [`references/audit_schema.json`](file:///c:/Users/Krish%20Bhandari/OneDrive/Documents/Adobe_26/skills/audit-orchestrator/references/audit_schema.json)
- Scoring Matrix: [`references/severity_matrix.md`](file:///c:/Users/Krish%20Bhandari/OneDrive/Documents/Adobe_26/skills/audit-orchestrator/references/severity_matrix.md)

## Scripts
- Master Orchestrator: [`scripts/orchestrator.py`](file:///c:/Users/Krish%20Bhandari/OneDrive/Documents/Adobe_26/skills/audit-orchestrator/scripts/orchestrator.py)
