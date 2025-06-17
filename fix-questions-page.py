#!/usr/bin/env python3
"""
Fix the questions page to use real existing question links
"""

import os

def generate_questions_html():
    """Generate the complete questions page with real links"""
    return '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Вопросы и ответы - Реальные вопросы и терапевтические инсайты от Ирины Монро">
    <title>Вопросы и ответы | Ирина Монро</title>
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Infant:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400;1,500;1,600;1,700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    
    <!-- External CSS -->
    <link rel="stylesheet" href="../../styles.css">
    <link rel="stylesheet" href="../../mobile-fixes.css">
    <link rel="stylesheet" href="../resources-styles.css">
</head>
<body>
    <!-- Placeholder header - will be replaced with actual header component -->
    <div class="header-placeholder"></div>

    <!-- Category Hero Section -->
    <section class="category-hero">
        <div class="container">
            <nav class="breadcrumb">
                <a href="../../index.html">Главная</a>
                <span>/</span>
                <a href="../../resources/">Ресурсы</a>
                <span>/</span>
                <span>Вопросы и ответы</span>
            </nav>
            <h1>Вопросы и ответы</h1>
            <p>Реальные вопросы от реальных людей с терапевтическими инсайтами и руководством</p>
        </div>
    </section>

    <!-- Q&A Categories and Search -->
    <section class="topics-section">
        <div class="container">
            <!-- Category Pills -->
            <div class="qa-categories">
                <a href="#" class="category-pill active" data-category="all">
                    <span>Все вопросы</span>
                </a>
                <a href="#" class="category-pill" data-category="relationships">
                    <span>Пары и отношения</span>
                </a>
                <a href="#" class="category-pill" data-category="family">
                    <span>Семья</span>
                </a>
                <a href="#" class="category-pill" data-category="general">
                    <span>Общие вопросы</span>
                </a>
            </div>

            <!-- Q&A List -->
            <div class="topics-list" id="qa-list">
                <!-- Family Questions -->
                <h2 style="font-family: 'Cormorant Infant', serif; font-size: 32px; margin: 40px 0 20px; color: var(--text-dark);">Семейные вопросы</h2>
                
                <a href="../../resources/questions/family/kak-vernut-lubov-muzha/" class="topic-item" data-category="family">
                    <h3>Как вернуть любовь мужа?</h3>
                    <p>Понимание динамики отношений и путей к восстановлению близости...</p>
                </a>
                
                <a href="../../resources/questions/family/otnosheniya-s-parnem/" class="topic-item" data-category="family">
                    <h3>Отношения с парнем</h3>
                    <p>Навигация в сложностях романтических отношений...</p>
                </a>
                
                <a href="../../resources/questions/family/izmena-muzha/" class="topic-item" data-category="family">
                    <h3>Измена мужа</h3>
                    <p>Как справиться с предательством и найти путь вперед...</p>
                </a>
                
                <a href="../../resources/questions/family/ne-mogu-prostit-proshloe/" class="topic-item" data-category="family">
                    <h3>Не могу простить прошлое</h3>
                    <p>Работа с обидами и путь к прощению...</p>
                </a>
                
                <a href="../../resources/questions/family/depressiya-kak-byt/" class="topic-item" data-category="family">
                    <h3>Депрессия - как быть?</h3>
                    <p>Понимание депрессии и поиск путей выхода...</p>
                </a>
                
                <a href="../../resources/questions/family/slognie-otnosheniya/" class="topic-item" data-category="family">
                    <h3>Сложные отношения</h3>
                    <p>Работа с трудностями в партнерских отношениях...</p>
                </a>
                
                <a href="../../resources/questions/family/emotsionalnoe-vigoranie/" class="topic-item" data-category="family">
                    <h3>Эмоциональное выгорание</h3>
                    <p>Распознавание и преодоление эмоционального истощения...</p>
                </a>
                
                <a href="../../resources/questions/family/kak-polyubit-sebya/" class="topic-item" data-category="family">
                    <h3>Как полюбить себя?</h3>
                    <p>Путь к самопринятию и внутренней гармонии...</p>
                </a>
                
                <!-- Relationships Questions -->
                <h2 style="font-family: 'Cormorant Infant', serif; font-size: 32px; margin: 40px 0 20px; color: var(--text-dark);">Вопросы отношений</h2>
                
                <a href="../../resources/questions/relationships/u-zheny-byl-drugoj-muzhchina/" class="topic-item" data-category="relationships">
                    <h3>У жены был другой мужчина</h3>
                    <p>Как справиться с изменой и восстановить доверие...</p>
                </a>
                
                <a href="../../resources/questions/relationships/gena-polubila-drugogo/" class="topic-item" data-category="relationships">
                    <h3>Жена полюбила другого</h3>
                    <p>Когда любовь уходит: понимание и принятие...</p>
                </a>
                
                <a href="../../resources/questions/relationships/on-genat-ya-zamugem-otnosheniya/" class="topic-item" data-category="relationships">
                    <h3>Он женат, я замужем</h3>
                    <p>Сложность запретных чувств и моральные дилеммы...</p>
                </a>
                
                <a href="../../resources/questions/relationships/izmena-vo-sne/" class="topic-item" data-category="relationships">
                    <h3>Измена во сне</h3>
                    <p>Что означают сны об измене и как с ними работать...</p>
                </a>
                
                <a href="../../resources/questions/relationships/revnost-k-proshlomu/" class="topic-item" data-category="relationships">
                    <h3>Ревность к прошлому</h3>
                    <p>Как справиться с ревностью к прошлому партнера...</p>
                </a>
                
                <a href="../../resources/questions/relationships/myg-stal-otreshennim/" class="topic-item" data-category="relationships">
                    <h3>Муж стал отрешенным</h3>
                    <p>Когда партнер эмоционально отдаляется...</p>
                </a>
                
                <a href="../../resources/questions/relationships/ne-chuvstvyu-sebya-schastlivoi/" class="topic-item" data-category="relationships">
                    <h3>Не чувствую себя счастливой</h3>
                    <p>Поиск счастья в отношениях и жизни...</p>
                </a>
                
                <!-- General Questions -->
                <h2 style="font-family: 'Cormorant Infant', serif; font-size: 32px; margin: 40px 0 20px; color: var(--text-dark);">Общие вопросы</h2>
                
                <a href="../../resources/questions/general/pochemu-ya-hochu-chtoby-menya/" class="topic-item" data-category="general">
                    <h3>Почему я хочу, чтобы меня...</h3>
                    <p>Исследование глубинных желаний и потребностей...</p>
                </a>
                
                <a href="../../resources/questions/general/mne-bezumno-stydno/" class="topic-item" data-category="general">
                    <h3>Мне безумно стыдно</h3>
                    <p>Работа с чувством стыда и самопринятие...</p>
                </a>
                
                <a href="../../resources/questions/general/rezhu-sebya/" class="topic-item" data-category="general">
                    <h3>Режу себя</h3>
                    <p>Понимание самоповреждения и поиск помощи...</p>
                </a>
                
                <a href="../../resources/questions/general/kleptomania/" class="topic-item" data-category="general">
                    <h3>Клептомания</h3>
                    <p>Понимание компульсивного поведения и путь к исцелению...</p>
                </a>
            </div>
        </div>
    </section>

    <!-- CTA Section -->
    <section style="background: var(--bg-light); padding: 60px 0; margin-top: 80px;">
        <div class="container" style="text-align: center;">
            <h2 style="font-family: 'Cormorant Infant', serif; font-size: 36px; margin-bottom: 20px;">
                Не нашли свой вопрос?
            </h2>
            <p style="font-size: 18px; margin-bottom: 30px; max-width: 600px; margin-left: auto; margin-right: auto;">
                Каждая ситуация уникальна. Я здесь, чтобы помочь вам найти ваш собственный путь к пониманию и исцелению.
            </p>
            <a href="../../therapy-sessions/" style="background: var(--primary-color); color: white; padding: 14px 40px; border-radius: 100px; text-decoration: none; display: inline-block; font-size: 16px; transition: all 0.3s ease;">
                Записаться на консультацию
            </a>
        </div>
    </section>

    <!-- Placeholder footer - will be replaced with actual footer component -->
    <div class="footer-placeholder"></div>

    <!-- External JavaScript -->
    <script src="../../script.js"></script>
    <script>
        // Category filtering
        const categoryPills = document.querySelectorAll('.category-pill');
        const qaItems = document.querySelectorAll('.topic-item');

        categoryPills.forEach(pill => {
            pill.addEventListener('click', (e) => {
                e.preventDefault();
                
                // Update active pill
                categoryPills.forEach(p => p.classList.remove('active'));
                pill.classList.add('active');
                
                // Filter items
                const category = pill.dataset.category;
                qaItems.forEach(item => {
                    if (category === 'all' || item.dataset.category === category) {
                        item.style.display = 'block';
                    } else {
                        item.style.display = 'none';
                    }
                });
                
                // Show/hide section headers
                const headers = document.querySelectorAll('.topics-list h2');
                if (category === 'all') {
                    headers.forEach(h => h.style.display = 'block');
                } else {
                    headers.forEach(h => h.style.display = 'none');
                }
            });
        });
    </script>
</body>
</html>'''

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    questions_file = os.path.join(script_dir, 'resources', 'questions', 'index.html')
    
    print("Fixing questions page with real links...")
    
    # Write the new content
    with open(questions_file, 'w', encoding='utf-8') as f:
        f.write(generate_questions_html())
    
    print(f"✅ Fixed: {questions_file}")
    print("\nThe questions page now contains real links to existing question pages.")

if __name__ == "__main__":
    main()