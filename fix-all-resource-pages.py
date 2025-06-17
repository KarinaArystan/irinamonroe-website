#!/usr/bin/env python3
"""
Comprehensive fix for all resource article pages
"""

import os
import re
import glob

def get_relative_path_prefix(file_path):
    """Get the correct relative path prefix based on file depth"""
    rel_path = os.path.relpath(file_path, os.path.dirname(os.path.abspath(__file__)))
    depth = len(rel_path.split(os.sep)) - 1
    
    if 'questions' in rel_path and rel_path.count(os.sep) == 4:
        return '../../../../'
    elif rel_path.count(os.sep) == 3:
        return '../../../'
    elif rel_path.count(os.sep) == 2:
        return '../../'
    else:
        return '../'

def create_header_html(prefix):
    """Create header HTML with correct relative paths"""
    return f'''    <!-- Header -->
    <header>
        <nav class="container">
            <a href="{prefix}index.html" class="logo-link"><div class="logo">IRINA MONROE</div></a>
            
            <!-- Mobile Header Controls -->
            <div class="mobile-controls">
                <!-- Mobile Menu Button -->
                <button class="mobile-menu-toggle" aria-label="Открыть меню">
                    <span class="hamburger"></span>
                    <span class="hamburger"></span>
                    <span class="hamburger"></span>
                </button>
            </div>
            
            <!-- Navigation -->
            <ul class="nav-links">
                <li><a href="{prefix}#about">О себе</a></li>
                <li><a href="{prefix}#services">С чем работаю</a></li>
                <li class="has-dropdown">
                    <a href="#" class="dropdown-toggle">Ресурсы
                        <svg class="dropdown-arrow" width="10" height="6" viewBox="0 0 10 6" fill="none">
                            <path d="M1 1L5 5L9 1" stroke="currentColor" stroke-width="1.5"/>
                        </svg>
                    </a>
                    <div class="dropdown-menu">
                        <a href="{prefix}resources/hypnotherapy/">Гипнотерапия</a>
                        <a href="{prefix}resources/psychology/">Психология и травма</a>
                        <a href="{prefix}resources/questions/">Вопросы и ответы</a>
                        <a href="{prefix}therapy-sessions/">Онлайн консультации</a>
                    </div>
                </li>
                <li><a href="{prefix}blog/">Блог</a></li>
                <li class="header-search">
                    <form action="{prefix}search/" method="GET">
                        <input type="text" name="q" placeholder="Поиск..." autocomplete="off">
                        <button type="button" onclick="toggleSearch(this)">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <circle cx="11" cy="11" r="8"></circle>
                                <path d="m21 21-4.35-4.35"></path>
                            </svg>
                        </button>
                    </form>
                </li>
                <li><a href="{prefix}#contact" class="nav-cta">Связаться</a></li>
                <!-- Social Icons for Mobile -->
                <li class="social-icons-mobile">
                    <a href="https://wa.me/YOUR_WHATSAPP_NUMBER" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.890-5.335 11.893-11.893A11.821 11.821 0 0020.525 3.488" fill="currentColor"/>
                        </svg>
                    </a>
                    <a href="https://t.me/YOUR_TELEGRAM" target="_blank" rel="noopener noreferrer" aria-label="Telegram">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z" fill="currentColor"/>
                        </svg>
                    </a>
                    <a href="https://www.youtube.com/@IrinaMonroe" target="_blank" rel="noopener noreferrer" aria-label="YouTube">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z" fill="currentColor"/>
                        </svg>
                    </a>
                    <a href="https://www.instagram.com/monroe__irina/" target="_blank" rel="noopener noreferrer" aria-label="Instagram">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zM5.838 12a6.162 6.162 0 1 1 12.324 0 6.162 6.162 0 0 1-12.324 0zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm4.965-10.405a1.44 1.44 0 1 1 2.881.001 1.44 1.44 0 0 1-2.881-.001z" fill="currentColor"/>
                        </svg>
                    </a>
                </li>
            </ul>
        </nav>
    </header>'''

