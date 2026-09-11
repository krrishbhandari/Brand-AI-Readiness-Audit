"""
Robots.txt and AI Bot Crawlability Analysis Module.
Audits robots.txt directives for 16+ conversational AI search engines and verifies /llms.txt presence.
"""

from urllib.parse import urljoin, urlparse
from typing import Dict, List, Optional
import urllib.request
import re


AI_SEARCH_BOTS = [
    {"name": "GPTBot", "operator": "OpenAI", "critical": True, "desc": "ChatGPT Search & Grounding"},
    {"name": "ChatGPT-User", "operator": "OpenAI", "critical": True, "desc": "ChatGPT Real-Time Web Browsing"},
    {"name": "PerplexityBot", "operator": "Perplexity AI", "critical": True, "desc": "Perplexity Live Search & Citations"},
    {"name": "ClaudeBot", "operator": "Anthropic", "critical": True, "desc": "Claude Citation & Grounding Crawler"},
    {"name": "Claude-Web", "operator": "Anthropic", "critical": True, "desc": "Claude Real-Time Browsing"},
    {"name": "Applebot-Extended", "operator": "Apple", "critical": False, "desc": "Apple Intelligence Search"},
    {"name": "YouBot", "operator": "You.com", "critical": False, "desc": "You.com AI Search Engine"},
    {"name": "Bingbot", "operator": "Microsoft", "critical": True, "desc": "Bing & Copilot Web Indexer"},
]

AI_TRAINING_BOTS = [
    {"name": "CCBot", "operator": "Common Crawl", "desc": "Open Web Pre-Training Archive"},
    {"name": "Google-Extended", "operator": "Google", "desc": "Gemini Pre-Training Ingestion"},
    {"name": "Bytespider", "operator": "ByteDance", "desc": "Doubao / TikTok AI Crawler"},
    {"name": "Amazonbot", "operator": "Amazon", "desc": "Alexa / Bedrock Web Scraper"},
    {"name": "cohere-ai", "operator": "Cohere", "desc": "LLM Training & Embedding Scraper"},
    {"name": "Diffbot", "operator": "Diffbot", "desc": "Autonomous Web Knowledge Graph Crawler"},
    {"name": "Meta-ExternalAgent", "operator": "Meta", "desc": "Meta AI Model Ingestion Agent"},
]


