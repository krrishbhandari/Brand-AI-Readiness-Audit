"""
Automated Packaging Script for Adobe University Hackathon Round 3 Submission.
Packages the marketplace root into brand-ai-readiness-audit.zip.
Usage:
    python package_marketplace.py
"""

import zipfile
import json
import os
import sys

def package_marketplace():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    zip_name = "brand-ai-readiness-audit.zip"
    zip_path = os.path.join(root_dir, zip_name)
    
    print(f"[*] Packaging marketplace from: {root_dir}")
    
    # 1. Verify marketplace.json
    manifest_path = os.path.join(root_dir, "marketplace.json")
    if not os.path.exists(manifest_path):
        print(f"[!] Error: marketplace.json not found at {manifest_path}", file=sys.stderr)
        return 1
        
    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
        
    print(f"[+] Loaded manifest for: {manifest.get('name')} (v{manifest.get('version')})")
    print(f"[+] Registered skills: {len(manifest.get('skills', []))}")
    
    # 2. Files to include
    include_patterns = [
        "marketplace.json",
        "README.md",
        "requirements.txt",
        "skills",
        "tests"
    ]
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for item in include_patterns:
            item_path = os.path.join(root_dir, item)
            if not os.path.exists(item_path):
                continue
                
            if os.path.isfile(item_path):
                zipf.write(item_path, arcname=item)
                print(f"  + Added file: {item}")
            elif os.path.isdir(item_path):
                for root, dirs, files in os.walk(item_path):
                    # Skip __pycache__ and .pytest_cache
                    dirs[:] = [d for d in dirs if d not in ['__pycache__', '.pytest_cache', '.git']]
                    for file in files:
                        if file.endswith(('.pyc', '.pyo', '.DS_Store')):
                            continue
                        file_full_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_full_path, root_dir)
                        zipf.write(file_full_path, arcname=rel_path)
                        print(f"  + Added: {rel_path}")
                        
    size_bytes = os.path.getsize(zip_path)
    size_mb = size_bytes / (1024 * 1024)
    print(f"\n[OK] Marketplace successfully packaged into: {zip_path}")
    print(f"[OK] Package size: {size_mb:.2f} MB ({size_bytes:,} bytes)")
    
    if size_mb > 50.0:
        print("[!] Warning: Package size exceeds 50 MB limit!", file=sys.stderr)
        return 1
    else:
        print("[OK] Package is well within the 50 MB limit.")
        
    return 0

if __name__ == '__main__':
    sys.exit(package_marketplace())
