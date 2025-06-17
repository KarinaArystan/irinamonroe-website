#!/usr/bin/env python3
"""
Fix broken resource links in hypnotherapy and questions sections
Maps English URLs to actual Russian directory names
"""

import os
import re
from datetime import datetime

# Mapping of incorrect English links to actual Russian directory names
HYPNOTHERAPY_MAPPINGS = {
    'what-is-hypnosis/': 'gipnos/',
    'how-it-works/': 'gipnoterapia-kak-eto-rabotaet/',
    'who-is-hypnotherapist/': 'kto-takoi-gipnoterapevt/',
    'sensations-during-hypnosis/': 'ctho-chuvstvuetsya-vo-vremya-gipnoza/',
    'stages-of-hypnosis/': 'stadii-gipnoxa/',
    'self-hypnosis/': 'samogipnoz/',
    'time-distortion/': 'iskageniya-vremeni-v-gipnoze/',
    'meditation-vs-hypnosis/': 'raznitsa-megdu-meditatsiei-i-gipnozom/',
    'hypersuggestibility/': 'chto-takoe-gipervnushaemost/',
    'suggestibility/': 'vnushaemost-opredelenie/',
}

# List of actual question directories to display
QUESTION_DIRECTORIES = {
    'family': [
        'kak-vernut-lubov-muzha',
        'otnosheniya-s-parnem',
        'izmena-muzha',
        'ne-mogu-prostit-proshloe',
        'depressiya-kak-byt',
        'slognie-otnosheniya',
        'emotsionalnoe-vigoranie',
        'kak-polyubit-sebya'
    ],
    'relationships': [
        'u-zheny-byl-drugoj-muzhchina',
        'gena-polubila-drugogo',
        'on-genat-ya-zamugem-otnosheniya',
        'izmena-vo-sne',
        'revnost-k-proshlomu',
        'myg-stal-otreshennim',
        'ne-chuvstvyu-sebya-schastlivoi'
    ],
    'general': [
        'pochemu-ya-hochu-chtoby-menya',
        'mne-bezumno-stydno',
        'rezhu-sebya',
        'kleptomania'
    ]
}

def fix_hypnotherapy_links(content):
    """Fix hypnotherapy section links"""
    changes_made = []
    
    for old_link, new_link in HYPNOTHERAPY_MAPPINGS.items():
        pattern = f'href="([^"]*{old_link}[^"]*)"'
        
        def replace_func(match):
            old_href = match.group(0)
            new_href = old_href.replace(old_link, new_link)
            if old_href != new_href:
                changes_made.append(f"  {old_href} → {new_href}")
            return new_href
        
        content = re.sub(pattern, replace_func, content)
    
    return content, changes_made

def get_question_title(directory_name):
    """Convert directory name to human-readable title"""
    titles = {
        'kak-vernut-lubov-muzha': 'Как вернуть любовь мужа?',
        'otnosheniya-s-parnem': 'Отношения с парнем',
        'izmena-muzha': 'Измена мужа',
        'ne-mogu-prostit-proshloe': 'Не могу простить прошлое',
        'depressiya-kak-byt': 'Депрессия - как быть?',
        'slognie-otnosheniya': 'Сложные отношения',
        'emotsionalnoe-vigoranie': 'Эмоциональное выгорание',
        'kak-polyubit-sebya': 'Как полюбить себя?',
        'u-zheny-byl-drugoj-muzhchina': 'У жены был другой мужчина',
        'gena-polubila-drugogo': 'Жена полюбила другого',
        'on-genat-ya-zamugem-otnosheniya': 'Он женат, я замужем',
        'izmena-vo-sne': 'Измена во сне',
        'revnost-k-proshlomu': 'Ревность к прошлому',
        'myg-stal-otreshennim': 'Муж стал отрешенным',
        'ne-chuvstvyu-sebya-schastlivoi': 'Не чувствую себя счастливой',
        'pochemu-ya-hochu-chtoby-menya': 'Почему я хочу, чтобы меня...',
        'mne-bezumno-stydno': 'Мне безумно стыдно',
        'rezhu-sebya': 'Режу себя',
        'kleptomania': 'Клептомания'
    }
    return titles.get(directory_name, directory_name.replace('-', ' ').title())

