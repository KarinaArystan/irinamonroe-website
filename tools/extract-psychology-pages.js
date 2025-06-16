const fs = require('fs');
const csv = require('csv-parse');
const path = require('path');
const { JSDOM } = require('jsdom');

// Psychology pages we're looking for
const psychologyPages = [
    { url: 'vnytrenniy-rebenok', title: 'Внутренний ребенок' },
    { url: 'travma-iskagaet-vospriyatie', title: 'Травма искажает восприятие' },
    { url: 'travma-moget-emotsionalno-zamorozit', title: 'Травма может эмоционально заморозить' },
    { url: 'istselenie-travmi-trebuet-vremeni', title: 'Исцеление травмы требует времени' },
    { url: 'emotsii-svyazani-s-telom', title: 'Эмоции связаны с телом' },
    { url: 'emotsionalnie-sostoyaniya', title: 'Эмоциональные состояния' },
    { url: 'proektsia-zerkalo-vneyrennego-mira', title: 'Проекция зеркало внутреннего мира' },
    { url: 'linza-vospriyatia-sebya-i-mira', title: 'Линза восприятия себя и мира' },
    { url: 'vzglyad-na-travmy', title: 'Взгляд на травмы' }
];

// Function to extract clean text from HTML
function extractTextFromHTML(html) {
    try {
        const dom = new JSDOM(html);
        const document = dom.window.document;
        
        // Remove script and style elements
        const scripts = document.querySelectorAll('script, style');
        scripts.forEach(el => el.remove());
        
        // Try to find main content
        let mainContent = document.querySelector('.content-main') || 
                         document.querySelector('.main-content') ||
                         document.querySelector('article') ||
                         document.querySelector('main') ||
                         document.body;
        
        if (!mainContent) return '';
        
        // Extract text
        const paragraphs = mainContent.querySelectorAll('p, h1, h2, h3, h4, h5, h6, li');
        const content = [];
        
        paragraphs.forEach(p => {
            const text = p.textContent.trim();
            if (text && text.length > 10) {
                content.push(text);
            }
        });
        
        return content.join('\n\n');
    } catch (error) {
        console.error('Error extracting text:', error);
        return '';
    }
}

// Function to generate slug from title
function generateSlug(title) {
    const translitMap = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '',
        'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
    };
    
    return title.toLowerCase()
        .split('')
        .map(char => translitMap[char] || char)
        .join('')
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/^-+|-+$/g, '');
}

// Process CSV files
async function processCsvFiles() {
    const csvFiles = [
        '/Users/Karina/Library/CloudStorage/GoogleDrive-karina.arystan@gmail.com/My Drive/Projects/irinamonroe.com/current-site/custom_extraction_all.csv',
        '/Users/Karina/Library/CloudStorage/GoogleDrive-karina.arystan@gmail.com/My Drive/Projects/irinamonroe.com/current-site/custom_extraction_part1.csv',
        '/Users/Karina/Library/CloudStorage/GoogleDrive-karina.arystan@gmail.com/My Drive/Projects/irinamonroe.com/current-site/internal_all.csv'
    ];
    
    const foundPages = [];
    
    for (const csvFile of csvFiles) {
        if (!fs.existsSync(csvFile)) {
            console.log(`File not found: ${csvFile}`);
            continue;
        }
        
        console.log(`\nProcessing: ${path.basename(csvFile)}`);
        
        const fileContent = fs.readFileSync(csvFile, 'utf-8');
        
        await new Promise((resolve, reject) => {
            csv.parse(fileContent, {
                columns: false,
                skip_empty_lines: true,
                relax_quotes: true,
                relax_column_count: true,
                skip_records_with_error: true
            }, (err, records) => {
                if (err) {
                    console.error('CSV parsing error:', err);
                    resolve();
                    return;
                }
                
                records.forEach((row, index) => {
                    const rowText = row.join(' ').toLowerCase();
                    
                    psychologyPages.forEach(page => {
                        // Check if this row contains our target URL
                        if (rowText.includes(page.url) || rowText.includes(page.title.toLowerCase())) {
                            console.log(`Found potential match for ${page.title} at row ${index}`);
                            
                            // Try to extract content from the row
                            const fullRow = row.join(' ');
                            const htmlMatch = fullRow.match(/<[^>]+>[\s\S]*<\/[^>]+>/);
                            
                            if (htmlMatch) {
                                const content = extractTextFromHTML(htmlMatch[0]);
                                if (content && content.length > 100) {
                                    foundPages.push({
                                        url: page.url,
                                        title: page.title,
                                        content: content,
                                        source: path.basename(csvFile)
                                    });
                                    console.log(`✓ Extracted content for ${page.title} (${content.length} chars)`);
                                }
                            }
                        }
                    });
                });
                
                resolve();
            });
        });
    }
    
    return foundPages;
}