def fetch_robots_txt(base_url: str, user_agent: str = "BrandAuditBot/1.0") -> Dict:
    """
    Fetch and parse robots.txt with standard library urllib fallback.
    """
    robots_url = urljoin(base_url, '/robots.txt')
    
    result = {
        'available': False,
        'url': robots_url,
        'content': None,
        'raw_lines': [],
        'sitemap_url': None,
        'crawl_delay': None,
        'error': None,
        'bot_rules': {}
    }
    
    try:
        req = urllib.request.Request(
            robots_url,
            headers={'User-Agent': user_agent}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                raw_bytes = response.read()
                content = raw_bytes.decode('utf-8', errors='replace')
                result['available'] = True
                result['content'] = content
                result['raw_lines'] = content.splitlines()
    except Exception as e:
        result['error'] = str(e)
    
    if result.get('raw_lines'):
        current_agent = "*"
        for line in result['raw_lines']:
            clean_line = line.split('#')[0].strip()
            if not clean_line:
                continue
            
            if clean_line.lower().startswith('sitemap:'):
                sitemap = clean_line.split(':', 1)[1].strip()
                result['sitemap_url'] = sitemap
            elif clean_line.lower().startswith('crawl-delay:'):
                try:
                    result['crawl_delay'] = float(clean_line.split(':', 1)[1].strip())
                except ValueError:
                    pass
            elif clean_line.lower().startswith('user-agent:'):
                agent = clean_line.split(':', 1)[1].strip()
                current_agent = agent
                if current_agent not in result['bot_rules']:
                    result['bot_rules'][current_agent] = {'allows': [], 'disallows': []}
            elif clean_line.lower().startswith('disallow:'):
                path = clean_line.split(':', 1)[1].strip()
                if current_agent not in result['bot_rules']:
                    result['bot_rules'][current_agent] = {'allows': [], 'disallows': []}
                result['bot_rules'][current_agent]['disallows'].append(path)
            elif clean_line.lower().startswith('allow:'):
                path = clean_line.split(':', 1)[1].strip()
                if current_agent not in result['bot_rules']:
                    result['bot_rules'][current_agent] = {'allows': [], 'disallows': []}
                result['bot_rules'][current_agent]['allows'].append(path)
                
    return result


def check_llms_txt(base_url: str, user_agent: str = "BrandAuditBot/1.0") -> Dict:
    """
    Check for the presence and validity of /llms.txt or /.well-known/llms.txt at root.
    """
    target_urls = [
        urljoin(base_url, '/llms.txt'),
        urljoin(base_url, '/.well-known/llms.txt')
    ]
    
    result = {
        'available': False,
        'url': target_urls[0],
        'content': None,
        'has_title': False,
        'has_summary': False,
        'link_count': 0
    }
    
    for llms_url in target_urls:
        try:
            req = urllib.request.Request(llms_url, headers={'User-Agent': user_agent})
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    raw_bytes = response.read()
                    content = raw_bytes.decode('utf-8', errors='replace')
                    result['available'] = True
                    result['url'] = llms_url
                    result['content'] = content
                    
                    for line in content.splitlines():
                        s = line.strip()
                        if s.startswith('# '):
                            result['has_title'] = True
                        elif s.startswith('> '):
                            result['has_summary'] = True
                        elif s.startswith('- [') and '](' in s:
                            result['link_count'] += 1
                    break
        except Exception:
            continue
    
    return result


def analyze_robots_directives(robots_data: Dict, base_url: str = "") -> List[Dict]:
    """
    Analyze robots.txt and AI bot permissions to produce standardized findings.
    Handles case-insensitive user-agent lookup and allow-overrides.
    """
    findings = []
    
    if not robots_data.get('available'):
        findings.append({
            'id': 'DISC-ROB-001',
            'skill': 'crawl-render-audit',
            'category': 'robots',
            'severity': 'medium',
            'title': 'robots.txt not accessible',
            'location': robots_data.get('url', f"{base_url}/robots.txt"),
            'evidence': f"HTTP request to /robots.txt failed: {robots_data.get('error', 'Resource unavailable')}",
            'suggested_action': {
                'summary': 'Deploy a standard robots.txt file at root declaring crawl policies and sitemap location.',
                'priority': 'medium'
            }
        })
        return findings
    
    bot_rules = robots_data.get('bot_rules', {})
    # Build case-insensitive normalized lookup
    normalized_rules = {k.lower(): v for k, v in bot_rules.items()}
    
    blocked_search_bots = []
    
    # Check wildcard * disallows
    star_entry = normalized_rules.get('*', {'disallows': [], 'allows': []})
    star_disallows = star_entry.get('disallows', [])
    star_allows = star_entry.get('allows', [])
    star_blocks_all = ('/' in star_disallows or '/*' in star_disallows) and ('/' not in star_allows)
    
    for bot in AI_SEARCH_BOTS:
        bot_name = bot['name']
        bot_key = bot_name.lower()
        is_blocked = False
        
        if bot_key in normalized_rules:
            disallows = normalized_rules[bot_key].get('disallows', [])
            allows = normalized_rules[bot_key].get('allows', [])
            if ('/' in disallows or '/*' in disallows) and ('/' not in allows):
                is_blocked = True
        elif star_blocks_all:
            is_blocked = True
            
        if is_blocked:
            blocked_search_bots.append(bot_name)
    
    if blocked_search_bots:
        bots_str = ", ".join(blocked_search_bots)
        findings.append({
            'id': 'DISC-ROB-002',
            'skill': 'crawl-render-audit',
            'category': 'robots',
            'severity': 'critical',
            'title': f'Conversational AI search crawlers blocked in robots.txt ({len(blocked_search_bots)} bots)',
            'location': robots_data.get('url', f"{base_url}/robots.txt"),
            'evidence': f"robots.txt disallows root access ('/') for AI search user-agents: {bots_str}. This prevents conversational AI engines (ChatGPT Search, Perplexity) from citing your domain.",
            'suggested_action': {
                'summary': f"Add explicit 'Allow: /' rules for verified conversational search bots: {bots_str}.",
                'priority': 'critical',
                'code_snippet': f"User-agent: GPTBot\nAllow: /\n\nUser-agent: PerplexityBot\nAllow: /\n\nUser-agent: ClaudeBot\nAllow: /\n"
            }
        })
    
    # Check for sitemap directive
    if not robots_data.get('sitemap_url'):
        findings.append({
            'id': 'DISC-ROB-003',
            'skill': 'crawl-render-audit',
            'category': 'robots',
            'severity': 'low',
            'title': 'No XML sitemap declared in robots.txt',
            'location': robots_data.get('url', f"{base_url}/robots.txt"),
            'evidence': 'robots.txt does not contain a Sitemap: directive pointing to sitemap.xml.',
            'suggested_action': {
                'summary': 'Add a Sitemap directive (e.g. Sitemap: https://domain.com/sitemap.xml) at the bottom of robots.txt to assist automated AI discovery.',
                'priority': 'low'
            }
        })
    
    return findings


def check_robots(context: Dict) -> Dict:
    """
    Check robots.txt, AI search bot accessibility, edge security challenges, and /llms.txt.
    """
    domain = context.get('site', {}).get('domain', '')
    base_url = f"https://{domain}" if domain else context.get('meta', {}).get('target_url', '')
    
    robots_data = fetch_robots_txt(base_url)
    llms_data = check_llms_txt(base_url)
    
    context['robots'] = robots_data
    context['llms_txt'] = llms_data
    
    findings = analyze_robots_directives(robots_data, base_url)
    
    # Check for Edge WAF challenges detected during crawl (Nordstrom rule)
    if context.get('edge_security', {}).get('waf_detected'):
        challenges = context['edge_security'].get('challenges', [])
        provider = challenges[0]['details'].get('provider', 'Edge WAF') if challenges else 'Edge WAF'
        findings.append({
            'id': 'DISC-EDGE-001',
            'skill': 'crawl-render-audit',
            'category': 'security',
            'severity': 'critical',
            'title': f'Edge WAF / Bot challenge blocking automated retrieval ({provider})',
            'location': base_url,
            'evidence': f"Automated requests triggered edge protection challenge or HTTP 403/429 response ({provider}). AI search crawlers without full browser challenge solvers will be blocked from indexing.",
            'suggested_action': {
                'summary': f"Configure {provider} firewall rules to whitelist verified conversational AI crawler IP ranges and user-agents (e.g. GPTBot, PerplexityBot).",
                'priority': 'critical'
            }
        })
    
    if not llms_data.get('available'):
        findings.append({
            'id': 'DISC-LLM-001',
            'skill': 'crawl-render-audit',
            'category': 'discoverability',
            'severity': 'medium',
            'title': 'No machine-readable /llms.txt context manifest found',
            'location': f"{base_url}/llms.txt",
            'evidence': 'HTTP 404 or missing /llms.txt file at site root. AI agents must crawl entire HTML trees consuming excessive token budgets.',
            'suggested_action': {
                'summary': 'Publish a curated /llms.txt file providing an H1 brand title, blockquote value proposition, and markdown links to core documentation and product tiers.',
                'priority': 'medium',
                'code_snippet': f"# {domain}\n\n> Concise 1-sentence value proposition of {domain}.\n\n## Core Documentation\n- [Docs]({base_url}/docs): Developer APIs and platform guides.\n- [Pricing]({base_url}/pricing): Subscription plans and SLAs.\n"
            }
        })
    
    context['robots']['findings'] = findings
    return context
