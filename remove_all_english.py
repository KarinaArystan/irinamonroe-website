#!/usr/bin/env python3
"""
Comprehensive script to remove all English content from the website.
"""

import os
import re
import sys

def clean_translation_placeholders(content):
    """Remove [Translation needed: ...] placeholders and keep only Russian text."""
    # Pattern to match [Translation needed: Russian text]
    pattern = r'\[Translation needed:\s*([^\]]+)\]'
    content = re.sub(pattern, r'\1', content)
    
    # Remove standalone [Translation needed] tags
    content = content.replace('[Translation needed]', '')
    
    return content

def remove_english_titles(content):
    """Remove English titles and navigation."""
    replacements = {
        '| Hypnotherapy | Irina Monroe': '| Гипнотерапия | Ирина Монро',
        '| Psychology | Irina Monroe': '| Психология | Ирина Монро',
        '| Irina Monroe': '| Ирина Монро',
        'Irina Monroe': 'Ирина Монро',
        'Published on': 'Опубликовано',
        'Home': 'Главная',
        'About': 'О себе',
        'Services': 'Услуги',
        'Blog': 'Блог',
        'Resources': 'Ресурсы',
        'Contact': 'Контакты',
        'Contact Me': 'Связаться со мной',
        'Hypnotherapy': 'Гипнотерапия',
        'Psychology': 'Психология',
        'Questions and Answers': 'Вопросы и ответы',
        'FAQ': 'Часто задаваемые вопросы',
        'All hypnotherapy topics': 'Все темы гипнотерапии',
        'Return to hypnotherapy overview': 'Вернуться к обзору гипнотерапии',
        'Ready to experience hypnotherapy?': 'Готовы испытать гипнотерапию?',
        'Discover how hypnotherapy can help you create positive changes in your life.': 'Откройте для себя, как гипнотерапия может помочь вам создать позитивные изменения в вашей жизни.',
        'Book a session': 'Записаться на сеанс',
        'Explore more topics': 'Исследуйте больше тем'
    }
    
    for eng, rus in replacements.items():
        content = content.replace(eng, rus)
    
    return content

def process_html_file(file_path):
    """Process a single HTML file to remove all English content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Update html lang attribute
        content = content.replace('<html lang="en">', '<html lang="ru">')
        
        # Clean translation placeholders
        content = clean_translation_placeholders(content)
        
        # Remove English titles and navigation
        content = remove_english_titles(content)
        
        # Remove elements with lang="en" that have corresponding lang="ru" versions
        # This regex finds pairs of elements where one has lang="en" and the next has lang="ru"
        pattern = r'<(\w+)([^>]*?)\s+lang="en"([^>]*?)>(.*?)</\1>\s*\n?\s*<\1([^>]*?)\s+lang="ru"([^>]*?)>(.*?)</\1>'
        
        def replace_bilingual(match):
            tag = match.group(1)
            attrs_before = match.group(2)
            attrs_after = match.group(3)
            ru_attrs_before = match.group(5)
            ru_attrs_after = match.group(6)
            ru_content = match.group(7)
            
            # Combine attributes, preferring Russian version's attributes
            combined_attrs = (ru_attrs_before + ' ' + ru_attrs_after).strip()
            if attrs_before and not ru_attrs_before:
                combined_attrs = (attrs_before + ' ' + attrs_after + ' ' + combined_attrs).strip()
            
            return f'<{tag} {combined_attrs}>{ru_content}</{tag}>'
        
        content = re.sub(pattern, replace_bilingual, content, flags=re.DOTALL)
        
        # Remove standalone elements with lang="en"
        content = re.sub(r'<(\w+)([^>]*?)\s+lang="en"([^>]*?)>.*?</\1>\s*\n?', '', content, flags=re.DOTALL)
        
        # Remove lang="ru" attributes from remaining elements
        content = re.sub(r'\s+lang="ru"', '', content)
        
        # Clean up empty lines
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        # Save if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def find_html_files(directory):
    """Find all HTML files in the directory."""
    html_files = []
    for root, dirs, files in os.walk(directory):
        # Skip hidden directories and build directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'dist', 'build']]
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    return html_files

def main():
    directory = '.'
    
    # Find all HTML files
    html_files = find_html_files(directory)
    print(f"Found {len(html_files)} HTML files")
    
    # Process each file
    processed = 0
    for file_path in html_files:
        if process_html_file(file_path):
            processed += 1
            print(f"Processed: {file_path}")
    
    print(f"\nProcessed {processed} files")
    
    # Final check for remaining English content
    print("\nChecking for remaining English content...")
    remaining = 0
    for file_path in html_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'lang="en"' in content or '[Translation needed' in content:
            remaining += 1
            print(f"Still has English: {file_path}")
    
    if remaining == 0:
        print("All English content has been removed!")
    else:
        print(f"\n{remaining} files still contain English content")

if __name__ == '__main__':
    main()