// Generate psychology page HTML
function generatePsychologyPage(pageData) {
    const template = `<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- SEO Meta Tags -->
    <meta name="description" content="${pageData.title} - психологические материалы от Ирины Монро">
    <meta name="keywords" content="психология, травма, исцеление, ${pageData.title.toLowerCase()}">
    <meta name="author" content="Ирина Монро">
    
    <!-- Open Graph Meta Tags -->
    <meta property="og:title" content="${pageData.title} | Ирина Монро">
    <meta property="og:description" content="${pageData.content.substring(0, 150)}...">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://www.irinamonroe.com/resources/psychology/${pageData.url}/">
    
    <title>${pageData.title} | Психология | Ирина Монро</title>
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Infant:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400;1,500;1,600;1,700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    
    <!-- External CSS -->
    <link rel="stylesheet" href="../../styles.css">
    <link rel="stylesheet" href="../../mobile-fixes.css">
    <link rel="stylesheet" href="../resources-styles.css">
    
    <style>
        .psychology-article {
            max-width: 800px;
            margin: 0 auto;
            padding: 0 40px;
        }
        
        .psychology-header {
            text-align: center;
            margin-bottom: 60px;
        }
        
        .psychology-header h1 {
            font-family: 'Cormorant Infant', serif;
            font-size: 48px;
            color: var(--text-dark);
            margin-bottom: 20px;
            font-weight: 400;
            line-height: 1.2;
        }
        
        .psychology-meta {
            font-size: 14px;
            color: var(--text-muted);
        }
        
        .psychology-content {
            font-size: 18px;
            line-height: 1.8;
            color: var(--text-dark);
        }
        
        .psychology-content p {
            margin-bottom: 28px;
        }
        
        .psychology-content h2 {
            font-family: 'Cormorant Infant', serif;
            font-size: 32px;
            color: var(--text-dark);
            margin: 48px 0 24px;
            font-weight: 400;
        }
        
        .psychology-content h3 {
            font-family: 'Cormorant Infant', serif;
            font-size: 26px;
            color: var(--text-dark);
            margin: 36px 0 18px;
            font-weight: 400;
        }
        
        .psychology-content ul,
        .psychology-content ol {
            margin: 24px 0 32px;
            padding-left: 32px;
        }
        
        .psychology-content li {
            margin-bottom: 16px;
            line-height: 1.8;
        }
        
        .psychology-content blockquote {
            border-left: 4px solid var(--primary-color);
            padding-left: 24px;
            margin: 32px 0;
            font-style: italic;
            color: var(--text-muted);
        }
        
        .related-articles {
            margin-top: 80px;
            padding-top: 60px;
            border-top: 1px solid var(--border-color);
        }
        
        .related-articles h2 {
            font-family: 'Cormorant Infant', serif;
            font-size: 36px;
            color: var(--text-dark);
            margin-bottom: 40px;
            text-align: center;
        }
        
        .related-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 30px;
        }
        
        .related-card {
            background: var(--bg-lighter);
            padding: 30px;
            border-radius: 8px;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        
        .related-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }
        
        .related-card h3 {
            font-family: 'Cormorant Infant', serif;
            font-size: 24px;
            color: var(--text-dark);
            margin-bottom: 12px;
            font-weight: 400;
        }
        
        .related-card p {
            font-size: 15px;
            color: var(--text-muted);
            line-height: 1.6;
        }
        
        @media (max-width: 768px) {
            .psychology-article {
                padding: 0 20px;
            }
            
            .psychology-header h1 {
                font-size: 36px;
            }
            
            .psychology-content {
                font-size: 17px;
            }
            
            .related-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <!-- Header Placeholder -->
    <div class="header-placeholder"></div>

    <!-- Breadcrumb Navigation -->
    <section class="category-hero" style="padding: 40px 0 20px;">
        <div class="container">
            <nav class="breadcrumb">
                <a href="/">Главная</a>
                <span>/</span>
                <a href="/resources/">Ресурсы</a>
                <span>/</span>
                <a href="/resources/psychology/">Психология и травма</a>
                <span>/</span>
                <span>${pageData.title}</span>
            </nav>
        </div>
    </section>

    <!-- Psychology Content -->
    <section class="topics-section" style="padding-top: 40px;">
        <article class="psychology-article">
            <header class="psychology-header">
                <h1>${pageData.title}</h1>
                <div class="psychology-meta">
                    <time datetime="${new Date().toISOString().split('T')[0]}">${new Date().toLocaleDateString('ru-RU', { year: 'numeric', month: 'long', day: 'numeric' })}</time>
                </div>
            </header>

            <div class="psychology-content">
                ${pageData.content.split('\n\n').map(paragraph => 
                    paragraph.trim() ? `<p>${paragraph}</p>` : ''
                ).join('\n                ')}
            </div>

            <!-- Related Articles -->
            <aside class="related-articles">
                <h2>Другие статьи по теме</h2>
                
                <div class="related-grid">
                    ${psychologyPages
                        .filter(p => p.url !== pageData.url)
                        .slice(0, 3)
                        .map(related => `
                    <a href="/resources/psychology/${related.url}/" class="related-card">
                        <h3>${related.title}</h3>
                        <p>Узнайте больше о психологических аспектах травмы и исцеления</p>
                    </a>`).join('')}
                </div>
            </aside>
        </article>
    </section>

    <!-- CTA Section -->
    <section style="background: var(--bg-light); padding: 60px 0; margin-top: 80px;">
        <div class="container" style="text-align: center;">
            <h2 style="font-family: 'Cormorant Infant', serif; font-size: 36px; margin-bottom: 20px;">
                Готовы к глубокой работе?
            </h2>
            <p style="font-size: 18px; margin-bottom: 30px; max-width: 600px; margin-left: auto; margin-right: auto;">
                Исцеление начинается с понимания. Я здесь, чтобы поддержать вас на этом пути.
            </p>
            <a href="/#contact" class="nav-cta" style="padding: 14px 40px; font-size: 16px; display: inline-block;">
                Записаться на консультацию
            </a>
        </div>
    </section>

    <!-- Footer Placeholder -->
    <div class="footer-placeholder"></div>

    <!-- Scripts -->
    <script src="../../script.js"></script>
</body>
</html>`;
    
    return template;
}

