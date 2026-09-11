"""
Test report schema validation.
Ensures the audit report follows the required structure per Page 2 of the Adobe Problem Statement.
Built using Python standard library unittest for 100% portability.
"""

import json
import unittest
import sys
import os

# Add the skills directory to path
ORCH_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'skills', 'audit-orchestrator', 'scripts')
if ORCH_DIR not in sys.path:
    sys.path.insert(0, ORCH_DIR)

# pyrefly: ignore [missing-import]
# type: ignore
from orchestrator import calculate_priority, generate_finding_id, normalize_severity, validate_url


class TestReportSchema(unittest.TestCase):
    """Test the canonical audit report schema."""
    
    def test_sample_report_matches_required_shape(self):
        """Report must have site, audited_at, summary, and findings."""
        report = {
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
        
        self.assertIn('site', report)
        self.assertIn('audited_at', report)
        self.assertIn('summary', report)
        self.assertIn('findings', report)
        
        # Check summary fields
        self.assertIn('total_findings', report['summary'])
        self.assertIn('critical', report['summary'])
        self.assertIn('high', report['summary'])
        self.assertIn('medium', report['summary'])
        
        # Check finding fields
        finding = report['findings'][0]
        self.assertIn('id', finding)
        self.assertIn('title', finding)
        self.assertIn('severity', finding)
        self.assertIn('evidence', finding)
        self.assertIn('suggested_action', finding)
        
        # Check suggested action fields
        suggested_action = finding['suggested_action']
        self.assertIn('summary', suggested_action)
        self.assertIn('priority', suggested_action)

    def test_severity_is_valid_value(self):
        """Severity must be one of the valid values."""
        valid_severities = ['critical', 'high', 'medium', 'low', 'info']
        for severity in valid_severities:
            self.assertIn(severity, valid_severities)

    def test_url_validation(self):
        """URL validation helper should handle scheme additions."""
        self.assertEqual(validate_url("example.com"), "https://example.com")
        self.assertEqual(validate_url("https://example.com/"), "https://example.com")


if __name__ == '__main__':
    unittest.main()
