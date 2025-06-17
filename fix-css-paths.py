#!/usr/bin/env python3
"""
Fix CSS paths in individual article pages
"""

import os
import re
import glob

def fix_css_paths_in_file(file_path):
    """Fix CSS paths based on directory depth"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Determine the depth based on path
    rel_path = os.path.relpath(file_path, os.path.dirname(os.path.abspath(__file__)))
    depth = len(rel_path.split(os.sep)) - 1  # -1 for the filename
    
    # Determine correct number of ../
    if 'hypnotherapy' in rel_path or 'psychology' in rel_path:
        if rel_path.count(os.sep) == 3:  # resources/hypnotherapy/topic/index.html
            prefix = '../../../'
        else:
            prefix = '../../'
    elif 'questions' in rel_path:
        if rel_path.count(os.sep) == 4:  # resources/questions/category/topic/index.html
            prefix = '../../../../'
        elif rel_path.count(os.sep) == 3:  # resources/questions/topic/index.html
            prefix = '../../../'
        else:
            prefix = '../../'
    elif 'blog' in rel_path and rel_path.count(os.sep) >= 2:
        prefix = '../../'
    else:
        return False  # Skip files that don't need fixing
    
    # Fix CSS links
    css_patterns = [
        (r'href="\.\.\/styles\.css"', f'href="{prefix}styles.css"'),
        (r'href="\.\.\/mobile-fixes\.css"', f'href="{prefix}mobile-fixes.css"'),
        (r'href="\.\.\/\.\.\/styles\.css"', f'href="{prefix}styles.css"'),
        (r'href="\.\.\/\.\.\/mobile-fixes\.css"', f'href="{prefix}mobile-fixes.css"'),
        (r'href="\.\.\/\.\.\/blog-styles\.css"', f'href="{prefix}blog-styles.css"'),
    ]
    
    # Fix script links
    script_patterns = [
        (r'src="\.\.\/script\.js"', f'src="{prefix}script.js"'),
        (r'src="\.\.\/\.\.\/script\.js"', f'src="{prefix}script.js"'),
        (r'src="\.\.\/\.\.\/\.\.\/script\.js"', f'src="{prefix}script.js"'),
        (r'src="\.\.\/blog-script\.js"', f'src="{prefix}blog-script.js"'),
    ]
    
    # Fix resource-styles.css path
    resource_style_patterns = [
        (r'href="\.\.\/resources-styles\.css"', f'href="../../resources-styles.css"'),
        (r'href="\.\.\/\.\.\/resources-styles\.css"', f'href="../../resources-styles.css"'),
    ]
    
    # Apply fixes
    original = content
    for pattern, replacement in css_patterns + script_patterns + resource_style_patterns:
        content = re.sub(pattern, replacement, content)
    
    # Fix contact links
    content = re.sub(r'href="\.\.\/\.\.\/\.\.#contact"', f'href="{prefix}#contact"', content)
    content = re.sub(r'href="\.\.\/\.\.\/\.\.\/\.\.#contact"', f'href="{prefix}#contact"', content)
    
    # Fix index.html links
    content = re.sub(r'href="\.\.\/\.\.\/\.\.\/index\.html"', f'href="{prefix}index.html"', content)
    content = re.sub(r'href="\.\.\/\.\.\/\.\.\/\.\.\/index\.html"', f'href="{prefix}index.html"', content)
    
    # Fix resources links
    content = re.sub(r'href="\.\.\/\.\.\/\.\.\/resources\/"', f'href="{prefix}resources/"', content)
    content = re.sub(r'href="\.\.\/\.\.\/\.\.\/\.\.\/resources\/"', f'href="{prefix}resources/"', content)
    
    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("CSS Path Fixer")
    print("=" * 50)
    print("Fixing CSS and script paths in article pages...\n")
    
    # Patterns to find article pages
    patterns = [
        'resources/hypnotherapy/*/index.html',
        'resources/psychology/*/index.html', 
        'resources/questions/*/index.html',
        'resources/questions/*/*/index.html',
        'blog/*/index.html'
    ]
    
    total_fixed = 0
    for pattern in patterns:
        files = glob.glob(os.path.join(script_dir, pattern))
        for file_path in files:
            if 'index.html' in os.path.basename(os.path.dirname(file_path)):
                continue  # Skip category index pages
            
            if fix_css_paths_in_file(file_path):
                print(f"✓ Fixed: {os.path.relpath(file_path, script_dir)}")
                total_fixed += 1
    
    print(f"\n✅ Fixed {total_fixed} files")
    print("\nCSS paths are now correct for all article pages!")

if __name__ == "__main__":
    main()