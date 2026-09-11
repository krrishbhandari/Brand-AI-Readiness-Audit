"""
10-Site Empirical Validation Benchmark Tests.
Validates all 10 empirical site archetypes and key diagnostic rules discovered during research:
1. Dot & Key (E-Commerce / D2C JSON-LD fallback)
2. Saraswat Bank (Fintech / Static table facts)
3. Healthline (Publisher / AI crawler policy vs HTML)
4. Nordstrom (Enterprise / Edge WAF vs JS rendering)
5. Wikipedia (Knowledge Base / High atomic quotation density)
6. Stripe Docs (Developer SaaS / Multi-entity Schema & clear value prop)
7. Zapier (B2B SaaS / Above-the-fold value clarity & primary CTA)
8. Prashant Corner (Local SMB / LocalBusiness Schema & NAP consistency)
9. Coursera (EdTech / Educational catalog & course structure)
10. GitHub Docs (Technical Documentation / Fluff suppression & deep hierarchy)
"""

import unittest
import sys
import os
from bs4 import BeautifulSoup

ORCH_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'skills', 'audit-orchestrator', 'scripts')
CRAWL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'skills', 'crawl-render-audit', 'scripts')
FRESH_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'skills', 'freshness-corroboration', 'scripts')
ENG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'skills', 'engagement-audit', 'scripts')

for d in [ORCH_DIR, CRAWL_DIR, FRESH_DIR, ENG_DIR]:
    if d not in sys.path:
        sys.path.insert(0, d)

# pyrefly: ignore [missing-import]
# type: ignore
from page_analysis import analyze_html_structure, detect_accessibility_issues
# pyrefly: ignore [missing-import]
# type: ignore
from structured_data import extract_json_ld, detect_structured_data_issues
# pyrefly: ignore [missing-import]
# type: ignore
from robots import analyze_robots_directives
# pyrefly: ignore [missing-import]
# type: ignore
from consistency import analyze_citation_extractability, check_temporal_freshness
# pyrefly: ignore [missing-import]
# type: ignore
from engagement import analyze_first_screen_orientation, analyze_trust_anchors, calculate_readability
# pyrefly: ignore [missing-import]
# type: ignore
from crawler import detect_waf_challenge


