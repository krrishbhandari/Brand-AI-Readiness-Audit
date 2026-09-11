1. What is the actual objective?

Your Round 3 project is:

Give your agent any website URL, and your marketplace should automatically analyze that website for problems affecting:

AI discoverability: Can AI systems find, understand, trust, and cite the brand?
On-site engagement: Once a visitor reaches the site, does the site provide enough context/orientation to keep them engaged?

The system must then output:

problems detected
evidence for each problem
severity
recommended fix
priority of the fix

This is explicitly the purpose of Round 3. 
6a8ffdf33590a_round3-handout-up…

So the core pipeline is:

Website URL
     ↓
ENTRYPOINT SKILL
     ↓
 ┌───────────────┬──────────────────┬─────────────────┐
 │               │                  │                 │
 ▼               ▼                  ▼                 ▼
Crawl / Render   Freshness /       Engagement       Other
Audit            Corroboration     Audit             Checks
 │               │                  │
 └───────────────┴──────────────────┴─────────────────┘
                         ↓
                  Combine Findings
                         ↓
                  Prioritize Fixes
                         ↓
                    Final Report
2. What exactly do you have to submit?

Your final submission is ONE ZIP FILE, maximum 50 MB.

The ZIP must contain the marketplace root directory.

The handout explicitly gives this structure as an example and requires the marketplace manifest, skills, and README. 
6a8ffdf33590a_round3-handout-up…

A good structure for you would be:

brand-ai-readiness-audit/
│
├── marketplace.json
├── README.md
│
└── skills/
    │
    ├── audit-orchestrator/
    │   ├── SKILL.md
    │   ├── scripts/
    │   └── references/
    │
    ├── crawl-render-audit/
    │   ├── SKILL.md
    │   ├── scripts/
    │   └── references/
    │
    ├── freshness-corroboration/
    │   ├── SKILL.md
    │   ├── scripts/
    │   └── references/
    │
    └── engagement-audit/
        ├── SKILL.md
        ├── scripts/
        └── references/

You do not have to use exactly these four skills. They are an illustrative layout.

The important requirements are:

one or more valid Agent Skills
every skill has a valid SKILL.md
marketplace.json
exactly one entrypoint
root README.md
entrypoint composes the other skills
final output is the required audit report. 
6a8ffdf33590a_round3-handout-up…
3. The most important part: your skills

This is where the actual competition is.

You should not just create one giant SKILL.md saying:

"Analyze the website and find problems."

That would technically be a submission, but it misses the point.

The organizers explicitly say decomposition into multiple focused skills is the point of the marketplace format and is rewarded. 
6a8ffdf33590a_round3-handout-up…

I recommend 4 skills.

Skill 1: audit-orchestrator

This is your entrypoint.

It receives:

URL / domain

and coordinates everything.

Its job:

1. Validate URL
2. Invoke crawl/render audit
3. Invoke freshness/corroboration audit
4. Invoke engagement audit
5. Collect findings
6. Remove duplicates
7. Assess severity
8. Prioritize recommendations
9. Generate final JSON report

This must be the only entrypoint.

Your marketplace.json should therefore contain something conceptually like:

{
  "name": "brand-ai-readiness-audit",
  "version": "1.0.0",
  "skills": [
    {
      "id": "audit-orchestrator",
      "path": "skills/audit-orchestrator",
      "entrypoint": true
    },
    {
      "id": "crawl-render-audit",
      "path": "skills/crawl-render-audit"
    },
    {
      "id": "freshness-corroboration",
      "path": "skills/freshness-corroboration"
    },
    {
      "id": "engagement-audit",
      "path": "skills/engagement-audit"
    }
  ]
}

The contest requires exactly one entrypoint. 
6a8ffdf33590a_round3-handout-up…

4. Skill 2: Crawl / Render Audit

This skill handles:

"Can machines actually access and understand this website?"

You need checks around things such as:

Crawlability

Check:

robots.txt
whether important pages are crawlable
HTTP status codes
redirects
broken links
canonical URLs
sitemap availability
important content hidden behind inaccessible routes

