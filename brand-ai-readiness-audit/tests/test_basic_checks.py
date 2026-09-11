"""
Test basic checks.
Tests for URL validation, crawler configuration, and HTML analysis.
Built using Python standard library unittest for 100% portability.
"""

import unittest
import sys
import os

# Add the skills directory to path
ORCH_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'skills', 'audit-orchestrator', 'scripts')
CRAWL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'skills', 'crawl-render-audit', 'scripts')

for d in [ORCH_DIR, CRAWL_DIR]:
    if d not in sys.path:
        sys.path.insert(0, d)

# pyrefly: ignore [missing-import]
# type: ignore
from orchestrator import validate_url
# pyrefly: ignore [missing-import]
# type: ignore
from crawler import normalize_url, get_domain, is_same_domain, CrawlerConfig


class TestUrlValidation(unittest.TestCase):
    """Test URL validation."""
    
    def test_valid_https_url(self):
        """Valid HTTPS URL should pass."""
        url = "https://example.com"
        result = validate_url(url)
        self.assertEqual(result, url)
    
    def test_valid_http_url(self):
        """Valid HTTP URL should pass."""
        url = "http://example.com"
        result = validate_url(url)
        self.assertEqual(result, url)
    
    def test_domain_without_scheme(self):
        """Domain without scheme should get https."""
        url = "example.com"
        result = validate_url(url)
        self.assertEqual(result, "https://example.com")
    
    def test_trailing_slash_removed(self):
        """Trailing slash should be removed."""
        url = "https://example.com/"
        result = validate_url(url)
        self.assertEqual(result, "https://example.com")
    
    def test_empty_url_raises_error(self):
        """Empty URL should raise ValueError."""
        with self.assertRaises(ValueError):
            validate_url("")
    
    def test_invalid_url_raises_error(self):
        """Invalid URL should raise ValueError."""
        with self.assertRaises(ValueError):
            validate_url("not a url")
    
    def test_url_with_path(self):
        """URL with path should be preserved."""
        url = "https://example.com/page"
        result = validate_url(url)
        self.assertEqual(result, url)


class TestUrlNormalization(unittest.TestCase):
    """Test URL normalization."""
    
    def test_remove_tracking_params(self):
        """Tracking parameters should be removed."""
        url = "https://example.com/page?utm_source=test&utm_medium=campaign&id=123"
        normalized = normalize_url(url)
        
        self.assertNotIn('utm_source', normalized)
        self.assertNotIn('utm_medium', normalized)
        self.assertIn('id=123', normalized)
    
    def test_remove_fragment(self):
        """Fragment should be removed."""
        url = "https://example.com/page#section"
        normalized = normalize_url(url)
        self.assertNotIn('#', normalized)
    
    def test_normalize_path(self):
        """Path should be normalized."""
        url = "https://example.com/page/"
        normalized = normalize_url(url)
        self.assertEqual(normalized, "https://example.com/page")
    
    def test_remove_index_html(self):
        """index.html should be removed."""
        url = "https://example.com/index.html"
        normalized = normalize_url(url)
        self.assertNotIn('index.html', normalized)


class TestDomainExtraction(unittest.TestCase):
    """Test domain extraction."""
    
    def test_simple_domain(self):
        """Simple domain should be extracted."""
        url = "https://example.com"
        domain = get_domain(url)
        self.assertEqual(domain, "example.com")
    
    def test_www_domain(self):
        """www domain should be extracted."""
        url = "https://www.example.com"
        domain = get_domain(url)
        self.assertEqual(domain, "www.example.com")
    
    def test_domain_with_path(self):
        """Domain should be extracted without path."""
        url = "https://example.com/page"
        domain = get_domain(url)
        self.assertEqual(domain, "example.com")
    
    def test_case_insensitive(self):
        """Domain extraction should be case insensitive."""
        url = "https://EXAMPLE.COM"
        domain = get_domain(url)
        self.assertEqual(domain, "example.com")


