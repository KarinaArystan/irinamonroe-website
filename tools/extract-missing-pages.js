const fs = require('fs');
const path = require('path');
const { parse } = require('csv-parse');
const { JSDOM } = require('jsdom');

// Missing psychology pages to find
const missingPages = [
    { url: 'vnytrenniy-rebenok', title: 'Внутренний ребенок' },
    { url: 'kto-takoi-vnytrennii-rebenok', title: 'Внутренний ребенок' },
    { url: 'travma-iskagaet-vospriyatie', title: 'Травма искажает восприятие' },
    { url: 'travma-moget-emotsionalno-zamorozit', title: 'Травма может эмоционально заморозить' },
    { url: 'vzglyad-na-travmu', title: 'Взгляд на травму' },
    { url: 'istselenie-travmi-trebuet-vremeni', title: 'Исцеление травмы требует времени' },
    { url: 'emotsii-svyazani-s-telom', title: 'Эмоции связаны с телом' },
    { url: 'emotsionalnie-sostoyaniya', title: 'Эмоциональные состояния' },
    { url: 'proektsia-zerkalo-vneyrennego-mira', title: 'Проекция зеркало внутреннего мира' },
    { url: 'linza-vospriyatia-sebya-i-mira', title: 'Линза восприятия себя и мира' }
];

// Extract content from HTML
function extractContent(html, url) {
    if (!html || typeof html !== 'string') return null;
    
    const dom = new JSDOM(html);
    const document = dom.window.document;
    
    // Remove scripts and styles
    const scripts = document.querySelectorAll('script, style, noscript');
    scripts.forEach(el => el.remove());
    
    // Extract title
    let title = '';
    const titleElements = document.querySelectorAll('h1, h2, h3, h4, h5');
    for (let el of titleElements) {
        const text = el.textContent.trim();
        if (text && text.length > 5 && !text.includes('font_')) {
            title = text;
            break;
        }
    }
    
    // Extract paragraphs
    const paragraphs = [];
    const contentElements = document.querySelectorAll('p, h6');
    contentElements.forEach(el => {
        const text = el.textContent.trim();
        if (text && text.length > 20) {
            paragraphs.push(text);
        }
    });
    
    return {
        url,
        title: title || '',
        content: paragraphs.join('\n\n')
    };
}