The Round 2 background specifically establishes the crawl → read → extract chain. If any stage fails, the information can effectively become invisible to the machine. 
6a8ffdf33590a_round3-handout-up…

Rendering

Compare what is available in:

Raw HTML
       vs
Rendered DOM

You want to detect situations such as:

Human sees:

"Premium accounting software for Indian startups"

But raw machine-readable content:

<body>
    <div id="root"></div>
    <script src="app.js"></script>
</body>

That is potentially significant.

Structured data

Look for:

JSON-LD
Schema.org
organization information
product information
article information
breadcrumbs
FAQ where appropriate

Don't blindly say:

"No schema = critical."

The skill needs to reason about whether the missing structured data actually matters.

That matters because the rubric explicitly cares about false positives. 
6a8ffdf33590a_round3-handout-up…

Text accessibility

Detect important facts that are:

only images
embedded in canvas
hidden in UI widgets
inaccessible without JavaScript
represented only visually
poorly represented in text

The handout specifically states that facts visible to humans can be invisible to machine readers, and that explicit readable text is easier to extract correctly. 
6a8ffdf33590a_round3-handout-up…

5. Skill 3: Freshness + Corroboration

This is about:

Can an AI system trust what this brand says?

This is a major part of the Round 2 reasoning.

You need to investigate things such as:

Freshness

Look for potentially stale:

product information
pricing
company descriptions
contact information
service descriptions
dates
statistics
announcements

For example:

Homepage:
"We have 50 employees."

About page:
"We have 200 employees."

Linked source:
"We have 120 employees."

That's a problem.

Your system should report something like:

{
  "title": "Conflicting company-size claims",
  "severity": "high",
  "evidence": "...",
  "suggested_action": {
    "summary": "Establish a single authoritative company-size statement and update conflicting pages.",
    "priority": "high"
  }
}
Cross-web corroboration

The handout explicitly emphasizes that agreement between independent sources affects trust. 
6a8ffdf33590a_round3-handout-up…

So your skill can investigate:

Official website
       ↓
External references
       ↓
Independent sources
       ↓
Consistency

Potential problems:

Brand name ambiguity
Conflicting descriptions
Conflicting location
Conflicting services
Conflicting company facts
Outdated external information
Insufficient corroboration
Entity ambiguity

For example:

"Apple"

could refer to:

Apple Inc.
Apple Records
apple fruit
another organization

Your system should look for signals that clearly identify the entity.

Things like:

Organization name
Location
Official URL
Social profiles
sameAs
contact information
company description

The handout specifically calls out mistaken identity as a problem when multiple entities share a name. 
6a8ffdf33590a_round3-handout-up…

6. Skill 4: Engagement Audit

This is the part people could easily forget.

The assignment is not only about SEO/AI discoverability.

You must also investigate:

"Someone reached the website. Why didn't they stay?"

The handout explicitly requires both:

off-site discoverability
on-site engagement. 
6a8ffdf33590a_round3-handout-up…

Your engagement skill should examine things like:

Orientation

Can a visitor immediately understand:

What is this?
Who is it for?
What does it offer?
Why should I care?
What should I do next?
Context retention

Check whether navigation preserves context.

For example:

Homepage
   ↓
Product
   ↓
Pricing

Does the visitor still understand:

Which product?
Which plan?
What problem does it solve?
Why am I here?
Weak information architecture

Look for:

confusing navigation
unclear hierarchy
orphaned pages
important pages difficult to reach
unclear CTAs
unclear product/service relationships
Content gaps

For example:

Product page
    ↓
"Enterprise AI platform"
    ↓
No clear explanation
    ↓
Visitor has to figure out what it actually does

That should potentially become a finding.

7. Your skills should NOT just give opinions

This is critical.

Your marketplace needs to produce evidence-backed findings.

Bad:

The website has poor SEO.

Good:

12 product pages were crawled.
0/12 contain Product/Offer structured data.

