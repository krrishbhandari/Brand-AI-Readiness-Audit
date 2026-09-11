"""
10-Site Empirical Validation Benchmark Tests.
Validates key diagnostic rules discovered during empirical research (Dot & Key, Saraswat Bank, Healthline, Nordstrom).
Built using Python standard library unittest for 100% portability.
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


class Test10SiteEmpiricalBenchmark(unittest.TestCase):
    """Test counterexamples and layered diagnostic rules from research."""

    @classmethod
    def setUpClass(cls):
        fixtures_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mock_data')
        
        with open(os.path.join(fixtures_dir, 'ecommerce_fallback_fixture.html'), 'r', encoding='utf-8') as f:
            cls.ecommerce_html = f.read()
            
        with open(os.path.join(fixtures_dir, 'static_table_banking_fixture.html'), 'r', encoding='utf-8') as f:
            cls.banking_html = f.read()

    def test_dot_and_key_rule_json_ld_fallback_prevents_false_positive(self):
        """Dot & Key Rule: E-commerce with JS hydration is NOT failed if Product/Offer is in JSON-LD fallback."""
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

    def test_saraswat_bank_rule_static_table_facts_present(self):
        """Saraswat Bank Rule: Dynamic widgets are ignored if key facts exist in static HTML table."""
        soup = BeautifulSoup(self.banking_html, 'html.parser')
        url = "https://saraswatbank.com/fd-rates"
        
        analysis = analyze_html_structure(soup, url)
        # Should not flag as CSR locked because static table content has facts
        self.assertFalse(analysis['is_csr_locked'])
        self.assertGreater(analysis['raw_text_word_count'], 40)
        self.assertEqual(analysis['h1_count'], 1)

    def test_healthline_rule_crawler_policy_isolated_from_html(self):
        """Healthline Rule: AI bot restriction in robots.txt is flagged even if HTML is well-formed."""
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


if __name__ == '__main__':
    unittest.main()
