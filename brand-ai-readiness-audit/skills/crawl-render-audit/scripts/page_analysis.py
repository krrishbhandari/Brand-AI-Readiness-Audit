"""
Page Analysis Module.
Analyzes HTML content for AI crawlability, JS-render locks (SSR vs CSR), SEO, and information hierarchy.
"""

import re
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def analyze_html_structure(soup: BeautifulSoup, url: str) -> Dict:
    """
    Analyze HTML structure, metadata, rendering markers, and text content.
    """
    analysis = {
        'title': None,
        'title_length': 0,
        'meta_description': None,
        'meta_description_length': 0,
        'canonical': None,
        'h1_tags': [],
        'h2_tags': [],
        'h1_count': 0,
        'h2_count': 0,
        'images': [],
        'images_without_alt': 0,
        'links': [],
        'internal_links': 0,
        'external_links': 0,
        'open_graph': {},
        'twitter_cards': {},
        'viewport': None,
        'charset': None,
        'language': None,
        'raw_text_word_count': 0,
        'is_csr_locked': False
    }
    
    # Title
    if soup.title and soup.title.string:
        analysis['title'] = soup.title.string.strip()
        analysis['title_length'] = len(analysis['title'])
    
    # Meta description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc:
        analysis['meta_description'] = meta_desc.get('content', '').strip()
        analysis['meta_description_length'] = len(analysis['meta_description'])
    
    # Canonical URL
    canonical = soup.find('link', rel='canonical')
    if canonical:
        analysis['canonical'] = canonical.get('href')
    
    # Headings
    analysis['h1_tags'] = [h1.get_text(strip=True) for h1 in soup.find_all('h1') if h1.get_text(strip=True)]
    analysis['h1_count'] = len(analysis['h1_tags'])
    analysis['h2_tags'] = [h2.get_text(strip=True) for h2 in soup.find_all('h2') if h2.get_text(strip=True)]
    analysis['h2_count'] = len(analysis['h2_tags'])
    
    # Images
    images = soup.find_all('img')
    for img in images:
        src = img.get('src', '')
        alt = img.get('alt')
        if not alt or not alt.strip():
            analysis['images_without_alt'] += 1
        analysis['images'].append({'src': src, 'alt': alt})
    
    # Links
    links = soup.find_all('a', href=True)
    base_domain = urlparse(url).netloc.lower()
    for link in links:
        href = link.get('href', '')
        text = link.get_text(strip=True)
        if not href or href.startswith('#'):
            continue
        try:
            parsed = urlparse(href)
            is_internal = parsed.netloc.lower() == base_domain if parsed.netloc else True
        except Exception:
            is_internal = True
        
        analysis['links'].append({'href': href, 'text': text, 'is_internal': is_internal})
        if is_internal:
            analysis['internal_links'] += 1
        else:
            analysis['external_links'] += 1
    
    # OpenGraph & Twitter
    for og in soup.find_all('meta', property=re.compile(r'^og:')):
        prop = og.get('property', '').replace('og:', '')
        analysis['open_graph'][prop] = og.get('content', '')
    
    for tw in soup.find_all('meta', attrs={'name': re.compile(r'^twitter:')}):
        name = tw.get('name', '').replace('twitter:', '')
        analysis['twitter_cards'][name] = tw.get('content', '')
        
    viewport = soup.find('meta', attrs={'name': 'viewport'})
    if viewport:
        analysis['viewport'] = viewport.get('content')
        
    # Word count and CSR Detection
    body = soup.find('body')
    if body:
        text = body.get_text(separator=' ', strip=True)
        words = text.split()
        analysis['raw_text_word_count'] = len(words)
        
        # Check for empty SPA root containers
        spa_roots = body.find_all(['div', 'main'], id=re.compile(r'^(root|app|__next)$'))
        scripts = soup.find_all('script')
        if spa_roots and len(words) < 50 and len(scripts) >= 2:
            analysis['is_csr_locked'] = True
            
    return analysis


