#!/usr/bin/env python3
"""
Comprehensive fix for inline styles in resource pages
Replace inline styles with proper CSS classes
"""

import os
import re
import glob

def fix_inline_style_sections(content):
    """Replace sections with inline styles with proper CSS classes"""
    
    # Pattern to match sections with inline background styles
    patterns = [
        # Sections with var(--bg-light) background
        (
            r'<section\s+style="[^"]*background:\s*var\(--bg-light\)[^"]*"[^>]*>(.*?)</section>',
            'bg-light-section'
        ),
        # Sections with #F4F2EF background
        (
            r'<section\s+style="[^"]*background:\s*#F4F2EF[^"]*"[^>]*>(.*?)</section>',
            'bg-section'
        ),
        # CTA sections with inline styles
        (
            r'<section\s+style="[^"]*background:[^"]*padding:\s*60px\s*0[^"]*"[^>]*>(.*?)</section>',
            'cta-or-related'
        ),
    ]
    
    for pattern, section_type in patterns:
        matches = list(re.finditer(pattern, content, re.DOTALL))
        
        for match in matches:
            full_match = match.group(0)
            inner_content = match.group(1)
            
            # Determine the type of section based on content
            if any(keyword in inner_content for keyword in ['Похожие темы', 'Исследуйте больше тем', 'Связанные темы', 'Related Topics']):
                # This is a related topics section
                new_section = '<section class="related-topics-section">\n' + inner_content + '\n</section>'
            elif 'Есть свой вопрос?' in inner_content or 'Готовы начать' in inner_content:
                # This is a CTA section
                new_section = '<section class="article-cta">\n' + inner_content + '\n</section>'
            else:
                # Generic section with proper class
                new_section = '<section class="content-section">\n' + inner_content + '\n</section>'
            
            content = content.replace(full_match, new_section)
    
    # Also fix any divs or other elements with inline styles
    content = re.sub(
        r'(<(?:div|article|aside)[^>]*)\s+style="[^"]*background:\s*(?:var\(--bg-light\)|#F4F2EF)[^"]*"([^>]*>)',
        r'\1 class="light-bg-section"\2',
        content
    )
    
    return content

def add_missing_css_classes(content):
    """Add CSS classes for sections that were using inline styles"""
    
    # Check if we need to add styles
    if '<style>' in content and any(cls in content for cls in ['article-cta', 'content-section', 'light-bg-section']):
        style_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
        if style_match:
            styles = style_match.group(1)
            
            additional_css = ''
            
            # Add article-cta if missing
            if 'article-cta' in content and '.article-cta' not in styles:
                additional_css += '''
        /* Article CTA Section */
        .article-cta {
            background: var(--bg-light);
            padding: 80px 0;
            margin-top: 80px;
            text-align: center;
        }
        
        .article-cta h2 {
            font-family: 'Cormorant Infant', serif;
            font-size: 36px;
            font-weight: 400;
            margin-bottom: 20px;
            color: var(--text-dark);
        }
        
        .article-cta p {
            font-size: 18px;
            margin-bottom: 30px;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
            color: var(--text-dark);
        }'''
            
            # Add content-section if missing
            if 'content-section' in content and '.content-section' not in styles:
                additional_css += '''
        /* Content Section */
        .content-section {
            background: var(--bg-section);
            padding: 60px 0;
            margin-top: 60px;
        }'''
            
            # Add light-bg-section if missing
            if 'light-bg-section' in content and '.light-bg-section' not in styles:
                additional_css += '''
        /* Light Background Section */
        .light-bg-section {
            background: var(--bg-lighter);
            padding: 40px;
            border-radius: 12px;
            margin: 40px 0;
        }'''
            
            if additional_css:
                # Insert before closing style tag
                content = content.replace('</style>', additional_css + '\n    </style>')
    
    return content

def fix_double_tone_issue(content):
    """Fix double-tone visual issues by ensuring consistent backgrounds"""
    
    # Ensure category-hero sections don't have conflicting styles
    content = re.sub(
        r'<section\s+class="category-hero"[^>]*style="[^"]*"[^>]*>',
        '<section class="category-hero">',
        content
    )
    
    return content

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("Comprehensive Inline Styles Fix")
    print("=" * 50)
    print("Replacing inline styles with proper CSS classes...\n")
    
    # Fix resource pages
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
                
                # Fix inline styles
                content = fix_inline_style_sections(content)
                
                # Add missing CSS classes
                content = add_missing_css_classes(content)
                
                # Fix double-tone issues
                content = fix_double_tone_issue(content)
                
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    fixed += 1
                    print(f"Fixed: {os.path.relpath(file_path, script_dir)}")
                    
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
    
    # Also fix category pages for double-tone issues
    print("\nFixing category pages...")
    category_pages = [
        'resources/hypnotherapy/index.html',
        'resources/psychology/index.html', 
        'resources/questions/index.html'
    ]
    
    for page_path in category_pages:
        full_path = os.path.join(script_dir, page_path)
        if os.path.exists(full_path):
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                content = fix_double_tone_issue(content)
                
                if content != original_content:
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"✅ Fixed {page_path}")
            except Exception as e:
                print(f"Error processing {full_path}: {e}")
    
    print(f"\n✅ Fixed {fixed} pages")
    print("\nAll inline styles have been replaced with:")
    print("- Proper CSS classes for related topics sections")
    print("- Consistent background colors using CSS variables")
    print("- Fixed double-tone visual issues")

if __name__ == "__main__":
    main()