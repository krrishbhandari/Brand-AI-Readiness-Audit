# Severity Classification Matrix & Scoring Rubric

## Severity Levels

| Severity Level | Definition | Impact on AI Assistants / Visitors | Example Conditions |
| :--- | :--- | :--- | :--- |
| **`critical`** | Complete barrier to discoverability or engagement | AI crawlers completely blocked; site 100% invisible to LLM answers; critical security/trust failure. | `robots.txt` disallowing all AI bots (`GPTBot`, `PerplexityBot`); 0 pages crawlable; HTTP 5xx errors on key endpoints. |
| **`high`** | Severe degradation of machine understanding or trust | AI confuses brand identity with another entity; key data (pricing, catalog) locked in CSR/images; high immediate bounce rate. | Missing Schema.org `Organization`/`Product` JSON-LD; no `sameAs` entity links; client-side rendering with empty initial DOM. |
| **`medium`** | Suboptimal grounding, citation difficulty, or friction | Content is crawlable but hard for LLMs to quote cleanly; reading complexity is high; missing `/llms.txt`. | Missing `/llms.txt`; Flesch-Kincaid Grade Level > 14; missing OpenGraph tags; lack of clear H1 value proposition. |
| **`low`** | Minor technical or stylistic imperfection | Slight loss of metadata fidelity without blocking indexing or comprehension. | Missing image `alt` tags on decorative images; minor heading hierarchy skip (e.g. H1 -> H3). |
| **`info`** | Diagnostic observations & proactive suggestions | Non-defective informational notes or forward-looking architectural upgrades. | Verification that SSL is active; presence of sitemap; proactive recommendation to publish `/llms-full.txt`. |

---

## Composite Readiness Score Calculation (0 - 100)

The overall `ai_readiness_score` is computed starting from a base score of 100:

$$\text{Score} = \max\left(0, 100 - \sum \text{Deductions}\right)$$

### Deductions per Severity:
- **`critical`**: -25 points each
- **`high`**: -12 points each
- **`medium`**: -5 points each
- **`low`**: -2 points each
- **`info`**: 0 points
