# Granular Task Checklist: Brand AI-Readiness Audit Marketplace

**Hackathon**: Adobe University Hackathon 2026 — Round 3 (Development Round)  
**Standard**: [`agentskills.io`](https://agentskills.io)  
**Status**: In Progress

---

## Phase 1: Foundation, Spec Alignment & Marketplace Manifest
- [x] **1.1. Marketplace Manifest**: Validate `marketplace.json` contains 4 skills and designates `audit-orchestrator` as `entrypoint: true`.
- [x] **1.2. Root Documentation**: Write comprehensive `README.md` with architecture diagrams, composition explanation, and research rationale.
- [x] **1.3. Spec Compliance (`audit-orchestrator`)**: Ensure `skills/audit-orchestrator/SKILL.md` has YAML frontmatter, input/output contracts, and procedures.
- [x] **1.4. Spec Compliance (`crawl-render-audit`)**: Ensure `skills/crawl-render-audit/SKILL.md` has YAML frontmatter and procedure.
- [x] **1.5. Spec Compliance (`freshness-corroboration`)**: Ensure `skills/freshness-corroboration/SKILL.md` has YAML frontmatter and procedure.
- [x] **1.6. Spec Compliance (`engagement-audit`)**: Ensure `skills/engagement-audit/SKILL.md` has YAML frontmatter and procedure.
- [x] **1.7. Formal JSON Schema**: Create `skills/audit-orchestrator/references/audit_schema.json` matching Page 2 schema.
- [x] **1.8. Severity Rubric**: Create `skills/audit-orchestrator/references/severity_matrix.md`.

---

## Phase 2: Technical Discoverability & Fact-Aware Rendering Engine (`crawl-render-audit`)
- [x] **2.1. AI Bot Matrix**: Implement 12+ AI bot permissions parser in `skills/crawl-render-audit/scripts/robots.py` (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, Bytespider, CCBot).
- [x] **2.2. `/llms.txt` Standard Parser**: Implement `check_llms_txt()` in `robots.py` to audit `/llms.txt` and `/.well-known/llms.txt`.
- [x] **2.3. AI Bot Reference Catalog**: Create `skills/crawl-render-audit/references/ai_bot_directory.md`.
- [x] **2.4. `/llms.txt` Syntax Spec**: Create `skills/crawl-render-audit/references/llms_txt_spec.md`.
- [x] **2.5. Fact-Aware Rendering Check**: Enhance `skills/crawl-render-audit/scripts/page_analysis.py` to compare raw HTML vs. raw JSON-LD fallback before diagnosing CSR locks (preventing Dot & Key false positives).
- [x] **2.6. Crawl & Render Check Catalog**: Update `skills/crawl-render-audit/references/checks.md`.

---

## Phase 3: Knowledge Graph, Entity Disambiguation & Quotation Engine (`freshness-corroboration`)
- [x] **3.1. Schema.org JSON-LD Parser**: Implement `@graph` parser in `skills/crawl-render-audit/scripts/structured_data.py`.
- [x] **3.2. Wikidata Entity Disambiguation**: Implement `sameAs` Knowledge Graph check in `structured_data.py` (Wikidata QID, Crunchbase, LinkedIn).
- [x] **3.3. Schema Types Guide**: Create `skills/freshness-corroboration/references/schema_types_guide.md`.
- [x] **3.4. Citation Extractability Heuristics**: Create `skills/freshness-corroboration/references/citation_heuristics.md`.
- [x] **3.5. Atomic Quotation Density Engine**: Implement `analyze_citation_extractability()` in `skills/freshness-corroboration/scripts/consistency.py`.
- [x] **3.6. Stale Temporal Signals**: Implement copyright date & freshness checks in `consistency.py`.

---

## Phase 4: Human Engagement, Orientation & Trust Engine (`engagement-audit`)
- [x] **4.1. Above-the-Fold Value Clarity**: Implement `analyze_first_screen_orientation()` in `skills/engagement-audit/scripts/engagement.py`.
- [x] **4.2. Flesch-Kincaid Readability**: Implement syllable counter and Flesch Reading Ease / Grade Level in `engagement.py`.
- [x] **4.3. Essential Trust Anchors**: Implement Privacy Policy, Terms, and Contact detector in `engagement.py`.
- [x] **4.4. Engagement Rubric Reference**: Create `skills/engagement-audit/references/engagement_rubric.md`.
- [x] **4.5. Trust Signals Guide**: Create `skills/engagement-audit/references/trust_signals_guide.md`.

---

## Phase 5: Master Orchestrator, Deduplication & Princeton GEO Scoring (`audit-orchestrator`)
- [x] **5.1. Master Pipeline Execution**: Implement `run_audit()` in `skills/audit-orchestrator/scripts/orchestrator.py`.
- [x] **5.2. Strict Page 2 Report Emission**: Ensure top-level fields (`site`, `audited_at`, `summary`, `findings`) and nested `suggested_action` objects match schema.
- [x] **5.3. Finding Deduplication**: Implement deterministic signature hashing (`category + title + location`) in `orchestrator.py`.
- [x] **5.4. Proactive Recommendations Engine**: Implement `generate_proactive_recommendations()` in `orchestrator.py` (auto-generating `/llms.txt` recipes and unified `@graph` schemas).
- [x] **5.5. Princeton GEO Scoring Model**: Document 4-Vector scoring weights in `skills/audit-orchestrator/references/geo_scoring_model.md`.

---

## Phase 6: Comprehensive Benchmark Suite & Packaging
- [x] **6.1. Unit Tests Setup**: Implement `tests/test_basic_checks.py`, `tests/test_finding_normalization.py`, and `tests/test_report_schema.py` using standard library `unittest`.
- [x] **6.2. Universal Test Runner**: Create `tests/run_tests.py` (zero external dependencies).
- [x] **6.3. Synthetic Site Tests**: Implement `tests/test_synthetic_sites.py` testing against `poor_ai_readiness_fixture.html` and `optimized_brand_fixture.html`.
- [x] **6.4. 10-Site Benchmark Fixtures**: Create fixtures for Dot & Key (JSON-LD fallback) and Saraswat Bank (static table).
- [x] **6.5. 10-Site Benchmark Tests**: Create `tests/test_10_site_benchmark.py` validating counterexamples from research.
- [x] **6.6. Automated Packaging Script**: Create `package_marketplace.py` generating `brand-ai-readiness-audit.zip`.
- [x] **6.7. Final Submission Validation**: Verify zip file size (< 1 MB), manifest validity, and runtime (< 5s).