The assignment's sample report uses exactly this evidence-oriented approach. 
6a8ffdf33590a_round3-handout-up…

Your skill should therefore collect evidence such as:

URL
HTTP status
HTML snippet/context
DOM information
number of affected pages
page title
meta description
structured-data presence
robots.txt result
sitemap result
rendered vs raw content
timestamps
cross-page conflicts
etc.
8. The final report format is mandatory

Your entrypoint needs to emit a report with at least:

{
  "site": "example.com",
  "audited_at": "2026-09-20T14:32:00Z",

  "summary": {
    "total_findings": 6,
    "critical": 1,
    "high": 2,
    "medium": 3
  },

  "findings": [
    {
      "id": "F-001",
      "title": "No JSON-LD structured data on product pages",
      "severity": "high",
      "evidence": "Crawled 12 product pages; 0/12 contain schema.org markup.",
      "suggested_action": {
        "summary": "Add Product/Offer JSON-LD to every product page.",
        "priority": "high"
      }
    }
  ]
}

The required fields are explicitly specified:

Report metadata
site
audited_at
summary
Summary

Must contain counts by severity:

critical
high
medium
Every finding

Must contain:

id
title
severity
evidence
suggested_action

And the suggested action must include at least:

summary
priority

These are mandatory minimums, although you can add more fields. 
6a8ffdf33590a_round3-handout-up…

9. I recommend adding more fields

Don't stop at the minimum.

A stronger schema would be:

{
  "id": "F-001",
  "category": "ai_discoverability",
  "sub_category": "crawlability",
  "title": "Important product pages blocked from crawling",

  "severity": "high",

  "confidence": 0.94,

  "affected_urls": [
    "https://example.com/product/a",
    "https://example.com/product/b"
  ],

  "evidence": {
    "description": "...",
    "observations": [
      "..."
    ]
  },

  "impact": "AI systems may fail to discover these product pages.",

  "suggested_action": {
    "summary": "Remove the blocking directive...",
    "how_to_fix": [
      "...",
      "..."
    ],
    "priority": "high"
  }
}

That makes your report substantially more useful to the evaluator.

10. You also need proactive recommendations

This is another easy thing to miss.

The marketplace shouldn't only say:

"You have a problem."

It should also say:

"Here are improvements you should make even though I didn't detect an outright defect."

The assignment explicitly allows and encourages proactive improvements. 
6a8ffdf33590a_round3-handout-up…

For example:

Finding:
No organization structured data.

Fix:
Add Organization JSON-LD.


But even if structured data is already present:

Proactive recommendation:
Strengthen entity identity by consistently exposing:
- official name
- canonical URL
- location
- organization description
- relevant sameAs relationships

This directly addresses the rubric's "beyond fixing specific defects" criterion. 
6a8ffdf33590a_round3-handout-up…

11. You are NOT supposed to modify websites

Very important.

Your marketplace is:

READ → ANALYZE → REPORT

NOT:

READ → MODIFY

No:

editing websites
publishing content
authenticated actions
destructive requests
changing CMS data
submitting forms
altering anything

The handout explicitly says the marketplace is recommend-only and runs read-only in a sandbox. 
6a8ffdf33590a_round3-handout-up…

So your architecture should be:

             WEBSITE
                │
                │ read-only
                ▼
        ┌─────────────────┐
        │    CRAWLER      │
        └────────┬────────┘
                 │
       ┌─────────┼──────────┐
       ▼         ▼          ▼
    Crawl     Freshness   Engagement
    Audit      Audit        Audit
       │         │          │
       └─────────┼──────────┘
                 ▼
          ORCHESTRATOR
                 │
                 ▼
          FINDING ENGINE
                 │
                 ▼
        SEVERITY + PRIORITY
                 │
                 ▼
             REPORT
12. You have a runtime constraint

Your audit must run in:

less than 5 minutes on a standard machine for a typical website.

And:

ZIP ≤ 50 MB

Also:

No pretrained model weights.

These are explicit submission constraints. 
6a8ffdf33590a_round3-handout-up…

