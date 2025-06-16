const fs = require('fs');
const path = require('path');
const { parse } = require('csv-parse');
const { JSDOM } = require('jsdom');

// Helper function to extract text content from HTML
function extractTextFromHTML(html) {
  if (!html || typeof html !== 'string') return '';
  
  const dom = new JSDOM(html);
  const document = dom.window.document;
  
  // Remove script and style elements
  const scripts = document.querySelectorAll('script, style, noscript');
  scripts.forEach(el => el.remove());
  
  // Get text content
  const textContent = document.body ? document.body.textContent : '';
  
  // Clean up whitespace
  return textContent.replace(/\s+/g, ' ').trim();
}

// Helper function to extract structured content from HTML
function extractStructuredContent(html, url) {
  if (!html || typeof html !== 'string') return null;
  
  const dom = new JSDOM(html);
  const document = dom.window.document;
  
  // Extract title
  let title = '';
  const titleElements = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
  for (let el of titleElements) {
    const text = el.textContent.trim();
    if (text && text.length > 3 && !text.includes('font_')) {
      title = text;
      break;
    }
  }
  
  // Extract paragraphs
  const paragraphs = [];
  const paragraphElements = document.querySelectorAll('p, h6');
  paragraphElements.forEach(el => {
    const text = el.textContent.trim();
    if (text && text.length > 10) {
      paragraphs.push(text);
    }
  });
  
  // Extract slug from URL
  const urlParts = url.split('/').filter(p => p);
  const slug = urlParts[urlParts.length - 1];
  
  return {
    url,
    slug,
    title,
    content: paragraphs.join('\n\n'),
    rawHtml: html
  };
}

// Page categorizer
function categorizeContent(url, title, content) {
  const fullText = `${url} ${title} ${content}`.toLowerCase();
  
  // Service pages
  if (url.includes('/kak-ya-mogu-pomoch')) return { type: 'service', category: 'how-i-help' };
  if (url.includes('/skype-sessia')) return { type: 'service', category: 'skype-session' };
  if (url.includes('/sovmestnaya-rabota')) return { type: 'service', category: 'joint-work' };
  if (url.includes('/vopros-otvet')) return { type: 'service', category: 'question-answer' };
  if (url.includes('/zadat-svoi-vopros')) return { type: 'service', category: 'ask-question' };
  
  // Hypnotherapy pages
  if (url.includes('/gipno') || fullText.includes('гипно')) return { type: 'hypnotherapy', category: 'hypnosis' };
  if (url.includes('/samogipnoz')) return { type: 'hypnotherapy', category: 'self-hypnosis' };
  if (url.includes('/vnushaemost')) return { type: 'hypnotherapy', category: 'suggestibility' };
  if (url.includes('/meditatsie')) return { type: 'hypnotherapy', category: 'meditation' };
  
  // Psychology topics
  if (url.includes('/soznanie') || fullText.includes('сознани')) return { type: 'psychology', category: 'consciousness' };
  if (url.includes('/rebenok') || fullText.includes('ребенок') || fullText.includes('ребёнок')) return { type: 'psychology', category: 'inner-child' };
  if (url.includes('/travma') || fullText.includes('травм')) return { type: 'psychology', category: 'trauma' };
  if (url.includes('/emotsi') || fullText.includes('эмоци')) return { type: 'psychology', category: 'emotions' };
  if (url.includes('/stress') || fullText.includes('стресс')) return { type: 'psychology', category: 'stress' };
  if (url.includes('/ubezhdeni') || fullText.includes('убеждени')) return { type: 'psychology', category: 'beliefs' };
  if (url.includes('/proektsi') || fullText.includes('проекци')) return { type: 'psychology', category: 'projection' };
  if (url.includes('/vospriyati') || fullText.includes('восприяти')) return { type: 'psychology', category: 'perception' };
  if (url.includes('/bei-begi') || fullText.includes('бей-беги')) return { type: 'psychology', category: 'fight-flight' };
  if (url.includes('/vigorani') || fullText.includes('выгорани')) return { type: 'psychology', category: 'burnout' };
  
  // Main pages
  if (url === 'https://www.irinamonroe.com/' || url.includes('/home')) return { type: 'main', category: 'homepage' };
  if (url.includes('/aboutme')) return { type: 'main', category: 'about' };
  if (url.includes('/faq')) return { type: 'main', category: 'faq' };
  if (url.includes('/form')) return { type: 'main', category: 'form' };
  if (url.includes('/contract') || url.includes('/kontract')) return { type: 'main', category: 'contract' };
  if (url.includes('/privacy-policy')) return { type: 'main', category: 'privacy' };
  if (url.includes('/stati')) return { type: 'main', category: 'articles' };
  
  // Default to Q&A if contains question-like content
  if (fullText.includes('здравствуйте') || fullText.includes('вопрос') || 
      fullText.includes('ответ') || paragraphs.some(p => p.includes('?'))) {
    // Further categorize Q&A
    if (fullText.includes('ребен') || fullText.includes('дет') || fullText.includes('родител')) {
      return { type: 'qa', category: 'family' };
    }
    if (fullText.includes('работ') || fullText.includes('карьер')) {
      return { type: 'qa', category: 'career' };
    }
    if (fullText.includes('развод') || fullText.includes('расставан')) {
      return { type: 'qa', category: 'divorce' };
    }
    if (fullText.includes('измен') || fullText.includes('предател')) {
      return { type: 'qa', category: 'infidelity' };
    }
    if (fullText.includes('секс') || fullText.includes('интим')) {
      return { type: 'qa', category: 'intimacy' };
    }
    return { type: 'qa', category: 'relationships' };
  }
  
  return { type: 'unknown', category: 'uncategorized' };
}

