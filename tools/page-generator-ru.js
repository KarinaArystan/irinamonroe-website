#!/usr/bin/env node

/**
 * Russian-Only Page Generator for Irina Monroe Website
 * 
 * This script generates pages in Russian only
 * Usage: node page-generator-ru.js [type] [data-file]
 * 
 * Types: qa, hypnotherapy, psychology, service
 */

const fs = require('fs');
const path = require('path');

// Template for Q&A pages
const generateQAPage = (data) => {
    const {
        category,
        categoryName,
        urlSlug,
        questionRu,
        descriptionRu,
        keywords,
        contentRu,
        publishDate,
        relatedQuestions = []
    } = data;

    // Read the Russian template
    const templatePath = path.join(__dirname, '../resources/questions/qa-template-ru.html');
    let template = fs.readFileSync(templatePath, 'utf8');

    // Replace placeholders
    template = template.replace(/\[КАТЕГОРИЯ\]/g, category);
    template = template.replace(/\[НАЗВАНИЕ КАТЕГОРИИ\]/g, categoryName);
    template = template.replace(/\[URL-SLUG\]/g, urlSlug);
    template = template.replace(/\[ЗАГОЛОВОК ВОПРОСА\]/g, questionRu);
    template = template.replace(/\[ОПИСАНИЕ ВОПРОСА\]/g, descriptionRu);
    template = template.replace(/\[КЛЮЧЕВЫЕ СЛОВА\]/g, keywords);
    template = template.replace(/\[ДАТА ПУБЛИКАЦИИ\]/g, publishDate);
    template = template.replace(/\[ДАТА ИЗМЕНЕНИЯ\]/g, publishDate);
    template = template.replace(/\[ФОРМАТИРОВАННАЯ ДАТА\]/g, formatDateRu(publishDate));

    // Replace content section
    const russianContent = contentRu.split('\n').map(p => `<p>${p}</p>`).join('\n                ');
    template = template.replace('<!-- КОНТЕНТ ОТВЕТА -->', russianContent);

    // Handle related questions
    if (relatedQuestions.length > 0) {
        let relatedHTML = '';
        relatedQuestions.forEach((q, index) => {
            const relatedSlug = q.slug || `related-${index + 1}`;
            const relatedTemplate = `
                    <!-- Связанный вопрос ${index + 1} -->
                    <a href="/resources/questions/${category}/${relatedSlug}/" class="related-card">
                        <h3>${q.titleRu}</h3>
                        <p>${q.excerptRu}</p>
                    </a>`;
            relatedHTML += relatedTemplate;
        });
        
        // Replace the placeholder related questions
        const relatedSection = template.match(/<div class="related-grid">[\s\S]*?<\/div>/)[0];
        const newRelatedSection = `<div class="related-grid">${relatedHTML}
                </div>`;
        template = template.replace(relatedSection, newRelatedSection);
    }

    return template;
};

// Template for Hypnotherapy pages
const generateHypnotherapyPage = (data) => {
    const {
        urlSlug,
        titleRu,
        descriptionRu,
        keywords,
        contentRu,
        publishDate,
        relatedPages = []
    } = data;

    // Create simple template for now
    const template = `<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="${descriptionRu}">
    <meta name="keywords" content="${keywords}">
    <title>${titleRu} | Гипнотерапия | Ирина Монро</title>
    
    <link rel="stylesheet" href="../../styles.css">
    <link rel="stylesheet" href="../../mobile-fixes.css">
    <link rel="stylesheet" href="../resources-styles.css">
</head>
<body>
    <div class="header-placeholder"></div>
    
    <section class="category-hero">
        <div class="container">
            <nav class="breadcrumb">
                <a href="/">Главная</a>
                <span>/</span>
                <a href="/resources/">Ресурсы</a>
                <span>/</span>
                <a href="/resources/hypnotherapy/">Гипнотерапия</a>
                <span>/</span>
                <span>${titleRu}</span>
            </nav>
        </div>
    </section>
    
    <section class="topics-section">
        <article class="article-content" style="max-width: 800px; margin: 0 auto; padding: 0 40px;">
            <div class="article-header" style="text-align: center; margin-bottom: 50px;">
                <h1 style="font-family: 'Cormorant Infant', serif; font-size: 42px; color: var(--text-dark); margin-bottom: 20px;">${titleRu}</h1>
                <div class="article-meta" style="font-size: 14px; color: var(--text-muted);">
                    <time datetime="${publishDate}">Опубликовано ${formatDateRu(publishDate)}</time>
                </div>
            </div>
            
            <div class="article-body" style="font-size: 17px; line-height: 1.8; color: var(--text-dark);">
                ${contentRu.split('\n').map(p => `<p>${p}</p>`).join('\n                ')}
            </div>
        </article>
    </section>
    
    <div class="footer-placeholder"></div>
    <script src="../../script.js"></script>
</body>
</html>`;

    return template;
};

