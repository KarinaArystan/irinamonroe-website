#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

// Function to remove social media bar from HTML content
function removeSocialBar(htmlContent) {
    const dom = new JSDOM(htmlContent);
    const document = dom.window.document;
    
    // Find and remove all social-bar divs
    const socialBars = document.querySelectorAll('.social-bar');
    socialBars.forEach(bar => {
        bar.remove();
    });
    
    // Return the modified HTML
    return dom.serialize();
}

// Function to process a single HTML file
function processFile(filePath) {
    try {
        const content = fs.readFileSync(filePath, 'utf8');
        const modifiedContent = removeSocialBar(content);
        
        if (content !== modifiedContent) {
            fs.writeFileSync(filePath, modifiedContent, 'utf8');
            console.log(`✓ Removed social bar from: ${filePath}`);
            return true;
        }
        return false;
    } catch (error) {
        console.error(`Error processing ${filePath}:`, error.message);
        return false;
    }
}

// Function to recursively find all HTML files
function findHtmlFiles(dir, fileList = []) {
    const files = fs.readdirSync(dir);
    
    files.forEach(file => {
        const filePath = path.join(dir, file);
        const stat = fs.statSync(filePath);
        
        if (stat.isDirectory() && !file.startsWith('.') && file !== 'node_modules') {
            findHtmlFiles(filePath, fileList);
        } else if (file.endsWith('.html')) {
            fileList.push(filePath);
        }
    });
    
    return fileList;
}

// Main function
function main() {
    console.log('Removing social media bars from all HTML files...\n');
    
    const htmlFiles = findHtmlFiles(__dirname);
    let modifiedCount = 0;
    
    htmlFiles.forEach(file => {
        if (processFile(file)) {
            modifiedCount++;
        }
    });
    
    console.log(`\nProcessed ${htmlFiles.length} HTML files`);
    console.log(`Modified ${modifiedCount} files`);
}

// Run the script
main();