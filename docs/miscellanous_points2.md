I'd recommend something like:

Skill 1 — Crawl & Render Audit

Checks:

robots.txt
crawlability
HTTP status
redirects
HTML availability
JS-rendered content
meta information
canonical
sitemap

Question:

Can a machine actually reach and read the website?

Skill 2 — AI Content / Entity Audit

Checks:

structured data
JSON-LD
schema.org
organization information
product/service information
entity ambiguity
important facts
plain-text accessibility

Question:

Once the machine reaches the page, can it understand the important facts?

The handout specifically calls out missing/invalid structured data, facts locked in non-text, and entity ambiguity.

Skill 3 — Freshness & Corroboration

This is an important one because it connects directly to what you studied in Round 2.

Check:

Are important claims current?
Are dates visible?
Are old claims still present?
Do independent sources agree?
Is the brand information consistent?
Could AI confuse this entity with another?

The underlying principle from the handout is that consistent information across independent sources makes a claim more trustworthy, while inconsistent/isolated information is fragile.

Skill 4 — Engagement Audit

This is the other half of the challenge.

Check things like:

Can a visitor understand what this page is about?
Is the primary CTA obvious?
Is navigation understandable?
Does the page provide context?
Are there dead ends?
Can the user easily continue their journey?
Is important information buried?

The handout specifically mentions:

weak on-site orientation / no context retention

as an example of an engagement problem.

Skill 5 — AI Answerability / Citation Readiness

I would seriously consider adding this as a separate skill.

The question becomes:

If an AI assistant searched this website, could it confidently extract a useful answer and cite it?

For example:

Website says:

We offer many excellent services

Bad.

Better:

We provide GST filing services for small businesses in Mumbai.
Our standard GST filing plan costs ₹X/month.

Your skill should detect whether important information is:

explicit
specific
textual
unambiguous
easy to extract

The handout explains that machines are more likely to extract clearly stated plain-text facts than information that is implied or buried in non-textual elements.4. There is an even better Adobe case

Adobe says that when it applied GEO practices internally:

Firefly saw a 5× increase in citations
Acrobat saw 200% increase in LLM visibility
Acrobat saw a 41% increase in LLM referral traffic

Adobe also reports customer examples such as GM and Slalom improving AI visibility/citations.

So the real business problem isn't:

"Does this website have good SEO?"

It's more like:

"When AI systems answer a customer's question, does the brand become a trusted source, and when that customer reaches the site, does the site actually help them?"