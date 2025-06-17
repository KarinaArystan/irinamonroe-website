#!/usr/bin/env python3
"""
Fix styling issues for individual article pages and blog footers
"""

import os
import re
from datetime import datetime
import glob

def create_article_styles():
    """Create comprehensive styles for article pages"""
    return '''
    <style>
        /* Article Page Styles */
        .article-hero {
            background: var(--bg-lighter);
            padding: 120px 0 60px;
            margin-top: 76px;
        }
        
        .article-header {
            max-width: 800px;
            margin: 0 auto;
            text-align: center;
        }
        
        .article-header h1 {
            font-family: 'Cormorant Infant', serif;
            font-size: 48px;
            color: var(--text-dark);
            margin-bottom: 20px;
            font-weight: 400;
            line-height: 1.2;
        }
        
        .article-meta {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px;
            font-size: 14px;
            color: var(--accent-brown);
            margin-bottom: 40px;
        }
        
        .article-category {
            text-transform: uppercase;
            letter-spacing: 1px;
            padding: 4px 12px;
            border: 1px solid var(--accent-terra);
            border-radius: 100px;
            color: var(--accent-terra);
        }
        
        .article-content {
            max-width: 800px;
            margin: 0 auto;
            padding: 0 40px;
            font-size: 18px;
            line-height: 1.8;
            color: var(--text-dark);
        }
        
        .article-content h2 {
            font-family: 'Cormorant Infant', serif;
            font-size: 36px;
            color: var(--text-dark);
            margin: 60px 0 30px;
            font-weight: 400;
        }
        
        .article-content h3 {
            font-family: 'Cormorant Infant', serif;
            font-size: 28px;
            color: var(--text-dark);
            margin: 40px 0 20px;
            font-weight: 400;
        }
        
        .article-content p {
            margin-bottom: 25px;
        }
        
        .article-content ul,
        .article-content ol {
            margin: 0 0 25px 20px;
            padding-left: 20px;
        }
        
        .article-content li {
            margin-bottom: 10px;
        }
        
        .article-content blockquote {
            border-left: 4px solid var(--accent-terra);
            padding-left: 30px;
            margin: 40px 0;
            font-style: italic;
            color: #666;
        }
        
        .article-content em {
            font-style: italic;
        }
        
        .article-content strong {
            font-weight: 600;
        }
        
        /* Back to Category Link */
        .back-to-category {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            color: var(--accent-terra);
            text-decoration: none;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 30px;
            transition: all 0.3s ease;
        }
        
        .back-to-category:hover {
            transform: translateX(-5px);
        }
        
        .back-to-category svg {
            transform: rotate(180deg);
        }
        
        /* Article Navigation */
        .article-nav {
            max-width: 800px;
            margin: 80px auto 0;
            padding: 40px;
            border-top: 1px solid #E5E1DC;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .article-nav-link {
            text-decoration: none;
            color: var(--text-dark);
            transition: all 0.3s ease;
        }
        
        .article-nav-link:hover {
            color: var(--accent-terra);
        }
        
        .article-nav-label {
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--accent-brown);
            margin-bottom: 5px;
        }
        
        .article-nav-title {
            font-family: 'Cormorant Infant', serif;
            font-size: 20px;
        }
        
        /* CTA Section */
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
        }
        
        .cta-button {
            background: var(--primary-color);
            color: white;
            padding: 14px 40px;
            border-radius: 100px;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .cta-button:hover {
            background: var(--accent-terra);
            transform: translateY(-2px);
        }
        
        /* Question Page Specific */
        .question-box {
            background: var(--bg-lighter);
            border-left: 4px solid var(--accent-terra);
            padding: 30px;
            margin-bottom: 40px;
            font-style: italic;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .article-header h1 {
                font-size: 36px;
            }
            
            .article-content {
                padding: 0 20px;
                font-size: 16px;
            }
            
            .article-content h2 {
                font-size: 28px;
            }
            
            .article-nav {
                flex-direction: column;
                gap: 30px;
                text-align: center;
            }
        }
    </style>
'''

