# 🚀 Quick Start: Push to GitHub

## Step-by-Step Commands

### 1. Initialize Git (if not already done)

```powershell
cd "C:\Users\sanat\OneDrive\Desktop\sahana\AI_image_generator"
git init
```

### 2. Add All Files

```powershell
git add .
```

### 3. Make First Commit

```powershell
git commit -m "Initial commit: AI Image Generator with advanced features"
```

### 4. Create GitHub Repository First

**Before running the next commands:**
1. Go to https://github.com/new
2. Create a new repository (don't initialize with README)
3. Copy the repository URL (e.g., `https://github.com/YOUR_USERNAME/AI_image_generator.git`)

### 5. Connect to GitHub

**Replace `YOUR_USERNAME` with your actual GitHub username:**

```powershell
git remote add origin https://github.com/YOUR_USERNAME/AI_image_generator.git
```

### 6. Push to GitHub

```powershell
git branch -M main
git push -u origin main
```

**Note:** You'll be prompted for credentials:
- **Username**: Your GitHub username
- **Password**: Use a Personal Access Token (not your password)
  - Get token: https://github.com/settings/tokens
  - Create token with `repo` permissions

## ✅ Verify

1. Go to your GitHub repository page
2. You should see all files uploaded
3. README.md will display automatically

## 🔄 Future Updates

```powershell
git add .
git commit -m "Your commit message"
git push
```

## ⚠️ Important

**Before pushing, update README.md:**
- Replace `yourusername` with your actual GitHub username (line 19 and other places)
- Update the repository URL in the README

---

**That's it! Your project is on GitHub! 🎉**

