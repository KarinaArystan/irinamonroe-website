const fs = require('fs');
const path = require('path');

// True psychology/trauma pages that should remain
const psychologyPages = [
    'vnytrenniy-rebenok',
    'travma-iskagaet-vospriyatie',
    'travma-moget-emotsionalno-zamorozit',
    'istselenie-travmi-trebuet-vremeni',
    'emotsii-svyazani-s-telom',
    'emotsionalnie-sostoyaniya',
    'proektsia-zerkalo-vneyrennego-mira',
    'linza-vospriyatia-sebya-i-mira'
];

const psychologyDir = '/Users/Karina/Library/CloudStorage/GoogleDrive-karina.arystan@gmail.com/My Drive/Projects/irinamonroe.com/new-site/resources/psychology';
const questionsDir = '/Users/Karina/Library/CloudStorage/GoogleDrive-karina.arystan@gmail.com/My Drive/Projects/irinamonroe.com/new-site/resources/questions';

// Get all subdirectories in psychology folder
const entries = fs.readdirSync(psychologyDir, { withFileTypes: true });
const directories = entries.filter(dirent => dirent.isDirectory()).map(dirent => dirent.name);

console.log(`Found ${directories.length} directories in psychology folder\n`);

let movedCount = 0;
let keptCount = 0;

directories.forEach(dir => {
    if (!psychologyPages.includes(dir)) {
        // This is a Q&A page that needs to be moved
        const sourcePath = path.join(psychologyDir, dir);
        
        // Check if this page has content that suggests a category
        const indexPath = path.join(sourcePath, 'index.html');
        if (fs.existsSync(indexPath)) {
            const content = fs.readFileSync(indexPath, 'utf-8');
            
            // Determine category from content
            let category = 'general';
            if (content.includes('семья') || content.includes('дети') || content.includes('родител')) {
                category = 'family';
            } else if (content.includes('отношения') || content.includes('любов') || content.includes('партнер')) {
                category = 'relationships';
            } else if (content.includes('измен')) {
                category = 'infidelity';
            }
            
            // Create category directory if needed
            const categoryDir = path.join(questionsDir, category);
            if (!fs.existsSync(categoryDir)) {
                fs.mkdirSync(categoryDir, { recursive: true });
            }
            
            // Move the directory
            const targetPath = path.join(categoryDir, dir);
            if (!fs.existsSync(targetPath)) {
                fs.renameSync(sourcePath, targetPath);
                console.log(`✓ Moved ${dir} to questions/${category}/`);
                movedCount++;
            } else {
                // If target exists, remove source as it's a duplicate
                fs.rmSync(sourcePath, { recursive: true, force: true });
                console.log(`✓ Removed duplicate ${dir}`);
                movedCount++;
            }
        }
    } else {
        console.log(`✓ Kept ${dir} in psychology/`);
        keptCount++;
    }
});

console.log(`\nSummary:`);
console.log(`- Moved/removed ${movedCount} Q&A pages`);
console.log(`- Kept ${keptCount} psychology pages`);

