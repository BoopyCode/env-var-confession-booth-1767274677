#!/usr/bin/env python3
"""
.env Confession Booth - Where your environment variables come to confess their sins.
"""

import os
import re
from pathlib import Path
from collections import defaultdict

def analyze_env_file(filepath='.env'):
    """
    Reads your .env file and judges you silently (but thoroughly).
    """
    path = Path(filepath)
    if not path.exists():
        print("No .env found. Either you're perfect or in denial.")
        return
    
    with open(path, 'r') as f:
        lines = f.readlines()
    
    sins = defaultdict(list)
    used_vars = set()
    
    # Check actual usage in project files
    for py_file in Path('.').rglob('*.py'):
        try:
            with open(py_file, 'r') as f:
                content = f.read()
                for match in re.findall(r'os\.getenv\(["\']([^"\']+)["\']\)', content):
                    used_vars.add(match)
        except:
            continue
    
    # Analyze each .env line
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
            
        if '=' not in line:
            sins['malformed'].append(f"Line {i}: '{line}' - Missing '=', are you even trying?")
            continue
            
        var, value = line.split('=', 1)
        var = var.strip()
        
        # Sin detection logic
        if var not in used_vars:
            sins['unused'].append(f"Line {i}: {var} - Nobody calls you anymore")
        
        if value.strip() == '':
            sins['empty'].append(f"Line {i}: {var} - Set to nothing, like your promises")
        
        if re.search(r'password|secret|key', var, re.I) and len(value) < 10:
            sins['weak'].append(f"Line {i}: {var} - Shorter than your attention span")
        
        if var != var.upper():
            sins['case'].append(f"Line {i}: {var} - Not screaming, are you shy?")
    
    # Confession time
    if not sins:
        print("\nNo sins detected! (Or you're really good at hiding them)")
        return
    
    print(f"\n=== .ENV CONFESSION BOOTH ===")
    print(f"Found {len(lines)} lines in {filepath}\n")
    
    for sin_type, confessions in sins.items():
        print(f"{sin_type.upper()} SINS ({len(confessions)}):")
        for confession in confessions:
            print(f"  - {confession}")
        print()
    
    print(f"Total sins: {sum(len(v) for v in sins.values())}")
    print("Go forth and repent. Or don't. I'm a script, not a therapist.")

if __name__ == '__main__':
    analyze_env_file()