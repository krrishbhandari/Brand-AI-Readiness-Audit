"""
End-to-End Synthetic Site Audit Tests.
Verifies audit detection against mock websites with known defect patterns.
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
from engagement import analyze_first_screen_orientation, analyze_trust_anchors, calculate_readability
# pyrefly: ignore [missing-import]
# type: ignore
from orchestrator import deduplicate_findings, calculate_overall_score


class TestSyntheticSiteAudits(unittest.TestCase):
    """End-to-End verification against synthetic test fixtures."""

    @classmethod
    def setUpClass(cls):
        fixtures_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mock_data')
        
        poor_path = os.path.join(fixtures_dir, 'poor_ai_readiness_fixture.html')
        with open(poor_path, 'r', encoding='utf-8') as f:
            cls.poor_html = f.read()
            
        opt_path = os.path.join(fixtures_dir, 'optimized_brand_fixture.html')
        with open(opt_path, 'r', encoding='utf-8') as f:
            cls.opt_html = f.read()

    def test_poor_ai_readiness_fixture_triggers_critical_findings(self):
        """Poor fixture (CSR lock, no title, no schema) should trigger multiple critical/high findings."""
        soup = BeautifulSoup(self.poor_html, 'html.parser')
        url = "https://poor-fixture.example.com"
        
        # 1. Page Analysis (HTML & CSR)
        analysis = analyze_html_structure(soup, url)
        html_findings = detect_accessibility_issues(analysis, url)
        
        # Should detect missing title
        self.assertTrue(any(f['id'] == 'DISC-SEO-001' for f in html_findings), "Should detect missing title")
        # Should detect CSR render lock
        self.assertTrue(any(f['id'] == 'DISC-RND-001' for f in html_findings), "Should detect CSR render lock")
        
        # 2. Structured Data
        json_ld = extract_json_ld(soup)
        schema_findings = detect_structured_data_issues(json_ld, url, "poor-fixture.example.com")
        self.assertTrue(any('KNOW-' in f['id'] for f in schema_findings), "Should detect missing structured data")
        
        # 3. Overall Score
        all_findings = deduplicate_findings(html_findings + schema_findings)
        score = calculate_overall_score(all_findings)
        self.assertLess(score, 60, f"Poor fixture score should be penalized (score: {score})")

    def test_optimized_brand_fixture_scores_high(self):
        """Optimized fixture (valid JSON-LD, Wikidata sameAs, SSR text, trust anchors) should score high."""
        soup = BeautifulSoup(self.opt_html, 'html.parser')
        url = "https://acme-security.com"
        
        # 1. Page Analysis
        analysis = analyze_html_structure(soup, url)
        html_findings = detect_accessibility_issues(analysis, url)
        # Should not flag CSR or missing title
        self.assertFalse(any(f['id'] == 'DISC-SEO-001' for f in html_findings))
        self.assertFalse(any(f['id'] == 'DISC-RND-001' for f in html_findings))
        
        # 2. Structured Data with Wikidata sameAs
        json_ld = extract_json_ld(soup)
        self.assertTrue(len(json_ld) >= 1)
        schema_findings = detect_structured_data_issues(json_ld, url, "acme-security.com")
        # Should NOT flag missing Wikidata sameAs because it is present in fixture
        self.assertFalse(any(f['id'] == 'KNOW-ID-001' for f in schema_findings))
        
        # 3. Engagement & Trust
        orientation = analyze_first_screen_orientation(soup, url)
        trust = analyze_trust_anchors(soup)
        self.assertTrue(orientation['has_concrete_value_prop'])
        self.assertTrue(trust['has_privacy_policy'])
        self.assertTrue(trust['has_terms'])
        
        # 4. Overall Score
        all_findings = deduplicate_findings(html_findings + schema_findings)
        score = calculate_overall_score(all_findings)
        self.assertGreaterEqual(score, 80, f"Optimized fixture score should be >= 80 (score: {score})")


if __name__ == '__main__':
    unittest.main()