class TestSameDomainCheck(unittest.TestCase):
    """Test same domain checking."""
    
    def test_same_domain(self):
        """Same domain should return True."""
        url = "https://example.com/page"
        base = "example.com"
        self.assertTrue(is_same_domain(url, base))
    
    def test_different_domain(self):
        """Different domain should return False."""
        url = "https://other.com/page"
        base = "example.com"
        self.assertFalse(is_same_domain(url, base))
    
    def test_subdomain(self):
        """Subdomain should be treated as different."""
        url = "https://sub.example.com/page"
        base = "example.com"
        self.assertFalse(is_same_domain(url, base))


class TestCrawlerConfig(unittest.TestCase):
    """Test crawler configuration."""
    
    def test_default_values(self):
        """Default configuration should have expected values."""
        config = CrawlerConfig()
        self.assertEqual(config.max_pages, 20)
        self.assertEqual(config.max_depth, 2)
        self.assertEqual(config.timeout, 10)
        self.assertEqual(config.delay, 1.0)
    
    def test_custom_values(self):
        """Custom configuration should override defaults."""
        config = CrawlerConfig(
            max_pages=50,
            max_depth=5,
            timeout=30,
            delay=2.0
        )
        self.assertEqual(config.max_pages, 50)
        self.assertEqual(config.max_depth, 5)
        self.assertEqual(config.timeout, 30)
        self.assertEqual(config.delay, 2.0)
    
    def test_user_agent(self):
        """User agent should be configurable."""
        config = CrawlerConfig(user_agent="CustomBot/1.0")
        self.assertEqual(config.user_agent, "CustomBot/1.0")


