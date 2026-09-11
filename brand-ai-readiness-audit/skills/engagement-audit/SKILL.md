---
name: engagement-audit
description: Audits on-site visitor retention, orientation clarity, information hierarchy, signal-to-noise ratio, and conversion friction for traffic arriving via AI referrals or search engines. Measures above-the-fold value proposition clarity, calculates Flesch-Kincaid readability metrics, detects content fluff and jargon, and validates essential trust anchors (contact details, privacy policy, security certifications). Use when diagnosing why visitors referred to a site bounce immediately.
license: MIT
allowed-tools:
  - python
  - bash
  - web_fetch
---

# Engagement Audit Skill (Visitor Retention & Orientation)

## When to use
Use this skill when auditing a website to diagnose high bounce rates, unclear brand positioning, low signal-to-noise copy, poor reading accessibility, or missing trust anchors for referred visitors.

## Inputs
- `url` *(string, required)*: The target website URL or domain.
- `crawled_pages` *(list of objects, optional)*: List of crawled page dictionaries containing HTML, URLs, and parsed text.

## Procedure
1. **Above-the-Fold Immediate Orientation**:
   - Inspect the primary `<h1>` tag and first 500 characters of rendered text.
   - Verify presence of explicit product category, target audience, and primary value proposition.
   - Flag vague marketing slogans ("Empowering Synergies") as **`medium`** severity.
2. **Signal-to-Noise Ratio & Fluff Detection**:
   - Calculate ratio of substantive copy vs. boilerplate and filler text.
   - Detect empty buzzwords and high jargon density.
3. **Readability & Comprehension Metrics**:
   - Calculate **Flesch Reading Ease** and **Flesch-Kincaid Grade Level**.
   - Flag pages with excessive reading difficulty (> Grade 14) or massive unformatted text blocks as **`medium`** severity.
4. **Information Architecture & Context Retention**:
   - Verify heading hierarchy (`h1` -> `h2` -> `h3`) and breadcrumb navigation.
   - Check presence of clear next-step Calls-to-Action (CTAs).
5. **Trust Anchors & Friction Analysis**:
   - Check for contact details (email, phone, physical address), privacy policy, terms of service, and security badges.
   - Flag missing contact or privacy links as **`high`** severity.

## Output
Emits a list of normalized findings:

```json
[
  {
    "id": "ENG-001",
    "title": "Weak above-the-fold value proposition on landing page",
    "severity": "medium",
    "category": "orientation",
    "skill": "engagement-audit",
    "location": "https://example.com",
    "evidence": "Primary H1 tag 'Innovation Redefined' does not state what the product is or who it serves.",
    "suggested_action": {
      "summary": "Revise H1 and hero sub-headline to clearly declare the product category, core capability, and target audience.",
      "priority": "medium"
    }
  },
  {
    "id": "ENG-002",
    "title": "Missing visible contact and privacy policy links",
    "severity": "high",
    "category": "trust",
    "skill": "engagement-audit",
    "location": "https://example.com",
    "evidence": "Footer contains no direct contact email or link to Privacy Policy, degrading visitor trust.",
    "suggested_action": {
      "summary": "Add clear footer links to Privacy Policy, Terms of Service, and a verifiable contact support email.",
      "priority": "high"
    }
  }
]
```

## References
- Engagement Rubric: [`references/engagement_rubric.md`](file:///c:/Users/Krish%20Bhandari/OneDrive/Documents/Adobe_26/skills/engagement-audit/references/engagement_rubric.md)
- Trust Signals Guide: [`references/trust_signals_guide.md`](file:///c:/Users/Krish%20Bhandari/OneDrive/Documents/Adobe_26/skills/engagement-audit/references/trust_signals_guide.md)
- Check Catalog: [`references/checks.md`](file:///c:/Users/Krish%20Bhandari/OneDrive/Documents/Adobe_26/skills/engagement-audit/references/checks.md)

## Scripts
- Engagement Engine: [`scripts/engagement.py`](file:///c:/Users/Krish%20Bhandari/OneDrive/Documents/Adobe_26/skills/engagement-audit/scripts/engagement.py)
