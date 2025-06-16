#!/usr/bin/env python3
"""
Script to remove all English content from HTML files in the website.
This script will:
1. Find all HTML files with lang="en" attributes
2. Remove elements with lang="en" attribute
3. Update html tag from lang="en" to lang="ru"
4. Remove English-specific meta descriptions and titles
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup, Comment
import argparse

def process_html_file(file_path):
    """Process a single HTML file to remove English content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse HTML
        soup = BeautifulSoup(content, 'html.parser')
        changes_made = False
        
        # Update html tag lang attribute
        html_tag = soup.find('html')
        if html_tag and html_tag.get('lang') == 'en':
            html_tag['lang'] = 'ru'
            changes_made = True
            print(f"  Updated <html lang='en'> to <html lang='ru'>")
        
        # Remove all elements with lang="en"
        en_elements = soup.find_all(attrs={'lang': 'en'})
        if en_elements:
            for element in en_elements:
                # Check if there's a corresponding Russian element
                parent = element.parent
                if parent:
                    ru_siblings = [sib for sib in element.find_next_siblings() 
                                  if sib.name == element.name and sib.get('lang') == 'ru']
                    if ru_siblings:
                        # If there's a Russian version, remove the English one
                        element.decompose()
                        changes_made = True
                        print(f"  Removed {element.name} with lang='en'")
            
            # Remove lang="ru" attributes from remaining elements
            ru_elements = soup.find_all(attrs={'lang': 'ru'})
            for element in ru_elements:
                del element['lang']
                changes_made = True
        
        # Update meta descriptions and titles containing English
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            content = meta_desc['content']
            # Check if it contains English text patterns
            if any(word in content.lower() for word in ['services', 'about', 'therapy', 'psychologist', 'hypnotherapist', 'irina monroe']):
                # You might want to translate these or remove them
                print(f"  Found English meta description: {content[:50]}...")
                changes_made = True
        
        # Update title if it contains English
        title_tag = soup.find('title')
        if title_tag and title_tag.string:
            title = title_tag.string
            if any(word in title.lower() for word in ['services', 'about', 'faq', 'blog', 'resources', 'irina monroe']):
                print(f"  Found English title: {title}")
                # Replace common English words in titles
                new_title = title
                replacements = {
                    'Services': 'Услуги',
                    'About': 'О себе',
                    'FAQ': 'Часто задаваемые вопросы',
                    'Blog': 'Блог',
                    'Resources': 'Ресурсы',
                    'Contact': 'Контакты',
                    'Irina Monroe': 'Ирина Монро'
                }
                for eng, rus in replacements.items():
                    new_title = new_title.replace(eng, rus)
                if new_title != title:
                    title_tag.string = new_title
                    changes_made = True
                    print(f"  Updated title to: {new_title}")
        
        # Save changes if any were made
        if changes_made:
            # Pretty print the HTML
            pretty_html = soup.prettify()
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(pretty_html)
            return True
        return False
        
    except Exception as e:
        print(f"  Error processing {file_path}: {e}")
        return False

def find_html_files(directory):
    """Find all HTML files in the given directory recursively."""
    html_files = []
    for root, dirs, files in os.walk(directory):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    return html_files

def main():
    parser = argparse.ArgumentParser(description='Remove English content from HTML files')
    parser.add_argument('--directory', default='.', help='Directory to process (default: current directory)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be changed without making changes')
    args = parser.parse_args()
    
    # Find all HTML files
    html_files = find_html_files(args.directory)
    print(f"Found {len(html_files)} HTML files to process")
    
    # Process each file
    processed = 0
    for file_path in html_files:
        print(f"\nProcessing: {file_path}")
        if not args.dry_run:
            if process_html_file(file_path):
                processed += 1
        else:
            # In dry-run mode, just check for English content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            if 'lang="en"' in content:
                print(f"  Would process this file (contains lang='en')")
                processed += 1
    
    print(f"\n{'Would process' if args.dry_run else 'Processed'} {processed} files with English content")

if __name__ == '__main__':
    main()