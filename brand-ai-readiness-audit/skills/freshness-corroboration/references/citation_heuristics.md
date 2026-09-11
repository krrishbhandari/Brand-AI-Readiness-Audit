# Citation Heuristics & Machine Fact Extractability

This reference details the mechanics of how conversational AI models extract, verify, and cite factual claims from web pages.

---

## 1. The Mechanics of AI Citations

Conversational AI search engines (ChatGPT Search, Perplexity, Claude) operate in three extraction phases:
1. **Passage Retrieval**: Matching query embeddings to clean text chunks (200-500 tokens).
2. **Fact Grounding**: Identifying declarative subject-verb-object assertions with low syntactic ambiguity.
3. **Attribution & Quotation**: Selecting atomic sentences that can be quoted directly with high confidence.

---

## 2. Key Failure Modes (Round 2 Connection)

### A. The "Locked in Non-Text" Failure Mode
- **Symptom**: Pricing tables, architecture diagrams, or client rosters are embedded solely inside raster images (`.png`, `.jpg`), `<canvas>` widgets, or downloadable PDFs.
- **Result**: AI crawlers cannot extract the text; users asking *"What is the starting price?"* get *"Price not available"* or hallucinated figures.

### B. The "Entity Collision / Mistaken Identity" Failure Mode
- **Symptom**: The brand shares a common noun name (e.g. *Apex*, *Echo*, *Pulse*, *Forge*) but provides no `sameAs` link to Wikidata or Crunchbase in its structured data.
- **Result**: The AI assistant conflates the brand with a musical artist, open-source library, or medical product.

### C. The "Vague Buzzword / Zero Atomic Claims" Failure Mode
- **Symptom**: Landing pages use abstract slogans (*"Unleashing Next-Gen Synergies for Paradigm Elevation"*) without stating what the product actually does, what it costs, or what features exist.
- **Result**: AI search engines cannot match the page to concrete user queries like *"Best SOC2 compliance monitoring tool for AWS"*.

---

## 3. High-Citation Passage Architecture (The 4-Point Standard)

1. **Lead with Declarative Statement**: State the core fact in the first sentence of each section.
2. **Include Exact Units & Quantifiers**: Specific numbers (e.g. "$49/month", "99.99% uptime SLA", "50+ integrations").
3. **Structured Tables & Lists**: Use native HTML `<table>`, `<ul>`, `<ol>` rather than custom CSS grid div soup.
4. **Link to Verifiable Sources**: Anchor claims to authoritative whitepapers, documentation, or public registries.
