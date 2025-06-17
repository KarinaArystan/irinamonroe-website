#!/usr/bin/env python3
"""
Comprehensive fix for resource page styling issues
- Fix related articles styling
- Fix footer consistency
- Fix color inconsistencies and double-tone issues
- Standardize page structure
"""

import os
import re
import glob

def fix_related_articles_styling(content):
    """Fix related articles/topics section styling"""
    
    # Pattern to find related topics sections with inline styles
    related_pattern = r'<section[^>]*style="background:\s*#F4F2EF[^"]*"[^>]*>.*?<h2[^>]*>(?:Похожие темы|Related Topics|Похожие вопросы)</h2>.*?</section>'
    
    # Replace with properly styled section
    def replace_related_section(match):
        section_content = match.group(0)
        
        # Extract the inner content
        inner_content = re.search(r'<h2[^>]*>.*?</h2>(.*?)</section>', section_content, re.DOTALL)
        if inner_content:
            # Check if it's a topics grid or related questions grid
            if 'topics-grid' in section_content or 'topic-card' in section_content:
                return '''<section class="related-topics-section">
        <div class="container">
            <h2>Похожие темы</h2>''' + inner_content.group(1) + '''
        </div>
    </section>'''
            else:
                # For related questions
                return '''<section class="related-questions">
        <h2>Похожие вопросы</h2>''' + inner_content.group(1) + '''
    </section>'''
        
        return section_content
    
    content = re.sub(related_pattern, replace_related_section, content, flags=re.DOTALL)
    
    # Also fix topic cards that use inline styles
    content = re.sub(
        r'<a[^>]*class="topic-card"[^>]*style="[^"]*"[^>]*>',
        '<a class="topic-card">',
        content
    )
    
    return content

def fix_category_hero_styling(content):
    """Fix double-tone issues in category pages"""
    
    # Remove duplicate category-hero sections
    # Keep only the first occurrence with standardized margin
    if 'category-hero' in content:
        # Standardize the margin-top for all category-hero sections
        content = re.sub(
            r'(\.category-hero\s*{[^}]*margin-top:\s*)\d+px',
            r'\g<1>91px',
            content
        )
        
        # For HTML files, ensure proper structure
        content = re.sub(
            r'<section[^>]*class="category-hero"[^>]*style="[^"]*"[^>]*>',
            '<section class="category-hero">',
            content
        )
    
    return content

def add_related_articles_css(css_content):
    """Add proper CSS for related articles sections"""
    
    # Check if related-topics-section styles already exist
    if '.related-topics-section' not in css_content:
        related_css = '''
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
}

/* Mobile responsive for related topics */
@media (max-width: 768px) {
    .related-topics-section {
        padding: 60px 0;
    }
    
    .related-topics-section h2 {
        font-size: 32px;
        margin-bottom: 40px;
    }
    
    .related-topics-section .topics-grid {
        grid-template-columns: 1fr;
        gap: 20px;
        padding: 0 20px;
    }
    
    .related-topics-section .topic-card {
        padding: 25px;
    }
    
    .related-topics-section .topic-card h3 {
        font-size: 24px;
    }
}
'''
        # Add to CSS content before the last closing comment or at the end
        css_content = css_content.rstrip() + '\n' + related_css
    
    return css_content

def fix_footer_in_article_pages(content, file_path):
    """Ensure consistent footer structure in article pages"""
    
    # Get the relative path depth
    rel_path = os.path.relpath(file_path, os.path.dirname(os.path.abspath(__file__)))
    depth = len(rel_path.split(os.sep)) - 1
    
    # Determine the correct prefix
    if depth == 4:
        prefix = '../../../../'
    elif depth == 3:
        prefix = '../../../'
    elif depth == 2:
        prefix = '../../'
    else:
        prefix = '../'
    
    # Check if page has footer placeholder
    if '<div class="footer-placeholder"></div>' in content:
        # This page relies on JavaScript - it should already be fixed by previous script
        return content
    
    # Ensure footer has correct structure and paths
    footer_pattern = r'<footer[^>]*>.*?</footer>'
    footer_match = re.search(footer_pattern, content, re.DOTALL)
    
    if footer_match:
        footer_content = footer_match.group(0)
        # Fix any absolute paths in footer
        footer_content = re.sub(r'href="/', f'href="{prefix}', footer_content)
        content = re.sub(footer_pattern, footer_content, content, flags=re.DOTALL)
    
    return content

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("Comprehensive Resource Styling Fix")
    print("=" * 50)
    print("Fixing styling issues across resource pages...\n")
    
    # First, fix the CSS files
    print("1. Fixing CSS files...")
    
    # Fix resources-styles.css
    resources_css_path = os.path.join(script_dir, 'resources/resources-styles.css')
    if os.path.exists(resources_css_path):
        with open(resources_css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        # Remove duplicate category-hero definitions
        # Keep only the first one with consistent styling
        css_lines = css_content.split('\n')
        new_lines = []
        in_category_hero = False
        category_hero_count = 0
        
        for line in css_lines:
            if '.category-hero {' in line:
                category_hero_count += 1
                if category_hero_count == 1:
                    in_category_hero = True
                    new_lines.append(line)
                else:
                    # Skip duplicate definition
                    in_category_hero = True
                    continue
            elif in_category_hero and line.strip() == '}':
                if category_hero_count == 1:
                    new_lines.append(line)
                in_category_hero = False
            elif in_category_hero and category_hero_count > 1:
                # Skip lines in duplicate definition
                continue
            else:
                new_lines.append(line)
        
        css_content = '\n'.join(new_lines)
        
        # Fix the margin-top to be consistent
        css_content = re.sub(
            r'(\.category-hero\s*{[^}]*margin-top:\s*)\d+px',
            r'\g<1>91px',
            css_content
        )
        
        # Add related articles CSS
        css_content = add_related_articles_css(css_content)
        
        with open(resources_css_path, 'w', encoding='utf-8') as f:
            f.write(css_content)
        
        print("✅ Fixed resources-styles.css")
    
    # Fix article pages
    print("\n2. Fixing article pages...")
    
    patterns = [
        'resources/hypnotherapy/*/index.html',
        'resources/psychology/*/index.html',
        'resources/questions/*/index.html',
        'resources/questions/*/*/index.html'
    ]
    
    fixed_articles = 0
    for pattern in patterns:
        files = glob.glob(os.path.join(script_dir, pattern))
        for file_path in files:
            # Skip category index pages
            if file_path.endswith(('hypnotherapy/index.html', 'psychology/index.html', 'questions/index.html')):
                continue
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix related articles styling
            content = fix_related_articles_styling(content)
            
            # Fix footer consistency
            content = fix_footer_in_article_pages(content, file_path)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_articles += 1
                print(f"Fixed: {os.path.relpath(file_path, script_dir)}")
    
    # Fix category pages
    print("\n3. Fixing category pages...")
    
    category_pages = [
        'resources/hypnotherapy/index.html',
        'resources/psychology/index.html',
        'resources/questions/index.html'
    ]
    
    for page_path in category_pages:
        full_path = os.path.join(script_dir, page_path)
        if os.path.exists(full_path):
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fix any inline styles on category-hero sections
            content = fix_category_hero_styling(content)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Fixed {page_path}")
    
    print(f"\n✅ Fixed {fixed_articles} article pages")
    print("\nAll styling issues have been addressed:")
    print("- Related articles sections now have proper styling")
    print("- Removed duplicate category-hero definitions")
    print("- Standardized margin-top to prevent double-tone effect")
    print("- Ensured footer consistency across pages")

if __name__ == "__main__":
    main()