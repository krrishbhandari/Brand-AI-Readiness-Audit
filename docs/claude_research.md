1. Does Adobe already have a tool for this? Yes — and it matters a lot for your strategy

Adobe launched Adobe Brand Visibility in April 2026 as a unified GEO (Generative Engine Optimization) product, positioned to help brands stay visible, accurate and trusted across AI discovery surfaces while deepening engagement on owned properties. The core engine inside it is Adobe LLM Optimizer, which Adobe strengthened by acquiring Semrush in April 2026 to add SEO, GEO, and "agentic search optimization" capabilities. 
Adobe Newsroom
Adobe Newsroom

What LLM Optimizer actually does (mechanically):

It sends a set of brand-relevant prompts to LLM-based assistants via a Data Retrieval Service, then uses Azure OpenAI to determine whether the brand was mentioned in the responses — i.e., it doesn't crawl-and-infer, it literally asks ChatGPT/Copilot/etc. questions and checks the answers. 
adobe
It separately ingests CDN log data to compute agentic traffic, referral traffic, and crawl failures. 
adobe
For fixes, it sends historical prompt data where visibility is low to Azure OpenAI, which proposes content changes, and separately analyzes technical/crawl errors to recommend fixes. 
adobe
Its standout feature is "Optimize at Edge" — deploying schema, copy, and code fixes directly at the CDN layer through Fastly, Akamai, or Cloudflare, so the underlying CMS is never touched. 
Dwao
It surfaces opportunities like FAQs, abstracts, schema, and crawlability/indexing fixes tied to boosting citations, and reports a documented case where auto-optimization increased citations 5x within a week for Adobe Firefly. 
adobe
SourcedCode

Where the loopholes are (this is your unfair advantage):

It requires infrastructure access your marketplace won't have. It only works for brands with an existing Adobe/Semrush account, CDN edge access, and often AEM integration. Round 3 explicitly wants recommend-only auditing of any unseen site with zero infrastructure — a fundamentally different (harder, more general) problem than "optimize a site I already control."
It's non-deterministic and slow at its core — it works by literally querying live AI assistants and waiting for Azure OpenAI to judge the answers. That's expensive, rate-limited, and impossible inside your 5-minute runtime budget. Your marketplace has to substitute this with deterministic, evidence-based proxy signals (structured data, plain-text facts, crawlability) instead of live-querying LLMs — which is actually closer to real GEO research methodology than what Adobe ships.
Its fixes are an opaque black box — "Azure OpenAI proposes content changes" with no visible reasoning chain. Your rubric explicitly rewards evidence + severity + mechanism-sound fixes a non-expert can verify. Transparency is a genuine differentiator here, not just an aesthetic choice.
It's heavily weighted toward off-site citation tracking, thin on true on-site engagement. Its marketed strengths are visibility scores, share-of-voice, and citation traffic — not navigation clarity, context retention, or dead-end journeys, which is literally half of what Round 3 asks you to detect. If your marketplace treats engagement as a first-class, equally-elaborated skill (not an afterthought), you're covering ground Adobe's own flagship product treats lightly.

So: don't try to "build a mini LLM Optimizer." Build the thing Adobe's tool structurally can't be — a zero-infrastructure, deterministic, transparent, evidence-first auditor for both halves of the problem.

2. What data you actually extract, and why each piece matters
Data	How you get it	Why it matters (mechanism, from Round 2 appendix)
Raw server HTML	requests/httpx GET	Baseline of what a non-JS crawler sees
Rendered DOM	Playwright render, diff vs raw HTML	Reveals facts that only exist after JS runs — invisible to simpler crawlers/extractors (Appendix C)
robots.txt, meta robots, X-Robots-Tag	urllib.robotparser + header check	Gate #1: is the crawler even let in? (Appendix A)
HTTP status / redirect chains	response headers	Gate #1 continued — broken/looping paths = invisible pages
sitemap.xml	fetch + parse	Coverage — what the site wants discovered
JSON-LD (<script type="application/ld+json">)	parse as JSON, validate against schema.org types (Organization, Product, FAQPage, Article, BreadcrumbList)	The single richest machine-readable entity signal — explicit, unambiguous structured facts (Appendix C)
Microdata/RDFa, Open Graph/Twitter tags	HTML attribute parsing	Secondary structured signals, useful when JSON-LD is absent
Main plain-text content (boilerplate-stripped)	readability-style extraction	Tests whether the actual fact (price, spec, address) lives in readable text vs. only implied
Images/canvas/charts	<img> alt text presence + flag when key numeric/textual facts appear to live only inside an image	Facts locked in non-text are effectively invisible to extraction (Appendix C)
Heading structure (H1–H6)	DOM parse	Both a human-orientation signal and a content-hierarchy signal for engagement checks
Internal nav/link graph	DOM parse	Engagement: is there an obvious next step, or dead ends?
Visible dates (published/modified) + dateModified in JSON-LD	text + structured extraction	Freshness signal (Appendix D)
Entity identity signals: NAP consistency, sameAs links to Wikipedia/Wikidata/socials in JSON-LD	JSON-LD + text scan	Disambiguation — does anything distinguish this entity from others sharing its name? (Appendix D)

