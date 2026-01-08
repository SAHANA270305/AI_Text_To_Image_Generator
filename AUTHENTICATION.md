# HuggingFace Authentication Guide

## Why Authentication is Needed

Some Stable Diffusion models (like `stabilityai/*` and `runwayml/*`) are **gated models** that require HuggingFace authentication to access. This is a security measure by the model creators.

## Quick Fix: Use a Non-Gated Model

**Easiest Solution:** Select `CompVis/stable-diffusion-v1-4` in the model dropdown - it works without authentication!

## Option 1: Provide Token in the App (Recommended for Gated Models)

1. **Get your HuggingFace token:**
   - Go to https://huggingface.co/settings/tokens
   - Create a new token or copy an existing one
   - Make sure you have "Read" access

2. **Accept the model license (one-time):**
   - Visit the model page (e.g., https://huggingface.co/stabilityai/stable-diffusion-2-1)
   - Click "Agree and access repository"

3. **Enter token in the app:**
   - Open the "🔑 HuggingFace Authentication" section in the sidebar
   - Paste your token
   - Load the model

## Option 2: Authenticate via Command Line

Run this command once to log in permanently:

```bash
# Install huggingface-hub if not already installed
pip install huggingface-hub

# Login interactively
huggingface-cli login
```

Enter your token when prompted. This saves it to `~/.huggingface/token`.

## Option 3: Use Environment Variable

Set your token as an environment variable:

### Windows (PowerShell):
```powershell
$env:HF_TOKEN = "your_token_here"
streamlit run app.py
```

### Windows (Command Prompt):
```cmd
set HF_TOKEN=your_token_here
streamlit run app.py
```

### Linux/Mac:
```bash
export HF_TOKEN=your_token_here
streamlit run app.py
```

### Permanent (add to your shell config):
```bash
# Add to ~/.bashrc or ~/.zshrc
export HF_TOKEN="your_token_here"
```

## Model Comparison

| Model | Authentication Required | Quality | Speed |
|-------|------------------------|---------|-------|
| `CompVis/stable-diffusion-v1-4` | ❌ No | Good | Fast |
| `runwayml/stable-diffusion-v1-5` | ✅ Yes | Better | Fast |
| `stabilityai/stable-diffusion-2-1` | ✅ Yes | Best | Moderate |
| `stabilityai/stable-diffusion-2-1-base` | ✅ Yes | Great | Fast |

## Troubleshooting

### Error: "Invalid username or password"
- Your token is incorrect or expired
- Get a new token from https://huggingface.co/settings/tokens

### Error: "401 Client Error"
- You haven't accepted the model license
- Visit the model page and click "Agree and access repository"

### Error: "Repository not found"
- Check if the model name is spelled correctly
- Ensure you have internet connectivity

## Security Note

⚠️ **Never share your HuggingFace token publicly or commit it to version control!**

The app's token input is password-protected and not stored permanently.
