# Git Setup Instructions

## Quick Setup Steps:

1. **Create a GitHub Personal Access Token:**
   - Open this link: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Name: "CLI Access" (or any name you prefer)
   - Expiration: Choose your preference (90 days is fine)
   - Scopes: Check only "repo" (Full control of private repositories)
   - Click "Generate token" at the bottom
   - **IMPORTANT: Copy the token immediately! You won't see it again.**

2. **Once you have your token copied, run this command:**
   ```bash
   git remote set-url origin https://KarinaArystan:YOUR_TOKEN_HERE@github.com/KarinaArystan/irinamonroe-website.git
   ```
   Replace `YOUR_TOKEN_HERE` with the token you just copied.

3. **Test it:**
   ```bash
   git push
   ```

## Alternative: Use macOS Keychain

If you prefer not to include the token in the URL, you can use macOS keychain:

```bash
# Reset to regular HTTPS URL
git remote set-url origin https://github.com/KarinaArystan/irinamonroe-website.git

# Next push will prompt for username/password
# Username: KarinaArystan
# Password: [paste your token here]
# macOS will save it to keychain
git push
```

## Security Note
- Personal access tokens are like passwords - keep them secret
- If you accidentally expose a token, revoke it immediately on GitHub
- The token in the remote URL is stored in your local git config