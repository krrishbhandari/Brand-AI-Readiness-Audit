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


if __name__ == '__main__':
    unittest.main()