So don't build:

crawl entire internet
        ↓
train giant ML model
        ↓
wait 45 minutes

Humanity has suffered enough from unnecessarily complicated architecture.

Build deterministic, targeted checks.

13. You need to research real websites

The organizers specifically tell you to do field research.

They want you to find websites that:

AI assistants cite frequently

versus:

AI assistants ignore / misrepresent

and determine what distinguishes them. 
6a8ffdf33590a_round3-handout-up…

But there is an important catch:

You don't submit those websites as your test set.

They're for developing your logic.

Your final marketplace must generalize to unseen websites.

Therefore your workflow should be:

Research websites
       ↓
Observe patterns
       ↓
Identify root causes
       ↓
Convert root causes into deterministic checks
       ↓
Implement skills
       ↓
Test on additional unseen websites

Not:

Research 10 websites
       ↓
Hard-code rules for those 10
       ↓
Hope nobody notices

The evaluation specifically tests generalization. 
6a8ffdf33590a_round3-handout-up…

14. What each SKILL.md should contain

Every skill must follow the Agent Skills format.

The handout gives the basic structure:

---
name: ...
description: ...
license: ...
---

# Skill Name

## When to use

## Inputs

## Procedure

## Output

The procedure should be deterministic.

The handout specifically recommends keeping SKILL.md lean and pushing detailed checklists into:

references/

and executable checks into:

scripts/

This is called progressive disclosure. 
6a8ffdf33590a_round3-handout-up…

So, for example:

crawl-render-audit/
│
├── SKILL.md
│
├── scripts/
│   ├── crawl.py
│   ├── render.py
│   ├── structured_data.py
│   └── robots.py
│
└── references/
    ├── crawlability-checklist.md
    ├── structured-data-checklist.md
    └── rendering-checklist.md

That's a much stronger design than stuffing 2,000 lines into SKILL.md.

15. What I would actually build

If I were structuring your project, I'd use this:

brand-ai-readiness-audit/
│
├── marketplace.json
├── README.md
│
└── skills/
    │
    ├── audit-orchestrator/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── compose_report.py
    │
    ├── crawl-render-audit/
    │   ├── SKILL.md
    │   ├── scripts/
    │   │   ├── crawler.py
    │   │   ├── renderer.py
    │   │   ├── structured_data.py
    │   │   └── accessibility.py
    │   └── references/
    │       ├── crawlability.md
    │       └── machine_readability.md
    │
    ├── freshness-corroboration/
    │   ├── SKILL.md
    │   ├── scripts/
    │   │   ├── fact_extractor.py
    │   │   └── consistency.py
    │   └── references/
    │       ├── freshness.md
    │       └── entity-identity.md
    │
    └── engagement-audit/
        ├── SKILL.md
        ├── scripts/
        │   ├── navigation.py
        │   └── content_orientation.py
        └── references/
            └── engagement-checklist.md
16. Your actual development tasks

I would break your work into these phases.

Phase 1: Research

Study real websites and identify:

AI discoverability
Crawlability
Rendering
Machine-readable content
Structured data
Entity identity
Fact clarity
Fact consistency
Freshness
External corroboration
Engagement
Homepage clarity
Navigation
Information architecture
Context retention
Content completeness
CTA clarity
Product/service understanding

Turn these observations into generalizable rules.

Phase 2: Build the website inspection engine

You need a mechanism to take:

https://example.com

and gather useful evidence.

At minimum:

robots.txt
sitemap
HTML
rendered page
links
metadata
structured data
headings
visible text
important page relationships
Phase 3: Build the individual skills

Create:

audit-orchestrator
crawl-render-audit
freshness-corroboration
engagement-audit

Each skill should have a clearly defined responsibility.

Phase 4: Build finding generation

Every detected issue should become:

Finding
   ↓
Evidence
   ↓
Severity
   ↓
Impact
   ↓
Fix
   ↓
Priority

For example:

F-004

Problem:
Important product information exists only inside client-rendered UI.