def create_footer_html(prefix):
    """Create footer HTML with correct relative paths"""
    return f'''    <!-- Footer -->
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
                        <li><a href="{prefix}#about">О себе</a></li>
                        <li><a href="{prefix}#services">С чем работаю</a></li>
                        <li><a href="{prefix}blog/">Блог</a></li>
                        <li><a href="{prefix}resources/">Ресурсы</a></li>
                    </ul>
                </div>
                
                <div class="footer-section">
                    <h4>Ресурсы</h4>
                    <ul class="footer-links">
                        <li><a href="{prefix}resources/hypnotherapy/">Гипнотерапия</a></li>
                        <li><a href="{prefix}resources/psychology/">Психология</a></li>
                        <li><a href="{prefix}resources/questions/">Вопросы и ответы</a></li>
                        <li><a href="{prefix}faq/">FAQ</a></li>
                    </ul>
                </div>
                
                <div class="footer-section">
                    <h4>Контакты</h4>
                    <ul class="footer-links">
                        <li><a href="{prefix}#contact">Записаться на сессию</a></li>
                        <li><a href="{prefix}online-sessions/">Онлайн консультации</a></li>
                        <li><a href="{prefix}effective-collaboration/">Эффективное сотрудничество</a></li>
                    </ul>
                </div>
            </div>
            
            <div class="footer-bottom">
                <div class="footer-legal">
                    <a href="{prefix}privacy-policy/">Политика конфиденциальности</a>
                    <span>•</span>
                    <a href="{prefix}therapeutic-contract/">Терапевтический контракт</a>
                </div>
                <p class="copyright">© 2024 IRINA MONROE. ВСЕ ПРАВА ЗАЩИЩЕНЫ.</p>
            </div>
        </div>
    </footer>'''

def fix_resource_page(file_path):
    """Fix an individual resource page with proper header, footer, and paths"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    prefix = get_relative_path_prefix(file_path)
    
    # Replace header placeholder
    header_html = create_header_html(prefix)
    content = re.sub(
        r'<!-- Header Placeholder -->.*?<div class="header-placeholder"></div>',
        header_html,
        content,
        flags=re.DOTALL
    )
    
    # If no header placeholder found, add after <body>
    if '<div class="header-placeholder"></div>' not in content and header_html not in content:
        content = content.replace('<body>', f'<body>\n{header_html}')
    
    # Replace footer placeholder
    footer_html = create_footer_html(prefix)
    content = re.sub(
        r'<!-- Footer Placeholder -->.*?<div class="footer-placeholder"></div>',
        footer_html,
        content,
        flags=re.DOTALL
    )
    
    # If no footer placeholder found, add before </body>
    if '<div class="footer-placeholder"></div>' not in content and footer_html not in content:
        content = content.replace('</body>', f'{footer_html}\n</body>')
    
    # Ensure CSS variables are defined
    if '<style>' in content and '--bg-light' not in content:
        css_vars = '''
        :root {
            --primary-color: #93884A;
            --accent-terra: #AB7C5B;
            --accent-green: #7A9F6B;
            --accent-brown: #8B8680;
            --text-dark: #2C2B29;
            --text-light: #6B6966;
            --bg-light: #F9F7F5;
            --bg-lighter: #FAF8F6;
            --bg-section: #F4F2EF;
            --white: #FFFFFF;
            --border-color: #E5E1DC;
            --text-muted: #8B8680;
        }
        '''
        content = content.replace('<style>', f'<style>\n{css_vars}')
    
    return content

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("Comprehensive Resource Page Fix")
    print("=" * 50)
    print("Fixing all resource pages with proper headers, footers, and paths...\n")
    
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
            
            print(f"Fixing: {os.path.relpath(file_path, script_dir)}")
            
            fixed_content = fix_resource_page(file_path)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            
            fixed += 1
    
    print(f"\n✅ Fixed {fixed} resource pages")
    print("\nAll pages now have:")
    print("- Proper header with correct relative paths")
    print("- Proper footer with correct relative paths") 
    print("- CSS variables defined")
    print("- Correct styling")

if __name__ == "__main__":
    main()