// Process different content types
function processContent(data, type) {
  const { url, slug, title, content } = data;
  const { category } = type;
  
  // Common fields
  const base = {
    url,
    urlSlug: slug,
    titleRu: title,
    contentRu: content,
    publishDate: new Date().toISOString().split('T')[0],
    category
  };
  
  // Type-specific processing
  switch (type.type) {
    case 'hypnotherapy':
      return {
        ...base,
        titleEn: `[Translation needed: ${title}]`,
        descriptionEn: `[Translation needed: ${content.substring(0, 150)}...]`,
        descriptionRu: content.substring(0, 200) + '...',
        contentEn: `[Translation needed]`,
        keywords: 'hypnotherapy, hypnosis, therapy, healing'
      };
      
    case 'psychology':
      return {
        ...base,
        titleEn: `[Translation needed: ${title}]`,
        descriptionEn: `[Translation needed: ${content.substring(0, 150)}...]`,
        descriptionRu: content.substring(0, 200) + '...',
        contentEn: `[Translation needed]`,
        keywords: 'psychology, therapy, mental health, wellness'
      };
      
    case 'service':
      return {
        ...base,
        titleEn: `[Translation needed: ${title}]`,
        descriptionEn: `[Translation needed: ${content.substring(0, 150)}...]`,
        descriptionRu: content.substring(0, 200) + '...',
        contentEn: `[Translation needed]`,
        keywords: 'therapy, counseling, services, support'
      };
      
    case 'qa':
      // Extract question and answer
      const paragraphs = content.split('\n\n');
      let question = '';
      let answer = '';
      let isQuestion = true;
      
      paragraphs.forEach(p => {
        if (p.toLowerCase().includes('здравствуйте') || p.includes('?')) {
          question += p + '\n\n';
        } else if (isQuestion && p.length > 50) {
          isQuestion = false;
          answer += p + '\n\n';
        } else if (!isQuestion) {
          answer += p + '\n\n';
        }
      });
      
      return {
        ...base,
        questionEn: `[Translation needed: ${title}]`,
        questionRu: title,
        descriptionEn: `[Translation needed: ${answer.substring(0, 150)}...]`,
        descriptionRu: answer.substring(0, 200) + '...',
        contentEn: `[Translation needed]`,
        keywords: 'psychology, therapy, counseling, relationships',
        categoryName: getCategoryName(category),
        originalQuestion: question.trim()
      };
      
    default:
      return base;
  }
}

