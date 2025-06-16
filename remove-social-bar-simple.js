#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Function to remove social media bar from HTML content using regex
function removeSocialBar(htmlContent) {
    // Pattern to match the entire social-bar div
    const socialBarPattern = /<!-- Social Media Bar -->[\s\S]*?<div class="social-bar">[\s\S]*?<\/div>[\s\S]*?<\/div>[\s\n]*(?=<!-- Header -->|<header>)/g;
    
    // Remove the social bar
    let modifiedContent = htmlContent.replace(socialBarPattern, '');
    
    // Also try a simpler pattern if the first one doesn't match
    if (modifiedContent === htmlContent) {
        const simpleSocialBarPattern = /<div class="social-bar">[\s\S]*?<\/div>\s*<\/div>/g;
        modifiedContent = htmlContent.replace(simpleSocialBarPattern, '');
    }
    
    return modifiedContent;
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