class TestHtmlAnalysis(unittest.TestCase):
    """Test HTML analysis functions."""
    
    def test_analyze_html_structure(self):
        """HTML structure analysis should extract key elements."""
        from bs4 import BeautifulSoup
        # pyrefly: ignore [missing-import]
        # type: ignore
        from page_analysis import analyze_html_structure
        
        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <title>Test Page Title</title>
            <meta name="description" content="Test description">
            <link rel="canonical" href="https://example.com">
            <meta property="og:title" content="OG Title">
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body>
            <h1>Main Heading</h1>
            <h2>Subheading</h2>
            <img src="image.jpg" alt="Test image">
            <a href="/page">Link</a>
        </body>
        </html>
        """
        
        soup = BeautifulSoup(html, 'html.parser')
        analysis = analyze_html_structure(soup, "https://example.com")
        
        self.assertEqual(analysis['title'], "Test Page Title")
        self.assertEqual(analysis['meta_description'], "Test description")
        self.assertEqual(analysis['canonical'], "https://example.com")
        self.assertEqual(analysis['h1_count'], 1)
        self.assertEqual(analysis['h2_count'], 1)
        self.assertEqual(analysis['images_without_alt'], 0)
        self.assertIsNotNone(analysis['viewport'])
    
    def test_missing_title_detected(self):
        """Missing title should be detected."""
        from bs4 import BeautifulSoup
        # pyrefly: ignore [missing-import]
        # type: ignore
        from page_analysis import analyze_html_structure
        
        html = "<html><body><h1>Content</h1></body></html>"
        soup = BeautifulSoup(html, 'html.parser')
        analysis = analyze_html_structure(soup, "https://example.com")
        
        self.assertIsNone(analysis['title'])
        self.assertEqual(analysis['title_length'], 0)
    
    def test_images_without_alt(self):
        """Images without alt text should be counted."""
        from bs4 import BeautifulSoup
        # pyrefly: ignore [missing-import]
        # type: ignore
        from page_analysis import analyze_html_structure
        
        html = """
        <html><body>
            <img src="img1.jpg" alt="Has alt">
            <img src="img2.jpg">
            <img src="img3.jpg">
        </body></html>
        """
        soup = BeautifulSoup(html, 'html.parser')
        analysis = analyze_html_structure(soup, "https://example.com")
        
        self.assertEqual(analysis['images_without_alt'], 2)


class TestRobotsAnalyzer(unittest.TestCase):
    """Test robots.txt directives and AI bot matrix parsing."""

    def test_blocked_ai_search_bots_detected(self):
        """Specific AI search bot disallow is detected as critical."""
        # pyrefly: ignore [missing-import]
        # type: ignore
        from robots import analyze_robots_directives
        
        mock_robots = {
            'available': True,
            'url': 'https://example.com/robots.txt',
            'sitemap_url': 'https://example.com/sitemap.xml',
            'bot_rules': {
                'GPTBot': {'disallows': ['/'], 'allows': []},
                'PerplexityBot': {'disallows': ['/'], 'allows': []}
            }
        }
        findings = analyze_robots_directives(mock_robots, 'https://example.com')
        crit_findings = [f for f in findings if f.get('severity') == 'critical']
        self.assertTrue(len(crit_findings) >= 1)
        self.assertIn('GPTBot', crit_findings[0]['evidence'])
        self.assertIn('PerplexityBot', crit_findings[0]['evidence'])

    def test_wildcard_block_with_allow_override(self):
        """Wildcard Disallow / is overridden by specific bot Allow /."""
        # pyrefly: ignore [missing-import]
        # type: ignore
        from robots import analyze_robots_directives
        
        mock_robots = {
            'available': True,
            'url': 'https://example.com/robots.txt',
            'sitemap_url': 'https://example.com/sitemap.xml',
            'bot_rules': {
                '*': {'disallows': ['/'], 'allows': []},
                'GPTBot': {'disallows': [], 'allows': ['/']},
                'PerplexityBot': {'disallows': [], 'allows': ['/']},
                'ClaudeBot': {'disallows': [], 'allows': ['/']},
                'ChatGPT-User': {'disallows': [], 'allows': ['/']},
                'Claude-Web': {'disallows': [], 'allows': ['/']},
                'Applebot-Extended': {'disallows': [], 'allows': ['/']},
                'YouBot': {'disallows': [], 'allows': ['/']},
                'Bingbot': {'disallows': [], 'allows': ['/']}
            }
        }
        findings = analyze_robots_directives(mock_robots, 'https://example.com')
        # All search bots explicitly allowed, should not trigger DISC-ROB-002
        self.assertFalse(any(f['id'] == 'DISC-ROB-002' for f in findings))

    def test_case_insensitive_agent_matching(self):
        """User-agent matching must be case insensitive (e.g. gptbot)."""
        # pyrefly: ignore [missing-import]
        # type: ignore
        from robots import analyze_robots_directives
        
        mock_robots = {
            'available': True,
            'url': 'https://example.com/robots.txt',
            'sitemap_url': 'https://example.com/sitemap.xml',
            'bot_rules': {
                'gptbot': {'disallows': ['/'], 'allows': []}
            }
        }
        findings = analyze_robots_directives(mock_robots, 'https://example.com')
        crit_findings = [f for f in findings if f.get('severity') == 'critical']
        self.assertTrue(len(crit_findings) >= 1)
        self.assertIn('GPTBot', crit_findings[0]['evidence'])

    def test_missing_sitemap_finding(self):
        """Missing sitemap in robots.txt should trigger low severity finding."""
        # pyrefly: ignore [missing-import]
        # type: ignore
        from robots import analyze_robots_directives
        
        mock_robots = {
            'available': True,
            'url': 'https://example.com/robots.txt',
            'sitemap_url': None,
            'bot_rules': {}
        }
        findings = analyze_robots_directives(mock_robots, 'https://example.com')
        self.assertTrue(any(f['id'] == 'DISC-ROB-003' for f in findings))


class TestWafAndEdgeDetection(unittest.TestCase):
    """Test Edge WAF fingerprinting and anti-bot challenge detection."""

    def test_cloudflare_waf_detected(self):
        """Cloudflare server header or challenge triggers WAF detection."""
        # pyrefly: ignore [missing-import]
        # type: ignore
        from crawler import detect_waf_challenge
        
        headers = {'Server': 'cloudflare', 'cf-ray': '8c123456789-ORD'}
        res = detect_waf_challenge(403, headers, "Just a moment... Attention Required! Cloudflare")
        self.assertIsNotNone(res)
        self.assertTrue(res['detected'])
        self.assertEqual(res['provider'], 'Cloudflare')

    def test_akamai_waf_detected(self):
        """Akamai edge transformation header is detected."""
        # pyrefly: ignore [missing-import]
        # type: ignore
        from crawler import detect_waf_challenge
        
        headers = {'Server': 'AkamaiGHost', 'x-akamai-transformed': '9 - 0 p_s'}
        res = detect_waf_challenge(403, headers, "Access Denied")
        self.assertIsNotNone(res)
        self.assertEqual(res['provider'], 'Akamai')

    def test_aws_waf_detected(self):
        """AWS CloudFront WAF header is detected."""
        # pyrefly: ignore [missing-import]
        # type: ignore
        from crawler import detect_waf_challenge
        
        headers = {'Server': 'CloudFront', 'x-amz-cf-id': 'xyz987'}
        res = detect_waf_challenge(403, headers, "403 Forbidden")
        self.assertIsNotNone(res)
        self.assertEqual(res['provider'], 'AWS CloudFront WAF')


class TestCSRAndAccessibilityFindings(unittest.TestCase):
    """Test Client-Side Rendering locks and heading hierarchy findings."""

    def test_csr_locked_empty_root_with_scripts(self):
        """Empty SPA root with multiple scripts and low words is flagged as CSR locked."""
        from bs4 import BeautifulSoup
        # pyrefly: ignore [missing-import]
        # type: ignore
        from page_analysis import analyze_html_structure, detect_accessibility_issues
        
        html = """
        <!DOCTYPE html>
        <html>
        <head><title>SPA App</title><meta name="description" content="A NextJS SPA"></head>
        <body>
            <div id="root"></div>
            <script src="/static/js/main.chunk.js"></script>
            <script src="/static/js/bundle.js"></script>
        </body>
        </html>
        """
        soup = BeautifulSoup(html, 'html.parser')
        analysis = analyze_html_structure(soup, "https://example.com/app")
        self.assertTrue(analysis['is_csr_locked'])
        
        findings = detect_accessibility_issues(analysis, "https://example.com/app")
        self.assertTrue(any(f['id'] == 'DISC-RND-001' for f in findings))

    def test_heading_hierarchy_findings(self):
        """Test missing H1 and multiple H1 detections."""
        from bs4 import BeautifulSoup
        # pyrefly: ignore [missing-import]
        # type: ignore
        from page_analysis import analyze_html_structure, detect_accessibility_issues
        
        # 0 H1
        html_no_h1 = "<html><head><title>T</title><meta name='description' content='D'></head><body><h2>H2</h2></body></html>"
        soup = BeautifulSoup(html_no_h1, 'html.parser')
        analysis = analyze_html_structure(soup, "https://example.com")
        findings = detect_accessibility_issues(analysis, "https://example.com")
        self.assertTrue(any(f['id'] == 'DISC-STR-001' for f in findings))
        
        # Multiple H1s
        html_multi_h1 = "<html><head><title>T</title><meta name='description' content='D'></head><body><h1>H1 A</h1><h1>H1 B</h1></body></html>"
        soup = BeautifulSoup(html_multi_h1, 'html.parser')
        analysis = analyze_html_structure(soup, "https://example.com")
        findings = detect_accessibility_issues(analysis, "https://example.com")
        self.assertTrue(any(f['id'] == 'DISC-STR-002' for f in findings))


if __name__ == '__main__':
    unittest.main()
