# AI Crawler & Bot User-Agent Directory (2026 Reference)

This directory details major AI crawlers, their operational category (Live Search / RAG vs. Training Scrapers), operators, and the implications of blocking them in `robots.txt`.

---

## 1. Conversational AI Assistants & Live Search (High Citation Impact)

Blocking these bots makes your brand completely invisible in real-time AI answers and conversational search:

| Bot User-Agent | Operator | Purpose | Impact if Blocked |
| :--- | :--- | :--- | :--- |
| **`ChatGPT-User`** | OpenAI | Direct web browsing on behalf of ChatGPT Plus/Team/Enterprise users. | ChatGPT cannot browse or fetch live URLs given by users; fails real-time queries. |
| **`GPTBot`** | OpenAI | Content crawler for ChatGPT search index & grounding. | Brand disappears from ChatGPT Search citations and product recommendations. |
| **`PerplexityBot`** | Perplexity AI | Live search indexing and real-time query retrieval for Perplexity answers. | Zero visibility in Perplexity citations, source links, and direct answer cards. |
| **`ClaudeBot`** | Anthropic | Content indexing and citation retrieval for Claude.ai. | Claude cannot ground answers using your domain's live documentation or pages. |
| **`Claude-Web`** | Anthropic | Real-time browsing invoked directly by Claude users. | Claude fails when asked to inspect or summarize your site URL. |
| **`Applebot-Extended`** | Apple | Indexing for Apple Intelligence & Siri conversational search. | Excluded from Apple Intelligence search overviews and Siri smart answers. |

---

## 2. Foundation Model Pre-Training Scrapers (Optional / Selective Blocking)

Brands that wish to prevent their data from being used in pre-training model weights while remaining visible in live search can selectively block these:

| Bot User-Agent | Operator | Purpose | Recommended Policy |
| :--- | :--- | :--- | :--- |
| **`CCBot`** | Common Crawl | Open web archive used for bulk model pre-training. | Block if concerned about AI model weight ingestion. |
| **`Google-Extended`** | Google | Controls training data ingestion for Gemini models. | Disallow if training opt-out desired; does not affect regular Google Search. |
| **`Bytespider`** | ByteDance | Pre-training and Doubao AI search scraper. | Block if aggressive crawl rates cause server strain. |
| **`Amazonbot`** | Amazon | Web scraper for Amazon Bedrock / Alexa AI training. | Configurable per brand policy. |

---

## 3. Best Practice `robots.txt` AI Policy

```robots.txt
# Allow live conversational assistants for brand discovery & citation
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

# Disallow bulk open-web training scrapers if desired
User-agent: CCBot
Disallow: /

Sitemap: https://example.com/sitemap.xml
```
