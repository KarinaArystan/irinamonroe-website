# Migration TODO List - Priority Order

## 🔴 CRITICAL - Must Complete First

### 1. About Me Page (/aboutme)
- **Why Critical**: Establishes credibility and personal connection
- **Content Needed**: Bio, credentials, approach, photo
- **URL**: `/aboutme/` or `/about/`

### 2. Contact Form Page (/form)
- **Why Critical**: Primary lead generation tool
- **Content Needed**: Contact form fields, privacy notice
- **URL**: `/form/` or `/contact/`

### 3. Service Description Pages
Missing key service pages that explain offerings:
- **How I Can Help** (`/kak-ya-mogu-pomoch/`)
- **Skype Sessions** (`/skype-sessia/`)
- **Joint Work** (`/sovmestnaya-rabota-s-psixologom/`)

## 🟡 HIGH PRIORITY - Complete Soon

### 4. Psychology/Trauma Educational Pages (9 pages)
Important educational content about trauma and healing:
- Inner Child (`/vnytrenniy-rebenok/`)
- Trauma Distorts Perception (`/travma-iskagaet-vospriyatie/`)
- Trauma Can Emotionally Freeze (`/travma-moget-emotsionalno-zamorozit/`)
- View on Trauma (`/vzglyad-na-travmu/`)
- Healing Trauma Takes Time (`/istselenie-travmi-trebuet-vremeni/`)
- Emotions Connected to Body (`/emotsii-svyazani-s-telom/`)
- Emotional States (`/emotsionalnie-sostoyaniya/`)
- Projection Mirror (`/proektsia-zerkalo-vneyrennego-mira/`)
- Lens of Perception (`/linza-vospriyatia-sebya-i-mira/`)

### 5. Ask Your Question Form
- **URL**: `/zadat-svoi-vopros/`
- **Functionality**: Form for users to submit questions
- **Integration**: Should connect to email or database

## 🟢 MEDIUM PRIORITY - Bulk Migration

### 6. Remaining Q&A Pages (~130 pages)
- Only 20 of ~150 Q&A pages migrated
- Need to extract and migrate remaining content
- Categories to organize:
  - Relationships & Couples
  - Family & Parenting
  - Personal Development
  - Mental Health
  - Life Transitions

### 7. Clean Up Duplicates
Remove or consolidate duplicate pages:
- `копия-краски-природы` and `копия-краски-природы-1`
- `copy-of-что-такое-сознание`
- `ssori-s-mygem` and `ssori-s-mygem-1`
- `alkogolnaya-zavisimost-c1zze` and `alkogolnaya-zavisimost-chvu`

## 🔵 NICE TO HAVE - Enhancements

### 8. Technical Improvements
- Add header/footer components (currently placeholders)
- Implement search functionality for Q&A section
- Add sitemap.xml
- Set up 301 redirects from old URLs
- Optimize images

### 9. Content Enhancements
- Add related content links
- Create topic hubs
- Add newsletter signup
- Implement testimonials section

## Migration Status Summary

| Section | Total Pages | Migrated | Remaining | % Complete |
|---------|------------|----------|-----------|------------|
| Main Pages | 7 | 3 | 4 | 43% |
| Service Pages | 5 | 1 | 4 | 20% |
| Hypnotherapy | 10 | 14 | 0 | 140% ✅ |
| Psychology Topics | 14 | 5 | 9 | 36% |
| Blog Articles | 60+ | 60+ | 0 | 100% ✅ |
| Q&A Pages | ~150 | 20 | ~130 | 13% |
| **TOTAL** | **~246** | **~103** | **~143** | **42%** |

## Next Steps

1. **Create About Me page** - Use existing content from old site
2. **Build Contact Form** - Simple form with email integration
3. **Migrate Service Pages** - Extract content from CSV
4. **Bulk migrate Q&A pages** - Use automated tools
5. **Add navigation** - Update menu with all new pages

## Resources Available

- `custom_extraction_part2.csv` - Contains raw content
- `page-generator-ru.js` - For generating Russian pages
- `parse-all-content.js` - For extracting content from CSV
- Templates ready for all page types