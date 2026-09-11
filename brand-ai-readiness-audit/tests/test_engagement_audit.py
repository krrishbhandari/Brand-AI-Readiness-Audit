"""
Unit Tests for Phase 4: Human Engagement, Orientation & Trust Engine.
Tests above-the-fold value clarity, Flesch-Kincaid readability, signal-to-noise, and trust anchors.
Built using Python standard library unittest for 100% portability.
"""

import unittest
import sys
import os
from bs4 import BeautifulSoup

# Setup paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
ENG_DIR = os.path.join(PROJECT_ROOT, 'skills', 'engagement-audit', 'scripts')
ORCH_DIR = os.path.join(PROJECT_ROOT, 'skills', 'audit-orchestrator', 'scripts')

for d in [ENG_DIR, ORCH_DIR]:
    if d not in sys.path:
        sys.path.insert(0, d)

from engagement import (
    count_syllables,
    calculate_readability,
    analyze_first_screen_orientation,
    analyze_trust_anchors,
    analyze_engagement
)


class TestReadabilityEngine(unittest.TestCase):
    """Test syllable counting and Flesch-Kincaid readability calculations."""

    def test_syllable_counter(self):
        """Test accuracy of pure-Python syllable counter."""
        self.assertEqual(count_syllables("cat"), 1)
        self.assertEqual(count_syllables("developer"), 4)
        self.assertEqual(count_syllables("transformation"), 4)
        self.assertEqual(count_syllables("AI"), 1)

    def test_accessible_copy_scores_healthy_grade(self):
        """Clean, accessible copy targets grade 7-9 and high reading ease."""
        text = "Our software helps teams build web apps faster. You can connect your database in two minutes. Start your free trial today."
        stats = calculate_readability(text)
        self.assertGreater(stats['reading_ease'], 65.0)
        self.assertLessEqual(stats['grade_level'], 10.0)

    def test_dense_academic_copy_scores_high_grade(self):
        """Dense polysyllabic jargon scores high grade level and low reading ease."""
        text = """
        The epistemological paradigm shifts fundamentally necessitate unprecedented multidimensional architectural conceptualizations,
        thereby manifesting multifaceted institutional implementations characterized by hyper-specialized algorithmic optimization protocols.
        """
        stats = calculate_readability(text)
        self.assertLess(stats['reading_ease'], 35.0)
        self.assertGreater(stats['grade_level'], 14.0)


class TestFirstScreenOrientation(unittest.TestCase):
    """Test above-the-fold value proposition and Call-to-Action detection."""

    def test_clear_value_prop_and_cta_detected(self):
        """Hero with concrete software capability and CTA passes orientation check."""
        html = """
        <html>
        <body>
            <header><nav><a href="/">Home</a></nav></header>
            <h1>Developer Analytics Platform</h1>
            <p>Our platform automates infrastructure monitoring and provides real-time security intelligence for engineering teams.</p>
            <a href="/signup" class="btn">Get Started Free</a>
        </body>
        </html>
        """
        soup = BeautifulSoup(html, 'html.parser')
        res = analyze_first_screen_orientation(soup, "https://acme.io")
        self.assertTrue(res['has_concrete_value_prop'])
        self.assertTrue(res['has_primary_cta'])
        self.assertEqual(res['h1_text'], "Developer Analytics Platform")

    def test_vague_value_prop_triggers_finding(self):
        """Hero with ambiguous slogan triggers ENG-VAL-001 finding."""
        html = """
        <html>
        <body>
            <h1>Innovation Redefined</h1>
            <p>Dreaming the future of possibilities today.</p>
        </body>
        </html>
        """
        mock_context = {
            'meta': {'target_url': 'https://vague.io'},
            'site': {'domain': 'vague.io'},
            'pages': [{'url': 'https://vague.io', 'html': html}]
        }
        _, findings = analyze_engagement(mock_context)
        self.assertTrue(any(f['id'] == 'ENG-VAL-001' for f in findings))
        f = [x for x in findings if x['id'] == 'ENG-VAL-001'][0]
        self.assertEqual(f['severity'], 'medium')


class TestTrustAnchors(unittest.TestCase):
    """Test essential privacy, terms, contact, and security signals."""

    def test_complete_trust_anchors_pass(self):
        """Page with Privacy Policy, Terms, and contact email passes trust audit."""
        html = """
        <html>
        <body>
            <p>Welcome</p>
            <footer>
                <a href="/privacy-policy">Privacy Policy</a>
                <a href="/terms-of-service">Terms of Service</a>
                <a href="mailto:support@acme.com">Contact Support</a>
            </footer>
        </body>
        </html>
        """
        soup = BeautifulSoup(html, 'html.parser')
        trust = analyze_trust_anchors(soup)
        self.assertTrue(trust['has_privacy_policy'])
        self.assertTrue(trust['has_terms'])
        self.assertTrue(trust['has_contact_info'])

    def test_missing_privacy_and_terms_triggers_finding(self):
        """Homepage missing Privacy Policy and Terms triggers ENG-TRU-001."""
        html = """
        <html>
        <body>
            <p>Welcome to NoTrust Brand</p>
            <footer>Copyright © 2026</footer>
        </body>
        </html>
        """
        mock_context = {
            'meta': {'target_url': 'https://notrust.com'},
            'site': {'domain': 'notrust.com'},
            'pages': [{'url': 'https://notrust.com', 'html': html}]
        }
        _, findings = analyze_engagement(mock_context)
        self.assertTrue(any(f['id'] == 'ENG-TRU-001' for f in findings))
        f = [x for x in findings if x['id'] == 'ENG-TRU-001'][0]
        self.assertEqual(f['severity'], 'high')


if __name__ == '__main__':
    unittest.main()
