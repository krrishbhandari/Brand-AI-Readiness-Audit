"""
Unit Tests for Phase 3: Knowledge Graph, Entity Disambiguation & Quotation Engine.
Tests Schema.org parsing, Wikidata sameAs disambiguation, Atomic Quotation Density, and Freshness.
Built using Python standard library unittest for 100% portability.
"""

import unittest
import sys
import os
from bs4 import BeautifulSoup

# Setup paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
FRESH_DIR = os.path.join(PROJECT_ROOT, 'skills', 'freshness-corroboration', 'scripts')
CRAWL_DIR = os.path.join(PROJECT_ROOT, 'skills', 'crawl-render-audit', 'scripts')
ORCH_DIR = os.path.join(PROJECT_ROOT, 'skills', 'audit-orchestrator', 'scripts')

for d in [FRESH_DIR, CRAWL_DIR, ORCH_DIR]:
    if d not in sys.path:
        sys.path.insert(0, d)

from structured_data import extract_json_ld, validate_json_ld, check_entity_disambiguation, detect_structured_data_issues
from consistency import (
    analyze_citation_extractability,
    extract_entity_identity,
    check_identity_consistency,
    check_temporal_freshness,
    check_citability_across_pages
)


class TestStructuredData(unittest.TestCase):
    """Test Schema.org JSON-LD extraction, @graph support, and syntax validation."""

    def test_extract_single_and_graph_json_ld(self):
        """Test extraction of both standalone and @graph JSON-LD objects."""
        html = """
        <html>
        <head>
            <script type="application/ld+json">
            {
                "@context": "https://schema.org",
                "@type": "Organization",
                "name": "Acme Corp",
                "url": "https://acme.com"
            }
            </script>
            <script type="application/ld+json">
            {
                "@context": "https://schema.org",
                "@graph": [
                    {
                        "@type": "Product",
                        "name": "Widget Pro",
                        "offers": {
                            "@type": "Offer",
                            "price": "99.00",
                            "priceCurrency": "USD"
                        }
                    },
                    {
                        "@type": "FAQPage",
                        "mainEntity": []
                    }
                ]
            }
            </script>
        </head>
        <body></body>
        </html>
        """
        soup = BeautifulSoup(html, 'html.parser')
        extracted = extract_json_ld(soup)
        self.assertEqual(len(extracted), 3)
        types = [item.get('@type') for item in extracted]
        self.assertIn('Organization', types)
        self.assertIn('Product', types)
        self.assertIn('FAQPage', types)

    def test_invalid_json_ld_syntax_handled_gracefully(self):
        """Test that syntax errors in JSON-LD are caught and flagged."""
        html = """
        <html>
        <head>
            <script type="application/ld+json">
            {
                "@context": "https://schema.org",
                "@type": "Organization",
                "name": "Broken JSON,
            }
            </script>
        </head>
        </html>
        """
        soup = BeautifulSoup(html, 'html.parser')
        extracted = extract_json_ld(soup)
        self.assertEqual(len(extracted), 1)
        self.assertTrue(extracted[0].get('_error'))
        
        issues = validate_json_ld(extracted[0])
        self.assertTrue(len(issues) >= 1)
        self.assertIn("Invalid JSON-LD syntax", issues[0])


class TestEntityDisambiguation(unittest.TestCase):
    """Test Wikidata QID sameAs Knowledge Graph entity grounding."""

    def test_missing_wikidata_sameas_triggers_finding(self):
        """Organization schema without Wikidata sameAs link triggers KNOW-ID-001."""
        json_ld = [{
            '@context': 'https://schema.org',
            '@type': 'Organization',
            'name': 'GenericBrand',
            'url': 'https://genericbrand.com'
        }]
        findings = check_entity_disambiguation(json_ld, 'https://genericbrand.com', 'genericbrand.com')
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]['id'], 'KNOW-ID-001')
        self.assertEqual(findings[0]['severity'], 'high')
        self.assertIn('Wikidata', findings[0]['evidence'])

    def test_valid_wikidata_sameas_passes(self):
        """Organization schema with official Wikidata QID link passes disambiguation check."""
        json_ld = [{
            '@context': 'https://schema.org',
            '@type': 'Organization',
            'name': 'Adobe Inc.',
            'url': 'https://adobe.com',
            'sameAs': [
                'https://www.wikidata.org/wiki/Q11463',
                'https://en.wikipedia.org/wiki/Adobe_Inc.',
                'https://www.crunchbase.com/organization/adobe'
            ]
        }]
        findings = check_entity_disambiguation(json_ld, 'https://adobe.com', 'adobe.com')
        self.assertEqual(len(findings), 0)


