"""
Crawler Module for Conservative, Fact-Aware Website Crawling.
Implements same-domain crawling, WAF/Edge detection, and polite traversal limits.
"""

import time
import re
from urllib.parse import urljoin, urlparse, parse_qs, urlencode, urlunparse
from collections import deque
from typing import Dict, List, Optional, Set
import urllib.request
from bs4 import BeautifulSoup

TRACKING_PARAMS = {
    'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
    'fbclid', 'gclid', 'mc_cid', 'mc_eid', 'ref', 'source', 'medium',
    'campaign', 'term', 'content', '_ga', '_gl', 'hsa_cam', 'hsa_grp',
    'hsa_mt', 'hsa_src', 'hsa_ad', 'hsa_acc', 'hsa_net', 'hsa_ver',
    'hsa_la', 'hsa_ol', 'hsa_kw', 'hsa_tgt', 'hsa_cam_id', 'hsa_ad_id',
    'hsa_ad_set_id', 'hsa_net_id', 'hsa_ver_id', 'hsa_la_id', 'hsa_ol_id',
    'hsa_kw_id', 'hsa_tgt_id'
}


class CrawlerConfig:
    """Configuration for conservative, high-performance crawling."""
    def __init__(
        self,
        max_pages: int = 20,
        max_depth: int = 2,
        timeout: int = 10,
        delay: float = 1.0,
        user_agent: str = "BrandAuditBot/1.0"
    ):
        self.max_pages = max_pages
        self.max_depth = max_depth
        self.timeout = timeout
        self.delay = delay
        self.user_agent = user_agent


def normalize_url(url: str) -> str:
    """Normalize URL by removing tracking parameters, fragments, and trailing slashes."""
    if not url:
        return ""
    if not url.startswith(('http://', 'https://')):
        url = f"https://{url}"
        
    parsed = urlparse(url)
    parsed = parsed._replace(fragment='')
    
    query_params = parse_qs(parsed.query)
    cleaned_params = {
        k: v for k, v in query_params.items() 
        if k.lower() not in TRACKING_PARAMS
    }
    
    new_query = urlencode(cleaned_params, doseq=True) if cleaned_params else ''
    parsed = parsed._replace(query=new_query)
    
    path = parsed.path
    if path != '/' and path.endswith('/'):
        path = path[:-1]
    path = re.sub(r'/index\.(html?|php)$', '', path, flags=re.IGNORECASE)
    parsed = parsed._replace(path=path)
    
    return urlunparse(parsed)


def get_domain(url: str) -> str:
    """Extract domain host from URL."""
    parsed = urlparse(url)
    return parsed.netloc.lower()


def is_same_domain(url: str, base_domain: str) -> bool:
    """Check if URL belongs to the same base domain."""
    return get_domain(url) == base_domain.lower()


def detect_waf_challenge(status_code: int, headers: Dict, body_text: str) -> Optional[Dict]:
    """
    Detect Edge WAF / Bot challenge blocks (Nordstrom rule from research).
    """
    is_waf = False
    provider = "Generic WAF"
    
    # Header signatures
    server = headers.get('Server', '').lower()
    if 'cloudflare' in server or 'cf-ray' in headers:
        provider = "Cloudflare"
    elif 'akamai' in server or 'x-akamai-transformed' in headers:
        provider = "Akamai"
    elif 'fastly' in server or 'x-fastly-request-id' in headers:
        provider = "Fastly"
    elif 'aws' in server or 'x-amz-cf-id' in headers:
        provider = "AWS CloudFront WAF"
        
    # Status and body signatures
    if status_code in [403, 429]:
        is_waf = True
    elif re.search(r'(cf-browser-verification|challenge-platform|turnstile|attention required|just a moment\.\.\.|access denied|captcha)', body_text[:1000], re.IGNORECASE):
        is_waf = True
        
    if is_waf:
        return {
            'detected': True,
            'provider': provider,
            'status_code': status_code,
            'reason': f"Edge security challenge or HTTP {status_code} encountered ({provider})."
        }
    return None


def fetch_page(url: str, config: CrawlerConfig) -> Dict:
    """
    Fetch single page with headers and WAF inspection.
    """
    result = {
        'url': url,
        'status_code': 0,
        'html': '',
        'headers': {},
        'error': None,
        'waf_challenge': None
    }
    
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': config.user_agent,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9'
            }
        )
        with urllib.request.urlopen(req, timeout=config.timeout) as response:
            result['status_code'] = response.status
            result['headers'] = dict(response.headers)
            raw_bytes = response.read()
            html = raw_bytes.decode('utf-8', errors='replace')
            result['html'] = html
            
            waf = detect_waf_challenge(response.status, result['headers'], html)
            if waf:
                result['waf_challenge'] = waf
    except urllib.error.HTTPError as e:
        result['status_code'] = e.code
        result['headers'] = dict(e.headers) if hasattr(e, 'headers') else {}
        err_body = ""
        try:
            err_body = e.read().decode('utf-8', errors='replace')
        except Exception:
            pass
        waf = detect_waf_challenge(e.code, result['headers'], err_body)
        result['waf_challenge'] = waf
        result['error'] = f"HTTP {e.code}: {e.reason}"
    except Exception as e:
        result['error'] = str(e)
        
    return result


def extract_internal_links(html: str, base_url: str, base_domain: str) -> List[str]:
    """Extract and normalize internal crawlable links."""
    links = set()
    try:
        soup = BeautifulSoup(html, 'html.parser')
        for a in soup.find_all('a', href=True):
            href = a['href'].strip()
            if not href or href.startswith(('#', 'javascript:', 'mailto:', 'tel:')):
                continue
            full_url = urljoin(base_url, href)
            norm_url = normalize_url(full_url)
            if is_same_domain(norm_url, base_domain):
                # Avoid binary assets and image files
                if not re.search(r'\.(pdf|jpg|jpeg|png|gif|svg|zip|tar|gz|mp4|webm|css|js)$', norm_url, re.IGNORECASE):
                    links.add(norm_url)
    except Exception:
        pass
    return list(links)


def crawl_website(start_url: str, config: CrawlerConfig = None) -> Dict:
    """
    Perform a polite, breadth-first crawl of internal pages within limits.
    """
    if config is None:
        config = CrawlerConfig()
        
    start_url = normalize_url(start_url)
    base_domain = get_domain(start_url)
    
    context = {
        'meta': {
            'target_url': start_url,
            'start_time': time.time(),
            'version': '1.0.0'
        },
        'site': {
            'input_url': start_url,
            'normalized_url': start_url,
            'domain': base_domain,
            'scheme': urlparse(start_url).scheme or 'https'
        },
        'pages': [],
        'edge_security': {
            'waf_detected': False,
            'challenges': []
        }
    }
    
    visited: Set[str] = set()
    queue = deque([(start_url, 0)])
    
    while queue and len(visited) < config.max_pages:
        current_url, depth = queue.popleft()
        if current_url in visited:
            continue
            
        visited.add(current_url)
        page_result = fetch_page(current_url, config)
        context['pages'].append(page_result)
        
        # Check WAF
        if page_result.get('waf_challenge'):
            context['edge_security']['waf_detected'] = True
            context['edge_security']['challenges'].append({
                'url': current_url,
                'details': page_result['waf_challenge']
            })
            
        # Discover deeper links if within depth limit
        if depth < config.max_depth and page_result.get('html'):
            new_links = extract_internal_links(page_result['html'], current_url, base_domain)
            for link in new_links:
                if link not in visited:
                    queue.append((link, depth + 1))
                    
        if config.delay > 0:
            time.sleep(config.delay)
            
    return context
