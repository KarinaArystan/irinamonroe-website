#!/usr/bin/env python3
"""
Final CSS path fix for resource pages
"""

import os
import re
import glob

def fix_css_paths_in_file(file_path):
    """Fix CSS paths based on the actual file depth"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get the relative path from the new-site directory
    rel_path = os.path.relpath(file_path, os.path.dirname(os.path.abspath(__file__)))
    
    # Count directory depth
    depth = len(rel_path.split(os.sep)) - 1
    
    # Determine the correct prefix based on depth
    if depth == 4:  # e.g., resources/questions/family/kak-vernut-lubov-muzha/index.html
        css_prefix = '../../../../'
        resources_prefix = '../../../'
    elif depth == 3:  # e.g., resources/hypnotherapy/gipnos/index.html
        css_prefix = '../../../'
        resources_prefix = '../../'
    elif depth == 2:  # e.g., resources/hypnotherapy/index.html
        css_prefix = '../../'
        resources_prefix = '../'
    else:
        css_prefix = '../'
        resources_prefix = ''
    
    # Fix CSS paths - Update all variations
    patterns = [
        # Fix styles.css paths
        (r'href="\.\.\/\.\.\/styles\.css"', f'href="{css_prefix}styles.css"'),
        (r'href="\.\.\/\.\.\/\.\.\/styles\.css"', f'href="{css_prefix}styles.css"'),
        (r'href="\.\.\/\.\.\/\.\.\/\.\.\/styles\.css"', f'href="{css_prefix}styles.css"'),
        
        # Fix mobile-fixes.css paths
        (r'href="\.\.\/\.\.\/mobile-fixes\.css"', f'href="{css_prefix}mobile-fixes.css"'),
        (r'href="\.\.\/\.\.\/\.\.\/mobile-fixes\.css"', f'href="{css_prefix}mobile-fixes.css"'),
        (r'href="\.\.\/\.\.\/\.\.\/\.\.\/mobile-fixes\.css"', f'href="{css_prefix}mobile-fixes.css"'),
        
        # Fix resources-styles.css paths
        (r'href="\.\.\/resources-styles\.css"', f'href="{resources_prefix}resources-styles.css"'),
        (r'href="\.\.\/\.\.\/resources-styles\.css"', f'href="{resources_prefix}resources-styles.css"'),
        (r'href="\.\.\/\.\.\/\.\.\/resources-styles\.css"', f'href="{resources_prefix}resources-styles.css"'),
    ]
    
    # Apply all fixes
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    return content

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("Final CSS Path Fix")
    print("=" * 50)
    print("Fixing CSS paths in all resource pages...\n")
    
    # Patterns to find resource pages
    patterns = [
        'resources/hypnotherapy/*/index.html',
        'resources/psychology/*/index.html',
        'resources/questions/*/index.html',
        'resources/questions/*/*/index.html'
    ]
    
    fixed = 0
    for pattern in patterns:
        files = glob.glob(os.path.join(script_dir, pattern))
        for file_path in files:
            # Skip category index pages
            if file_path.endswith(('hypnotherapy/index.html', 'psychology/index.html', 'questions/index.html')):
                continue
            
            print(f"Fixing CSS paths in: {os.path.relpath(file_path, script_dir)}")
            
            fixed_content = fix_css_paths_in_file(file_path)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            
            fixed += 1
    
    print(f"\n✅ Fixed CSS paths in {fixed} resource pages")

if __name__ == "__main__":
    main()