// Process CSV and extract pages
async function extractMissingPages() {
    const inputFile = path.join(__dirname, '../../current-site/custom_extraction_part2.csv');
    const results = {
        psychology: [],
        qa: []
    };
    
    console.log('Starting extraction of missing pages...\n');
    
    // Create parser
    const parser = fs
        .createReadStream(inputFile)
        .pipe(parse({
            delimiter: ',',
            quote: '"',
            escape: '"',
            relax_quotes: true,
            skip_empty_lines: true,
            relax_column_count: true
        }));
    
    let foundCount = 0;
    
    for await (const record of parser) {
        try {
            if (record.length >= 4 && record[0] && record[0].startsWith('https://www.irinamonroe.com')) {
                const [url, statusCode, statusText, ...htmlParts] = record;
                
                if (statusCode !== '200') continue;
                
                // Check if this is one of our missing pages
                const urlPath = url.split('/').pop();
                const missingPage = missingPages.find(p => 
                    p.url === urlPath || url.includes(p.url)
                );
                
                if (missingPage) {
                    const html = htmlParts.join(',');
                    const extracted = extractContent(html, url);
                    
                    if (extracted && extracted.content) {
                        foundCount++;
                        console.log(`✅ Found: ${missingPage.title} (${urlPath})`);
                        
                        // Create psychology page data
                        const pageData = {
                            urlSlug: urlPath,
                            titleRu: extracted.title || missingPage.title,
                            descriptionRu: extracted.content.substring(0, 200) + '...',
                            keywords: 'психология, терапия, травма, исцеление, эмоции',
                            contentRu: extracted.content,
                            publishDate: new Date().toISOString().split('T')[0],
                            category: 'trauma'
                        };
                        
                        results.psychology.push(pageData);
                    }
                }
            }
        } catch (error) {
            // Skip errors
        }
    }
    
    // Save psychology pages
    if (results.psychology.length > 0) {
        const outputFile = path.join(__dirname, 'missing-psychology-pages.json');
        fs.writeFileSync(outputFile, JSON.stringify(results.psychology, null, 2));
        console.log(`\n✅ Saved ${results.psychology.length} psychology pages to missing-psychology-pages.json`);
    }
    
    console.log(`\n📊 Summary:`);
    console.log(`Found ${foundCount} of ${missingPages.length} missing psychology pages`);
    
    // Now extract ALL Q&A pages for bulk migration
    console.log('\n\nExtracting Q&A pages...');
    
    // Re-read for Q&A extraction
    const parser2 = fs
        .createReadStream(inputFile)
        .pipe(parse({
            delimiter: ',',
            quote: '"',
            escape: '"',
            relax_quotes: true,
            skip_empty_lines: true,
            relax_column_count: true
        }));
    
    let qaCount = 0;
    const qaPages = [];
    
    for await (const record of parser2) {
        try {
            if (record.length >= 4 && record[0] && record[0].startsWith('https://www.irinamonroe.com')) {
                const [url, statusCode, statusText, ...htmlParts] = record;
                
                if (statusCode !== '200') continue;
                
                const html = htmlParts.join(',');
                const urlPath = url.split('/').pop();
                
                // Skip if it's a known page type
                if (url.includes('/blog/') || 
                    url.includes('/resources/') || 
                    url.includes('/services/') ||
                    url.includes('/aboutme') ||
                    url.includes('/faq') ||
                    url.includes('/form') ||
                    url.includes('/privacy') ||
                    url === 'https://www.irinamonroe.com/' ||
                    missingPages.find(p => urlPath === p.url)) {
                    continue;
                }
                
                // Check if content looks like Q&A
                if (html.includes('Здравствуйте') || 
                    html.includes('вопрос') || 
                    html.includes('Ответ')) {
                    
                    const extracted = extractContent(html, url);
                    if (extracted && extracted.content && extracted.content.length > 100) {
                        qaCount++;
                        
                        // Determine category
                        let category = 'general';
                        const content = extracted.content.toLowerCase();
                        
                        if (content.includes('ребен') || content.includes('родител') || content.includes('дет')) {
                            category = 'family';
                        } else if (content.includes('муж') || content.includes('жен') || content.includes('отношен') || content.includes('любов')) {
                            category = 'relationships';
                        } else if (content.includes('развод') || content.includes('расстав')) {
                            category = 'divorce';
                        } else if (content.includes('измен') || content.includes('предател')) {
                            category = 'infidelity';
                        } else if (content.includes('секс') || content.includes('интим')) {
                            category = 'intimacy';
                        } else if (content.includes('работ') || content.includes('карьер')) {
                            category = 'career';
                        } else if (content.includes('депресс') || content.includes('тревог') || content.includes('страх')) {
                            category = 'mental-health';
                        }
                        
                        const categoryNames = {
                            'relationships': 'Отношения',
                            'family': 'Семья и дети',
                            'divorce': 'Развод и расставание',
                            'infidelity': 'Измена и доверие',
                            'intimacy': 'Интимность',
                            'career': 'Карьера и работа',
                            'mental-health': 'Психическое здоровье',
                            'general': 'Общие вопросы'
                        };
                        
                        const pageData = {
                            category,
                            categoryName: categoryNames[category],
                            urlSlug: urlPath,
                            questionRu: extracted.title || 'Вопрос',
                            descriptionRu: extracted.content.substring(0, 200) + '...',
                            keywords: 'психология, консультация, вопросы, ответы',
                            contentRu: extracted.content,
                            publishDate: new Date().toISOString().split('T')[0]
                        };
                        
                        qaPages.push(pageData);
                        
                        if (qaCount % 10 === 0) {
                            console.log(`Processed ${qaCount} Q&A pages...`);
                        }
                    }
                }
            }
        } catch (error) {
            // Skip errors
        }
    }
    
    // Save Q&A pages in batches
    if (qaPages.length > 0) {
        // Save all Q&A pages
        const qaOutputFile = path.join(__dirname, 'all-qa-pages.json');
        fs.writeFileSync(qaOutputFile, JSON.stringify(qaPages, null, 2));
        console.log(`\n✅ Saved ${qaPages.length} Q&A pages to all-qa-pages.json`);
        
        // Also save by category for easier management
        const categories = [...new Set(qaPages.map(p => p.category))];
        categories.forEach(cat => {
            const categoryPages = qaPages.filter(p => p.category === cat);
            const catFile = path.join(__dirname, `qa-${cat}-pages.json`);
            fs.writeFileSync(catFile, JSON.stringify(categoryPages, null, 2));
            console.log(`📁 ${cat}: ${categoryPages.length} pages`);
        });
    }
    
    console.log('\n✅ Extraction complete!');
}

// Run the extraction
extractMissingPages().catch(error => {
    console.error('Fatal error:', error);
    process.exit(1);
});