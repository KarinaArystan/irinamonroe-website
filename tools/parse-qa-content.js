const fs = require('fs');
const path = require('path');
const { parse } = require('csv-parse');
const { JSDOM } = require('jsdom');

// Helper function to extract text content from HTML
function extractTextFromHTML(html) {
  const dom = new JSDOM(html);
  const document = dom.window.document;
  
  // Remove script and style elements
  const scripts = document.querySelectorAll('script, style');
  scripts.forEach(el => el.remove());
  
  // Get text content
  const textContent = document.body.textContent;
  
  // Clean up whitespace
  return textContent.replace(/\s+/g, ' ').trim();
}

// Category mapping
const categoryMap = {
  'relationships': 'Couples & Relationships',
  'family': 'Family & Parenting',
  'divorce': 'Divorce & Separation',
  'infidelity': 'Trust & Infidelity',
  'intimacy': 'Intimacy & Sexuality',
  'self-esteem': 'Self-Esteem & Personal Growth',
  'career': 'Career & Life Balance',
  'anxiety': 'Anxiety & Stress',
  'depression': 'Depression & Mood',
  'grief': 'Grief & Loss'
};

// Helper function to create a simple English translation placeholder
function createEnglishPlaceholder(russianText) {
  // This is a placeholder - in production, you'd use a translation API
  return `[Translation needed: ${russianText.substring(0, 50)}...]`;
}

// Helper function to extract Q&A from HTML
function extractQAFromHTML(html, url) {
  const dom = new JSDOM(html);
  const document = dom.window.document;
  
  // Extract title from h5 or h2 elements with specific classes
  let title = '';
  const titleElements = document.querySelectorAll('h5.font_5, h2.font_2');
  if (titleElements.length > 0) {
    // Find the first non-empty title
    for (let el of titleElements) {
      const text = el.textContent.trim();
      if (text && text !== ' ' && text !== '​') {
        title = text;
        break;
      }
    }
  }
  
  // Extract question and answer content
  let questionContent = [];
  let answerContent = [];
  let isQuestion = true;
  
  // Get all paragraph and heading elements
  const contentElements = document.querySelectorAll('p.font_7, h6.font_6');
  
  contentElements.forEach((el) => {
    const text = el.textContent.trim();
    if (!text || text === ' ' || text === '​') return;
    
    // Check if this is italic text (usually the question)
    const hasItalic = el.querySelector('span[style*="font-style:italic"]');
    
    if (hasItalic || (isQuestion && el.tagName === 'P')) {
      questionContent.push(text);
    } else if (el.tagName === 'H6' || (!hasItalic && el.tagName === 'P')) {
      isQuestion = false;
      answerContent.push(text);
    }
  });
  
  // Extract slug from URL
  const urlParts = url.split('/');
  const slug = urlParts[urlParts.length - 1];
  
  // Try to categorize based on content
  let category = 'relationships'; // default category
  const contentText = (title + ' ' + questionContent.join(' ') + ' ' + answerContent.join(' ')).toLowerCase();
  
  if (contentText.includes('ребен') || contentText.includes('дет') || contentText.includes('родител')) {
    category = 'family';
  } else if (contentText.includes('работ') || contentText.includes('карьер')) {
    category = 'career';
  } else if (contentText.includes('развод') || contentText.includes('расставан')) {
    category = 'divorce';
  } else if (contentText.includes('измен') || contentText.includes('предател') || contentText.includes('довер')) {
    category = 'infidelity';
  } else if (contentText.includes('секс') || contentText.includes('интим')) {
    category = 'intimacy';
  } else if (contentText.includes('самооценк') || contentText.includes('уверен')) {
    category = 'self-esteem';
  } else if (contentText.includes('тревог') || contentText.includes('страх') || contentText.includes('паник')) {
    category = 'anxiety';
  } else if (contentText.includes('депресс') || contentText.includes('грусть') || contentText.includes('печал')) {
    category = 'depression';
  } else if (contentText.includes('потер') || contentText.includes('смерт') || contentText.includes('утрат')) {
    category = 'grief';
  }
  
  // Generate keywords based on content
  const keywords = [];
  if (contentText.includes('отношен')) keywords.push('relationships');
  if (contentText.includes('любов')) keywords.push('love');
  if (contentText.includes('довер')) keywords.push('trust');
  if (contentText.includes('семь')) keywords.push('family');
  if (contentText.includes('терапи')) keywords.push('therapy');
  if (contentText.includes('психолог')) keywords.push('psychology');
  if (contentText.includes('эмоци')) keywords.push('emotions');
  if (contentText.includes('чувств')) keywords.push('feelings');
  
  // Create the formatted object
  const questionText = questionContent.join('\n\n');
  const answerText = answerContent.join('\n\n');
  const description = answerText.substring(0, 200) + '...';
  
  return {
    category,
    categoryName: categoryMap[category] || 'General Psychology',
    urlSlug: slug,
    questionEn: createEnglishPlaceholder(title),
    questionRu: title || 'Вопрос',
    descriptionEn: createEnglishPlaceholder(description),
    descriptionRu: description,
    keywords: keywords.join(', ') || 'psychology, therapy, counseling',
    contentEn: createEnglishPlaceholder(answerText),
    contentRu: answerText,
    publishDate: new Date().toISOString().split('T')[0],
    relatedQuestions: [],
    originalQuestion: questionText,
    url
  };
}