def detect_accessibility_issues(analysis: Dict, url: str) -> List[Dict]:
    """
    Detect crawlability, SEO, and rendering parity findings.
    """
    findings = []
    
    # Missing title
    if not analysis['title']:
        findings.append({
            'id': 'DISC-SEO-001',
            'skill': 'crawl-render-audit',
            'category': 'html',
            'severity': 'critical',
            'title': 'Missing HTML page title tag',
            'location': url,
            'evidence': f"Page {url} has no <title> tag. AI search models cannot establish document topic.",
            'suggested_action': {
                'summary': 'Add a unique, descriptive <title> tag declaring the brand and page purpose (50-60 characters).',
                'priority': 'critical'
            }
        })
    
    # CSR Lock
    if analysis.get('is_csr_locked'):
        findings.append({
            'id': 'DISC-RND-001',
            'skill': 'crawl-render-audit',
            'category': 'rendering',
            'severity': 'high',
            'title': 'Content locked in Client-Side JavaScript Rendering (CSR)',
            'location': url,
            'evidence': f"Initial raw HTML contains only {analysis.get('raw_text_word_count', 0)} words and relies on client-side JS hydration. AI crawlers that do not execute full JS engines will see an empty page.",
            'suggested_action': {
                'summary': 'Implement Server-Side Rendering (SSR) or Static Site Generation (SSG) so critical content is present in raw HTML.',
                'priority': 'high'
            }
        })
    
    # Missing Meta Description
    if not analysis['meta_description']:
        findings.append({
            'id': 'DISC-SEO-002',
            'skill': 'crawl-render-audit',
            'category': 'html',
            'severity': 'medium',
            'title': 'Missing meta description tag',
            'location': url,
            'evidence': f"No <meta name='description'> found on {url}.",
            'suggested_action': {
                'summary': 'Add a 150-160 character meta description summarizing key capabilities for snippet generation.',
                'priority': 'medium'
            }
        })
    
    # Heading issues
    if analysis['h1_count'] == 0:
        findings.append({
            'id': 'DISC-STR-001',
            'skill': 'crawl-render-audit',
            'category': 'html',
            'severity': 'medium',
            'title': 'Missing primary H1 heading tag',
            'location': url,
            'evidence': f"0 <h1> tags found on {url}. AI parsers cannot identify the primary topic hierarchy.",
            'suggested_action': {
                'summary': 'Add exactly one <h1> tag communicating the core value proposition of the page.',
                'priority': 'medium'
            }
        })
    elif analysis['h1_count'] > 1:
        findings.append({
            'id': 'DISC-STR-002',
            'skill': 'crawl-render-audit',
            'category': 'html',
            'severity': 'low',
            'title': 'Multiple H1 headings detected',
            'location': url,
            'evidence': f"Found {analysis['h1_count']} <h1> tags on {url}. Best practice for machine parsing is a single <h1>.",
            'suggested_action': {
                'summary': 'Retain a single primary <h1> tag and convert secondary sections to <h2> and <h3> tags.',
                'priority': 'low'
            }
        })
        
    # Images without alt text
    if analysis['images_without_alt'] > 0:
        total_imgs = len(analysis['images'])
        findings.append({
            'id': 'DISC-IMG-001',
            'skill': 'crawl-render-audit',
            'category': 'accessibility',
            'severity': 'medium',
            'title': f'Images missing descriptive alt text ({analysis["images_without_alt"]}/{total_imgs})',
            'location': url,
            'evidence': f"{analysis['images_without_alt']} of {total_imgs} images lack 'alt' attributes. Critical facts or diagrams embedded in graphics are inaccessible to AI crawlers.",
            'suggested_action': {
                'summary': 'Add descriptive alt text to all informational images and transcribe text embedded in diagrams.',
                'priority': 'medium'
            }
        })
        
    return findings


def analyze_pages(context: Dict) -> List[Dict]:
    """
    Analyze all crawled pages and return normalized findings.
    """
    all_findings = []
    
    if 'robots' in context and 'findings' in context['robots']:
        all_findings.extend(context['robots']['findings'])
        
    if 'structured_data_findings' in context:
        all_findings.extend(context['structured_data_findings'])
        
    for page in context.get('pages', []):
        html = page.get('html', '')
        if not html:
            continue
        try:
            soup = BeautifulSoup(html, 'html.parser')
            analysis = analyze_html_structure(soup, page.get('url', ''))
            page['html_analysis'] = analysis
            page_findings = detect_accessibility_issues(analysis, page.get('url', ''))
            all_findings.extend(page_findings)
        except Exception:
            continue
            
    return all_findings
