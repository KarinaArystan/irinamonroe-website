#!/usr/bin/env node

/**
 * Batch Page Generator
 * Generates all extracted pages from JSON files
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Color codes for console output
const colors = {
    reset: '\x1b[0m',
    bright: '\x1b[1m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    red: '\x1b[31m'
};

function log(message, color = 'reset') {
    console.log(`${colors[color]}${message}${colors.reset}`);
}

// Generate pages for each content type
function generatePages() {
    const contentTypes = [
        { type: 'qa', file: 'qa-content.json', name: 'Q&A' },
        { type: 'hypnotherapy', file: 'hypnotherapy-content.json', name: 'Hypnotherapy' },
        { type: 'psychology', file: 'psychology-content.json', name: 'Psychology Topics' },
        { type: 'service', file: 'service-content.json', name: 'Service' }
    ];
    
    let totalGenerated = 0;
    let totalErrors = 0;
    
    log('\n🚀 Starting batch page generation...', 'bright');
    
    contentTypes.forEach(({ type, file, name }) => {
        const filePath = path.join(__dirname, file);
        
        if (!fs.existsSync(filePath)) {
            log(`⚠️  ${name} content file not found: ${file}`, 'yellow');
            return;
        }
        
        log(`\n📁 Processing ${name} pages...`, 'blue');
        
        try {
            // First check if we need templates
            if (type === 'hypnotherapy' || type === 'psychology') {
                const templateFile = type === 'hypnotherapy' 
                    ? '../resources/hypnotherapy/hypnotherapy-template.html'
                    : '../resources/psychology/psychology-template.html';
                    
                const templatePath = path.join(__dirname, templateFile);
                
                if (!fs.existsSync(templatePath)) {
                    log(`   Creating ${type} template...`, 'yellow');
                    createTemplate(type, templatePath);
                }
            }
            
            // Run the page generator
            const output = execSync(`node page-generator.js ${type} ${file}`, {
                cwd: __dirname,
                encoding: 'utf8'
            });
            
            // Extract count from output
            const match = output.match(/Successfully generated (\d+)/);
            if (match) {
                const count = parseInt(match[1]);
                totalGenerated += count;
                log(`   ✅ Generated ${count} ${name} pages`, 'green');
            }
            
        } catch (error) {
            totalErrors++;
            log(`   ❌ Error generating ${name} pages: ${error.message}`, 'red');
        }
    });
    
    // Summary
    log('\n' + '='.repeat(50), 'bright');
    log(`📊 Generation Summary:`, 'bright');
    log(`   Total pages generated: ${totalGenerated}`, 'green');
    if (totalErrors > 0) {
        log(`   Errors encountered: ${totalErrors}`, 'red');
    }
    log('='.repeat(50) + '\n', 'bright');
    
    // Next steps
    if (totalGenerated > 0) {
        log('✨ Next steps:', 'yellow');
        log('   1. Review generated pages in /resources/');
        log('   2. Add English translations where needed');
        log('   3. Update navigation and related links');
        log('   4. Test bilingual functionality');
        log('   5. Deploy to production\n');
    }
}

// Create template files if they don't exist
function createTemplate(type, templatePath) {
    let template = '';
    
    if (type === 'hypnotherapy') {
        template = createHypnotherapyTemplate();
    } else if (type === 'psychology') {
        template = createPsychologyTemplate();
    }
    
    // Ensure directory exists
    const dir = path.dirname(templatePath);
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
    
    fs.writeFileSync(templatePath, template, 'utf8');
}

function createHypnotherapyTemplate() {
    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="[ENGLISH DESCRIPTION]">
    <title>[ENGLISH TITLE] | Hypnotherapy | Irina Monroe</title>
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Infant:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400;1,500;1,600;1,700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    
    <!-- External CSS -->
    <link rel="stylesheet" href="../../styles.css">
    <link rel="stylesheet" href="../../mobile-fixes.css">
    <link rel="stylesheet" href="../resources-styles.css">
    
    <!-- SEO Meta Tags -->
    <meta name="keywords" content="[KEYWORDS]">
    <meta property="og:title" content="[ENGLISH TITLE]">
    <meta property="og:description" content="[ENGLISH DESCRIPTION]">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://www.irinamonroe.com/resources/hypnotherapy/[URL-SLUG]/">
    
    <style>
        .article-content {
            max-width: 800px;
            margin: 0 auto;
            padding: 0 40px;
        }
        
        .article-header {
            text-align: center;
            margin-bottom: 50px;
        }
        
        .article-header h1 {
            font-family: 'Cormorant Infant', serif;
            font-size: 42px;
            color: var(--text-dark);
            margin-bottom: 20px;
            font-weight: 400;
            line-height: 1.3;
        }
        
        .article-meta {
            font-size: 14px;
            color: var(--text-muted);
            margin-bottom: 30px;
        }
        
        .article-body {
            font-size: 17px;
            line-height: 1.8;
            color: var(--text-dark);
        }
        
        .article-body p {
            margin-bottom: 24px;
        }
        
        .article-body h2 {
            font-family: 'Cormorant Infant', serif;
            font-size: 32px;
            color: var(--text-dark);
            margin: 40px 0 20px;
            font-weight: 400;
        }
        
        .highlight-box {
            background: rgba(147, 136, 74, 0.08);
            padding: 30px;
            border-radius: 12px;
            margin: 40px 0;
            border-left: 4px solid var(--primary-color);
        }
        
        @media (max-width: 768px) {
            .article-content {
                padding: 0 20px;
            }
            
            .article-header h1 {
                font-size: 32px;
            }
            
            .article-body {
                font-size: 16px;
            }
        }
    </style>
</head>
<body>
    <!-- Header Placeholder -->
    <div class="header-placeholder"></div>

    <!-- Breadcrumb Navigation -->
    <section class="category-hero">
        <div class="container">
            <nav class="breadcrumb">
                <a href="/" lang="en">Home</a>
                <a href="/" lang="ru">Главная</a>
                <span>/</span>
                <a href="/resources/" lang="en">Resources</a>
                <a href="/resources/" lang="ru">Ресурсы</a>
                <span>/</span>
                <a href="/resources/hypnotherapy/" lang="en">Hypnotherapy</a>
                <a href="/resources/hypnotherapy/" lang="ru">Гипнотерапия</a>
                <span>/</span>
                <span>[ENGLISH TITLE]</span>
            </nav>
        </div>
    </section>

    <!-- Article Content -->
    <section class="topics-section">
        <article class="article-content">
            <div class="article-header">
                <h1 lang="en">[ENGLISH TITLE]</h1>
                <h1 lang="ru">[RUSSIAN TITLE]</h1>
                <div class="article-meta">
                    <time datetime="[PUBLISH DATE]">Published on [PUBLISH DATE]</time>
                </div>
            </div>
            
            <div class="article-body">
                <div lang="en">
                    <!-- ENGLISH CONTENT GOES HERE -->
                </div>
                
                <div lang="ru">
                    <!-- RUSSIAN CONTENT GOES HERE -->
                </div>
            </div>
        </article>
    </section>

    <!-- Related Topics -->
    <section style="background: var(--bg-light); padding: 60px 0; margin-top: 80px;">
        <div class="container">
            <h2 style="font-family: 'Cormorant Infant', serif; font-size: 36px; text-align: center; margin-bottom: 40px;">
                <span lang="en">Explore More Topics</span>
                <span lang="ru">Исследуйте больше тем</span>
            </h2>
            <div class="topics-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 25px; max-width: 900px; margin: 0 auto;">
                <a href="/resources/hypnotherapy/" class="topic-card">
                    <h3 lang="en">All Hypnotherapy Topics</h3>
                    <h3 lang="ru">Все темы гипнотерапии</h3>
                    <p lang="en">Return to the hypnotherapy overview</p>
                    <p lang="ru">Вернуться к обзору гипнотерапии</p>
                </a>
            </div>
        </div>
    </section>

    <!-- CTA Section -->
    <section style="padding: 60px 0;">
        <div class="container" style="text-align: center;">
            <h2 style="font-family: 'Cormorant Infant', serif; font-size: 36px; margin-bottom: 20px;">
                <span lang="en">Ready to Experience Hypnotherapy?</span>
                <span lang="ru">Готовы испытать гипнотерапию?</span>
            </h2>
            <p style="font-size: 18px; margin-bottom: 30px; max-width: 600px; margin-left: auto; margin-right: auto;">
                <span lang="en">Discover how hypnotherapy can help you create positive change in your life.</span>
                <span lang="ru">Откройте для себя, как гипнотерапия может помочь вам создать позитивные изменения в вашей жизни.</span>
            </p>
            <a href="/#contact" class="nav-cta" style="padding: 14px 40px; font-size: 16px; display: inline-block;">
                <span lang="en">Book a Session</span>
                <span lang="ru">Записаться на сеанс</span>
            </a>
        </div>
    </section>

    <!-- Footer Placeholder -->
    <div class="footer-placeholder"></div>

    <!-- Scripts -->
    <script src="../../script.js"></script>
</body>
</html>`;
}

function createPsychologyTemplate() {
    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="[ENGLISH DESCRIPTION]">
    <title>[ENGLISH TITLE] | Psychology Topics | Irina Monroe</title>
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Infant:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400;1,500;1,600;1,700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    
    <!-- External CSS -->
    <link rel="stylesheet" href="../../styles.css">
    <link rel="stylesheet" href="../../mobile-fixes.css">
    <link rel="stylesheet" href="../resources-styles.css">
    
    <!-- SEO Meta Tags -->
    <meta name="keywords" content="[KEYWORDS]">
    <meta property="og:title" content="[ENGLISH TITLE]">
    <meta property="og:description" content="[ENGLISH DESCRIPTION]">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://www.irinamonroe.com/resources/psychology/[URL-SLUG]/">
    
    <style>
        .article-content {
            max-width: 800px;
            margin: 0 auto;
            padding: 0 40px;
        }
        
        .article-header {
            margin-bottom: 50px;
        }
        
        .category-badge {
            display: inline-block;
            background: rgba(147, 136, 74, 0.1);
            color: var(--primary-color);
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 500;
            margin-bottom: 20px;
            text-transform: capitalize;
        }
        
        .article-header h1 {
            font-family: 'Cormorant Infant', serif;
            font-size: 42px;
            color: var(--text-dark);
            margin-bottom: 20px;
            font-weight: 400;
            line-height: 1.3;
        }
        
        .article-intro {
            font-size: 20px;
            line-height: 1.6;
            color: var(--text-muted);
            margin-bottom: 40px;
        }
        
        .article-body {
            font-size: 17px;
            line-height: 1.8;
            color: var(--text-dark);
        }
        
        .article-body p {
            margin-bottom: 24px;
        }
        
        .article-body h2 {
            font-family: 'Cormorant Infant', serif;
            font-size: 32px;
            color: var(--text-dark);
            margin: 40px 0 20px;
            font-weight: 400;
        }
        
        .key-points {
            background: var(--bg-lighter);
            padding: 30px;
            border-radius: 12px;
            margin: 40px 0;
        }
        
        .key-points h3 {
            font-family: 'Cormorant Infant', serif;
            font-size: 24px;
            color: var(--text-dark);
            margin-bottom: 20px;
        }
        
        .key-points ul {
            list-style: none;
            padding: 0;
        }
        
        .key-points li {
            position: relative;
            padding-left: 30px;
            margin-bottom: 15px;
        }
        
        .key-points li:before {
            content: "→";
            position: absolute;
            left: 0;
            color: var(--primary-color);
            font-weight: bold;
        }
        
        @media (max-width: 768px) {
            .article-content {
                padding: 0 20px;
            }
            
            .article-header h1 {
                font-size: 32px;
            }
            
            .article-intro {
                font-size: 18px;
            }
            
            .article-body {
                font-size: 16px;
            }
        }
    </style>
</head>
<body>
    <!-- Header Placeholder -->
    <div class="header-placeholder"></div>

    <!-- Breadcrumb Navigation -->
    <section class="category-hero">
        <div class="container">
            <nav class="breadcrumb">
                <a href="/" lang="en">Home</a>
                <a href="/" lang="ru">Главная</a>
                <span>/</span>
                <a href="/resources/" lang="en">Resources</a>
                <a href="/resources/" lang="ru">Ресурсы</a>
                <span>/</span>
                <a href="/resources/psychology/" lang="en">Psychology Topics</a>
                <a href="/resources/psychology/" lang="ru">Темы психологии</a>
                <span>/</span>
                <span>[ENGLISH TITLE]</span>
            </nav>
        </div>
    </section>

    <!-- Article Content -->
    <section class="topics-section">
        <article class="article-content">
            <div class="article-header">
                <div class="category-badge">[CATEGORY]</div>
                <h1 lang="en">[ENGLISH TITLE]</h1>
                <h1 lang="ru">[RUSSIAN TITLE]</h1>
                <p class="article-intro" lang="en">[ENGLISH DESCRIPTION]</p>
                <p class="article-intro" lang="ru">[RUSSIAN DESCRIPTION]</p>
            </div>
            
            <div class="article-body">
                <div lang="en">
                    <!-- ENGLISH CONTENT GOES HERE -->
                </div>
                
                <div lang="ru">
                    <!-- RUSSIAN CONTENT GOES HERE -->
                </div>
            </div>
        </article>
    </section>

    <!-- Related Topics -->
    <section style="background: var(--bg-light); padding: 60px 0; margin-top: 80px;">
        <div class="container">
            <h2 style="font-family: 'Cormorant Infant', serif; font-size: 36px; text-align: center; margin-bottom: 40px;">
                <span lang="en">Related Topics</span>
                <span lang="ru">Связанные темы</span>
            </h2>
            <div class="topics-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 25px; max-width: 900px; margin: 0 auto;">
                <a href="/resources/psychology/" class="topic-card">
                    <h3 lang="en">All Psychology Topics</h3>
                    <h3 lang="ru">Все темы психологии</h3>
                    <p lang="en">Explore more psychological concepts</p>
                    <p lang="ru">Исследуйте больше психологических концепций</p>
                </a>
            </div>
        </div>
    </section>

    <!-- CTA Section -->
    <section style="padding: 60px 0;">
        <div class="container" style="text-align: center;">
            <h2 style="font-family: 'Cormorant Infant', serif; font-size: 36px; margin-bottom: 20px;">
                <span lang="en">Ready to Explore Deeper?</span>
                <span lang="ru">Готовы исследовать глубже?</span>
            </h2>
            <p style="font-size: 18px; margin-bottom: 30px; max-width: 600px; margin-left: auto; margin-right: auto;">
                <span lang="en">Understanding is the first step. Let's explore your unique journey together.</span>
                <span lang="ru">Понимание - это первый шаг. Давайте вместе исследуем ваше уникальное путешествие.</span>
            </p>
            <a href="/#contact" class="nav-cta" style="padding: 14px 40px; font-size: 16px; display: inline-block;">
                <span lang="en">Start Your Journey</span>
                <span lang="ru">Начать ваше путешествие</span>
            </a>
        </div>
    </section>

    <!-- Footer Placeholder -->
    <div class="footer-placeholder"></div>

    <!-- Scripts -->
    <script src="../../script.js"></script>
</body>
</html>`;
}

// Run the batch generator
generatePages();