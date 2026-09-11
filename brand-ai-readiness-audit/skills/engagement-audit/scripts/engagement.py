"""
Engagement, Visitor Retention, and Readability Analysis Module.
Audits above-the-fold value clarity, Flesch-Kincaid readability, signal-to-noise ratio, and essential trust signals.
"""

import re
import math
from typing import Dict, List, Optional, Tuple
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def count_syllables(word: str) -> int:
    """Estimate syllable count in a word."""
    word = word.lower().strip()
    if len(word) <= 3:
        return 1
    word = re.sub(r'(?:[^laeiouy]|ed|es|e)$', '', word)
    word = re.sub(r'^y', '', word)
    matches = re.findall(r'[aeiouy]{1,2}', word)
    return max(1, len(matches))


def calculate_readability(text: str) -> Dict:
    """
    Calculate Flesch Reading Ease and Flesch-Kincaid Grade Level.
    """
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
    words = [w.strip() for w in re.findall(r'\b[a-zA-Z]+\b', text) if w.strip()]
    
    total_sentences = max(1, len(sentences))
    total_words = max(1, len(words))
    total_syllables = sum(count_syllables(w) for w in words)
    
    words_per_sentence = total_words / total_sentences
    syllables_per_word = total_syllables / total_words
    
    # Standard Flesch formulas
    reading_ease = 206.835 - (1.015 * words_per_sentence) - (84.6 * syllables_per_word)
    grade_level = (0.39 * words_per_sentence) + (11.8 * syllables_per_word) - 15.59
    
    reading_ease = max(0.0, min(100.0, round(reading_ease, 1)))
    grade_level = max(1.0, min(20.0, round(grade_level, 1)))
    
    return {
        'total_words': total_words,
        'total_sentences': total_sentences,
        'words_per_sentence': round(words_per_sentence, 1),
        'reading_ease': reading_ease,
        'grade_level': grade_level
    }


def analyze_first_screen_orientation(soup: BeautifulSoup, url: str) -> Dict:
    """
    Analyze above-the-fold value proposition and primary action signals.
    """
    orientation = {
        'h1_text': None,
        'first_500_chars': '',
        'has_concrete_value_prop': False,
        'has_primary_cta': False,
        'primary_cta_text': None,
        'has_nav': False
    }
    
    h1 = soup.find('h1')
    if h1:
        orientation['h1_text'] = h1.get_text(strip=True)
        
    # Get clean text
    for elem in soup(['script', 'style', 'noscript', 'svg']):
        elem.extract()
        
    body = soup.find('body')
    if body:
        visible_text = body.get_text(separator=' ', strip=True)
        orientation['first_500_chars'] = visible_text[:500]
        
        # Check for concrete value positioning patterns
        val_patterns = [
            r'\b(platform|software|api|tool|service|solution|analytics|automation|intelligence|security|infrastructure|agent|bank|account|skincare|serum|course|learning|product)\b',
            r'\b(built for|designed to|helps|enables|automates|manages|secures|scales|provides|offers|features|rates|effective|brightening)\b'
        ]
        if all(re.search(pat, visible_text[:600], re.IGNORECASE) for pat in val_patterns):
            orientation['has_concrete_value_prop'] = True
            
    # Check for CTA buttons
    buttons = soup.find_all(['button', 'a'], string=re.compile(r'(?:get started|start free|try|demo|sign up|book a demo|contact|download|learn more|shop|cart|apply)', re.IGNORECASE))
    if buttons:
        orientation['has_primary_cta'] = True
        orientation['primary_cta_text'] = buttons[0].get_text(strip=True)
        
    nav = soup.find(['nav', 'header'])
    if nav:
        orientation['has_nav'] = True
        
    return orientation


def analyze_trust_anchors(soup: BeautifulSoup) -> Dict:
    """
    Detect presence of privacy policy, terms, contact email, and security markers.
    """
    links = soup.find_all('a', href=True)
    all_text = soup.get_text(separator=' ', strip=True)
    
    trust = {
        'has_privacy_policy': False,
        'has_terms': False,
        'has_contact_info': False,
        'has_security_cert': False
    }
    
    for link in links:
        href = link.get('href', '').lower()
        text = link.get_text(strip=True).lower()
        if 'privacy' in href or 'privacy' in text:
            trust['has_privacy_policy'] = True
        if 'terms' in href or 'tos' in href or 'terms of' in text:
            trust['has_terms'] = True
        if 'contact' in href or 'support' in href or 'contact' in text:
            trust['has_contact_info'] = True
            
    if re.search(r'\b(soc2|soc 2|iso 27001|gdpr|hipaa|pci-dss|ssl certified)\b', all_text, re.IGNORECASE):
        trust['has_security_cert'] = True
        
    if re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', all_text):
        trust['has_contact_info'] = True
        
    return trust


