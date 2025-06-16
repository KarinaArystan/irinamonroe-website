# Migration Context Summary - January 19, 2025

## Current State of Site Migration

### Completed Infrastructure

#### 1. Navigation Structure
- **Removed**: "How It Works" from main nav (section still exists on page)
- **Added**: "Resources" dropdown with 4 subsections:
  - Hypnotherapy
  - Psychology Topics
  - Q&A / Consultations
  - Services

#### 2. Directory Structure Created
```
/resources/
  - index.html (Resources hub with 4 cards)
  - resources-styles.css (shared styles)
  /hypnotherapy/
    - index.html (10 topic placeholders)
  /psychology/
    - index.html (14 topics organized by theme)
  /questions/
    - index.html (searchable Q&A directory)
    - qa-template.html (master template)
/services/
  - index.html (Services overview)
/faq/
  - index.html (FAQ accordion)
/tools/
  - page-generator.js (automated page creation)
  - example-qa-data.json
  - README.md
```

#### 3. Key Files & Their Purpose

**Q&A Template** (`/resources/questions/qa-template.html`):
- Full SEO optimization with meta tags
- Bilingual support (EN/RU)
- Related questions section
- Previous/Next navigation
- Structured data for search engines
- Placeholders marked with [BRACKETS]

**Page Generator** (`/tools/page-generator.js`):
- Node.js script for batch page creation
- Reads JSON data and generates HTML
- Usage: `node page-generator.js qa data.json`
- Creates proper directory structure automatically

**Resources Styles** (`/resources/resources-styles.css`):
- Shared styles for all resource pages
- Card layouts, hover effects
- Category pills, search box
- Mobile responsive

### Pages Still Needing Migration (186 total)

#### Main Pages (7)
1. Homepage
2. About Me (/aboutme)
3. FAQ (/faq) - DONE
4. Form (/form)
5. Contract (/contract) - Partially done
6. Privacy Policy (/privacy-policy) - Partially done
7. Articles/Stati (/stati)

#### Service Pages (5)
1. How I Can Help (/kak-ya-mogu-pomoch)
2. Skype Session (/skype-sessia)
3. Joint Work (/sovmestnaya-rabota-s-psixologom)
4. Question-Answer (/vopros-otvet)
5. Ask Your Question (/zadat-svoi-vopros)

#### Hypnotherapy Pages (10)
All have placeholders in `/resources/hypnotherapy/`

#### Psychology Topics (14)
All have placeholders in `/resources/psychology/`

#### Q&A Pages (~150)
Categories established:
- Couples & Relationships
- Family & Parenting
- Personal Development
- Mental Wellness
- Life Transitions
- Intimacy & Connection

### Current Design System

**Colors**:
- Primary: #93884a (olive green)
- Accent Brown: #a59a84
- Background: #fdfcfa, #faf8f5, #f7f4f0

**Typography**:
- Headers: Cormorant Infant (serif)
- Body: Inter (sans-serif)
- H2 size: 36px (standardized)
- Section labels: 13.6px, uppercase, 3px letter-spacing

**Components Built**:
- Resource cards with hover effects
- Topic cards with arrow animations
- Category pills for filtering
- Search box with button
- Breadcrumb navigation
- Related content cards
- CTA sections

### JavaScript Functionality
- Language toggle (RU/EN)
- Mobile menu
- Dropdown menu (desktop hover, mobile click)
- FAQ accordion
- Q&A category filtering
- Search functionality

### Migration Process

1. **For Q&A Pages**:
   - Format content as JSON
   - Required fields: category, urlSlug, questionEn/Ru, contentEn/Ru, etc.
   - Run: `node tools/page-generator.js qa [data-file.json]`
   - Pages auto-generate in correct directories

2. **For Other Pages**:
   - Use existing templates as reference
   - Maintain consistent header/footer structure
   - Follow established URL patterns

### Important Notes

- All pages need header/footer components (currently placeholders)
- Bilingual support throughout (lang="en" / lang="ru")
- Mobile-first responsive design
- SEO optimization on all pages
- Content uses \n for paragraph breaks in JSON

### Ready for Content Migration
The infrastructure is complete. Next step is to provide content in JSON format for batch generation or individual page creation.