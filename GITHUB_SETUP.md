# 🚀 GitHub Setup Guide

This guide will help you push your AI Image Generator project to GitHub.

## Step 1: Create a GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the **"+"** icon in the top right → **"New repository"**
3. Fill in the details:
   - **Repository name**: `AI_image_generator` (or your preferred name)
   - **Description**: "AI-powered image generator using Stable Diffusion and Streamlit"
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
4. Click **"Create repository"**

## Step 2: Initialize Git in Your Project

Open your terminal/command prompt in the project directory and run:

```bash
# Initialize git repository
git init

# Add all files
git add .

# Make your first commit
git commit -m "Initial commit: AI Image Generator with advanced features"
```

## Step 3: Connect to GitHub

Copy the repository URL from GitHub (it will look like: `https://github.com/yourusername/AI_image_generator.git`)

Then run:

```bash
# Add GitHub as remote (replace with your actual URL)
git remote add origin https://github.com/yourusername/AI_image_generator.git

# Verify the remote was added
git remote -v
```

## Step 4: Push to GitHub

```bash
# Push to GitHub (first time)
git branch -M main
git push -u origin main
```

If prompted for credentials:
- **Username**: Your GitHub username
- **Password**: Use a Personal Access Token (not your password)
  - Go to: Settings → Developer settings → Personal access tokens → Tokens (classic)
  - Generate new token with `repo` permissions
  - Use this token as your password

## Step 5: Verify Upload

1. Refresh your GitHub repository page
2. You should see all your files uploaded
3. The README.md will automatically display on the main page

## 🔄 Making Future Updates

Whenever you make changes:

```bash
# Check what files changed
git status

# Add changed files
git add .

# Commit changes
git commit -m "Description of your changes"

# Push to GitHub
git push
```

## 📝 Common Git Commands

```bash
# Check status
git status

# See what changed
git diff

# View commit history
git log

# Create a new branch
git checkout -b feature/new-feature

# Switch branches
git checkout main

# Merge a branch
git merge feature/new-feature
```

## ⚠️ Important Notes

1. **Never commit sensitive data**: The `.gitignore` file excludes:
   - Generated images
   - Virtual environment
   - API tokens/keys
   - Cache files

2. **Update README.md**: Make sure to replace `yourusername` in the README with your actual GitHub username

3. **Add a License**: Consider adding a LICENSE file:
   - Go to GitHub → Add file → Create new file
   - Name it `LICENSE`
   - GitHub will suggest templates (MIT is common for open source)

## 🎨 Optional: Add Repository Topics

On your GitHub repository page:
1. Click the gear icon ⚙️ next to "About"
2. Add topics: `ai`, `image-generation`, `stable-diffusion`, `streamlit`, `python`, `deep-learning`

## 📸 Optional: Add Screenshots

Create a `docs/` or `images/` folder and add:
- Screenshots of your app
- Example generated images
- Update README.md to include these images

## 🐛 Troubleshooting

### Error: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/yourusername/AI_image_generator.git
```

### Error: "failed to push some refs"
```bash
git pull origin main --rebase
git push -u origin main
```

### Error: Authentication failed
- Use Personal Access Token instead of password
- Or set up SSH keys for GitHub

---

**That's it! Your project is now on GitHub! 🎉**