def generate_questions_section():
    """Generate the questions section with real links"""
    html = []
    
    # Family Questions
    if QUESTION_DIRECTORIES['family']:
        html.append('''
                <div class="qa-topic-block">
                    <h3>Семейные вопросы</h3>
                    <div class="question-links">''')
        
        for i, question in enumerate(QUESTION_DIRECTORIES['family'][:4]):
            title = get_question_title(question)
            html.append(f'''
                        <a href="../resources/questions/family/{question}/" class="question-link">
                            <span class="question-icon">?</span>
                            <span>{title}</span>
                        </a>''')
        
        html.append('''
                    </div>
                </div>''')
    
    # Relationship Questions
    if QUESTION_DIRECTORIES['relationships']:
        html.append('''
                <div class="qa-topic-block">
                    <h3>Вопросы отношений</h3>
                    <div class="question-links">''')
        
        for i, question in enumerate(QUESTION_DIRECTORIES['relationships'][:4]):
            title = get_question_title(question)
            html.append(f'''
                        <a href="../resources/questions/relationships/{question}/" class="question-link">
                            <span class="question-icon">?</span>
                            <span>{title}</span>
                        </a>''')
        
        html.append('''
                    </div>
                </div>''')
    
    # General Questions
    if QUESTION_DIRECTORIES['general']:
        html.append('''
                <div class="qa-topic-block">
                    <h3>Общие вопросы</h3>
                    <div class="question-links">''')
        
        for i, question in enumerate(QUESTION_DIRECTORIES['general'][:4]):
            title = get_question_title(question)
            html.append(f'''
                        <a href="../resources/questions/general/{question}/" class="question-link">
                            <span class="question-icon">?</span>
                            <span>{title}</span>
                        </a>''')
        
        html.append('''
                    </div>
                </div>''')
    
    return '\n'.join(html)

def fix_resource_pages(root_dir):
    """Fix all resource page links"""
    changes = {}
    
    # Fix hypnotherapy index page
    hypno_index = os.path.join(root_dir, 'resources', 'hypnotherapy', 'index.html')
    if os.path.exists(hypno_index):
        print(f"Fixing hypnotherapy links in: {hypno_index}")
        
        with open(hypno_index, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content, changes_made = fix_hypnotherapy_links(content)
        
        if changes_made:
            with open(hypno_index, 'w', encoding='utf-8') as f:
                f.write(new_content)
            changes['hypnotherapy'] = changes_made
            print(f"  ✓ Fixed {len(changes_made)} links")
        else:
            print("  - No changes needed")
    
    # Fix questions index page - replace placeholder content
    questions_index = os.path.join(root_dir, 'resources', 'questions', 'index.html')
    if os.path.exists(questions_index):
        print(f"\nFixing questions page: {questions_index}")
        
        with open(questions_index, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and replace the example topics section
        pattern = r'<!-- Example Topics -->(.*?)<!-- CTA Section -->'
        
        if re.search(pattern, content, re.DOTALL):
            new_topics_html = f'''<!-- Example Topics -->
            <div class="topics-examples">
                <h2>Примеры вопросов</h2>
                <p class="topics-intro">
                    Здесь вы найдете ответы на реальные вопросы от людей, 
                    столкнувшихся с похожими ситуациями. Каждый ответ написан с 
                    глубоким пониманием и заботой.
                </p>
                
{generate_questions_section()}
            </div>
            
            <!-- CTA Section -->'''
            
            content = re.sub(pattern, new_topics_html, content, flags=re.DOTALL)
            
            with open(questions_index, 'w', encoding='utf-8') as f:
                f.write(content)
            
            changes['questions'] = ['Replaced placeholder links with real question links']
            print("  ✓ Updated questions section with real links")
    
    # Save change log
    if changes:
        log_file = os.path.join(root_dir, 'resource_links_fix.log')
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(f"Resource Links Fixed on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for section, section_changes in changes.items():
                f.write(f"\n{section.upper()} Section:\n")
                f.write(f"{'=' * 50}\n")
                for change in section_changes:
                    f.write(f"{change}\n")
        
        print(f"\n📄 Change log saved to: resource_links_fix.log")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("Resource Links Fixer")
    print("=" * 50)
    print("This will fix broken links in hypnotherapy and questions sections\n")
    
    # Create backup first
    backup_dir = os.path.join(script_dir, f"backup_resources_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    os.makedirs(backup_dir, exist_ok=True)
    
    # Backup the resource files
    import shutil
    for file_path in ['resources/hypnotherapy/index.html', 'resources/questions/index.html']:
        full_path = os.path.join(script_dir, file_path)
        if os.path.exists(full_path):
            backup_path = os.path.join(backup_dir, file_path)
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)
            shutil.copy2(full_path, backup_path)
    
    print(f"Backup created: {backup_dir}\n")
    
    # Fix the resource pages
    fix_resource_pages(script_dir)
    
    print("\n✅ Done! Resource links have been fixed.")
    print("\nNext steps:")
    print("1. Test the links locally")
    print("2. Commit and push the changes")
    print("   git add -A")
    print('   git commit -m "Fix broken resource links - map English URLs to Russian directories"')
    print("   git push")

if __name__ == "__main__":
    main()