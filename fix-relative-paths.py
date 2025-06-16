#!/usr/bin/env python3
"""
Fix absolute paths to relative paths for GitHub Pages deployment
This script converts all absolute paths (starting with /) to relative paths
"""

import os
import re
from pathlib import Path

def get_relative_depth(file_path):
    """Calculate how many levels deep a file is from root"""
    parts = Path(file_path).parts
    # Don't count the filename itself
    return len(parts) - 1

def get_relative_prefix(depth):
    """Generate the relative path prefix based on depth"""
    if depth == 0:
        return ""
    return "../" * depth

def fix_paths_in_file(file_path, root_dir):
    """Fix absolute paths in a single HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Calculate relative depth
        rel_path = os.path.relpath(file_path, root_dir)
        depth = rel_path.count(os.sep)
        prefix = get_relative_prefix(depth)
        
        # Skip if no absolute paths found
        if 'href="/' not in content and 'action="/' not in content:
            return False
        
        print(f"Processing: {rel_path} (depth: {depth})")
        
        # Pattern to match absolute paths in href and action attributes
        # Excludes external URLs (http://, https://, //)
        patterns = [
            (r'href="/((?!/).+?)"', f'href="{prefix}\\1"'),
            (r'action="/((?!/).+?)"', f'action="{prefix}\\1"'),
            # Also fix links to root
            (r'href="/"', f'href="{prefix}index.html"' if prefix else 'href="index.html"'),
        ]
        
        original_content = content
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)
        
        # Write back if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def fix_all_paths(root_dir):
    """Fix paths in all HTML files"""
    fixed_count = 0
    total_count = 0
    
    for root, dirs, files in os.walk(root_dir):
        # Skip hidden directories and common non-content directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'tools']]
        
        for file in files:
            if file.endswith('.html'):
                total_count += 1
                file_path = os.path.join(root, file)
                if fix_paths_in_file(file_path, root_dir):
                    fixed_count += 1
    
    print(f"\nSummary: Fixed {fixed_count} out of {total_count} HTML files")

def main():
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("Starting to fix absolute paths for GitHub Pages deployment...")
    print(f"Working directory: {script_dir}")
    
    # Confirm before proceeding
    response = input("\nThis will modify all HTML files. Continue? (y/n): ")
    if response.lower() != 'y':
        print("Aborted.")
        return
    
    fix_all_paths(script_dir)
    print("\nDone! Now commit and push the changes to GitHub.")

if __name__ == "__main__":
    main()