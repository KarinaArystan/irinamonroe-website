# Page Generation Tools

This directory contains tools to help automate the migration and generation of pages for the Irina Monroe website.

## Page Generator

The `page-generator.js` script helps create consistent pages from JSON data files.

### Usage

```bash
node page-generator.js [type] [data-file]
```

### Available Types

- `qa` - Generate Q&A pages
- `hypnotherapy` - Generate hypnotherapy topic pages (coming soon)
- `psychology` - Generate psychology topic pages (coming soon)
- `service` - Generate service pages (coming soon)

### Example

```bash
# Generate a single Q&A page
node page-generator.js qa example-qa-data.json

# Generate multiple Q&A pages from a batch file
node page-generator.js qa batch-qa-data.json
```

### Q&A Data Structure

See `example-qa-data.json` for the required format. Key fields include:

- `category` - The Q&A category (relationships, family, personal, etc.)
- `categoryName` - Human-readable category name
- `urlSlug` - URL-friendly slug for the page
- `questionEn` / `questionRu` - The question in both languages
- `contentEn` / `contentRu` - The answer content (use \n for paragraphs)
- `relatedQuestions` - Array of related Q&A links

### Workflow for Migration

1. Extract content from old site into JSON format
2. Organize by category
3. Run the page generator
4. Review generated pages
5. Deploy to production

### Future Enhancements

- Add templates for hypnotherapy pages
- Add templates for psychology topic pages
- Add image handling
- Add automatic sitemap generation
- Add content validation