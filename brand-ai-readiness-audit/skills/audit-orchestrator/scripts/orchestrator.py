"""
Audit Orchestrator - Designated Master Entrypoint for Brand AI-Readiness Audit Marketplace.
Coordinates specialized sub-skills (crawl-render-audit, freshness-corroboration, engagement-audit),
deduplicates findings, calculates severity metrics, and emits the standardized JSON report (Page 2 schema).
"""

import json
import sys
import os
import time
import hashlib
import importlib.util
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse

# Define paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
SKILLS_DIR = os.path.dirname(BASE_DIR)

crawl_render_path = os.path.join(SKILLS_DIR, 'crawl-render-audit', 'scripts')
freshness_path = os.path.join(SKILLS_DIR, 'freshness-corroboration', 'scripts')
engagement_path = os.path.join(SKILLS_DIR, 'engagement-audit', 'scripts')

for p in [crawl_render_path, freshness_path, engagement_path, SCRIPT_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

# Import sub-skill engines
from crawler import crawl_website, CrawlerConfig, normalize_url, get_domain
from robots import check_robots
from structured_data import analyze_structured_data
from page_analysis import analyze_pages
from consistency import analyze_freshness_consistency
from engagement import analyze_engagement


def validate_url(url: str) -> str:
    """
    Validate and normalize input URL.
    """
    if not url:
        raise ValueError("URL cannot be empty")
    
    # Add scheme if missing
    if not url.startswith(('http://', 'https://')):
        url = f"https://{url}"
    
    parsed = urlparse(url)
    if not parsed.netloc:
        raise ValueError(f"Invalid URL: {url}")
    
    netloc = parsed.netloc.lower()
    if '.' not in netloc and not netloc.startswith('localhost'):
        raise ValueError(f"Invalid URL: {url}")
    
    if url.endswith('/'):
        url = url[:-1]
    
    return url


def normalize_severity(severity: str) -> str:
    """
    Normalize severity to one of standard values: critical, high, medium, low, info.
    """
    valid_severities = ['critical', 'high', 'medium', 'low', 'info']
    severity_lower = str(severity).lower().strip()
    
    if severity_lower in valid_severities:
        return severity_lower
    
    severity_map = {
        'error': 'high',
        'warning': 'medium',
        'notice': 'low',
        'debug': 'info',
        'major': 'high',
        'minor': 'low'
    }
    return severity_map.get(severity_lower, 'info')


def calculate_priority(finding: Dict) -> int:
    """
    Calculate numerical priority score (1-100, higher = more urgent).
    """
    severity_scores = {
        'critical': 90,
        'high': 70,
        'medium': 50,
        'low': 30,
        'info': 10
    }
    
    sev = normalize_severity(finding.get('severity', 'info'))
    base_score = severity_scores.get(sev, 10)
    
    category_multipliers = {
        'robots': 1.2,
        'rendering': 1.15,
        'identity': 1.1,
        'structured_data': 1.1,
        'orientation': 1.1,
        'html': 1.0,
        'trust': 1.0,
        'readability': 0.9,
        'freshness': 0.8
    }
    
    category = finding.get('category', '')
    multiplier = category_multipliers.get(category, 1.0)
    
    return min(100, max(1, int(base_score * multiplier)))


def generate_finding_id(finding: Dict) -> str:
    """
    Generate a unique, deterministic finding ID.
    """
    skill = finding.get('skill', 'audit')
    cat = finding.get('category', 'gen')
    title = finding.get('title', '')
    loc = finding.get('location', '')
    
    raw = f"{skill}|{cat}|{title}|{loc}"
    h = hashlib.md5(raw.encode('utf-8')).hexdigest()[:8]
    
    prefix = "DISC" if "crawl" in skill else ("KNOW" if "freshness" in skill else ("ENG" if "engagement" in skill else "AUD"))
    return f"{prefix}-{h}"


def deduplicate_findings(findings: List[Dict]) -> List[Dict]:
    """
    Deduplicate findings while standardizing the suggested_action structure.
    """
    seen = {}
    unique_findings = []
    
    for finding in findings:
        signature = f"{finding.get('category', '')}-{finding.get('title', '')}-{finding.get('location', '')}"
        
        if signature not in seen:
            seen[signature] = True
            
            # Ensure required schema structure
            finding_copy = dict(finding)
            
            if 'id' not in finding_copy or not finding_copy['id']:
                finding_copy['id'] = generate_finding_id(finding_copy)
                
            finding_copy['severity'] = normalize_severity(finding_copy.get('severity', 'info'))
            
            # Format suggested_action object
            if 'suggested_action' not in finding_copy or not isinstance(finding_copy['suggested_action'], dict):
                rec_text = finding_copy.get('recommendation') or finding_copy.get('description') or "Implement standard web and AI readiness best practices."
                finding_copy['suggested_action'] = {
                    'summary': rec_text,
                    'priority': finding_copy['severity']
                }
            else:
                sa = dict(finding_copy['suggested_action'])
                if 'summary' not in sa:
                    sa['summary'] = finding_copy.get('recommendation', 'Implement recommended remediation.')
                if 'priority' not in sa:
                    sa['priority'] = finding_copy['severity']
                finding_copy['suggested_action'] = sa
                
            unique_findings.append(finding_copy)
            
    return unique_findings


def calculate_overall_score(findings: List[Dict]) -> int:
    """
    Calculate composite AI readiness score (0-100) using the severity matrix deductions.
    """
    score = 100
    deductions = {
        'critical': 25,
        'high': 12,
        'medium': 5,
        'low': 2,
        'info': 0
    }
    
    for f in findings:
        sev = normalize_severity(f.get('severity', 'info'))
        score -= deductions.get(sev, 0)
        
    return max(0, min(100, score))


def generate_proactive_recommendations(context: Dict, findings: List[Dict]) -> List[Dict]:
    """
    Synthesize strategic proactive improvements that go beyond detected defects.
    """
    recs = []
    domain = context.get('site', {}).get('domain', 'example.com')
    
    # 1. /llms.txt Generator Recipe
    llms_data = context.get('llms_txt', {})
    if not llms_data.get('available'):
        recs.append({
            'id': 'PROACT-LLM-001',
            'title': 'Publish standardized /llms.txt machine-readable manifest',
            'summary': f"Deploy a curated /llms.txt at root containing an executive summary of {domain}, product tiers, and direct links to documentation to minimize LLM token consumption.",
            'priority': 'medium',
            'impact': 'high'
        })
        
    # 2. Unified Schema.org @graph entity linking
    recs.append({
        'id': 'PROACT-SCH-002',
        'title': 'Implement unified Schema.org @graph entity graph linking',
        'summary': 'Link Organization, WebSite, Product, and FAQPage nodes inside a single JSON-LD @graph tree with unambiguous sameAs Wikidata entity identifiers.',
        'priority': 'medium',
        'impact': 'high'
    })
    
    # 3. Atomic Quotation & Citation Snippet Structuring
    recs.append({
        'id': 'PROACT-CIT-003',
        'title': 'Format core value propositions into atomic quote-ready statements',
        'summary': 'Structure product specifications, pricing tiers, and SLA metrics into atomic declarative sentences with numerical precision for zero-ambiguity AI assistant citation.',
        'priority': 'low',
        'impact': 'medium'
    })
    
    return recs


def run_audit(
    url: str,
    max_pages: int = 20,
    max_depth: int = 2,
    timeout: int = 10,
    delay: float = 0.5,
    user_agent: str = "BrandAuditBot/1.0 (AI-Readiness-Audit)"
) -> Dict:
    """
    Run complete audit pipeline and emit standardized JSON report conforming to Page 2 schema.
    """
    start_time = time.time()
    normalized_url = validate_url(url)
    domain = get_domain(normalized_url)
    
    config = CrawlerConfig(
        max_pages=max_pages,
        max_depth=max_depth,
        timeout=timeout,
        delay=delay,
        user_agent=user_agent
    )
    
    # Execute Pipeline
    context = crawl_website(normalized_url, config)
    context = check_robots(context)
    context = analyze_structured_data(context)
    crawl_findings = analyze_pages(context)
    context, freshness_findings = analyze_freshness_consistency(context, crawl_findings)
    context, engagement_findings = analyze_engagement(context, crawl_findings)
    
    # Collect and normalize
    raw_findings = crawl_findings + freshness_findings + engagement_findings
    all_findings = deduplicate_findings(raw_findings)
    
    # Calculate priorities
    for f in all_findings:
        f['priority'] = calculate_priority(f)
    all_findings.sort(key=lambda x: x.get('priority', 0), reverse=True)
    
    # Calculate severity counts
    severity_counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0, 'info': 0}
    for f in all_findings:
        sev = f.get('severity', 'info')
        if sev in severity_counts:
            severity_counts[sev] += 1
            
    proactive_recs = generate_proactive_recommendations(context, all_findings)
    readiness_score = calculate_overall_score(all_findings)
    duration = time.time() - start_time
    
    # Format canonical JSON output strictly matching Page 2 schema
    report = {
        "site": domain,
        "audited_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "total_findings": len(all_findings),
            "critical": severity_counts['critical'],
            "high": severity_counts['high'],
            "medium": severity_counts['medium'],
            "low": severity_counts['low'],
            "ai_readiness_score": readiness_score
        },
        "findings": all_findings,
        "proactive_recommendations": proactive_recs,
        "meta": {
            "version": "1.0.0",
            "target_url": normalized_url,
            "pages_crawled": len(context.get('pages', [])),
            "duration_seconds": round(duration, 2)
        }
    }
    
    return report


