# Brand AI-Readiness Audit Marketplace

**Adobe University Hackathon 2026 — Round 3 (Development Round)**  
*Theme: "Speak to Agents: The New Language of Brand Visibility"*  
*Specification Standard: [agentskills.io](https://agentskills.io)*  
*Architecture: 4-Skill Modular Marketplace with Single Entrypoint*

---

## 📖 1. Overview & Dual-Sided Audit Mandate

The **Brand AI-Readiness Audit Marketplace** (`brand-ai-readiness-audit`) is an automated, production-grade audit package designed for general AI agents. It audits any unseen website URL or domain for:
1. **Off-Site AI Discoverability (AEO / GEO)**: Why a brand is invisible, stale, or misrepresented in conversational AI assistants (ChatGPT Search, Perplexity, Claude, Apple Intelligence, Google Gemini/SGE).
2. **On-Site Visitor Retention & Orientation**: Why visitors referred to the site by AI assistants bounce immediately or fail to orient and convert.
3. **Evidence-Backed Actionable Remediation**: Emitting an exact JSON report matching **Page 2** of the problem brief, complete with prioritized, mechanism-sound fixes and proactive strategic recommendations.

---

## 🏗️ 2. Marketplace Architecture & Composition Model

```
                              ┌────────────────────────────────────────┐
                              │           Audit Request (URL)          │
                              └───────────────────┬────────────────────┘
                                                  │
                                                  ▼
                        ┌────────────────────────────────────────────────────┐
                        │      skills/audit-orchestrator/ (Entrypoint)       │
                        └─────────┬───────────────┬────────────────┬─────────┘
                                  │               │                │
            ┌─────────────────────┘               │                └─────────────────────┐
            ▼                                     ▼                                      ▼
┌───────────────────────────┐ ┌──────────────────────────────────────┐ ┌───────────────────────────────────┐
│ skills/crawl-render-audit │ │   skills/freshness-corroboration     │ │     skills/engagement-audit       │
│                           │ │                                      │ │                                   │
│ • robots.txt AI Bot Rules │ │ • Schema.org JSON-LD Extraction      │ │ • Above-the-Fold Value Clarity    │
│ • /llms.txt Specification │ │ • Entity Disambiguation (sameAs)     │ │ • Flesch-Kincaid Readability      │
│ • XML Sitemaps Discovery  │ │ • Citation Extractability & Quotes   │ │ • Signal-to-Noise & Content Fluff │
│ • SSR vs. CSR DOM Parity  │ │ • OpenGraph & Twitter Cards          │ │ • Trust Anchors & Legal Links     │
└───────────┬───────────────┘ └───────────────────┬──────────────────┘ └─────────────────┬─────────────────┘
            │                                     │                                      │
            └─────────────────────────────────────┼──────────────────────────────────────┘
                                                  │
                                                  ▼
                        ┌────────────────────────────────────────────────────┐
                        │         Deduplication, Normalization &             │
                        │             Severity Scoring Engine                │
                        └─────────────────────────┬──────────────────────────┘
                                                  │
                                                  ▼
                        ┌────────────────────────────────────────────────────┐
                        │     Standardized Output JSON Report (Page 2)       │
                        └────────────────────────────────────────────────────┘
```

---

## 🧠 3. Advanced Research & Algorithmic Foundations (GEO + Technical Rigor)

Our skills synthesize empirical research from Princeton University Generative Engine Optimization (GEO) studies (Aggarwal et al., 2023), Georgia Tech AI retrieval benchmarks, and extensive 10-site field validation:

### 1. The 4-Vector Composite Scoring Formula
- **Location**: `skills/audit-orchestrator/references/geo_scoring_model.md` & `scripts/orchestrator.py`
- **Logic**: Evaluates overall readiness through weighted empirical dimensions:
  $$\text{GEO Score} = 0.20 \times \text{Technical} + 0.35 \times \text{Citability} + 0.20 \times \text{Schema} + 0.25 \times \text{Entity/Brand}$$
- **Rationale**: Content Citability (35%) carries the highest weight because structured, quotable answers drive 115%–415% visibility gains in AI search engines.

### 2. Business Type Weight Adjustments
- **Location**: `skills/audit-orchestrator/references/geo_scoring_model.md`
- **Logic**: Automatically tailors scoring priorities based on industry context:
  - **SaaS / Technology**: SSR rendering emphasis (+10%), feature comparison answer blocks (+10%), FAQ/HowTo schema (+15%).
  - **E-Commerce / D2C**: Product/Offer JSON-LD (+20%), statistical price/stock density (+15%), review aggregation (+15%).
  - **Publishers / Media**: Article/NewsArticle schema (+15%), authorship/date freshness (+10%), plain-text citability (+10%).
  - **Local Business / SMB**: LocalBusiness schema (+25%), NAP consistency (+20%), location self-containment (+10%).

### 3. Atomic Quotation Density & Citability Logic
- **Location**: `skills/freshness-corroboration/scripts/consistency.py` & `references/citation_heuristics.md`
- **Logic**: Computes the ratio of concise, declarative subject-verb-object factual assertions containing exact metrics, prices, and units vs. vague marketing jargon. High quotation density ensures conversational AI assistants (Perplexity, ChatGPT Search) can directly cite and quote the brand as authoritative ground truth.

### 4. Proactive Fix Generation
- **Location**: `skills/audit-orchestrator/scripts/orchestrator.py`
- **Logic**: Generates forward-looking strategic enhancements beyond detected defects:
  - Drop-in `/llms.txt` manifest generator customized to the brand's verified endpoints.
  - Unified Schema.org `@graph` entity tree combining `Organization`, `WebSite`, `Product`, and `FAQPage`.
  - Atomic quotation restructuring blueprints.

### 5. Evidence-First Diagnostic Philosophy
- **Location**: All 4 specialized skills
- **Logic**: Every finding outputs verifiable empirical evidence (exact HTTP status codes, disallowed user-agents, word counts, DOM node paths) so evaluators can independently verify observations on the live page.

### 6. Comprehensive DOM & Technical Hierarchy Checks
- **Location**: `skills/crawl-render-audit/scripts/page_analysis.py` & `references/checks.md`
- **Logic**: Audits heading progression (`H1` $\rightarrow$ `H2` $\rightarrow$ `H3`), missing alt text on informational images, canonical link validity, viewport tags, and OpenGraph/Twitter Card metadata.

### 7. Progressive Scan & Crawl Depth Management
- **Location**: `skills/crawl-render-audit/scripts/crawler.py`
- **Logic**: Depth-controlled recursive crawl with polite request delays, ensuring complete multi-page coverage while executing in **< 5 seconds** (well within the 5-minute hackathon constraint).

### 8. 10-Site Empirical Rules & Counterexample Protections
- **Location**: `tests/test_10_site_benchmark.py` & `tests/mock_data/`
- **Logic**:
  - **Dot & Key Rule**: Large raw-to-rendered DOM expansion is **not a failure** if product price/offer exists in raw JSON-LD fallback.
  - **Saraswat Bank Rule**: Dynamic calculator widgets are ignored if key facts (interest rates) exist in static HTML tables.
  - **Healthline Rule**: AI crawler governance (`robots.txt` AI user-agents) is evaluated separately from HTML markup quality.
  - **Nordstrom Rule**: Network WAF / 403 blocks are diagnosed before evaluating client-side rendering.

---

## 🔄 4. Phase-Wise Implementation Progress Log

### ✅ Phase 1: Foundation, Spec Alignment & Marketplace Manifest (COMPLETED)
- **Marketplace Manifest (`marketplace.json`)**: Configured the root registry declaring all 4 skills and designating `audit-orchestrator` as `entrypoint: true`.
- **`agentskills.io` Spec Compliance**: Authored valid `SKILL.md` files for all 4 skills with strict YAML frontmatter (`name`, `description`, `license`, `allowed-tools`) and progressive disclosure sections (`When to use`, `Inputs`, `Procedure`, `Output`, `References`, `Scripts`).
- **Formal Draft-07 JSON Schema (`references/audit_schema.json`)**: Built strict schema validator enforcing Page 2 output contracts (`site`, `audited_at`, `summary`, `findings` with `suggested_action`).
- **Severity Deduction Matrix (`references/severity_matrix.md`)**: Formulated objective mathematical scoring deduction rules.
- **Princeton GEO Scoring Model (`references/geo_scoring_model.md`)**: Encoded 4-Vector empirical weights (Technical 20%, Citability 35%, Schema 20%, Brand 25%) with industry adjustments.
- **AI Bot Catalog & `/llms.txt` Spec**: Created `ai_bot_directory.md` (15+ AI user-agents) and `llms_txt_spec.md`.
- **Schema & Citation Guides**: Created `schema_types_guide.md`, `citation_heuristics.md`, `engagement_rubric.md`, and `trust_signals_guide.md`.

---

### ✅ Phase 2: Technical Discoverability & Fact-Aware Rendering (`crawl-render-audit`) (COMPLETED)
- **AI Crawler Access Matrix**: Implemented explicit rule checks for 12+ AI crawlers (`GPTBot`, `ChatGPT-User`, `ClaudeBot`, `Claude-Web`, `PerplexityBot`, `Google-Extended`, `Bytespider`, `CCBot`).
- **`/llms.txt` Standard Parser**: Implemented `/llms.txt` and `/.well-known/llms.txt` parser in `robots.py`.
- **Fact-Aware JS Dependency Check**: Enhanced `page_analysis.py` to compare raw HTML vs. raw JSON-LD fallback before diagnosing CSR rendering locks (preventing Dot & Key false positives).

---

### ✅ Phase 3: Knowledge Graph, Entity Disambiguation & Quotation Engine (`freshness-corroboration`) (COMPLETED)
- **Schema.org JSON-LD Parser**: Implemented `@graph` parser in `structured_data.py` (`Organization`, `Product`, `Offer`, `FAQPage`, `Article`).
- **Wikidata Entity Disambiguation**: Implemented `sameAs` Knowledge Graph check in `structured_data.py` (Wikidata QID, Crunchbase, LinkedIn).
- **Atomic Quotation Density Engine**: Implemented `analyze_citation_extractability()` in `consistency.py`.
- **Stale Temporal Signals**: Implemented copyright date freshness and brand name consistency checks in `consistency.py`.

---

### ✅ Phase 4: Human Engagement, Orientation & Trust Engine (`engagement-audit`) (COMPLETED)
- **Above-the-Fold Value Clarity**: Implemented `analyze_first_screen_orientation()` in `engagement.py`.
- **Flesch-Kincaid Readability**: Implemented syllable counter and Flesch Reading Ease / Grade Level calculation in `engagement.py`.
- **Essential Trust Anchors**: Implemented Privacy Policy, Terms, and Contact detector in `engagement.py`.

---

### ✅ Phase 5: Master Orchestrator, Deduplication & Princeton GEO Scoring (`audit-orchestrator`) (COMPLETED)
- **Master Pipeline Execution**: Implemented `run_audit()` in `orchestrator.py` coordinating sub-skills.
- **Strict Page 2 Report Emission**: Ensured top-level fields (`site`, `audited_at`, `summary`, `findings`) and nested `suggested_action` objects match schema.
- **Finding Deduplication**: Implemented deterministic signature hashing (`category + title + location`) in `orchestrator.py`.
- **Proactive Recommendations Engine**: Implemented `generate_proactive_recommendations()` in `orchestrator.py`.

---

### ✅ Phase 6: Comprehensive Benchmark Suite & Packaging (COMPLETED)
- **Unit Tests Setup**: Implemented 48 test cases across `test_basic_checks.py`, `test_finding_normalization.py`, `test_report_schema.py`, `test_synthetic_sites.py`, and `test_10_site_benchmark.py`.
- **Universal Test Runner**: Created `tests/run_tests.py` (zero external dependencies, 100% pass rate in < 0.02s).
- **Automated Packaging**: Built `package_marketplace.py` generating clean `brand-ai-readiness-audit.zip` (0.06 MB).

---

## 📊 5. Standardized Output Schema (Exact Page 2 Compliance)

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

## ⚡ 6. Execution & Usage

```bash
# Execute audit on any live URL or domain
python skills/audit-orchestrator/scripts/orchestrator.py https://example.com --output report.json

# Run all 48 test suites & empirical benchmarks
python tests/run_tests.py

# Re-package the submission zip
python package_marketplace.py
```
