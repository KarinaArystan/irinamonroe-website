#!/usr/bin/env python3
"""
Fix absolute paths for GitHub Pages deployment
Converts absolute paths to work with GitHub Pages subdirectory structure
"""

import os
import re
from pathlib import Path
import shutil
from datetime import datetime

class GitHubPagesLinkFixer:
    def __init__(self, root_dir, repo_name="irinamonroe-website"):
        self.root_dir = root_dir
        self.repo_name = repo_name
        self.backup_dir = os.path.join(root_dir, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        self.changes_made = []
        
    def create_backup(self):
        """Create a backup of all HTML files before making changes"""
        print("Creating backup...")
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
            
        html_files = []
        for root, dirs, files in os.walk(self.root_dir):
            # Skip certain directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'tools', 'backup_']]
            
            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, self.root_dir)
                    html_files.append(rel_path)
                    
                    # Create backup
                    backup_path = os.path.join(self.backup_dir, rel_path)
                    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
                    shutil.copy2(file_path, backup_path)
        
        print(f"Backed up {len(html_files)} HTML files to {self.backup_dir}")
        return html_files
    
    def fix_paths_method1_relative(self, file_path):
        """Method 1: Convert to relative paths"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Calculate relative depth
            rel_path = os.path.relpath(file_path, self.root_dir)
            depth = rel_path.count(os.sep)
            prefix = "../" * depth if depth > 0 else ""
            
            original_content = content
            changes = []
            
            # Fix href attributes
            def replace_href(match):
                full_match = match.group(0)
                path = match.group(1)
                
                # Skip external URLs and anchors
                if path.startswith(('http://', 'https://', '//', '#', 'mailto:', 'tel:')):
                    return full_match
                
                # Handle root specifically
                if path == '/':
                    new_path = f'{prefix}index.html' if prefix else 'index.html'
                else:
                    new_path = f'{prefix}{path[1:]}'  # Remove leading /
                
                changes.append(f"  {full_match} → href=\"{new_path}\"")
                return f'href="{new_path}"'
            
            # Fix action attributes (for forms)
            def replace_action(match):
                full_match = match.group(0)
                path = match.group(1)
                
                if path.startswith('/'):
                    new_path = f'{prefix}{path[1:]}'
                    changes.append(f"  {full_match} → action=\"{new_path}\"")
                    return f'action="{new_path}"'
                
                return full_match
            
            # Apply replacements
            content = re.sub(r'href="(/[^"]*)"', replace_href, content)
            content = re.sub(r'action="(/[^"]*)"', replace_action, content)
            
            # Write back if changes were made
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                if changes:
                    self.changes_made.append({
                        'file': rel_path,
                        'changes': changes
                    })
                return True
            
            return False
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return False
    
    def fix_paths_method2_base_path(self, file_path):
        """Method 2: Add base path prefix (Alternative approach)"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            base_path = f"/{self.repo_name}"
            
            # Add base path to all absolute URLs
            content = re.sub(
                r'href="(/(?!/))',
                f'href="{base_path}\\1',
                content
            )
            content = re.sub(
                r'action="(/(?!/))',
                f'action="{base_path}\\1',
                content
            )
            
            # Fix root links
            content = content.replace('href="/"', f'href="{base_path}/"')
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True
            
            return False
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return False
    
    def fix_all_files(self, method='relative'):
        """Fix all HTML files using specified method"""
        html_files = self.create_backup()
        fixed_count = 0
        
        print(f"\nFixing links using {method} method...")
        
        for rel_path in html_files:
            file_path = os.path.join(self.root_dir, rel_path)
            
            if method == 'relative':
                if self.fix_paths_method1_relative(file_path):
                    fixed_count += 1
            elif method == 'base_path':
                if self.fix_paths_method2_base_path(file_path):
                    fixed_count += 1
        
        print(f"\nFixed {fixed_count} out of {len(html_files)} HTML files")
        
        # Save change log
        if self.changes_made:
            log_file = os.path.join(self.root_dir, 'link_changes.log')
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write(f"Link changes made on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Method: {method}\n\n")
                
                for item in self.changes_made:
                    f.write(f"\nFile: {item['file']}\n")
                    for change in item['changes']:
                        f.write(f"{change}\n")
            
            print(f"\nChange log saved to: link_changes.log")
        
        return fixed_count
    
    def restore_backup(self):
        """Restore files from backup"""
        if not os.path.exists(self.backup_dir):
            print("No backup found!")
            return
        
        print(f"Restoring from backup: {self.backup_dir}")
        
        for root, dirs, files in os.walk(self.backup_dir):
            for file in files:
                if file.endswith('.html'):
                    backup_file = os.path.join(root, file)
                    rel_path = os.path.relpath(backup_file, self.backup_dir)
                    original_file = os.path.join(self.root_dir, rel_path)
                    
                    shutil.copy2(backup_file, original_file)
        
        print("Restore complete!")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("GitHub Pages Link Fixer")
    print("=" * 50)
    print(f"Working directory: {script_dir}")
    print("\nThis tool will fix broken links for GitHub Pages deployment.")
    print("\nChoose a method:")
    print("1. Convert to relative paths (Recommended)")
    print("2. Add repository base path")
    print("3. Restore from backup")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ")
    
    fixer = GitHubPagesLinkFixer(script_dir)
    
    if choice == '1':
        confirm = input("\nThis will convert all absolute paths to relative paths. Continue? (y/n): ")
        if confirm.lower() == 'y':
            fixer.fix_all_files(method='relative')
            print("\n✅ Done! Now commit and push the changes to GitHub.")
            print("\nTo commit and push:")
            print("git add -A")
            print('git commit -m "Fix links for GitHub Pages deployment"')
            print("git push")
    
    elif choice == '2':
        confirm = input("\nThis will add repository base path to all links. Continue? (y/n): ")
        if confirm.lower() == 'y':
            fixer.fix_all_files(method='base_path')
            print("\n✅ Done! Now commit and push the changes to GitHub.")
    
    elif choice == '3':
        fixer.restore_backup()
    
    else:
        print("Exiting...")

if __name__ == "__main__":
    main()