def save_report(report: Dict, output_path: str = None) -> str:
    """Save audit report to JSON file."""
    if not output_path:
        domain = report.get('site', 'domain').replace('.', '_')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = f"audit_report_{domain}_{timestamp}.json"
        
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
        
    return output_path


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Run brand AI readiness audit')
    parser.add_argument('url', help='Target website URL or domain')
    parser.add_argument('--max-pages', type=int, default=15, help='Maximum pages to crawl')
    parser.add_argument('--max-depth', type=int, default=2, help='Maximum crawl depth')
    parser.add_argument('--timeout', type=int, default=8, help='Request timeout in seconds')
    parser.add_argument('--delay', type=float, default=0.5, help='Delay between requests')
    parser.add_argument('--output', '-o', help='Output JSON file path')
    
    args = parser.parse_args()
    
    try:
        report = run_audit(
            url=args.url,
            max_pages=args.max_pages,
            max_depth=args.max_depth,
            timeout=args.timeout,
            delay=args.delay
        )
        saved_file = save_report(report, args.output)
        print(f"\nAudit complete for {report['site']} in {report['meta']['duration_seconds']}s")
        print(f"Total Findings: {report['summary']['total_findings']} | AI Readiness Score: {report['summary']['ai_readiness_score']}/100")
        print(f"Report saved to: {saved_file}")
    except Exception as e:
        print(f"Error executing audit: {e}", file=sys.stderr)
        sys.exit(1)
