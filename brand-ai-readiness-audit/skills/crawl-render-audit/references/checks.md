# Crawl & Render Audit Reference Check Catalog

This catalog outlines all technical checks executed by the `crawl-render-audit` skill.

---

## 1. AI Bot Crawlability (`robots.txt`)
- **CHECK-ROB-01**: `robots.txt` Availability (`/robots.txt` returns HTTP 200).
- **CHECK-ROB-02**: AI Search Assistants Access (`GPTBot`, `ChatGPT-User`, `PerplexityBot`, `ClaudeBot` must not have blanket `Disallow: /`).
- **CHECK-ROB-03**: Training Bot Restrictions (Flags if `CCBot` or `Google-Extended` are unconfigured).
- **CHECK-ROB-04**: Sitemap Directive (Presence of `Sitemap: https://...` link in `robots.txt`).

---

## 2. Machine-Readable Context (`/llms.txt`)
- **CHECK-LLM-01**: `/llms.txt` Availability at root URL.
- **CHECK-LLM-02**: Markdown Heading & Blockquote Structure.
- **CHECK-LLM-03**: Curated Documentation & Product Deep Links.

---

## 3. Rendering & DOM Parity (SSR vs. CSR)
- **CHECK-RND-01**: Empty Initial Root Node (`<div id="root"></div>`, `<div id="app"></div>` with empty body).
- **CHECK-RND-02**: Raw HTML Text Content Ratio (Checks if raw HTML text length < 200 words despite large bundle scripts).
- **CHECK-RND-03**: Critical Metadata in Raw HTML (`<title>`, `<meta name="description">`, canonical links).
- **CHECK-RND-04**: HTTP Status Codes and Redirect Chains (Max 1 redirect hop).
