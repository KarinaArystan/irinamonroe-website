#!/usr/bin/env python3
"""
Simple script to remove English content from HTML files using regex.
"""

import os
import re
import sys

def process_html_file(file_path):
    """Process a single HTML file to remove English content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes = []
        
        # Update html tag lang attribute
        if '<html lang="en">' in content:
            content = content.replace('<html lang="en">', '<html lang="ru">')
            changes.append("Updated <html lang='en'> to <html lang='ru'>")
        
        # Find and remove elements with lang="en"
        # Pattern to match elements with lang="en" and their content
        patterns = [
            # Match tags with lang="en" that have corresponding lang="ru" versions
            (r'<(\w+)([^>]*)\s+lang="en"([^>]*)>([^<]*)</\1>\s*\n?\s*<\1([^>]*)\s+lang="ru"([^>]*)>([^<]*)</\1>', 
             r'<\1\2\3>\7</\1>'),
            # Remove standalone lang="en" elements
            (r'<(\w+)([^>]*)\s+lang="en"([^>]*)>([^<]*)</\1>\s*\n?', ''),
            # Remove lang="ru" attributes from remaining elements
            (r'\s+lang="ru"', '')
        ]
        
        for pattern, replacement in patterns:
            new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
            if new_content != content:
                changes.append(f"Applied pattern: {pattern[:50]}...")
                content = new_content
        
        # Update English meta descriptions and titles
        meta_replacements = {
            'Services - Individual therapy, online sessions, and collaborative work with Irina Monroe': 
                'Услуги - Индивидуальная терапия, онлайн сессии и совместная работа с Ириной Монро',
            'Frequently Asked Questions about therapy with Irina Monroe': 
                'Часто задаваемые вопросы о терапии с Ириной Монро',
            'Services | Irina Monroe': 'Услуги | Ирина Монро',
            'FAQ | Irina Monroe': 'Часто задаваемые вопросы | Ирина Монро',
            'About | Irina Monroe': 'О себе | Ирина Монро',
            'Blog | Irina Monroe': 'Блог | Ирина Монро',
            'Contact | Irina Monroe': 'Контакты | Ирина Монро',
            'Resources | Irina Monroe': 'Ресурсы | Ирина Монро'
        }
        
        for eng, rus in meta_replacements.items():
            if eng in content:
                content = content.replace(eng, rus)
                changes.append(f"Replaced: {eng} -> {rus}")
        
        # Save changes if any were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return changes
        return []
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return []

def find_html_files_with_english(directory):
    """Find HTML files containing English content."""
    html_files = []
    for root, dirs, files in os.walk(directory):
        # Skip hidden directories and common non-content directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'dist', 'build']]
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    # Check if file contains English markers
                    if 'lang="en"' in content:
                        html_files.append(file_path)
                except:
                    pass
    return html_files

def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--dry-run':
        dry_run = True
    else:
        dry_run = False
    
    # Find all HTML files with English content
    directory = '.'
    html_files = find_html_files_with_english(directory)
    print(f"Found {len(html_files)} HTML files with English content")
    
    if dry_run:
        print("\nDRY RUN - No changes will be made\n")
        for file_path in html_files[:10]:  # Show first 10 files
            print(f"Would process: {file_path}")
    else:
        # Process each file
        processed = 0
        for file_path in html_files:
            print(f"\nProcessing: {file_path}")
            changes = process_html_file(file_path)
            if changes:
                processed += 1
                for change in changes:
                    print(f"  - {change}")
        
        print(f"\nProcessed {processed} files")

if __name__ == '__main__':
    main()