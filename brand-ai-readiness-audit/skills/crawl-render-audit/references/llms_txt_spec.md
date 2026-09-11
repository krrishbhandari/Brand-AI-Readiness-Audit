# The `/llms.txt` Standard Specification

## Purpose
The `/llms.txt` file (and companion `/llms-full.txt`) is a standardized markdown file placed at the root of a website (e.g. `https://example.com/llms.txt`) designed to provide Large Language Models (LLMs) with concise, structured context regarding a website's content, APIs, and key pages.

---

## Canonical Format

```markdown
# Acme Corporation

> Acme provides enterprise-grade AI analytics and automated customer intelligence software for Fortune 500 retail companies.

## Core Products
- [Acme Intelligence Platform](https://acme.com/products/platform): Enterprise customer behavioral analytics engine with real-time SOC2-certified pipelines.
- [Acme Copilot for Retail](https://acme.com/products/copilot): Generative AI assistant for merchandising and inventory forecasting.

## Pricing & Packaging
- [Pricing Overview](https://acme.com/pricing): Tiered SaaS plans starting from $499/mo with dedicated SLAs.

## Documentation & API Reference
- [REST API Reference](https://docs.acme.com/api): Complete OpenAPI 3.0 specification for ingestion endpoints.
- [Authentication Guide](https://docs.acme.com/auth): OAuth2 and API Key token generation workflows.

## Company & Support
- [Contact Sales](https://acme.com/contact): Global sales inquiries and enterprise demonstrations.
- [Security & Compliance](https://acme.com/security): SOC2 Type II, ISO 27001, and GDPR compliance certifications.
```

---

## Audit Evaluation Criteria for `/llms.txt`

1. **HTTP Status**: Must return `200 OK` with `text/markdown` or `text/plain` content type.
2. **Structure**: Must contain a primary `# Title` (brand name), a `> Blockquote` (1-2 sentence executive value proposition), and markdown link lists organized by `## Section`.
3. **Link Validity**: All referenced links must be absolute HTTPS URLs with descriptive anchor text.