You generally don't need paid backlink/mention APIs to check "agreement across the web" — you can do a lightweight version (e.g., a few targeted searches for the brand name + a distinguishing fact) as a secondary corroboration check rather than a core crawl dependency, given your runtime budget.

3. Questions worth asking (yourself, your team, or an AI) before building

On the problem itself

Which specific Round-2 failure modes am I encoding, and which mechanism (A–F in the appendix) does each one map to?
For each check: what's the false positive case? (E.g., a site with no JSON-LD but excellent plain-text facts shouldn't automatically score "high severity.")
What's genuinely undetectable without live infrastructure (e.g., actual AI citation rate), and how do I state that limitation honestly instead of faking it?

On decomposition

What's the real separation of concerns — is "AI Content/Entity" actually different work from "Crawl/Render," or am I splitting arbitrarily to look more sophisticated?
Does my orchestrator do genuine composition (resolving conflicts, deduplicating overlapping findings, ranking across skills) or just concatenate JSON blobs?

On severity/evidence

What's my exact, reusable severity rubric (not vibes) — what numeric/structural threshold makes something Critical vs Medium?
For every finding, can I point to the literal evidence string a grader could verify by opening the page?

On generalization

Which of my checks are actually general rules vs. secretly tuned to the 20–30 sites I researched?
Have I run this on at least a few sites I did not use while designing the rules, and did anything break?

On engineering constraints

Does my whole pipeline realistically finish in under 5 minutes on a typical site (crawl depth caps, page sample size, Playwright usage only where needed)?
Is every skill folder independently SKILL.md-valid per the agentskills.io spec, and does marketplace.json have exactly one entrypoint: true?
Am I 100% read-only — no login, no form submission, robots.txt respected everywhere?

On differentiation

What would 500 teams prompted with "build a GEO audit agent skill" produce by default (probably: one skill, vague LLM-only checks, no evidence, no severity model) — and where am I deliberately doing the opposite?
4. Being unique among 500 teams

The rubric tells you exactly what most submissions will fail at: evidence-backed detection with few false positives, mechanism-sound fixes, genuine (not padded) decomposition, and generalization by construction. Given "AI assistance is allowed," the median team will ask an AI to scaffold the marketplace and ship generic checks like "improve SEO" with no thresholds. Your edge:

Do the field research first, on paper, before code — exactly like the roadmap you were given: signal → detection method → evidence format → severity → fix, as a spreadsheet, for ~20-30 real sites across categories.
Make every check falsifiable — a hardcoded number of pages checked, a specific threshold, not "seems unclear."
Hybrid, not LLM-everywhere — deterministic script for objective facts (schema exists? robots blocks path?), narrowly-scoped LLM reasoning only for genuinely judgment-based calls (is the value prop clear?). Say explicitly in your README which is which.
Tie every check back to a mechanism from the Round 2 appendix in your SKILL.md — reviewers grading many similar-looking submissions will notice the one that shows why a check exists, not just that it exists.
Test on a genuine holdout you didn't design against, and be honest in your README about what generalizes and what's a known limitation.
5. How to actually build a skill

Structure per skill:

skill-name/
├── SKILL.md        (required: YAML frontmatter + instructions)
├── scripts/         (executable checks — Python)
└── references/       (detailed rule tables, thresholds, checklists)
name: lowercase, hyphenated, ≤64 chars. description: this is the only thing loaded at discovery time by other agents/skills — it must state both what the skill does and when to use it precisely, per the agentskills.io spec, which also constrains the name field to lowercase letters, numbers, and hyphens with no leading, trailing, or consecutive hyphens. 
Medium
Body sections: When to use / Inputs / Procedure (numbered, deterministic) / Output (schema).
Keep SKILL.md lean — the spec describes a three-stage progressive disclosure model where agents load only name and description at discovery, the full SKILL.md on activation, and bundled scripts or references only during execution, so push detailed thresholds into references/ and actual crawling/parsing code into scripts/. 
GitHub
Root-level marketplace.json: list every skill's id/path, mark exactly one entrypoint: true.
Orchestrator skill: receives the URL, invokes the other skills' scripts, merges their findings into the single required report schema (site, audited_at, summary counts, findings[] with id/title/severity/evidence/suggested_action).
Validate each folder if you have Python/npm available — the spec ships a skills-ref validate convenience checker.