def analyze_engagement(context: Dict, crawl_findings: List[Dict] = None) -> Tuple[Dict, List[Dict]]:
    """
    Execute engagement, orientation, and trust audit.
    """
    findings = []
    
    for page in context.get('pages', []):
        html = page.get('html', '')
        url = page.get('url', '')
        if not html:
            continue
            
        try:
            soup = BeautifulSoup(html, 'html.parser')
            orientation = analyze_first_screen_orientation(soup, url)
            trust = analyze_trust_anchors(soup)
            
            body = soup.find('body')
            body_text = body.get_text(separator=' ', strip=True) if body else ''
            readability = calculate_readability(body_text)
            
            page['engagement_analysis'] = {
                'orientation': orientation,
                'trust': trust,
                'readability': readability
            }
            
            # 1. Weak Above-The-Fold Value Proposition
            if not orientation['has_concrete_value_prop']:
                h1_display = f"'{orientation['h1_text']}'" if orientation['h1_text'] else "None"
                findings.append({
                    'id': 'ENG-VAL-001',
                    'skill': 'engagement-audit',
                    'category': 'orientation',
                    'severity': 'medium',
                    'title': 'Vague or missing above-the-fold value proposition',
                    'location': url,
                    'evidence': f"Landing view contains no concrete product category or capability assertion in the first 500 characters. H1 is {h1_display}. Visitors arriving via AI search will bounce without clear orientation.",
                    'suggested_action': {
                        'summary': 'Craft a concrete H1 and sub-headline explicitly stating: what the product is, the core problem it solves, and who it is built for.',
                        'priority': 'medium'
                    }
                })
                
            # 2. Missing Primary Call-to-Action
            if not orientation['has_primary_cta']:
                findings.append({
                    'id': 'ENG-CTA-001',
                    'skill': 'engagement-audit',
                    'category': 'conversion',
                    'severity': 'medium',
                    'title': 'No clear next-step Call-to-Action (CTA) in initial viewport',
                    'location': url,
                    'evidence': f"No primary action button (e.g. 'Start Free Trial', 'View Documentation') found in header or hero section on {url}.",
                    'suggested_action': {
                        'summary': 'Add an unambiguous primary Call-to-Action button above the fold guiding visitors to convert or explore.',
                        'priority': 'medium'
                    }
                })
                
            # 3. High Reading Complexity
            if readability['grade_level'] > 14.5 and readability['total_words'] > 150:
                findings.append({
                    'id': 'ENG-READ-001',
                    'skill': 'engagement-audit',
                    'category': 'readability',
                    'severity': 'medium',
                    'title': f'High reading complexity (Grade {readability["grade_level"]} / Flesch {readability["reading_ease"]})',
                    'location': url,
                    'evidence': f"Average sentence length is {readability['words_per_sentence']} words with high polysyllabic word density. Complex syntax increases human cognitive friction and degrades AI snippet extraction.",
                    'suggested_action': {
                        'summary': 'Simplify sentence structures to target an 8th-10th grade reading level with bulleted lists and concise paragraphs.',
                        'priority': 'medium'
                    }
                })
                
            # 4. Missing Trust Anchors (Homepage only)
            if url == context.get('meta', {}).get('target_url', '') or url.endswith(context.get('site', {}).get('domain', '')):
                if not trust['has_privacy_policy'] or not trust['has_terms']:
                    findings.append({
                        'id': 'ENG-TRU-001',
                        'skill': 'engagement-audit',
                        'category': 'trust',
                        'severity': 'high',
                        'title': 'Missing essential legal and privacy trust links in footer',
                        'location': url,
                        'evidence': "Footer lacks direct links to Privacy Policy or Terms of Service. Enterprise AI search referrals evaluate legal transparency as an authority signal.",
                        'suggested_action': {
                            'summary': 'Add explicit footer navigation links to Privacy Policy and Terms of Service.',
                            'priority': 'high'
                        }
                    })
        except Exception:
            continue
            
    context['engagement_summary'] = {
        'pages_analyzed': len(context.get('pages', [])),
        'findings_count': len(findings)
    }
    
    return context, findings