class TestAtomicQuotationDensity(unittest.TestCase):
    """Test Princeton GEO Atomic Quotation Density and Citability Engine."""

    def test_high_density_factual_content_scores_high(self):
        """Content with clear metrics, prices, and stats achieves high quotation density."""
        html = """
        <html>
        <body>
            <p>CloudScale API handles 50,000 requests per second with 99.99% availability.</p>
            <p>The Pro Tier costs $49.00 per month with a 14-day free trial.</p>
            <p>Global edge caching delivers median response latency under 12ms across 280 regions.</p>
            <p>Over 10,000 engineering teams use our SDK daily.</p>
        </body>
        </html>
        """
        soup = BeautifulSoup(html, 'html.parser')
        res = analyze_citation_extractability(soup, 'https://cloudscale.io')
        
        self.assertEqual(res['total_sentences'], 4)
        self.assertEqual(res['factual_sentences'], 4)
        self.assertEqual(res['fluff_count'], 0)
        self.assertEqual(res['quotation_density'], 1.0)
        self.assertGreaterEqual(res['citability_score'], 80)

    def test_promotional_fluff_triggers_citability_finding(self):
        """Marketing fluff without metrics triggers KNOW-CIT-001 finding."""
        html = """
        <html>
        <body>
            <p>We provide revolutionary, world-class solutions for seamless business synergy.</p>
            <p>Our cutting-edge next-generation platform empowers transformative digital growth.</p>
            <p>Experience game-changing, unprecedented, holistic paradigm shifts.</p>
            <p>We supercharge your brand with magic, visionary tools.</p>
            <p>Discover effortless, ultra-intuitive software designed for perfection.</p>
        </body>
        </html>
        """
        soup = BeautifulSoup(html, 'html.parser')
        res = analyze_citation_extractability(soup, 'https://fluffbrand.com')
        
        self.assertEqual(res['factual_sentences'], 0)
        self.assertGreaterEqual(res['fluff_count'], 5)
        self.assertEqual(res['quotation_density'], 0.0)
        
        mock_context = {
            'pages': [{'url': 'https://fluffbrand.com', 'html': html}]
        }
        findings = check_citability_across_pages(mock_context)
        self.assertTrue(any(f['id'] == 'KNOW-CIT-001' for f in findings))
        cit_finding = [f for f in findings if f['id'] == 'KNOW-CIT-001'][0]
        self.assertEqual(cit_finding['severity'], 'high')


class TestTemporalFreshnessAndConsistency(unittest.TestCase):
    """Test outdated copyright and brand name consistency."""

    def test_outdated_copyright_year_detected(self):
        """Copyright year older than current year - 1 is flagged."""
        html = """
        <html>
        <body>
            <p>Welcome to Vintage Software</p>
            <footer>Copyright © 2019 Vintage Inc. All rights reserved.</footer>
        </body>
        </html>
        """
        mock_context = {
            'pages': [{'url': 'https://vintage.com', 'html': html}]
        }
        findings = check_temporal_freshness(mock_context)
        self.assertTrue(any(f['id'] == 'KNOW-DATE-001' for f in findings))
        f = [x for x in findings if x['id'] == 'KNOW-DATE-001'][0]
        self.assertEqual(f['severity'], 'low')
        self.assertIn('2019', f['evidence'])

    def test_brand_name_inconsistency_detected(self):
        """Conflicting brand names across pages are flagged."""
        identity = {
            'organization_names': ['Acme Cloud', 'Acme Networks LLC', 'Acme Global Services']
        }
        findings = check_identity_consistency(identity, 'acme.com')
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]['id'], 'KNOW-ID-002')
        self.assertEqual(findings[0]['severity'], 'medium')


if __name__ == '__main__':
    unittest.main()
