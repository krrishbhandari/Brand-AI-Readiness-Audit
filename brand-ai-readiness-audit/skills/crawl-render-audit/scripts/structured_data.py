"""
Structured Data Analysis Module.
Extracts and validates Schema.org JSON-LD, Microdata, entity disambiguation (sameAs), and Knowledge Graph anchors.
"""

import json
from typing import Dict, List, Optional
from bs4 import BeautifulSoup

SCHEMA_TYPES = {
    'Organization': 'Company/brand entity information',
    'Corporation': 'Corporate brand entity',
    'LocalBusiness': 'Physical business location',
    'Product': 'Product catalog information',
    'Offer': 'Pricing, currency, and availability',
    'Article': 'Authoritative articles and publications',
    'TechArticle': 'Technical documentation',
    'FAQPage': 'Frequently asked questions for direct citation',
    'BreadcrumbList': 'Navigation hierarchy',
    'WebSite': 'Website identity'
}

AUTHORITATIVE_ENTITY_DOMAINS = [
    'wikidata.org',
    'wikipedia.org',
    'crunchbase.com',
    'linkedin.com',
    'github.com',
    'twitter.com',
    'x.com'
]


def extract_json_ld(soup: BeautifulSoup) -> List[Dict]:
    """
    Extract all JSON-LD structured data objects from page scripts.
    """
    json_ld_data = []
    
    for script in soup.find_all('script', type='application/ld+json'):
        content = script.string or script.get_text()
        if content:
            try:
                data = json.loads(content.strip())
                if isinstance(data, list):
                    json_ld_data.extend(data)
                elif isinstance(data, dict):
                    if '@graph' in data and isinstance(data['@graph'], list):
                        json_ld_data.extend(data['@graph'])
                    else:
                        json_ld_data.append(data)
            except json.JSONDecodeError as e:
                json_ld_data.append({
                    '_error': True,
                    '_error_message': str(e),
                    '_raw': content[:200]
                })
    
    return json_ld_data


def validate_json_ld(data: Dict) -> List[str]:
    """
    Validate JSON-LD object for syntax and standard schema requirements.
    """
    issues = []
    if not isinstance(data, dict):
        return ['Invalid JSON-LD object structure']
    
    if data.get('_error'):
        issues.append(f"Invalid JSON-LD syntax: {data.get('_error_message', 'Parse error')}")
        return issues
    
    if '@context' not in data and '@type' not in data:
        issues.append('Missing @context or @type property')
    
    return issues


def check_entity_disambiguation(json_ld_list: List[Dict], page_url: str, domain: str = "") -> List[Dict]:
    """
    Audit Organization schema for sameAs Wikidata / Knowledge Graph disambiguation links.
    """
    findings = []
    org_found = False
    has_same_as = False
    same_as_urls = []
    has_wikidata = False
    
    for item in json_ld_list:
        if not isinstance(item, dict):
            continue
        schema_type = item.get('@type', '')
        if schema_type in ['Organization', 'Corporation', 'LocalBusiness', 'WebSite']:
            org_found = True
            same_as = item.get('sameAs', [])
            if isinstance(same_as, str):
                same_as = [same_as]
            if isinstance(same_as, list) and same_as:
                has_same_as = True
                same_as_urls.extend(same_as)
                if any('wikidata.org' in str(url) for url in same_as):
                    has_wikidata = True
    
    if not org_found:
        # If it's a product page or specific sub-page, organization is optional
        pass
    elif not has_same_as or not has_wikidata:
        findings.append({
            'id': 'KNOW-ID-001',
            'skill': 'freshness-corroboration',
            'category': 'identity',
            'severity': 'high',
            'title': 'Missing Wikidata / Knowledge Graph entity disambiguation links (sameAs)',
            'location': page_url,
            'evidence': f"Organization schema exists but lacks sameAs links to authoritative Knowledge Graphs (Wikidata / Crunchbase). LLMs risk confusing {domain or 'brand'} with similarly named entities.",
            'suggested_action': {
                'summary': 'Add sameAs array to Organization schema linking to official Wikidata QID, Wikipedia, LinkedIn, and Crunchbase profiles.',
                'priority': 'high',
                'code_snippet': '"sameAs": [\n  "https://www.wikidata.org/wiki/Q...",\n  "https://www.crunchbase.com/organization/...",\n  "https://www.linkedin.com/company/..."\n]'
            }
        })
        
    return findings


def detect_structured_data_issues(structured_data: List[Dict], page_url: str, domain: str = "") -> List[Dict]:
    """
    Detect missing or malformed structured data across pages.
    """
    findings = []
    
    if not structured_data:
        findings.append({
            'id': 'KNOW-SCH-001',
            'skill': 'freshness-corroboration',
            'category': 'structured_data',
            'severity': 'high',
            'title': 'No JSON-LD structured data detected on page',
            'location': page_url,
            'evidence': f"Crawled page {page_url}; 0 Schema.org JSON-LD blocks detected. AI assistants cannot extract structured brand facts.",
            'suggested_action': {
                'summary': 'Implement Schema.org JSON-LD markup appropriate for this page type (Organization, Product, Article, or FAQPage).',
                'priority': 'high'
            }
        })
        return findings
    
    for i, data in enumerate(structured_data):
        if not isinstance(data, dict):
            continue
        issues = validate_json_ld(data)
        if issues:
            findings.append({
                'id': f'KNOW-SYN-{i+1:03d}',
                'skill': 'freshness-corroboration',
                'category': 'structured_data',
                'severity': 'high',
                'title': f'Syntax or context error in JSON-LD ({data.get("@type", "Unknown")})',
                'location': page_url,
                'evidence': f"Errors: {'; '.join(issues)}",
                'suggested_action': {
                    'summary': 'Correct JSON-LD syntax and ensure @context: https://schema.org is declared.',
                    'priority': 'high'
                }
            })
            
    # Check entity disambiguation
    entity_findings = check_entity_disambiguation(structured_data, page_url, domain)
    findings.extend(entity_findings)
    
    return findings


def analyze_structured_data(context: Dict) -> Dict:
    """
    Analyze structured data across all crawled pages.
    """
    all_structured_data = []
    all_findings = []
    domain = context.get('site', {}).get('domain', '')
    
    for page in context.get('pages', []):
        html = page.get('html', '')
        if not html:
            continue
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
        except Exception:
            continue
        
        json_ld = extract_json_ld(soup)
        if json_ld:
            all_structured_data.extend(json_ld)
            page['structured_data'] = json_ld
        
        page_findings = detect_structured_data_issues(json_ld, page.get('url', ''), domain)
        all_findings.extend(page_findings)
    
    context['structured_data'] = all_structured_data
    context['structured_data_findings'] = all_findings
    return context
