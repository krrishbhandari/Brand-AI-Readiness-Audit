---
name: crawl-render-audit
description: Audits website crawler accessibility and rendering parity for conversational AI assistants and search bots. Inspects robots.txt for AI-specific crawler permissions (GPTBot, ClaudeBot, PerplexityBot), detects the presence of /llms.txt context files, verifies XML sitemaps, and diagnoses client-side JavaScript rendering locks where critical text is missing from raw server HTML. Use when determining why a site cannot be crawled, indexed, or read by AI agents.
license: MIT
allowed-tools:
  - python
  - bash
  - web_fetch
---

# Crawl & Render Audit Skill

## When to use
Use this skill when auditing a website's foundational infrastructure for AI crawler accessibility, robots.txt bot rules, `/llms.txt` presence, and JavaScript rendering reliance (SSR vs. CSR gaps).

## Inputs
- `url` *(string, required)*: The target website URL or domain.
- `robots_txt_content` *(string, optional)*: Raw content of robots.txt for offline testing.
- `raw_html` *(string, optional)*: Raw HTML string for offline DOM rendering checks.
- `user_agents` *(list of strings, optional)*: List of AI bot user-agents to test against robots rules.

## Procedure
1. **Fetch & Parse `robots.txt`**:
   - Query `/robots.txt` at the target root.
   - Evaluate rules for AI user-agents: `GPTBot`, `ChatGPT-User`, `ClaudeBot`, `Claude-Web`, `PerplexityBot`, `Google-Extended`, `Bytespider`, `CCBot`.
   - Flag any blanket `Disallow: /` on conversational search bots as **`critical`**.
   - Check for `Sitemap:` directive.
2. **Audit `/llms.txt` Context File**:
   - Query `/.well-known/llms.txt` and `/llms.txt`.
   - Validate format: H1 title, summary blockquote, and curated section links.
   - Flag missing `/llms.txt` as a **`medium`** proactive improvement.
3. **Crawl & Link Graph Analysis**:
   - Discover internal links and verify crawlable URL paths.
   - Identify broken links, 4xx/5xx status codes, and non-canonical redirects.
4. **Rendering Parity (SSR vs. CSR)**:
   - Inspect raw server HTML for empty root containers (`#root`, `#app`, `#__next`).
   - Compare textual substance in initial HTML vs. heavy client script tags.
   - Flag pure client-side rendering where core value propositions or pricing are absent from server response as **`high`**.

## Output
Emits a list of normalized findings:

```json
[
  {
    "id": "DISC-001",
    "title": "Conversational AI crawlers blocked in robots.txt",
    "severity": "critical",
    "category": "robots",
    "skill": "crawl-render-audit",
    "location": "/robots.txt",
    "evidence": "Disallow: / is active for GPTBot and PerplexityBot, making site uncitable in AI search.",
    "suggested_action": {
      "summary": "Add explicit Allow: / rules for User-agent: GPTBot and User-agent: PerplexityBot.",
      "priority": "critical"
    }
  }
]
```

## References
- AI Bot Catalog: [`references/ai_bot_directory.md`](file:///c:/Users/Krish%20Bhandari/OneDrive/Documents/Adobe_26/skills/crawl-render-audit/references/ai_bot_directory.md)
- llms.txt Specification: [`references/llms_txt_spec.md`](file:///c:/Users/Krish%20Bhandari/OneDrive/Documents/Adobe_26/skills/crawl-render-audit/references/llms_txt_spec.md)
- Check Catalog: [`references/checks.md`](file:///c:/Users/Krish%20Bhandari/OneDrive/Documents/Adobe_26/skills/crawl-render-audit/references/checks.md)

## Scripts
- Crawl & Render Engine: [`scripts/crawler.py`](file:///c:/Users/Krish%20Bhandari/OneDrive/Documents/Adobe_26/skills/crawl-render-audit/scripts/crawler.py)
- Robots.txt Analyzer: [`scripts/robots.py`](file:///c:/Users/Krish%20Bhandari/OneDrive/Documents/Adobe_26/skills/crawl-render-audit/scripts/robots.py)
- Page Analyzer: [`scripts/page_analysis.py`](file:///c:/Users/Krish%20Bhandari/OneDrive/Documents/Adobe_26/skills/crawl-render-audit/scripts/page_analysis.py)
