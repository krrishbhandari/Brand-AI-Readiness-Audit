"""
Freshness and Knowledge Corroboration Analysis Module.
Audits semantic structured data, entity disambiguation (sameAs),
Princeton GEO atomic quotation density, and temporal freshness signals.
"""

import re
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Buzzwords and promotional marketing fluff indicators
MARKETING_FLUFF_WORDS = {
    'revolutionary', 'world-class', 'cutting-edge', 'seamless', 'game-changing',
    'unprecedented', 'synergy', 'best-in-class', 'next-generation', 'state-of-the-art',
    'disruptive', 'paradigm', 'holistic', 'magic', 'effortless', 'supercharge',
    'ultra', 'incredible', 'miraculous', 'transformative', 'visionary'
}

# Quantitative fact markers: numbers, currencies, percentages, metric units
METRIC_PATTERNS = [
    r'\b\d+(?:\.\d+)?%',                          # Percentages: 99.9%, 15%
    r'[\$€£₹¥]\s*\d+(?:,\d{3})*(?:\.\d{2})?',     # Currencies: $99, ₹1,499, €49.90
    r'\b\d+(?:,\d{3})*(?:\.\d+)?\s*(?:USD|EUR|GBP|INR|CAD|AUD)\b', # Explicit currencies
    r'\b\d+(?:\.\d+)?\s*(?:ms|sec|min|hours?|days?|weeks?|months?|years?)\b', # Time
    r'\b\d+(?:\.\d+)?\s*(?:GB|TB|MB|KB|kbps|Mbps|Gbps|GHz|MHz)\b',          # Tech specs
    r'\b\d+(?:\.\d+)?\s*(?:x|times|fold|k|m|million|billion)\b',              # Multipliers/counts
    r'\b\d{1,3}(?:,\d{3})+\b'                     # Formatted integers: 10,000, 1,000,000
]


def normalize_text(text: str) -> str:
    """Normalize whitespace and HTML entities."""
    if not text:
        return ''
    text = re.sub(r'\s+', ' ', text).strip()
    text = text.replace('&amp;', '&').replace('&nbsp;', ' ').replace('\u00a0', ' ')
    return text


