#!/bin/bash

echo "Git Authentication Setup"
echo "======================="
echo ""
echo "This script will help you set up GitHub authentication."
echo ""
echo "First, you need to create a Personal Access Token on GitHub:"
echo "1. Go to: https://github.com/settings/tokens"
echo "2. Click 'Generate new token (classic)'"
echo "3. Name it something like 'CLI Access'"
echo "4. Select the 'repo' scope (full control of private repositories)"
echo "5. Generate the token and copy it"
echo ""
read -p "Have you created and copied your token? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo ""
    read -p "Enter your GitHub username: " username
    read -s -p "Enter your Personal Access Token: " token
    echo ""
    
    # Update the remote URL with authentication
    git remote set-url origin https://${username}:${token}@github.com/${username}/irinamonroe-website.git
    
    echo ""
    echo "✅ Git authentication configured!"
    echo ""
    echo "Testing connection..."
    git ls-remote > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        echo "✅ Connection successful! You can now push to GitHub."
        echo ""
        echo "Try running: git push"
    else
        echo "❌ Connection failed. Please check your token and try again."
    fi
else
    echo "Please create a token first, then run this script again."
fi