# Princeton GEO 4-Vector Scoring Model & Business Type Adjustments

This reference documents the empirical scoring weights, composite formula, and business type adjustments adapted from the Princeton Generative Engine Optimization (GEO) framework (Aggarwal et al., 2023).

---

## 1. Composite GEO Score Formula

$$\text{Composite GEO Score} = 0.20 \times \text{Technical} + 0.35 \times \text{Citability} + 0.20 \times \text{Schema} + 0.25 \times \text{Entity/Brand}$$

### Dimension Weights & Rationale:

| Dimension | Weight | Empirical Evidence & Mechanism |
| :--- | :--- | :--- |
| **Technical Accessibility** | **20%** | Baseline requirement: AI search crawlers (`GPTBot`, `PerplexityBot`, `ClaudeBot`) must be permitted by `robots.txt` and pages must not be locked behind WAF or blank CSR containers. |
| **Content Citability** | **35%** | Highest weight: Princeton research shows that declarative, atomic factual blocks with statistics, units, and concise sentences produce 115%–415% visibility improvements in AI citations. |
| **Structured Data (Schema.org)** | **20%** | Rich JSON-LD markup increases AI entity comprehension by 40%+ and directly feeds structured extraction in answer engines. |
| **Entity & Brand Grounding** | **25%** | Cross-source entity disambiguation (`sameAs` links to Wikidata, Crunchbase, Wikipedia) correlates with 2.5× higher AI citation accuracy, preventing identity collisions. |

---

## 2. Business Type Multiplier Adjustments

| Business Category | Primary Adjustments | Optimization Focus |
| :--- | :--- | :--- |
| **B2B SaaS / Tech** | Technical Rendering (+10%), Citability Answer Blocks (+10%), FAQ/HowTo Schema (+15%) | Feature comparison clarity, API/documentation indexing, and SSR rendering. |
| **E-Commerce / D2C** | Product/Offer Schema (+20%), Statistical Price/Stock Density (+15%), Review Aggregation (+15%) | Live price, currency, availability, and reviews in JSON-LD fallback. |
| **Publisher / Media** | Article/NewsArticle Schema (+15%), Citability (+10%), Authorship & Date Freshness (+10%) | High quote-density text, explicit modified dates, and author entity anchors. |
| **Local SMB / Services** | LocalBusiness Schema (+25%), NAP Consistency (+20%), Location Anchors (+10%) | Address, phone, operating hours, and geo-targeted service descriptions. |

---

## 3. Score Interpretation Bands

| Score Range | Grade | Label | Status |
| :--- | :--- | :--- | :--- |
| **85 – 100** | **A** | Excellent | Highly optimized for AI search engines and human retention. Focus on monitoring. |
| **70 – 84** | **B** | Good | Solid foundation with specific metadata or citability gaps. Fast remediation path. |
| **50 – 69** | **C** | Developing | Moderate issues (e.g. missing `/llms.txt`, no Wikidata `sameAs`, high fluff). Action plan required. |
| **30 – 49** | **D** | Needs Work | Major gaps across crawler permissions, missing schema, or CSR locks. |
| **0 – 29** | **F** | Critical | Fundamental barriers blocking AI retrieval (e.g. blanket bot disallow, blank DOM). Immediate triage. |