// Main execution
async function main() {
    console.log('Searching for psychology/trauma pages...\n');
    
    const foundPages = await processCsvFiles();
    
    console.log(`\n\nSummary: Found ${foundPages.length} psychology pages`);
    
    // Create psychology directory
    const psychologyDir = '/Users/Karina/Library/CloudStorage/GoogleDrive-karina.arystan@gmail.com/My Drive/Projects/irinamonroe.com/new-site/resources/psychology';
    
    if (!fs.existsSync(psychologyDir)) {
        fs.mkdirSync(psychologyDir, { recursive: true });
        console.log('\nCreated psychology directory');
    }
    
    // Generate pages
    foundPages.forEach(page => {
        const pageDir = path.join(psychologyDir, page.url);
        if (!fs.existsSync(pageDir)) {
            fs.mkdirSync(pageDir, { recursive: true });
        }
        
        const html = generatePsychologyPage(page);
        const filePath = path.join(pageDir, 'index.html');
        
        fs.writeFileSync(filePath, html);
        console.log(`✓ Generated: ${page.title} -> ${filePath}`);
    });
    
    // Report missing pages
    const foundUrls = foundPages.map(p => p.url);
    const missingPages = psychologyPages.filter(p => !foundUrls.includes(p.url));
    
    if (missingPages.length > 0) {
        console.log('\n⚠️ Missing pages:');
        missingPages.forEach(page => {
            console.log(`  - ${page.title} (${page.url})`);
        });
    }
    
    // Create psychology index page
    const indexHtml = generatePsychologyIndexPage(foundPages);
    fs.writeFileSync(path.join(psychologyDir, 'index.html'), indexHtml);
    console.log('\n✓ Generated psychology index page');
}

// Generate psychology index page
function generatePsychologyIndexPage(pages) {
    return `<!DOCTYPE html>
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
    <link rel="stylesheet" href="../styles.css">
    <link rel="stylesheet" href="../mobile-fixes.css">
    <link rel="stylesheet" href="resources-styles.css">
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
                ${pages.map(page => `
                <article class="topic-card">
                    <div class="topic-content">
                        <h2>${page.title}</h2>
                        <p>${page.content.substring(0, 200)}...</p>
                        <a href="/resources/psychology/${page.url}/" class="topic-link">
                            Читать далее
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                                <path d="M9 18l6-6-6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                            </svg>
                        </a>
                    </div>
                </article>`).join('')}
            </div>
        </div>
    </section>

    <!-- Footer Placeholder -->
    <div class="footer-placeholder"></div>

    <!-- Scripts -->
    <script src="../script.js"></script>
</body>
</html>`;
}

// Run the script
main().catch(console.error);