// Main parsing function
async function parseCSVFile(inputFile, outputFile) {
  const results = [];
  const errors = [];
  
  // Read and parse CSV
  const parser = fs
    .createReadStream(inputFile)
    .pipe(parse({
      delimiter: ',',
      quote: '"',
      escape: '"',
      relax_quotes: true,
      skip_empty_lines: true,
      relax_column_count: true,
      skip_records_with_error: true
    }));
  
  let rowIndex = 0;
  
  for await (const record of parser) {
    rowIndex++;
    
    try {
      // Check if this looks like a URL record
      if (record.length >= 4 && record[0] && record[0].startsWith('https://www.irinamonroe.com')) {
        const [url, statusCode, statusText, ...htmlParts] = record;
        
        // Join remaining parts in case HTML contained commas
        const html = htmlParts.join(',');
        
        // Only process successful requests with Q&A pages
        if (statusCode === '200' && !url.includes('/zadat-svoi-vopros')) {
          const qa = extractQAFromHTML(html, url);
          
          // Only add if we have both question and answer
          if (qa.contentRu && qa.contentRu.length > 100) { // Ensure we have substantial content
            results.push(qa);
            console.log(`Processed: ${qa.urlSlug} - ${qa.questionRu}`);
          }
        }
      }
    } catch (error) {
      errors.push({
        row: rowIndex,
        error: error.message
      });
      console.error(`Error processing row ${rowIndex}:`, error.message);
    }
  }
  
  // Sort results by category
  results.sort((a, b) => {
    if (a.category < b.category) return -1;
    if (a.category > b.category) return 1;
    return 0;
  });
  
  // Write results to JSON file in the format expected by page-generator.js
  fs.writeFileSync(outputFile, JSON.stringify(results, null, 2), 'utf8');
  
  // Also create a summary file
  const summaryFile = outputFile.replace('.json', '-summary.json');
  const summary = {
    totalQuestions: results.length,
    categories: [...new Set(results.map(r => r.category))],
    processingErrors: errors,
    questionsPerCategory: {}
  };
  
  // Count questions per category
  results.forEach(q => {
    if (!summary.questionsPerCategory[q.category]) {
      summary.questionsPerCategory[q.category] = 0;
    }
    summary.questionsPerCategory[q.category]++;
  });
  
  fs.writeFileSync(summaryFile, JSON.stringify(summary, null, 2), 'utf8');
  
  console.log(`\nProcessing complete!`);
  console.log(`Total questions extracted: ${results.length}`);
  console.log(`Categories found: ${summary.categories.join(', ')}`);
  console.log(`Errors encountered: ${errors.length}`);
  console.log(`Output saved to: ${outputFile}`);
  console.log(`Summary saved to: ${summaryFile}`);
}

// Run the parser
const inputFile = path.join(__dirname, '../../current-site/custom_extraction_part2.csv');
const outputFile = path.join(__dirname, 'qa-content.json');

// Check if input file exists
if (!fs.existsSync(inputFile)) {
  console.error(`Input file not found: ${inputFile}`);
  process.exit(1);
}

// Check if we need to install dependencies
try {
  require('csv-parse');
  require('jsdom');
} catch (error) {
  console.error('Missing dependencies. Please run: npm install csv-parse jsdom');
  process.exit(1);
}

parseCSVFile(inputFile, outputFile).catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});