// Template for Psychology Topic pages
const generatePsychologyPage = (data) => {
    const {
        urlSlug,
        titleRu,
        descriptionRu,
        keywords,
        contentRu,
        publishDate,
        category,
        relatedTopics = []
    } = data;

    // Create simple template for now
    const template = `<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="${descriptionRu}">
    <meta name="keywords" content="${keywords}">
    <title>${titleRu} | Темы психологии | Ирина Монро</title>
    
    <link rel="stylesheet" href="../../styles.css">
    <link rel="stylesheet" href="../../mobile-fixes.css">
    <link rel="stylesheet" href="../resources-styles.css">
</head>
<body>
    <div class="header-placeholder"></div>
    
    <section class="category-hero">
        <div class="container">
            <nav class="breadcrumb">
                <a href="/">Главная</a>
                <span>/</span>
                <a href="/resources/">Ресурсы</a>
                <span>/</span>
                <a href="/resources/psychology/">Темы психологии</a>
                <span>/</span>
                <span>${titleRu}</span>
            </nav>
        </div>
    </section>
    
    <section class="topics-section">
        <article class="article-content" style="max-width: 800px; margin: 0 auto; padding: 0 40px;">
            <div class="article-header">
                <h1 style="font-family: 'Cormorant Infant', serif; font-size: 42px; color: var(--text-dark); margin-bottom: 40px;">${titleRu}</h1>
                <p class="article-intro" style="font-size: 20px; line-height: 1.6; color: var(--text-muted); margin-bottom: 40px;">${descriptionRu}</p>
            </div>
            
            <div class="article-body" style="font-size: 17px; line-height: 1.8; color: var(--text-dark);">
                ${contentRu.split('\n').map(p => `<p>${p}</p>`).join('\n                ')}
            </div>
        </article>
    </section>
    
    <div class="footer-placeholder"></div>
    <script src="../../script.js"></script>
</body>
</html>`;

    return template;
};

// Generate a single page from JSON data
const generatePage = (type, jsonData) => {
    let html = '';
    let outputPath = '';

    switch(type) {
        case 'qa':
            html = generateQAPage(jsonData);
            outputPath = path.join(__dirname, `../resources/questions/${jsonData.category}/${jsonData.urlSlug}/index.html`);
            break;
        case 'hypnotherapy':
            html = generateHypnotherapyPage(jsonData);
            outputPath = path.join(__dirname, `../resources/hypnotherapy/${jsonData.urlSlug}/index.html`);
            break;
        case 'psychology':
            html = generatePsychologyPage(jsonData);
            outputPath = path.join(__dirname, `../resources/psychology/${jsonData.urlSlug}/index.html`);
            break;
        default:
            console.error('Unknown page type:', type);
            process.exit(1);
    }

    // Create directory if it doesn't exist
    const dir = path.dirname(outputPath);
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }

    // Write the file
    fs.writeFileSync(outputPath, html);
    console.log(`Generated: ${outputPath}`);
};

// Batch generate pages from a JSON file
const batchGenerate = (type, dataFile) => {
    try {
        const data = JSON.parse(fs.readFileSync(dataFile, 'utf8'));
        const pages = Array.isArray(data) ? data : [data];
        
        pages.forEach(pageData => {
            generatePage(type, pageData);
        });
        
        console.log(`\nSuccessfully generated ${pages.length} ${type} pages!`);
    } catch (error) {
        console.error('Error reading or parsing data file:', error);
        process.exit(1);
    }
};

// Helper function to format dates in Russian
const formatDateRu = (dateString) => {
    const date = new Date(dateString);
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return date.toLocaleDateString('ru-RU', options);
};

// CLI handling
const args = process.argv.slice(2);

if (args.length < 2) {
    console.log(`
Russian-Only Page Generator for Irina Monroe Website

Usage: node page-generator-ru.js [type] [data-file]

Types:
  qa           Generate Q&A pages
  hypnotherapy Generate hypnotherapy topic pages
  psychology   Generate psychology topic pages

Example:
  node page-generator-ru.js qa qa-data.json

Data file should be a JSON file with the required Russian fields for the page type.
    `);
    process.exit(0);
}

const [type, dataFile] = args;

// Check if data file exists
if (!fs.existsSync(dataFile)) {
    console.error(`Data file not found: ${dataFile}`);
    process.exit(1);
}

// Run the generator
batchGenerate(type, dataFile);