# Irina Monroe - Psychologist & Hypnotherapist Website

## Project Overview
A bilingual (English/Russian) website for Irina Monroe, a psychologist and hypnotherapist with 19+ years of experience. The design emphasizes a calm, professional aesthetic with a unique philosophical approach: "I don't treat or give advice. I create space where you can feel real."

## Design Specifications

### Color Palette
- Primary: `#93884a` (Olive green)
- Background Light: `#e8e4dd`
- Text Dark: `#574c40`
- Accent Brown: `#a59a84`
- Background Lighter: `#edeae4`
- Background Section: `#F2F0ED`
- Accent Green: `#9c9875`
- White: `#FFFFFF`

### Typography
- Headers: 'Cormorant Infant' (serif)
- Body: 'Inter' (sans-serif)
- Weights: 300, 400, 500, 600, 700

### Key Features
1. **Bilingual Support**: Full English/Russian language toggle with localStorage persistence
2. **Responsive Design**: Mobile-first approach with breakpoint at 968px
3. **Smooth Scrolling**: Navigation with smooth scroll behavior
4. **Interactive Elements**: Hover states on all interactive components
5. **Fixed Header**: With 15px green bottom border (signature element)

## File Structure
```
irina-monroe-website/
│
├── index.html          # Main HTML file
├── styles.css          # All CSS styles
├── script.js           # JavaScript functionality
├── README.md          # This file
└── images/            # Image assets
```

## Images Used
1. **Hero Section**: 
   - URL: `https://res.cloudinary.com/dfgcciytn/image/upload/v1749785867/124_f2xfen.png`
   - Fallback: Professional woman portrait

2. **Welcome Section Background**: 
   - URL: `https://res.cloudinary.com/dfgcciytn/image/upload/v1749852701/beige_background_pn4cvg.png`
   - Fallback: Beige color `#f5f3f0`

3. **About Section**: 
   - URL: `https://res.cloudinary.com/dfgcciytn/image/upload/v1749852730/Screenshot_2025-06-13_at_5.22.57_PM_fbzbnv.png`
   - Fallback: Professional headshot

## Sections

### 1. Header
- Fixed position with logo
- Navigation menu
- Language toggle (ENG/РУС)
- Green bottom border (15px)

### 2. Hero Section
- Split layout: Image left, text right
- Headline with italic emphasis on key words
- Tags: psychologist, hypnotherapist, 19+ years
- Dual CTA buttons (English/Russian)

### 3. Welcome Section
- Centered content with textured background
- Personal introduction
- Highlighted quote in primary color

### 4. About Section
- Image left, text right layout
- Professional journey description
- Experience box highlighting "19+ Years"

### 5. Services Section
- Three service categories with outline numbers
- Relationship Difficulties
- Personal Crises & Emotional States
- Dependent Behaviors

### 6. Process Section
- Three-step approach
- Large numbers in primary color
- Centered layout

### 7. Contact Section
- Dual language CTAs
- Three contact methods: Online Sessions, WhatsApp, Email
- Warm, inviting copy

### 8. Footer
- Dark background
- Links: Privacy Policy, Therapeutic Contract, Online Sessions
- Copyright notice

## Technical Implementation

### Language Toggle
```javascript
// Stores preference in localStorage
// Toggle between English and Russian content
// Uses lang attributes for content switching
```

### Responsive Breakpoints
- Desktop: > 968px
- Mobile: ≤ 968px

### CSS Architecture
- CSS Variables for consistent theming
- Grid and Flexbox for layouts
- No absolute positioning (fully responsive)
- Semantic HTML structure

## Content Philosophy
The website reflects Irina's unique therapeutic approach:
- Non-directive therapy
- Creating space rather than treating
- Focus on authenticity
- Gradual, patient-centered approach

## SEO Optimization
- Meta description in English
- Semantic HTML structure
- Alt tags on all images
- Clean URL structure potential

## Browser Support
- Modern browsers (Chrome, Firefox, Safari, Edge)
- CSS Grid and Flexbox support required
- JavaScript enabled for language toggle

## Future Enhancements
1. Blog section for articles
2. Online booking system
3. Client portal
4. Resources/downloads section
5. Testimonials expansion
6. SSL certificate implementation
7. Google Analytics integration

## Deployment Notes
- Can be hosted on any static hosting (Netlify, Vercel, GitHub Pages)
- No server-side requirements
- All assets are externally hosted (CDN)
- Mobile-responsive design ready

## Original Design Source
- Created in Figma
- Inspired by template: https://hereandnowbyapplet.squarespace.com/
- Customized for psychotherapy practice
- Maintains calm, professional aesthetic

## Contact
Website for: Irina Monroe
Email: irina@irinamonroe.com
Location: Florida, USA (previously Los Angeles)
Services: Online therapy via Zoom/Skype