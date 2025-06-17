#!/usr/bin/env python3
"""
Fix related articles/topics sections styling in resource pages
"""

import os
import re
import glob

def fix_related_section(content, file_path):
    """Fix related articles/topics section with proper styling"""
    
    # Pattern to find related sections with inline styles
    patterns = [
        # Style with background #F4F2EF
        (r'<section[^>]*style="[^"]*background:\s*#F4F2EF[^"]*"[^>]*>(.*?)</section>', 'style1'),
        # Style with background var(--bg-light)
        (r'<section[^>]*style="[^"]*background:\s*var\(--bg-light\)[^"]*"[^>]*>(.*?)</section>', 'style2'),
        # Related topics section without proper class
        (r'<section[^>]*>(?=\s*<div[^>]*>\s*<h2[^>]*>Похожие темы</h2>)(.*?)</section>', 'topics'),
    ]
    
    for pattern, style_type in patterns:
        matches = re.finditer(pattern, content, re.DOTALL)
        for match in matches:
            full_match = match.group(0)
            inner_content = match.group(1)
            
            # Check if this is a related section
            if 'Похожие темы' in inner_content or 'Related Topics' in inner_content:
                # Create properly styled section
                new_section = '''<section class="related-topics-section">
        <div class="container">
            <h2>Похожие темы</h2>
            <div class="topics-grid">'''
                
                # Extract topic cards
                topic_cards = re.findall(r'<a[^>]*class="topic-card"[^>]*>.*?</a>', inner_content, re.DOTALL)
                
                for card in topic_cards:
                    # Remove inline styles from cards
                    clean_card = re.sub(r'\s*style="[^"]*"', '', card)
                    new_section += f'\n                {clean_card}'
                
                new_section += '''
            </div>
        </div>
    </section>'''
                
                content = content.replace(full_match, new_section)
    
    # Also fix any remaining topic cards with inline styles
    content = re.sub(
        r'(<a[^>]*class="topic-card"[^>]*)\s*style="[^"]*"([^>]*>)',
        r'\1\2',
        content
    )
    
    return content

def ensure_css_in_page(content, file_path):
    """Ensure the page has necessary CSS for related topics"""
    
    # Check if page has inline styles for related topics that need to be added
    if 'related-topics-section' in content and '<style>' in content:
        # Find the style tag
        style_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
        if style_match and '.related-topics-section' not in style_match.group(1):
            # Add the CSS
            additional_css = '''
        /* Related Topics Section */
        .related-topics-section {
            background: var(--bg-section);
            padding: 80px 0;
            margin-top: 80px;
        }
        
        .related-topics-section h2 {
            font-family: 'Cormorant Infant', serif;
            font-size: 36px;
            color: var(--text-dark);
            text-align: center;
            margin-bottom: 50px;
            font-weight: 400;
        }
        
        .related-topics-section .topics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 30px;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .related-topics-section .topic-card {
            background: var(--white);
            border-radius: 12px;
            padding: 35px;
            text-decoration: none;
            transition: all 0.3s ease;
            display: block;
            position: relative;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        }
        
        .related-topics-section .topic-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: var(--primary-color);
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }
        
        .related-topics-section .topic-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
        }
        
        .related-topics-section .topic-card:hover::before {
            transform: scaleX(1);
        }
        
        .related-topics-section .topic-card h3 {
            font-family: 'Cormorant Infant', serif;
            font-size: 26px;
            color: var(--text-dark);
            margin-bottom: 15px;
            font-weight: 400;
            line-height: 1.3;
        }
        
        .related-topics-section .topic-card p {
            font-size: 16px;
            color: var(--text-muted);
            line-height: 1.6;
            margin: 0;
        }'''
            
            # Insert before closing style tag
            content = content.replace('</style>', additional_css + '\n    </style>')
    
    return content

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("Fixing Related Articles Styling")
    print("=" * 50)
    print("Searching for and fixing related sections...\n")
    
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
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Fix related sections
                content = fix_related_section(content, file_path)
                
                # Ensure CSS is present
                content = ensure_css_in_page(content, file_path)
                
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    fixed += 1
                    print(f"Fixed: {os.path.relpath(file_path, script_dir)}")
                    
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
    
    print(f"\n✅ Fixed {fixed} pages with related articles sections")
    print("\nRelated articles now have:")
    print("- Proper CSS classes instead of inline styles")
    print("- Consistent styling with hover effects")
    print("- Responsive grid layout")

if __name__ == "__main__":
    main()