# Visitor Engagement & Retention Heuristics Rubric

This rubric outlines the technical and perceptual signals that govern whether a visitor referred from an AI assistant (or search engine) stays on site or bounces immediately.

---

## 1. Above-the-Fold Immediate Orientation (The 3-Second Rule)

When a user clicks a citation link in ChatGPT, Perplexity, or Claude, they arrive with specific conversational context.

### The 3 Core Questions:
1. **What is this?** (Product / service category)
2. **Who is it for?** (Target audience / persona)
3. **What problem does it solve?** (Primary value proposition)

### Evaluation Metrics:
- Primary `<h1>` must contain concrete nouns and verbs, not vague marketing jargon (e.g. *"Enterprise Cloud Security Automation"* vs. *"Unleash The Future"*).
- First 500 characters of rendered body text must define the core capability.

---

## 2. Signal-to-Noise Ratio & Fluff Detection

- **Informational Density**: Ratio of substantive text (features, documentation, pricing, specs) against boilerplate (legal disclaimers, cookie banners, empty marketing fluff).
- **Fluff Penalty**: Excessive buzzword density (*"synergy"*, *"disruptive paradigm"*, *"cutting-edge next-gen"*) without technical specifics triggers an engagement warning.

---

## 3. Readability & Linguistic Accessibility

- **Flesch Reading Ease**: Optimal range is 50.0 - 75.0 (accessible yet professional).
- **Flesch-Kincaid Grade Level**: Ideal range is 8.0 - 12.0 for tech/B2B products. Scores > 15 indicate unnecessarily convoluted sentence structures that degrade human comprehension and AI summarizer quality.
- **Paragraph Chunking**: Paragraphs exceeding 120 words without headings, bullet points, or visual breaks increase bounce probability.
