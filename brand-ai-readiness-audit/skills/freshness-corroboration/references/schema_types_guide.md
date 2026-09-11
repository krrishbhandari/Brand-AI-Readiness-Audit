# Schema.org Structured Data & Entity Graph Guide

This guide outlines essential Schema.org structured data types and entity graph patterns required for Generative Engine Optimization (GEO) and AI assistant understanding.

---

## 1. Core Schema Types & Required Properties

### 1.1. `Organization` / `Corporation`
Crucial for brand entity grounding and preventing identity collisions across LLMs.
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Acme Global Technologies",
  "url": "https://acme.com",
  "logo": "https://acme.com/assets/logo.png",
  "description": "Enterprise cloud security and AI behavioral analytics platform.",
  "disambiguatingDescription": "B2B SaaS cybersecurity provider, not to be confused with Acme Audio Hardware.",
  "sameAs": [
    "https://www.wikidata.org/wiki/Q12345678",
    "https://www.crunchbase.com/organization/acme-global",
    "https://www.linkedin.com/company/acme-global",
    "https://twitter.com/AcmeGlobal"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "contactType": "customer support",
    "email": "support@acme.com"
  }
}
```

### 1.2. `Product` & `Offer`
Enables AI shopping assistants (ChatGPT Search, Perplexity) to cite live pricing, currency, and availability accurately.
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Acme Cloud Shield Pro",
  "description": "Real-time automated DDoS and API protection suite.",
  "brand": {
    "@type": "Brand",
    "name": "Acme"
  },
  "offers": {
    "@type": "Offer",
    "price": "499.00",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "url": "https://acme.com/products/cloud-shield"
  }
}
```

### 1.3. `FAQPage`
Exposes atomic question-answer pairs that LLMs can directly ingest and cite as ground truth.
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What compliance certifications does Acme hold?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Acme is SOC2 Type II, ISO 27001, HIPAA, and GDPR compliant."
      }
    }
  ]
}
```