// Update the psychology index page to only show actual psychology pages
const psychologyIndexPath = path.join(psychologyDir, 'index.html');
if (fs.existsSync(psychologyIndexPath)) {
    console.log('\nUpdating psychology index page...');
    
    const indexContent = `<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- SEO Meta Tags -->
    <meta name="description" content="Психология и травма - образовательные материалы от Ирины Монро. Исследование травмы, исцеления и эмоциональных состояний.">
    <meta name="keywords" content="психология, травма, исцеление, внутренний ребенок, эмоции">
    <meta name="author" content="Ирина Монро">
    
    <title>Психология и травма | Ресурсы | Ирина Монро</title>
    
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
    <!-- Header Placeholder -->
    <div class="header-placeholder"></div>

    <!-- Category Hero -->
    <section class="category-hero">
        <div class="container">
            <nav class="breadcrumb">
                <a href="/">Главная</a>
                <span>/</span>
                <a href="/resources/">Ресурсы</a>
                <span>/</span>
                <span>Психология и травма</span>
            </nav>
            <h1>Психология и травма</h1>
            <p>Образовательные материалы о травме, исцелении и эмоциональных состояниях</p>
        </div>
    </section>

    <!-- Psychology Articles Grid -->
    <section class="topics-section">
        <div class="container">
            <div class="topics-grid">
                <article class="topic-card">
                    <div class="topic-content">
                        <h2>Внутренний ребенок</h2>
                        <p>Исследование концепции внутреннего ребенка и его роли в нашей взрослой жизни. Как детские переживания формируют наше настоящее.</p>
                        <a href="/resources/psychology/vnytrenniy-rebenok/" class="topic-link">
                            Читать далее
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                                <path d="M9 18l6-6-6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                            </svg>
                        </a>
                    </div>
                </article>
                
                <article class="topic-card">
                    <div class="topic-content">
                        <h2>Травма искажает восприятие</h2>
                        <p>Как психологическая травма влияет на наше восприятие реальности и формирует искаженные паттерны мышления.</p>
                        <a href="/resources/psychology/travma-iskagaet-vospriyatie/" class="topic-link">
                            Читать далее
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                                <path d="M9 18l6-6-6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                            </svg>
                        </a>
                    </div>
                </article>
                
                <article class="topic-card">
                    <div class="topic-content">
                        <h2>Травма может эмоционально заморозить</h2>
                        <p>Понимание эмоционального замораживания как защитного механизма психики при травматическом опыте.</p>
                        <a href="/resources/psychology/travma-moget-emotsionalno-zamorozit/" class="topic-link">
                            Читать далее
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                                <path d="M9 18l6-6-6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                            </svg>
                        </a>
                    </div>
                </article>
                
                <article class="topic-card">
                    <div class="topic-content">
                        <h2>Исцеление травмы требует времени</h2>
                        <p>Почему процесс исцеления от психологической травмы не может быть быстрым и что важно знать на этом пути.</p>
                        <a href="/resources/psychology/istselenie-travmi-trebuet-vremeni/" class="topic-link">
                            Читать далее
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                                <path d="M9 18l6-6-6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                            </svg>
                        </a>
                    </div>
                </article>
                
                <article class="topic-card">
                    <div class="topic-content">
                        <h2>Эмоции связаны с телом</h2>
                        <p>Исследование связи между эмоциональными состояниями и телесными ощущениями. Как тело хранит эмоциональную память.</p>
                        <a href="/resources/psychology/emotsii-svyazani-s-telom/" class="topic-link">
                            Читать далее
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                                <path d="M9 18l6-6-6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                            </svg>
                        </a>
                    </div>
                </article>
                
                <article class="topic-card">
                    <div class="topic-content">
                        <h2>Эмоциональные состояния</h2>
                        <p>Понимание различных эмоциональных состояний, их природы и влияния на нашу жизнь и поведение.</p>
                        <a href="/resources/psychology/emotsionalnie-sostoyaniya/" class="topic-link">
                            Читать далее
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                                <path d="M9 18l6-6-6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                            </svg>
                        </a>
                    </div>
                </article>
                
                <article class="topic-card">
                    <div class="topic-content">
                        <h2>Проекция - зеркало внутреннего мира</h2>
                        <p>Как механизм проекции раскрывает наш внутренний мир и почему мы видим в других то, что есть в нас самих.</p>
                        <a href="/resources/psychology/proektsia-zerkalo-vneyrennego-mira/" class="topic-link">
                            Читать далее
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                                <path d="M9 18l6-6-6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                            </svg>
                        </a>
                    </div>
                </article>
                
                <article class="topic-card">
                    <div class="topic-content">
                        <h2>Линза восприятия себя и мира</h2>
                        <p>Как наши убеждения и прошлый опыт формируют линзу, через которую мы воспринимаем себя и окружающий мир.</p>
                        <a href="/resources/psychology/linza-vospriyatia-sebya-i-mira/" class="topic-link">
                            Читать далее
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                                <path d="M9 18l6-6-6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                            </svg>
                        </a>
                    </div>
                </article>
            </div>
        </div>
    </section>

    <!-- Footer Placeholder -->
    <div class="footer-placeholder"></div>

    <!-- Scripts -->
    <script src="../../script.js"></script>
</body>
</html>`;
    
    fs.writeFileSync(psychologyIndexPath, indexContent);
    console.log('✓ Updated psychology index page');
}