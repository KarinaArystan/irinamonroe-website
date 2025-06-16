#!/usr/bin/env python3
import os
import re
import sys

def remove_language_selectors(content):
    """Remove language selector functionality and English content from HTML files."""
    
    # Remove language selector dropdowns and related code
    patterns = [
        # Remove entire language selector divs
        r'<div class="lang-selector">.*?</div>\s*',
        
        # Remove language dropdown buttons
        r'<button class="lang-dropdown-btn"[^>]*>.*?</button>\s*',
        
        # Remove language options
        r'<button class="lang-option" data-lang="en">.*?</button>\s*',
        
        # Remove English language spans
        r'<span class="current-lang" data-lang="en"[^>]*>.*?</span>\s*',
        
        # Remove any elements with data-lang="en"
        r'<[^>]* data-lang="en"[^>]*>.*?</[^>]+>\s*',
        
        # Clean up empty language selector containers
        r'<div class="lang-dropdown">\s*<button class="lang-option" data-lang="ru">Русский</button>\s*</div>',
        
        # Remove mobile controls if they only contain language selector
        r'<div class="mobile-controls">\s*<!--[^>]*-->\s*</div>',
    ]
    
    for pattern in patterns:
        content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
    
    # Specific replacements for language selector remnants
    replacements = {
        'data-lang="en"': '',
        'data-lang="ru"': '',
        'style="display:none;"': '',
    }
    
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    # Clean up multiple empty lines
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    return content

def process_file(filepath):
    """Process a single HTML file to remove language selectors."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply language selector removal
        content = remove_language_selectors(content)
        
        # If content changed, write it back
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = "."
    
    processed = 0
    modified = 0
    
    # Process all HTML files
    for root, dirs, files in os.walk(directory):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                processed += 1
                
                if process_file(filepath):
                    modified += 1
                    print(f"Modified: {filepath}")
    
    print(f"\nProcessed {processed} HTML files")
    print(f"Modified {modified} files")
    
    # After removing language selectors, check for any remaining lang="en"
    remaining = 0
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    if 'lang="en"' in f.read():
                        remaining += 1
                        print(f"Still contains lang=\"en\": {filepath}")
    
    if remaining > 0:
        print(f"\n{remaining} files still contain lang=\"en\" attributes")

if __name__ == "__main__":
    main()