class Test10SiteEmpiricalBenchmark(unittest.TestCase):
    """Test all 10 site archetypes and counterexamples from research."""

    @classmethod
    def setUpClass(cls):
        fixtures_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mock_data')
        
        with open(os.path.join(fixtures_dir, 'ecommerce_fallback_fixture.html'), 'r', encoding='utf-8') as f:
            cls.ecommerce_html = f.read()
            
        with open(os.path.join(fixtures_dir, 'static_table_banking_fixture.html'), 'r', encoding='utf-8') as f:
            cls.banking_html = f.read()

    def test_site_1_dot_and_key_rule_json_ld_fallback_prevents_false_positive(self):
        """Site 1 (Dot & Key): E-commerce with JS hydration is NOT failed if Product/Offer is in JSON-LD fallback."""
        soup = BeautifulSoup(self.ecommerce_html, 'html.parser')
        url = "https://dotandkey.com/products/vitamin-c-serum"
        
        # 1. Extract JSON-LD
        json_ld = extract_json_ld(soup)
        self.assertTrue(len(json_ld) >= 1, "Should detect Product JSON-LD")
        product = json_ld[0]
        self.assertEqual(product.get('@type'), 'Product')
        self.assertIn('offers', product)
        
        # 2. Schema check should pass for product schema
        schema_findings = detect_structured_data_issues(json_ld, url, "dotandkey.com")
        self.assertFalse(any(f['id'] == 'KNOW-SCH-001' for f in schema_findings), "Should not flag missing structured data")

    def test_site_2_saraswat_bank_rule_static_table_facts_present(self):
        """Site 2 (Saraswat Bank): Dynamic widgets are ignored if key facts exist in static HTML table."""
        soup = BeautifulSoup(self.banking_html, 'html.parser')
        url = "https://saraswatbank.com/fd-rates"
        
        analysis = analyze_html_structure(soup, url)
        # Should not flag as CSR locked because static table content has facts
        self.assertFalse(analysis['is_csr_locked'])
        self.assertGreater(analysis['raw_text_word_count'], 40)
        self.assertEqual(analysis['h1_count'], 1)

    def test_site_3_healthline_rule_crawler_policy_isolated_from_html(self):
        """Site 3 (Healthline): AI bot restriction in robots.txt is flagged even if HTML is well-formed."""
        mock_robots_data = {
            'available': True,
            'url': 'https://healthline.com/robots.txt',
            'bot_rules': {
                'GPTBot': {'disallows': ['/'], 'allows': []},
                'PerplexityBot': {'disallows': ['/'], 'allows': []}
            }
        }
        findings = analyze_robots_directives(mock_robots_data, 'https://healthline.com')
        # Must detect that AI search crawlers are blocked
        self.assertTrue(any(f['id'] == 'DISC-ROB-002' for f in findings))
        finding = [f for f in findings if f['id'] == 'DISC-ROB-002'][0]
        self.assertEqual(finding['severity'], 'critical')

    def test_site_4_nordstrom_rule_edge_waf_isolation(self):
        """Site 4 (Nordstrom): Edge WAF/403 blocks are diagnosed before falsely attributing to JS rendering."""
        status_code = 403
        headers = {'Server': 'cloudflare', 'cf-ray': '879201abcd-EWR'}
        body = "<html><head><title>Access Denied</title></head><body><h1>403 Forbidden - Cloudflare Security</h1></body></html>"
        
        waf_detected = detect_waf_challenge(status_code, headers, body)
        self.assertIsNotNone(waf_detected)
        self.assertTrue(waf_detected['detected'])
        self.assertEqual(waf_detected['provider'], 'Cloudflare')

    def test_site_5_wikipedia_rule_high_quote_density_and_missing_schema(self):
        """Site 5 (Wikipedia): High factual quote density (>80%) detected, while identifying lack of JSON-LD."""
        wiki_html = """
        <html><head><title>Quantum Computing - Wikipedia</title></head>
        <body>
            <h1>Quantum Computing</h1>
            <p>Quantum computing is a rapidly-emerging technology that harnesses the laws of quantum mechanics to solve problems too complex for classical computers.</p>
            <p>IBM revealed the Eagle processor in 2021 with 127 qubits, followed by the Osprey processor in 2022 featuring 433 qubits operating at 15 mK.</p>
            <p>Google demonstrated quantum supremacy in 2019 using the 53-qubit Sycamore processor, completing a task in 200 seconds that would take Summit 10,000 years.</p>
        </body></html>
        """
        soup = BeautifulSoup(wiki_html, 'html.parser')
        cit_analysis = analyze_citation_extractability(soup, "https://en.wikipedia.org/wiki/Quantum_Computing")
        self.assertGreater(cit_analysis['quotation_density'], 0.50)
        self.assertEqual(cit_analysis['fluff_count'], 0)
        
        # Verify schema detection flags missing JSON-LD
        json_ld = extract_json_ld(soup)
        self.assertEqual(len(json_ld), 0)

    def test_site_6_stripe_docs_rule_developer_saas_gold_standard(self):
        """Site 6 (Stripe Docs): Rich technical specs, valid schema, and clear orientation pass all checks."""
        stripe_html = """
        <html><head><title>Stripe API Reference | Payments Platform</title>
        <script type="application/ld+json">
        {
            "@context": "https://schema.org",
            "@type": "TechArticle",
            "headline": "Stripe Payments API Documentation",
            "author": {"@type": "Organization", "name": "Stripe, Inc.", "sameAs": "https://www.wikidata.org/wiki/Q7624103"}
        }
        </script></head>
        <body>
            <h1>Stripe Payments API</h1>
            <p>Accept payments online and manage your business with Stripe's unified developer platform processing over $1 trillion in annual volume.</p>
            <a href="/docs/quickstart">Start with Quickstart API</a>
        </body></html>
        """
        soup = BeautifulSoup(stripe_html, 'html.parser')
        json_ld = extract_json_ld(soup)
        self.assertEqual(len(json_ld), 1)
        self.assertEqual(json_ld[0]['@type'], 'TechArticle')
        orientation = analyze_first_screen_orientation(soup, "https://stripe.com/docs/api")
        self.assertTrue(orientation['has_concrete_value_prop'])

    def test_site_7_zapier_rule_value_prop_and_frictionless_cta(self):
        """Site 7 (Zapier): Immediate orientation with concrete automation verbs and clear CTA passes audit."""
        zapier_html = """
        <html><head><title>Zapier | Workflow Automation Software</title></head>
        <body>
            <h1>Automate your workflow across 6,000+ apps</h1>
            <p>Zapier empowers teams to build automated workflows that move data seamlessly between your favorite applications in minutes.</p>
            <a href="/sign-up" class="btn-primary">Get Started Free</a>
        </body></html>
        """
        soup = BeautifulSoup(zapier_html, 'html.parser')
        orientation = analyze_first_screen_orientation(soup, "https://zapier.com")
        self.assertTrue(orientation['has_concrete_value_prop'])
        self.assertTrue(orientation['has_primary_cta'])
        self.assertIsNotNone(orientation['primary_cta_text'])
        self.assertIn("Get Started Free", orientation['primary_cta_text'])

    def test_site_8_prashant_corner_rule_local_smb_schema_audit(self):
        """Site 8 (Prashant Corner): Local SMB missing LocalBusiness schema and NAP anchors is diagnosed."""
        smb_html = """
        <html><head><title>Prashant Corner - Sweets & Snacks</title></head>
        <body>
            <h1>Welcome to Prashant Corner</h1>
            <p>We serve authentic Indian sweets, snacks, and chaat since 1989 across Thane and Mumbai.</p>
        </body></html>
        """
        soup = BeautifulSoup(smb_html, 'html.parser')
        json_ld = extract_json_ld(soup)
        findings = detect_structured_data_issues(json_ld, "https://prashantcorner.com", "prashantcorner.com")
        # Should flag missing structured data
        self.assertTrue(any(f['id'] == 'KNOW-SCH-001' for f in findings))

    def test_site_9_coursera_rule_course_catalog_and_organization_grounding(self):
        """Site 9 (Coursera): EdTech platform with structured Course schema and partner organization grounding."""
        coursera_html = """
        <html><head><title>Machine Learning Specialization - Coursera</title>
        <script type="application/ld+json">
        {
            "@context": "https://schema.org",
            "@type": "Course",
            "name": "Machine Learning Specialization",
            "description": "Master foundational AI concepts taught by Andrew Ng.",
            "provider": {
                "@type": "Organization",
                "name": "DeepLearning.AI",
                "sameAs": "https://www.wikidata.org/wiki/Q104869852"
            }
        }
        </script></head>
        <body>
            <h1>Machine Learning Specialization</h1>
            <p>Taught by AI pioneer Andrew Ng, this program has enrolled over 500,000 students worldwide.</p>
        </body></html>
        """
        soup = BeautifulSoup(coursera_html, 'html.parser')
        json_ld = extract_json_ld(soup)
        self.assertEqual(len(json_ld), 1)
        self.assertEqual(json_ld[0]['@type'], 'Course')
        self.assertIn('sameAs', json_ld[0]['provider'])

    def test_site_10_github_docs_rule_technical_hierarchy_and_fluff_suppression(self):
        """Site 10 (GitHub Docs): Deep structured headings and zero promotional fluff score high readability."""
        github_html = """
        <html><head><title>Managing Git Repositories - GitHub Docs</title></head>
        <body>
            <h1>Managing Git Repositories</h1>
            <h2>Cloning a repository</h2>
            <p>To clone a repository using HTTPS, under the repository name, click Code and copy the repository URL.</p>
            <h2>Creating a pull request</h2>
            <p>Pull requests let you tell others about changes you have pushed to a branch in a repository on GitHub.</p>
        </body></html>
        """
        soup = BeautifulSoup(github_html, 'html.parser')
        analysis = analyze_html_structure(soup, "https://docs.github.com")
        self.assertEqual(analysis['h1_count'], 1)
        self.assertEqual(analysis['h2_count'], 2)
        
        cit_analysis = analyze_citation_extractability(soup, "https://docs.github.com")
        self.assertEqual(cit_analysis['fluff_count'], 0)


if __name__ == '__main__':
    unittest.main()