def fix_individual_article_page(file_path, page_type):
    """Fix styling for individual article pages"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if styles already exist
    if '<style>' in content and 'article-content' in content:
        # Update existing styles
        style_pattern = r'<style>.*?</style>'
        new_styles = create_article_styles()
        content = re.sub(style_pattern, new_styles, content, flags=re.DOTALL)
    else:
        # Add new styles before </head>
        new_styles = create_article_styles() + '\n</head>'
        content = content.replace('</head>', new_styles)
    
    # Ensure proper structure for article pages
    if 'article-hero' not in content and 'article-header' in content:
        # Wrap header in hero section
        header_pattern = r'(<div class="article-header">.*?</div>)'
        replacement = r'''<section class="article-hero">
        <div class="container">
            \1
        </div>
    </section>'''
        content = re.sub(header_pattern, replacement, content, flags=re.DOTALL)
    
    # Add back to category link if missing
    if 'back-to-category' not in content:
        category_links = {
            'hypnotherapy': '../../hypnotherapy/',
            'psychology': '../../psychology/',
            'questions': '../../'
        }
        
        category_link = category_links.get(page_type, '../../')
        category_name = {
            'hypnotherapy': 'Гипнотерапия',
            'psychology': 'Психология',
            'questions': 'Вопросы и ответы'
        }.get(page_type, 'Назад')
        
        back_link = f'''
    <a href="{category_link}" class="back-to-category">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
            <path d="M9 18l6-6-6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
        <span>Вернуться к разделу {category_name}</span>
    </a>
'''
        
        # Insert after breadcrumb or at the beginning of article content
        if '<nav class="breadcrumb">' in content:
            content = re.sub(
                r'(</nav>\s*</div>\s*</section>)',
                r'\1\n    <section class="article-section">\n        <div class="container">' + back_link,
                content,
                count=1
            )
    
    # Add CTA section if missing
    if 'article-cta' not in content and 'footer-placeholder' in content:
        cta_text = {
            'hypnotherapy': ('Готовы исследовать возможности гипнотерапии?', 
                           'Давайте обсудим, как гипнотерапия может помочь именно вам'),
            'psychology': ('Нужна профессиональная поддержка?', 
                         'Я здесь, чтобы помочь вам на пути к пониманию и исцелению'),
            'questions': ('У вас есть свой вопрос?', 
                        'Каждая ситуация уникальна. Давайте найдем решение вместе')
        }.get(page_type, ('Готовы к переменам?', 'Начните свой путь к лучшей версии себя'))
        
        cta_section = f'''
    <!-- CTA Section -->
    <section class="article-cta">
        <div class="container">
            <h2>{cta_text[0]}</h2>
            <p>{cta_text[1]}</p>
            <a href="../../../#contact" class="cta-button">Записаться на консультацию</a>
        </div>
    </section>

    <!-- Footer Placeholder -->'''
        
        content = content.replace('<!-- Footer Placeholder -->', cta_section)
    
    return content

def fix_blog_footer(content):
    """Fix blog footer to match site standard"""
    
    # Standard footer HTML
    standard_footer = '''    <!-- Footer -->
    <footer>
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>IRINA MONROE</h3>
                    <p>Психолог, гипнотерапевт</p>
                    <p>Помогаю людям обрести внутреннюю гармонию и раскрыть свой потенциал</p>
                </div>
                
                <div class="footer-section">
                    <h4>Быстрые ссылки</h4>
                    <ul class="footer-links">
                        <li><a href="../#about">О себе</a></li>
                        <li><a href="../#services">С чем работаю</a></li>
                        <li><a href="../blog/">Блог</a></li>
                        <li><a href="../resources/">Ресурсы</a></li>
                    </ul>
                </div>
                
                <div class="footer-section">
                    <h4>Ресурсы</h4>
                    <ul class="footer-links">
                        <li><a href="../resources/hypnotherapy/">Гипнотерапия</a></li>
                        <li><a href="../resources/psychology/">Психология</a></li>
                        <li><a href="../resources/questions/">Вопросы и ответы</a></li>
                        <li><a href="../faq/">FAQ</a></li>
                    </ul>
                </div>
                
                <div class="footer-section">
                    <h4>Контакты</h4>
                    <ul class="footer-links">
                        <li><a href="../#contact">Записаться на сессию</a></li>
                        <li><a href="../online-sessions/">Онлайн консультации</a></li>
                        <li><a href="../effective-collaboration/">Эффективное сотрудничество</a></li>
                    </ul>
                </div>
            </div>
            
            <div class="footer-bottom">
                <div class="footer-legal">
                    <a href="../privacy-policy/">Политика конфиденциальности</a>
                    <span>•</span>
                    <a href="../therapeutic-contract/">Терапевтический контракт</a>
                </div>
                <p class="copyright">© 2024 IRINA MONROE. ВСЕ ПРАВА ЗАЩИЩЕНЫ.</p>
            </div>
        </div>
    </footer>'''
    
    # Replace existing footer
    footer_pattern = r'<!-- Footer -->.*?</footer>'
    if re.search(footer_pattern, content, re.DOTALL):
        content = re.sub(footer_pattern, standard_footer, content, flags=re.DOTALL)
    else:
        # If no footer found, add before closing body tag
        content = content.replace('</body>', f'{standard_footer}\n</body>')
    
    return content

def process_all_pages():
    """Process all individual article pages and blog pages"""
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create backup
    backup_dir = os.path.join(script_dir, f"backup_article_fixes_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    os.makedirs(backup_dir, exist_ok=True)
    
    fixes_applied = {
        'hypnotherapy': 0,
        'psychology': 0,
        'questions': 0,
        'blog': 0
    }
    
    # Fix individual resource pages
    resource_patterns = [
        ('resources/hypnotherapy/*/index.html', 'hypnotherapy'),
        ('resources/psychology/*/index.html', 'psychology'),
        ('resources/questions/*/index.html', 'questions'),
        ('resources/questions/*/*/index.html', 'questions')
    ]
    
    for pattern, page_type in resource_patterns:
        files = glob.glob(os.path.join(script_dir, pattern))
        for file_path in files:
            # Skip index pages of categories
            if file_path.endswith(f'{page_type}/index.html'):
                continue
                
            print(f"Processing {page_type} page: {os.path.basename(os.path.dirname(file_path))}")
            
            # Backup
            rel_path = os.path.relpath(file_path, script_dir)
            backup_path = os.path.join(backup_dir, rel_path)
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # Fix content
            fixed_content = fix_individual_article_page(file_path, page_type)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            
            fixes_applied[page_type] += 1
    
    # Fix blog pages (including main index and individual posts)
    blog_files = glob.glob(os.path.join(script_dir, 'blog/index.html'))
    blog_files.extend(glob.glob(os.path.join(script_dir, 'blog/*/index.html')))
    
    for file_path in blog_files:
        print(f"Processing blog page: {os.path.basename(os.path.dirname(file_path)) or 'index'}")
        
        # Backup
        rel_path = os.path.relpath(file_path, script_dir)
        backup_path = os.path.join(backup_dir, rel_path)
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original_content)
        
        # Fix footer
        fixed_content = fix_blog_footer(original_content)
        
        # For individual blog posts, also add article styling
        if '/blog/' in file_path and file_path != os.path.join(script_dir, 'blog/index.html'):
            # This is an individual blog post
            fixed_content = fix_individual_article_page(file_path, 'blog')
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        fixes_applied['blog'] += 1
    
    return fixes_applied, backup_dir

def main():
    print("Article Pages and Footer Fix")
    print("=" * 50)
    print("This will fix styling for individual article pages and blog footers\n")
    
    fixes_applied, backup_dir = process_all_pages()
    
    print(f"\n📁 Backup created: {backup_dir}")
    print("\n✅ Fixes applied:")
    print(f"- Hypnotherapy articles: {fixes_applied['hypnotherapy']}")
    print(f"- Psychology articles: {fixes_applied['psychology']}")
    print(f"- Question pages: {fixes_applied['questions']}")
    print(f"- Blog pages: {fixes_applied['blog']}")
    
    print("\nChanges made:")
    print("- Added comprehensive article page styling")
    print("- Fixed blog footers to match site standard")
    print("- Added CTA sections to article pages")
    print("- Improved typography and spacing")
    print("- Made all pages responsive")

if __name__ == "__main__":
    main()