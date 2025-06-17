#!/usr/bin/env python3
"""
Fix styling issues in psychology and questions resource pages
Makes them consistent with blog page styling and site aesthetics
"""

import os
import re
from datetime import datetime

def fix_psychology_page(content):
    """Add proper styling to psychology page to match blog aesthetics"""
    
    # Add inline styles for psychology page - similar to hypnotherapy page approach
    style_section = '''    
    <style>
        /* Psychology Page Styles - Matching Blog Card Aesthetics */
        .topics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 40px;
            margin-top: 40px;
        }
        
        .topic-card {
            background: white;
            border: 1px solid #E5E1DC;
            border-radius: 8px;
            overflow: hidden;
            transition: all 0.3s ease;
            text-decoration: none;
            display: block;
            height: 100%;
        }
        
        .topic-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            border-color: var(--accent-terra);
        }
        
        .topic-content {
            padding: 40px;
        }
        
        .topic-card h2 {
            font-family: 'Cormorant Infant', serif;
            font-size: 28px;
            font-weight: 400;
            color: var(--text-dark);
            margin-bottom: 15px;
            line-height: 1.2;
            transition: color 0.3s ease;
        }
        
        .topic-card:hover h2 {
            color: var(--accent-terra);
        }
        
        .topic-card p {
            font-size: 16px;
            line-height: 1.6;
            color: var(--text-dark);
            margin-bottom: 20px;
        }
        
        .topic-link {
            color: var(--accent-terra);
            font-size: 14px;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            text-decoration: none;
        }
        
        .topic-link svg {
            transition: transform 0.3s ease;
        }
        
        .topic-card:hover .topic-link {
            gap: 12px;
        }
        
        .topic-card:hover .topic-link svg {
            transform: translateX(4px);
        }
        
        /* Intro Section */
        .intro-section {
            max-width: 800px;
            margin: 0 auto 60px;
            text-align: center;
        }
        
        .intro-section p {
            font-size: 18px;
            line-height: 1.8;
            color: var(--text-dark);
        }
        
        /* CTA Section */
        .cta-section {
            background: var(--bg-light);
            padding: 80px 0;
            margin-top: 80px;
            text-align: center;
        }
        
        .cta-section h2 {
            font-family: 'Cormorant Infant', serif;
            font-size: 36px;
            font-weight: 400;
            margin-bottom: 20px;
            color: var(--text-dark);
        }
        
        .cta-section p {
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
        
        @media (max-width: 768px) {
            .topics-grid {
                grid-template-columns: 1fr;
                gap: 30px;
            }
            
            .topic-content {
                padding: 30px;
            }
            
            .topic-card h2 {
                font-size: 24px;
            }
        }
    </style>
</head>'''
    
    # Insert the styles before </head>
    content = content.replace('</head>', style_section)
    
    # Add intro section after category hero
    intro_html = '''
    <!-- Introduction -->
    <section class="topics-section">
        <div class="container">
            <div class="intro-section">
                <p>
                    Исследуйте глубинные аспекты человеческой психики, понимание травмы и путей исцеления. 
                    Эти материалы помогут вам лучше понять себя и свои эмоциональные состояния.
                </p>
            </div>'''
    
    # Replace the section opening
    content = content.replace(
        '<!-- Психология Articles Grid -->\n    <section class="topics-section">\n        <div class="container">',
        intro_html
    )
    
    # Add CTA section before footer
    cta_html = '''
    <!-- CTA Section -->
    <section class="cta-section">
        <div class="container">
            <h2>Готовы к глубинной работе?</h2>
            <p>
                Понимание психологических механизмов - первый шаг. 
                Давайте вместе исследуем ваш внутренний мир.
            </p>
            <a href="../../#contact" class="cta-button">
                Записаться на консультацию
            </a>
        </div>
    </section>

    <!-- Footer Placeholder -->'''
    
    # Replace footer placeholder
    content = content.replace('    <!-- Footer Placeholder -->', cta_html)
    
    return content