def extract_entity_identity(context: Dict) -> Dict:
    """
    Extract brand entity identity across all crawled pages.
    """
    identity = {
        'organization_names': set(),
        'descriptions': set(),
        'locations': set(),
        'contact_info': {
            'emails': set(),
            'phones': set()
        },
        'logos': set(),
        'social_profiles': set(),
        'canonical_urls': set(),
        'domains': set()
    }
    
    for page in context.get('pages', []):
        html = page.get('html', '')
        if not html:
            continue
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
        except Exception:
            continue
        
        # 1. From JSON-LD structured data
        for json_ld in page.get('structured_data', []):
            if isinstance(json_ld, dict):
                schema_type = json_ld.get('@type', '')
                if schema_type in ['Organization', 'Corporation', 'LocalBusiness', 'WebSite']:
                    if 'name' in json_ld and json_ld['name']:
                        identity['organization_names'].add(normalize_text(json_ld['name']))
                    if 'url' in json_ld and json_ld['url']:
                        identity['canonical_urls'].add(json_ld['url'])
                    if 'logo' in json_ld and json_ld['logo']:
                        logo = json_ld['logo']
                        logo_url = logo if isinstance(logo, str) else logo.get('url', '')
                        if logo_url:
                            identity['logos'].add(logo_url)
                    if 'sameAs' in json_ld and json_ld['sameAs']:
                        if isinstance(json_ld['sameAs'], list):
                            identity['social_profiles'].update([str(u) for u in json_ld['sameAs']])
                        else:
                            identity['social_profiles'].add(str(json_ld['sameAs']))
        
        # 2. From OpenGraph meta tags
        og_site_name = soup.find('meta', property='og:site_name')
        if og_site_name and og_site_name.get('content'):
            identity['organization_names'].add(normalize_text(og_site_name.get('content', '')))
        
        # 3. From Title Brand Separators
        if soup.title and soup.title.string:
            title = soup.title.string
            for separator in [' - ', ' | ', ' :: ', ' • ', ' — ']:
                if separator in title:
                    parts = title.split(separator)
                    for part in parts:
                        part = part.strip()
                        if 2 < len(part) < 35 and not part.lower().startswith(('http', 'www', 'home', 'welcome')):
                            identity['organization_names'].add(normalize_text(part))
                    break
        
        # 4. Extract Description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            identity['descriptions'].add(normalize_text(meta_desc.get('content', '')))
            
        # 5. Extract Contact Info & Phone Numbers
        text = soup.get_text()
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
        identity['contact_info']['emails'].update(emails)
        
        phone_matches = re.findall(r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
        identity['contact_info']['phones'].update(phone_matches)
        
        # 6. Canonical URLs
        canonical = soup.find('link', rel='canonical')
        if canonical and canonical.get('href'):
            identity['canonical_urls'].add(canonical.get('href', ''))
            
        domain = urlparse(page.get('url', '')).netloc
        if domain:
            identity['domains'].add(domain.lower())
    
    # Convert sets to sorted lists for JSON serialization
    serialized = {}
    for k, v in identity.items():
        if isinstance(v, set):
            serialized[k] = sorted(list(v))
        elif isinstance(v, dict):
            serialized[k] = {sk: sorted(list(sv)) for sk, sv in v.items()}
        else:
            serialized[k] = v
            
    return serialized


def analyze_citation_extractability(soup: BeautifulSoup, url: str) -> Dict:
    """
    Evaluate Atomic Quotation Density & Citability Heuristics (Princeton GEO Research).
    Measures the ratio of factual, quantitative assertions vs promotional marketing fluff.
    """
    result = {
        'total_paragraphs': 0,
        'total_sentences': 0,
        'factual_sentences': 0,
        'fluff_count': 0,
        'quotation_density': 0.0,
        'citability_score': 0,
        'sample_factual_quotes': []
    }
    
    # Extract body content elements
    body = soup.find('body')
    if not body:
        return result
    
    # Remove script, style, nav, footer from citability analysis
    content_soup = BeautifulSoup(str(body), 'html.parser')
    for tag in content_soup(['script', 'style', 'nav', 'footer', 'noscript']):
        tag.decompose()
        
    paragraphs = content_soup.find_all(['p', 'li', 'blockquote', 'dd'])
    result['total_paragraphs'] = len(paragraphs)
    
    all_sentences = []
    for p in paragraphs:
        text = p.get_text(strip=True)
        if len(text) < 20:
            continue
        # Split sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)
        for s in sentences:
            s_clean = s.strip()
            if len(s_clean) >= 15:
                all_sentences.append(s_clean)
                
    result['total_sentences'] = len(all_sentences)
    if not all_sentences:
        return result
        
    factual_count = 0
    fluff_count = 0
    sample_quotes = []
    
    for s in all_sentences:
        s_lower = s.lower()
        has_metric = any(re.search(pat, s, re.IGNORECASE) for pat in METRIC_PATTERNS)
        has_fluff = any(w in s_lower for w in MARKETING_FLUFF_WORDS)
        
        if has_fluff:
            fluff_count += 1
            
        # A sentence is an atomic factual assertion if it contains concrete numbers/metrics or exact pricing/specs
        if has_metric:
            factual_count += 1
            if len(sample_quotes) < 3:
                sample_quotes.append(s[:120])
                
    result['factual_sentences'] = factual_count
    result['fluff_count'] = fluff_count
    
    total = len(all_sentences)
    density = round(factual_count / total, 3) if total > 0 else 0.0
    result['quotation_density'] = density
    result['sample_factual_quotes'] = sample_quotes
    
    # Citability score (0-100) based on quotation density and fluff suppression
    base_citability = min(100, int(density * 200))
    fluff_penalty = min(30, fluff_count * 5)
    result['citability_score'] = max(0, min(100, base_citability - fluff_penalty + 20))
    
    return result


def check_identity_consistency(identity: Dict, domain: str) -> List[Dict]:
    """
    Check for brand identity and naming inconsistencies.
    """
    findings = []
    org_names = identity.get('organization_names', [])
    valid_names = [n for n in org_names if n and len(n) > 2]
    
    if len(valid_names) > 2:
        names_str = ", ".join(valid_names[:4])
        findings.append({
            'id': 'KNOW-ID-002',
            'skill': 'freshness-corroboration',
            'category': 'identity',
            'severity': 'medium',
            'title': f'Inconsistent brand entity names detected across pages ({len(valid_names)} variants)',
            'location': domain,
            'evidence': f"Found multiple conflicting brand representations: [{names_str}]. Inconsistent naming causes LLMs to split entity authority or hallucinate corporate structure.",
            'suggested_action': {
                'summary': f"Standardize official brand entity name across all page titles, headers, and Organization JSON-LD schemas to '{valid_names[0]}'.",
                'priority': 'medium'
            }
        })
        
    return findings


def check_temporal_freshness(context: Dict) -> List[Dict]:
    """
    Check for outdated copyright dates, stale temporal markers, and publication freshness.
    """
    findings = []
    current_year = datetime.now().year
    
    for page in context.get('pages', []):
        html = page.get('html', '')
        url = page.get('url', '')
        if not html:
            continue
            
        try:
            soup = BeautifulSoup(html, 'html.parser')
        except Exception:
            continue
            
        text = soup.get_text()
        
        # Check copyright year
        copyright_match = re.search(r'(?:©|copyright|&copy;)\s*(?:20\d{2}\s*-\s*)?(20\d{2})', text, re.IGNORECASE)
        if copyright_match:
            try:
                cp_year = int(copyright_match.group(1))
                if cp_year < current_year - 1:
                    findings.append({
                        'id': 'KNOW-DATE-001',
                        'skill': 'freshness-corroboration',
                        'category': 'freshness',
                        'severity': 'low',
                        'title': f'Outdated footer copyright year ({cp_year})',
                        'location': url,
                        'evidence': f"Page displays copyright notice '{copyright_match.group(0)}' which is older than {current_year - 1}. AI assistants interpret outdated copyright notices as abandoned or stale content.",
                        'suggested_action': {
                            'summary': f"Update copyright notice to current year ({current_year}) or use dynamic server-side year injection.",
                            'priority': 'low'
                        }
                    })
            except ValueError:
                pass
                
        # Check Schema.org dateModified freshness on articles
        for json_ld in page.get('structured_data', []):
            if isinstance(json_ld, dict):
                schema_type = json_ld.get('@type', '')
                if schema_type in ['Article', 'NewsArticle', 'TechArticle', 'BlogPosting']:
                    if 'dateModified' not in json_ld and 'datePublished' not in json_ld:
                        findings.append({
                            'id': 'KNOW-DATE-002',
                            'skill': 'freshness-corroboration',
                            'category': 'freshness',
                            'severity': 'medium',
                            'title': f'Missing datePublished / dateModified in {schema_type} structured data',
                            'location': url,
                            'evidence': f"{schema_type} JSON-LD lacks ISO-8601 publication or modification timestamps. Conversational AI models cannot determine content recency.",
                            'suggested_action': {
                                'summary': f"Add datePublished and dateModified ISO timestamps (e.g. '{datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')}') to Article schema.",
                                'priority': 'medium'
                            }
                        })
                        
    return findings


def check_citability_across_pages(context: Dict) -> List[Dict]:
    """
    Audit Atomic Quotation Density and Citability across all crawled pages.
    """
    findings = []
    
    for page in context.get('pages', []):
        html = page.get('html', '')
        url = page.get('url', '')
        if not html:
            continue
            
        try:
            soup = BeautifulSoup(html, 'html.parser')
            citability = analyze_citation_extractability(soup, url)
            page['citability_analysis'] = citability
            
            # If total sentences >= 5 and quotation density is very low (< 0.15) with promotional fluff
            if citability['total_sentences'] >= 5:
                if citability['quotation_density'] < 0.15 and citability['fluff_count'] >= 2:
                    findings.append({
                        'id': 'KNOW-CIT-001',
                        'skill': 'freshness-corroboration',
                        'category': 'citations',
                        'severity': 'high',
                        'title': 'Low atomic quotation density & promotional fluff concentration',
                        'location': url,
                        'evidence': f"Page has only {int(citability['quotation_density']*100)}% factual assertion density with {citability['fluff_count']} marketing buzzwords ({citability['total_sentences']} total sentences). Conversational AI engines (Perplexity, ChatGPT Search) cannot extract verbatim factual answers.",
                        'suggested_action': {
                            'summary': 'Structure product specifications, pricing, SLAs, and performance metrics into atomic declarative Subject-Verb-Object sentences with exact numerical precision.',
                            'priority': 'high',
                            'code_snippet': '<!-- Example Quote-Ready Pattern -->\n<p>Acme API processes 50,000 requests per second with 99.99% uptime and sub-15ms p99 latency.</p>'
                        }
                    })
        except Exception:
            continue
            
    return findings


def analyze_freshness_consistency(
    context: Dict,
    existing_findings: List[Dict] = None
) -> Tuple[Dict, List[Dict]]:
    """
    Execute full knowledge corroboration, identity consistency, citability, and freshness audit.
    """
    all_findings = []
    domain = context.get('site', {}).get('domain', '')
    
    # 1. Entity identity extraction
    identity = extract_entity_identity(context)
    context['entity_identity'] = identity
    
    # 2. Identity consistency
    id_findings = check_identity_consistency(identity, domain)
    all_findings.extend(id_findings)
    
    # 3. Temporal freshness & dates
    freshness_findings = check_temporal_freshness(context)
    all_findings.extend(freshness_findings)
    
    # 4. Atomic Quotation Density & Citability Engine
    citability_findings = check_citability_across_pages(context)
    all_findings.extend(citability_findings)
    
    context['freshness_corroboration_findings'] = all_findings
    return context, all_findings
