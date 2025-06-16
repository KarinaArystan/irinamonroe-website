#!/usr/bin/env node

/**
 * Page Generator for Irina Monroe Website
 * 
 * This script helps generate consistent pages from content data
 * Usage: node page-generator.js [type] [data-file]
 * 
 * Types: qa, hypnotherapy, psychology, service
 */

const fs = require('fs');
const path = require('path');

// Template for Hypnotherapy pages
const generateHypnotherapyPage = (data) => {
    const {
        urlSlug,
        titleEn,
        titleRu,
        descriptionEn,
        descriptionRu,
        keywords,
        contentEn,
        contentRu,
        publishDate,
        relatedPages = []
    } = data;

    // Read the hypnotherapy template
    const templatePath = path.join(__dirname, '../resources/hypnotherapy/hypnotherapy-template.html');
    let template = fs.readFileSync(templatePath, 'utf8');

    // Replace placeholders
    template = template.replace(/\[URL-SLUG\]/g, urlSlug);
    template = template.replace(/\[ENGLISH TITLE\]/g, titleEn);
    template = template.replace(/\[RUSSIAN TITLE\]/g, titleRu);
    template = template.replace(/\[ENGLISH DESCRIPTION\]/g, descriptionEn);
    template = template.replace(/\[RUSSIAN DESCRIPTION\]/g, descriptionRu);
    template = template.replace(/\[KEYWORDS\]/g, keywords);
    template = template.replace(/\[PUBLISH DATE\]/g, publishDate);

    // Replace content sections
    const englishContent = contentEn.split('\n').map(p => `<p>${p}</p>`).join('\n                    ');
    const russianContent = contentRu.split('\n').map(p => `<p>${p}</p>`).join('\n                    ');
    
    template = template.replace('<!-- ENGLISH CONTENT GOES HERE -->', englishContent);
    template = template.replace('<!-- RUSSIAN CONTENT GOES HERE -->', russianContent);

    return template;
};

// Template for Psychology Topic pages
const generatePsychologyPage = (data) => {
    const {
        urlSlug,
        titleEn,
        titleRu,
        descriptionEn,
        descriptionRu,
        keywords,
        contentEn,
        contentRu,
        publishDate,
        category,
        relatedTopics = []
    } = data;

    // Read the psychology template
    const templatePath = path.join(__dirname, '../resources/psychology/psychology-template.html');
    let template = fs.readFileSync(templatePath, 'utf8');

    // Replace placeholders
    template = template.replace(/\[URL-SLUG\]/g, urlSlug);
    template = template.replace(/\[ENGLISH TITLE\]/g, titleEn);
    template = template.replace(/\[RUSSIAN TITLE\]/g, titleRu);
    template = template.replace(/\[ENGLISH DESCRIPTION\]/g, descriptionEn);
    template = template.replace(/\[RUSSIAN DESCRIPTION\]/g, descriptionRu);
    template = template.replace(/\[KEYWORDS\]/g, keywords);
    template = template.replace(/\[PUBLISH DATE\]/g, publishDate);
    template = template.replace(/\[CATEGORY\]/g, category);

    // Replace content sections
    const englishContent = contentEn.split('\n').map(p => `<p>${p}</p>`).join('\n                    ');
    const russianContent = contentRu.split('\n').map(p => `<p>${p}</p>`).join('\n                    ');
    
    template = template.replace('<!-- ENGLISH CONTENT GOES HERE -->', englishContent);
    template = template.replace('<!-- RUSSIAN CONTENT GOES HERE -->', russianContent);

    return template;
};

// Template for Q&A pages
const generateQAPage = (data) => {
    const {
        category,
        categoryName,
        urlSlug,
        questionEn,
        questionRu,
        descriptionEn,
        descriptionRu,
        keywords,
        contentEn,
        contentRu,
        publishDate,
        relatedQuestions = []
    } = data;

    // Read the template
    const templatePath = path.join(__dirname, '../resources/questions/qa-template.html');
    let template = fs.readFileSync(templatePath, 'utf8');

    // Replace placeholders
    template = template.replace(/\[CATEGORY\]/g, category);
    template = template.replace(/\[CATEGORY NAME\]/g, categoryName);
    template = template.replace(/\[URL-SLUG\]/g, urlSlug);
    template = template.replace(/\[ENGLISH QUESTION TITLE\]/g, questionEn);
    template = template.replace(/\[RUSSIAN QUESTION TITLE\]/g, questionRu);
    template = template.replace(/\[QUESTION TITLE\]/g, questionEn);
    template = template.replace(/\[QUESTION DESCRIPTION\]/g, descriptionEn);
    template = template.replace(/\[RELEVANT KEYWORDS\]/g, keywords);
    template = template.replace(/\[PUBLISH DATE\]/g, publishDate);
    template = template.replace(/\[MODIFIED DATE\]/g, publishDate);
    template = template.replace(/\[FORMATTED DATE\]/g, formatDate(publishDate));

    // Replace content sections
    const englishContent = contentEn.split('\n').map(p => `<p>${p}</p>`).join('\n                    ');
    const russianContent = contentRu.split('\n').map(p => `<p>${p}</p>`).join('\n                    ');
    
    template = template.replace('<!-- ENGLISH CONTENT GOES HERE -->', englishContent);
    template = template.replace('<!-- RUSSIAN CONTENT GOES HERE -->', russianContent);

    // Handle related questions
    if (relatedQuestions.length > 0) {
        let relatedHTML = '';
        relatedQuestions.forEach((q, index) => {
            const relatedSlug = q.slug || `related-${index + 1}`;
            const relatedTemplate = `
                    <!-- Related Question ${index + 1} -->
                    <a href="/resources/questions/${category}/${relatedSlug}/" class="related-card">
                        <h3 lang="en">${q.titleEn}</h3>
                        <h3 lang="ru">${q.titleRu}</h3>
                        <p lang="en">${q.excerptEn}</p>
                        <p lang="ru">${q.excerptRu}</p>
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
        // Add more types as needed
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

// Helper function to format dates
const formatDate = (dateString) => {
    const date = new Date(dateString);
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return date.toLocaleDateString('en-US', options);
};

// CLI handling
const args = process.argv.slice(2);

if (args.length < 2) {
    console.log(`
Page Generator for Irina Monroe Website

Usage: node page-generator.js [type] [data-file]

Types:
  qa           Generate Q&A pages
  hypnotherapy Generate hypnotherapy topic pages
  psychology   Generate psychology topic pages
  service      Generate service pages

Example:
  node page-generator.js qa qa-data.json

Data file should be a JSON file with the required fields for the page type.

Example Q&A data structure:
{
    "category": "relationships",
    "categoryName": "Couples & Relationships",
    "urlSlug": "trust-after-betrayal",
    "questionEn": "How to rebuild trust after betrayal?",
    "questionRu": "Как восстановить доверие после предательства?",
    "descriptionEn": "Understanding the complex process of healing...",
    "descriptionRu": "Понимание сложного процесса исцеления...",
    "keywords": "trust, betrayal, relationships, healing",
    "contentEn": "First paragraph\\nSecond paragraph\\nThird paragraph",
    "contentRu": "Первый абзац\\nВторой абзац\\nТретий абзац",
    "publishDate": "2024-01-19",
    "relatedQuestions": [
        {
            "slug": "forgiveness-in-relationships",
            "titleEn": "The role of forgiveness",
            "titleRu": "Роль прощения",
            "excerptEn": "Exploring forgiveness...",
            "excerptRu": "Исследование прощения..."
        }
    ]
}
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