function getCategoryName(category) {
  const names = {
    'relationships': 'Couples & Relationships',
    'family': 'Family & Parenting',
    'career': 'Career & Life Balance',
    'divorce': 'Divorce & Separation',
    'infidelity': 'Trust & Infidelity',
    'intimacy': 'Intimacy & Sexuality'
  };
  return names[category] || 'General Psychology';
}

// Main parsing function
async function parseAllContent(inputFile) {
  const results = {
    qa: [],
    hypnotherapy: [],
    psychology: [],
    service: [],
    main: [],
    unknown: []
  };
  
  const errors = [];
  let rowCount = 0;
  let processedCount = 0;
  
  // Create parser
  const parser = fs
    .createReadStream(inputFile)
    .pipe(parse({
      delimiter: ',',
      quote: '"',
      escape: '"',
      relax_quotes: true,
      skip_empty_lines: true,
      relax_column_count: true,
      from_line: 1
    }));
  
  console.log('Starting to parse CSV file...');
  
  for await (const record of parser) {
    rowCount++;
    
    try {
      // Check if this looks like a URL record
      if (record.length >= 4 && record[0] && record[0].startsWith('https://www.irinamonroe.com')) {
        const [url, statusCode, statusText, ...htmlParts] = record;
        
        // Skip non-200 responses
        if (statusCode !== '200') continue;
        
        // Join remaining parts in case HTML contained commas
        const html = htmlParts.join(',');
        
        // Extract content
        const extracted = extractStructuredContent(html, url);
        if (!extracted || !extracted.content) continue;
        
        // Categorize
        const type = categorizeContent(url, extracted.title, extracted.content);
        
        // Process content
        const processed = processContent(extracted, type);
        
        // Add to appropriate array
        if (results[type.type]) {
          results[type.type].push(processed);
          processedCount++;
          
          if (processedCount % 10 === 0) {
            console.log(`Processed ${processedCount} pages...`);
          }
        }
      }
    } catch (error) {
      errors.push({
        row: rowCount,
        error: error.message
      });
      if (errors.length < 10) {
        console.error(`Error at row ${rowCount}: ${error.message}`);
      }
    }
  }
  
  // Save results
  console.log('\nSaving results...');
  
  // Save each type to separate files
  for (const [type, data] of Object.entries(results)) {
    if (data.length > 0) {
      const filename = path.join(__dirname, `${type}-content.json`);
      fs.writeFileSync(filename, JSON.stringify(data, null, 2), 'utf8');
      console.log(`Saved ${data.length} ${type} pages to ${filename}`);
    }
  }
  
  // Create summary
  const summary = {
    totalRows: rowCount,
    totalProcessed: processedCount,
    breakdown: {
      qa: results.qa.length,
      hypnotherapy: results.hypnotherapy.length,
      psychology: results.psychology.length,
      service: results.service.length,
      main: results.main.length,
      unknown: results.unknown.length
    },
    errors: errors.length,
    timestamp: new Date().toISOString()
  };
  
  fs.writeFileSync(
    path.join(__dirname, 'content-parsing-summary.json'),
    JSON.stringify(summary, null, 2),
    'utf8'
  );
  
  console.log('\nParsing complete!');
  console.log(`Total rows processed: ${rowCount}`);
  console.log(`Total pages extracted: ${processedCount}`);
  console.log(`Errors encountered: ${errors.length}`);
  console.log('\nBreakdown by type:');
  for (const [type, count] of Object.entries(summary.breakdown)) {
    if (count > 0) {
      console.log(`  ${type}: ${count}`);
    }
  }
}

// Run the parser
const inputFile = path.join(__dirname, '../../current-site/custom_extraction_part2.csv');

if (!fs.existsSync(inputFile)) {
  console.error(`Input file not found: ${inputFile}`);
  process.exit(1);
}

parseAllContent(inputFile).catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});