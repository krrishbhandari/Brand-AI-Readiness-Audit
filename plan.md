# Master Plan: Brand AI-Readiness Audit Marketplace (Adobe Round 3)

**Competition**: Adobe University Hackathon 2026 — Round 3 (Development Round)  
**Theme**: *"Speak to Agents: The New Language of Brand Visibility"*  
**Specification Standard**: [`agentskills.io`](https://agentskills.io)  
**Submission Deliverable**: `brand-ai-readiness-audit.zip` (Marketplace Manifest + 4 Skills + README)  
**Validation Benchmark**: 10-Site Empirical Dataset & Princeton GEO Research Framework  

---

## 1. Executive Summary & Research Synthesis

### 1.1. Core Problem & Dual-Sided Audit Mandate
Round 3 challenges us to build an automated, reusable Agent Skill Marketplace that audits any unseen website for two interconnected halves of modern brand visibility:
1. **Off-Site AI Discoverability (AEO / GEO)**: Can AI assistants (ChatGPT Search, Perplexity, Claude, Google Gemini/SGE, Apple Intelligence) find, crawl, read, trust, and quote facts from the brand?
2. **On-Site Human Retention & Conversion**: When AI engines refer visitors to the site, does the landing page orient them within 3 seconds, retain conversational context, deliver high signal-to-noise information, and provide clear next-step conversion pathways?

### 1.2. Key Empirical Insights from Our 10-Site Research
From our empirical field validation across 10 distinct website categories (Wikipedia, GitHub Docs, Stripe Docs, Zapier, Nordstrom, Healthline, Coursera, Prashant Corner, Saraswat Bank, Dot & Key), we established the foundational diagnostic rule:

> **"Target facts matter more than generic page metrics."**
> - **JavaScript present $\neq$ JavaScript dependency**: A modern web application using React/Next.js/Shopify for menus, analytics, and animations is NOT defective if core target facts are present in raw HTML or raw JSON-LD fallback.
> - **Strict 5-Stage Diagnostic Pipeline**:
>   $$\text{Edge Access (WAF/403)} \longrightarrow \text{Crawler Policy (robots.txt)} \longrightarrow \text{Raw HTML Fact Check} \longrightarrow \text{JSON-LD Fallback Check} \longrightarrow \text{Rendered DOM Delta Check}$$
> - **Counterexample Rules Built In**:
>   - *Dot & Key Rule*: High DOM expansion is NOT a failure if product price/offer exists in raw JSON-LD.
>   - *Healthline Rule*: HTML accessibility and AI crawler governance (`robots.txt` AI user-agents) are distinct layers.
>   - *Saraswat Bank Rule*: Rendered text expansion is ignored if key facts (interest rate tables) exist in static HTML tables.
>   - *Nordstrom Rule*: Network WAF/403 challenges must be isolated before diagnosing JavaScript rendering faults.

### 1.3. Princeton GEO & Multi-Vector Scoring Integration (From `geoskills-main` & `skills-main`)
We integrate the research-backed 4-Vector GEO scoring model into our deterministic scoring engine:
$$\text{Composite Score} = 0.20 \times \text{Technical} + 0.35 \times \text{Citability} + 0.20 \times \text{Schema} + 0.25 \times \text{Entity/Brand}$$

With automatic **Business Type Adjustments**:
- **SaaS / Technology**: SSR rendering emphasis, API/doc answer blocks (+10%), HowTo/FAQ schema (+15%).
- **E-Commerce / D2C**: Product/Offer JSON-LD (+20%), statistical pricing/spec density (+15%), review aggregation (+15%).
- **Publisher / Media**: Article/NewsArticle schema (+15%), freshness/authorship dates (+10%), plain-text fact citability (+10%).
- **Local Business / SMB**: LocalBusiness schema (+25%), NAP consistency (+20%), location self-containment (+10%).

---

## 2. Marketplace Architecture & 4-Skill Decomposition

```
brand-ai-readiness-audit/                       <-- Marketplace Root (Submission Zip)
├── marketplace.json                            <-- Contest Manifest (Registers 4 skills + 1 entrypoint)
├── README.md                                   <-- Comprehensive Architecture, Rationale & Usage Guide
├── requirements.txt                            <-- Lightweight dependencies (requests, beautifulsoup4)
├── package_marketplace.py                      <-- Automated packaging tool (creates .zip < 500 KB)
│
├── skills/
│   ├── audit-orchestrator/                     <-- [ENTRYPOINT SKILL]
│   │   ├── SKILL.md                            <-- agentskills.io YAML frontmatter + orchestration procedure
│   │   ├── scripts/
│   │   │   └── orchestrator.py                 <-- Master coordinator, deduplication, scoring & aggregator
│   │   └── references/
│   │       ├── audit_schema.json               <-- Formal Draft-07 JSON Schema validator
│   │       ├── severity_matrix.md              <-- Severity deduction weights & impact rubric
│   │       └── geo_scoring_model.md            <-- Princeton GEO 4-Vector scoring weights & business adjustments
│   │
│   ├── crawl-render-audit/                     <-- [SPECIALIZED SKILL 1: Technical & Rendering]
│   │   ├── SKILL.md                            <-- agentskills.io spec for AI bot crawling & rendering
│   │   ├── scripts/
│   │   │   ├── crawler.py                      <-- Multi-page crawl engine with depth & politeness control
│   │   │   ├── robots.py                       <-- AI Crawler Matrix (GPTBot, ClaudeBot, etc.) + /llms.txt check
│   │   │   ├── structured_data.py              <-- Schema.org JSON-LD & Wikidata sameAs extractor
│   │   │   └── page_analysis.py                <-- CSR render lock detection (SSR vs CSR) & HTML hierarchy
│   │   └── references/
│   │       ├── ai_bot_directory.md             <-- 15+ AI bot user-agents & token budget rules
│   │       ├── llms_txt_spec.md                <-- Standard /llms.txt syntax guide
│   │       └── checks.md                       <-- Catalog of crawlability & rendering checks
│   │
│   ├── freshness-corroboration/                <-- [SPECIALIZED SKILL 2: Citations & Knowledge Graph]
│   │   ├── SKILL.md                            <-- agentskills.io spec for entity identity & citations
│   │   ├── scripts/
│   │   │   └── consistency.py                  <-- Entity consistency, stale dates, atomic quote density
│   │   └── references/
│   │       ├── schema_types_guide.md           <-- Schema.org mapping (Organization, Product, FAQPage)
│   │       ├── citation_heuristics.md          <-- Atomic claim density & quote extractability rules
│   │       └── checks.md                       <-- Catalog of knowledge & freshness checks
│   │
│   └── engagement-audit/                       <-- [SPECIALIZED SKILL 3: Human Retention & UX]
│       ├── SKILL.md                            <-- agentskills.io spec for visitor retention & clarity
│       ├── scripts/
│       │   └── engagement.py                   <-- Above-the-fold clarity, Flesch-Kincaid readability, trust anchors
│       └── references/
│           ├── engagement_rubric.md            <-- Heuristics for orientation, fluff detection & layout
│           ├── trust_signals_guide.md          <-- Authority anchors, contact points & privacy checks
│           └── checks.md                       <-- Catalog of engagement checks
│
└── tests/                                      <-- Automated Verification Test Suite
    ├── run_tests.py                            <-- Universal one-command test runner (zero external dependencies)
    ├── test_basic_checks.py                    <-- URL validation & crawler config tests
    ├── test_finding_normalization.py           <-- Severity normalization & deduplication tests
    ├── test_report_schema.py                   <-- Page 2 JSON schema conformance tests
    ├── test_synthetic_sites.py                 <-- End-to-end tests against mock poor/optimized fixtures
    ├── test_10_site_benchmark.py               <-- Benchmark test against the 10-site validation dataset
    └── mock_data/                              <-- Synthetic HTML fixtures for offline testing
        ├── poor_ai_readiness_fixture.html      <-- Fixture with CSR lock, no title, missing schema
        ├── optimized_brand_fixture.html        <-- Fixture with valid JSON-LD, sameAs Wikidata, clear copy
        ├── ecommerce_fallback_fixture.html     <-- Dot & Key pattern: high CSR but rich JSON-LD fallback
        └── static_table_banking_fixture.html   <-- Saraswat Bank pattern: static interest rates in HTML table
```

---

## 3. Strict Page 2 Audit Report Schema

Every audit output strictly satisfies the mandatory schema defined on **Page 2** of the problem statement:

```json
{
  "site": "example.com",
  "audited_at": "2026-09-20T14:32:00Z",
  "summary": {
    "total_findings": 6,
    "critical": 1,
    "high": 2,
    "medium": 3,
    "low": 0,
    "ai_readiness_score": 68
  },
  "findings": [
    {
      "id": "DISC-001",
      "title": "Conversational AI crawlers blocked in robots.txt",
      "severity": "critical",
      "evidence": "robots.txt explicitly disallows User-Agent: GPTBot, ClaudeBot, and PerplexityBot from /.",
      "suggested_action": {
        "summary": "Update robots.txt to grant allow rules for conversational AI search engines (ChatGPT-User, PerplexityBot).",
        "priority": "critical"
      }
    },
    {
      "id": "KNOW-001",
      "title": "No JSON-LD structured data on product pages",
      "severity": "high",
      "evidence": "Crawled 12 product pages; 0/12 contain schema.org markup.",
      "suggested_action": {
        "summary": "Add Product/Offer JSON-LD to every product page.",
        "priority": "high"
      }
    }
  ],
  "proactive_recommendations": [
    {
      "id": "PROACT-001",
      "title": "Publish machine-readable /llms.txt documentation index",
      "summary": "Deploy a curated /llms.txt at root containing concise Markdown summaries and key URLs to optimize LLM context window ingestion.",
      "priority": "medium",
      "impact": "high"
    }
  ]
}
```

---

## 4. Phase-Wise Implementation Workflow

### Phase 1: Foundation, Spec Alignment & Marketplace Manifest
- Finalize `marketplace.json` registering all 4 skills with `audit-orchestrator` as `entrypoint: true`.
- Update all 4 `SKILL.md` files with valid `agentskills.io` YAML frontmatter, deterministic procedures, and tool definitions.
- Write root `README.md` documenting architecture, skill composition, research grounding, and usage.

### Phase 2: Technical Discoverability & Fact-Aware Rendering Engine (`crawl-render-audit`)
- Implement multi-crawler `robots.txt` parser for 12+ AI bots (`GPTBot`, `ClaudeBot`, `PerplexityBot`, `Google-Extended`, `Bytespider`, `CCBot`).
- Implement `/llms.txt` and `/llms-full.txt` context parser.
- Implement **Fact-Aware JS Dependency Check**: Compare raw HTML vs. raw JSON-LD fallback before diagnosing CSR rendering locks (preventing false positives like Dot & Key).

### Phase 3: Knowledge Graph, Entity Disambiguation & Quotation Engine (`freshness-corroboration`)
- Implement Schema.org JSON-LD parser supporting `@graph` entity trees (`Organization`, `Product`, `Offer`, `FAQPage`, `Article`).
- Implement Wikidata / Knowledge Graph `sameAs` entity disambiguation auditor (preventing LLM brand confusion).
- Implement **Atomic Quotation Density Calculator**: Measure density of declarative factual assertions containing metrics, pricing, and specs.

### Phase 4: Human Engagement, Orientation & Trust Engine (`engagement-audit`)
- Implement above-the-fold value proposition parser (analyzing primary H1 and top 500 characters).
- Implement Flesch-Kincaid Readability & Reading Ease scoring engine.
- Implement essential trust anchor detector (Privacy Policy, Terms of Service, contact support, security certifications).

### Phase 5: Master Orchestrator, Deduplication & Princeton GEO Scoring (`audit-orchestrator`)
- Implement pipeline coordinator executing sub-skills with deterministic timeouts.
- Implement finding deduplication using content hashing (`category + title + location`).
- Implement Princeton GEO 4-Vector scoring model with business-type adjustments.
- Implement proactive strategic recommendations engine (generating `/llms.txt` recipes and unified `@graph` schemas).
- Validate output JSON against Draft-07 JSON Schema.

### Phase 6: Comprehensive Benchmark Suite & Packaging
- Build test suite covering unit tests, schema tests, synthetic fixtures, and 10-site validation rules.
- Build automated packager (`package_marketplace.py`) producing clean `brand-ai-readiness-audit.zip` (< 1 MB, ≤ 50MB ceiling).
- Generate final walkthrough documentation.