Evidence:
Raw HTML contains no product description,
while rendered DOM contains 1,200 characters.

Severity:
Medium

Impact:
Some machine readers may fail to extract the product facts.

Action:
Expose core product information as crawlable text
in the initial HTML or equivalent machine-readable representation.

Priority:
High
Phase 5: Build the orchestrator

The orchestrator should:

Input URL
    ↓
Run Skill A
    ↓
Run Skill B
    ↓
Run Skill C
    ↓
Normalize findings
    ↓
Deduplicate
    ↓
Assign severity
    ↓
Assign priority
    ↓
Generate report
Phase 6: Test for false positives

This is extremely important.

The rubric doesn't only ask:

"Did you find problems?"

It asks whether you find the real problems with few false positives. 
6a8ffdf33590a_round3-handout-up…

So test:

Good website
Bad website
JS-heavy website
Static website
E-commerce website
SaaS website
Corporate website
Local business
Content-heavy website
Website with ambiguous branding

And ask:

Did the skill correctly detect the problem?

Did it provide actual evidence?

Was the severity reasonable?

Is the recommendation actually capable of fixing it?
17. What the judges are actually looking for

This is probably the most important section for your strategy.

The judges evaluate the marketplace itself, not whether one generated report happens to look good. 
6a8ffdf33590a_round3-handout-up…

There are six major areas:

Area	What you need to demonstrate
Detection accuracy	Finds real discoverability + engagement problems
Action quality	Gives technically correct fixes
Output design	Clear evidence + severity + prioritized action
Engineering hygiene	Valid skills, manifest, deterministic, safe
Marketplace composition	Skills genuinely separated and properly composed
Generalization	Works on websites it has never seen

So don't spend all your effort making a pretty README.

The actual detection logic is the product.

18. Your final submission checklist

Before submitting the ZIP, verify:

Marketplace
 marketplace.json
 exactly one entrypoint: true
 every listed skill exists
 every skill contains SKILL.md
 every SKILL.md follows agentskills.io format
 root README.md
Functionality
 accepts a website/domain
 audits AI discoverability
 audits on-site engagement
 produces evidence
 assigns severity
 produces suggested actions
 prioritizes actions
 includes proactive recommendations
 produces one final report
Report
 site
 audited_at
 severity counts
 finding id
 finding title
 finding severity
 finding evidence
 suggested_action
 action summary
 action priority
Safety
 read-only
 no website modification
 no authenticated areas
 no destructive requests
 respects robots.txt
 no rate abuse
Performance
 typical audit < 5 minutes
 ZIP < 50 MB
 no pretrained model weights

These constraints come directly from the submission and guardrail sections. 
6a8ffdf33590a_round3-handout-up…

19. In one sentence: what are you building?

You're building this:

A portable, multi-skill AI-agent package where an entrypoint receives any website URL, runs specialized audits for AI discoverability and visitor engagement, gathers evidence-backed problems, assigns severity, and produces prioritized recommendations without modifying the website.

That is the project.

And the key distinction is:

                 NOT THIS
                    ↓
       "AI agent that audits websites"
                    ❌


                 THIS
                    ↓
       ┌──────────────────────────┐
       │   AGENT SKILL MARKETPLACE │
       ├──────────────────────────┤
       │ Orchestrator              │
       │                           │
       │ Crawl/Render Skill        │
       │ Freshness/Entity Skill    │
       │ Engagement Skill          │
       │                           │
       │ Deterministic checks      │
       │ Evidence collection       │
       │ Severity + priority       │
       │                           │
       │       ↓                   │
       │ Structured audit report   │
       └──────────────────────────┘

The organizers are essentially asking you to turn the reasoning from Round 2 into reusable, executable inspection skills. The Round 2 appendix gives you the conceptual foundations, but explicitly says that working out the concrete checks and fixes is your job. 
6a8ffdf33590a_round3-handout-up…

So your next serious task should be to define the complete detection checklist for all four skills, because that checklist becomes the brain of the implementation rather than a pile of vaguely impressive agent instructions.