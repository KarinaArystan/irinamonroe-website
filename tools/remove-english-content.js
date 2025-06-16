const fs = require('fs');
const path = require('path');

// Function to remove English content from HTML
function removeEnglishContent(html) {
    // Remove lang="en" attributes and their associated elements
    html = html.replace(/<[^>]+lang="en"[^>]*>[\s\S]*?<\/[^>]+>/g, '');
    
    // Remove English-specific class references in content
    html = html.replace(/bodyElement\.classList\.contains\('ru'\)[^;]+;/g, '');
    
    // Update aria-label attributes that might be in English
    html = html.replace(/aria-label="Toggle menu"/g, 'aria-label="Открыть меню"');
    html = html.replace(/aria-label="Close menu"/g, 'aria-label="Закрыть меню"');
    
    // Remove any remaining English text patterns
    const englishPatterns = [
        /How I Work/g,
        /Stop and Listen/g,
        /What matters to me/g,
        /If this way of being/g,
        /Therapy is not a method/g
    ];
    
    englishPatterns.forEach(pattern => {
        html = html.replace(pattern, '');
    });
    
    return html;
}

// Function to process a single HTML file
function processFile(filePath) {
    if (!fs.existsSync(filePath)) {
        console.log(`File not found: ${filePath}`);
        return;
    }
    
    console.log(`Processing: ${filePath}`);
    
    let content = fs.readFileSync(filePath, 'utf-8');
    const originalLength = content.length;
    
    // Remove English content
    content = removeEnglishContent(content);
    
    // Write back if changes were made
    if (content.length !== originalLength) {
        fs.writeFileSync(filePath, content, 'utf-8');
        console.log(`✓ Updated: ${filePath} (removed ${originalLength - content.length} characters)`);
    } else {
        console.log(`✓ No English content found in: ${filePath}`);
    }
}

// Main execution
function main() {
    const baseDir = '/Users/Karina/Library/CloudStorage/GoogleDrive-karina.arystan@gmail.com/My Drive/Projects/irinamonroe.com/new-site';
    
    // Process main index.html
    processFile(path.join(baseDir, 'index.html'));
    
    // Process other key pages
    const keyPages = [
        'about/index.html',
        'contact/index.html',
        'services/index.html',
        'blog/index.html',
        'resources/index.html',
        'resources/hypnotherapy/index.html',
        'resources/psychology/index.html',
        'resources/questions/index.html'
    ];
    
    keyPages.forEach(page => {
        const filePath = path.join(baseDir, page);
        if (fs.existsSync(filePath)) {
            processFile(filePath);
        }
    });
    
    console.log('\nEnglish content removal complete!');
}

// Run the script
main();