# Q&A Content Parser

This tool extracts Q&A content from the CSV file containing HTML data from the current website.

## Overview

The `parse-qa-content.js` script:
- Reads the CSV file with HTML content extracted from irinamonroe.com
- Parses HTML to extract questions and answers
- Categorizes content automatically based on keywords
- Outputs JSON files compatible with the page-generator.js tool

## Usage

1. Ensure dependencies are installed:
```bash
cd tools
npm install
```

2. Run the parser:
```bash
node parse-qa-content.js
```

## Input

The parser expects a CSV file at:
```
../../current-site/custom_extraction_part2.csv
```

CSV structure:
- URL (e.g., "https://www.irinamonroe.com/vnebrachniy-rebenok")
- Status code (e.g., "200")
- Status text (e.g., "OK")
- HTML content containing the Q&A

## Output

The parser generates two files:

### 1. qa-content.json
Contains an array of Q&A objects ready for page generation:
```json
[
  {
    "category": "family",
    "categoryName": "Family & Parenting",
    "urlSlug": "vnebrachniy-rebenok",
    "questionEn": "[Translation needed: ...]",
    "questionRu": "Внебрачный ребенок",
    "descriptionEn": "[Translation needed: ...]",
    "descriptionRu": "...",
    "keywords": "relationships, trust, family",
    "contentEn": "[Translation needed: ...]",
    "contentRu": "Full answer content...",
    "publishDate": "2025-06-15",
    "relatedQuestions": [],
    "originalQuestion": "Original question text...",
    "url": "https://www.irinamonroe.com/vnebrachniy-rebenok"
  }
]
```

### 2. qa-content-summary.json
Contains parsing summary and statistics:
```json
{
  "totalQuestions": 6,
  "categories": ["career", "family"],
  "processingErrors": [],
  "questionsPerCategory": {
    "career": 1,
    "family": 5
  }
}
```

## Categories

Content is automatically categorized based on keywords:
- **relationships**: Default category for relationship-related content
- **family**: Keywords: ребен*, дет*, родител*
- **career**: Keywords: работ*, карьер*
- **divorce**: Keywords: развод*, расставан*
- **infidelity**: Keywords: измен*, предател*, довер*
- **intimacy**: Keywords: секс*, интим*
- **self-esteem**: Keywords: самооценк*, уверен*
- **anxiety**: Keywords: тревог*, страх*, паник*
- **depression**: Keywords: депресс*, грусть*, печал*
- **grief**: Keywords: потер*, смерт*, утрат*

## Features

- Automatic HTML parsing and text extraction
- Smart content categorization
- Keyword extraction from content
- English placeholder generation for Russian content
- Compatible output format for page-generator.js
- Error handling and reporting
- Progress logging during processing

## Generating Pages

After parsing, generate Q&A pages using:
```bash
node page-generator.js qa qa-content.json
```

This will create HTML pages in the appropriate directories under:
```
../resources/questions/[category]/[url-slug]/index.html
```

## Notes

- Currently generates English placeholders for Russian content
- For production, integrate a translation API to provide actual English translations
- The parser skips entries without substantial content (< 100 characters)
- Navigation links from the original site are preserved but may need updating