def fix_questions_page(content):
    """Update questions page styling to match site aesthetics"""
    
    # Add enhanced styles for questions page
    enhanced_styles = '''
    <style>
        /* Enhanced Questions Page Styles */
        .topics-list {
            margin-top: 40px;
        }
        
        .topics-list h2 {
            font-family: 'Cormorant Infant', serif;
            font-size: 32px;
            margin: 60px 0 30px;
            color: var(--text-dark);
            font-weight: 400;
            text-align: center;
            position: relative;
            padding-bottom: 20px;
        }
        
        .topics-list h2:after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 60px;
            height: 2px;
            background: var(--accent-terra);
        }
        
        .topics-list h2:first-child {
            margin-top: 40px;
        }
        
        .topic-item {
            display: block;
            background: white;
            border: 1px solid #E5E1DC;
            border-radius: 8px;
            padding: 30px 40px;
            margin-bottom: 20px;
            text-decoration: none;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .topic-item::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(147, 136, 74, 0.05), transparent);
            transition: left 0.5s ease;
        }
        
        .topic-item:hover::before {
            left: 100%;
        }
        
        .topic-item:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
            border-color: var(--accent-terra);
        }
        
        .topic-item h3 {
            font-family: 'Cormorant Infant', serif;
            font-size: 24px;
            color: var(--text-dark);
            margin-bottom: 10px;
            font-weight: 400;
            transition: color 0.3s ease;
        }
        
        .topic-item:hover h3 {
            color: var(--accent-terra);
        }
        
        .topic-item p {
            font-size: 16px;
            color: var(--text-dark);
            line-height: 1.6;
            margin: 0;
            opacity: 0.85;
        }
        
        /* Category Pills Enhancement */
        .qa-categories {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-bottom: 40px;
            flex-wrap: wrap;
        }
        
        .category-pill {
            padding: 10px 24px;
            border: 1px solid var(--accent-brown);
            border-radius: 100px;
            text-decoration: none;
            color: var(--accent-brown);
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s ease;
            background: white;
            cursor: pointer;
        }
        
        .category-pill:hover,
        .category-pill.active {
            background: var(--primary-color);
            color: white;
            border-color: var(--primary-color);
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(147, 136, 74, 0.2);
        }
        
        /* Intro Section */
        .intro-section {
            max-width: 800px;
            margin: 0 auto 50px;
            text-align: center;
        }
        
        .intro-section p {
            font-size: 18px;
            line-height: 1.8;
            color: var(--text-dark);
        }
        
        /* CTA Section Enhancement */
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
        
        @media (max-width: 768px) {
            .topic-item {
                padding: 25px 30px;
            }
            
            .topic-item h3 {
                font-size: 22px;
            }
            
            .topics-list h2 {
                font-size: 28px;
            }
            
            .qa-categories {
                gap: 10px;
            }
            
            .category-pill {
                padding: 8px 20px;
                font-size: 13px;
            }
        }
    </style>
</head>'''
    
    # Insert the styles before </head>
    content = content.replace('</head>', enhanced_styles)
    
    # Add intro section after category pills
    intro_html = '''
            <!-- Introduction -->
            <div class="intro-section">
                <p>
                    Каждый вопрос - это возможность для глубокого понимания и трансформации. 
                    Здесь вы найдете ответы на реальные вопросы от людей, ищущих путь к исцелению.
                </p>
            </div>
            
            <!-- Q&A List -->'''
    
    # Insert intro before Q&A List
    content = content.replace('            <!-- Q&A List -->', intro_html)
    
    # Update CTA button
    content = content.replace(
        '<a href="../../therapy-sessions/" style="background: var(--primary-color); color: white; padding: 14px 40px; border-radius: 100px; text-decoration: none; display: inline-block; font-size: 16px; transition: all 0.3s ease;">',
        '<a href="../../#contact" class="cta-button">'
    )
    
    return content


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("Resource Pages Styling Fix")
    print("=" * 50)
    print("This will fix styling issues in psychology and questions pages\n")
    
    # Create backup
    backup_dir = os.path.join(script_dir, f"backup_styling_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    os.makedirs(backup_dir, exist_ok=True)
    
    # Files to fix
    files_to_fix = {
        'resources/psychology/index.html': fix_psychology_page,
        'resources/questions/index.html': fix_questions_page
    }
    
    # Process each file
    for file_path, fix_function in files_to_fix.items():
        full_path = os.path.join(script_dir, file_path)
        
        if os.path.exists(full_path):
            print(f"Processing: {file_path}")
            
            # Backup
            import shutil
            backup_path = os.path.join(backup_dir, file_path)
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)
            shutil.copy2(full_path, backup_path)
            
            # Read and fix content
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            fixed_content = fix_function(content)
            
            # Write fixed content
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            
            print(f"  ✓ Fixed styling")
    
    print(f"\n📁 Backup created: {backup_dir}")
    print("\n✅ Done! Resource pages now have consistent styling.")
    print("\nChanges made:")
    print("- Psychology page: Added blog-style card layout with hover effects")
    print("- Questions page: Enhanced link styling with smooth transitions")
    print("- Both pages: Added intro sections and improved visual hierarchy")
    print("- Both pages: Added styled CTA sections")
    print("- Both pages: Made responsive for mobile devices")

if __name__ == "__main__":
    main()