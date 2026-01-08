# 🎨 AI-Powered Image Generator

A modern, interactive web application for generating stunning AI images using Stable Diffusion models. Built with Python and Streamlit, featuring an intuitive interface with advanced image editing capabilities.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.25+-red.svg)
![PyTorch](https://img.shields.io/badge/pytorch-2.0+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

### 🎯 Core Features
- **Text-to-Image Generation**: Create images from text descriptions using Stable Diffusion models
- **Multiple Model Support**: Choose from various Stable Diffusion models (v1.4, v1.5, v2.1)
- **Style Presets**: Realistic, Artistic, Cartoon, Anime, Cyberpunk, and Fantasy styles
- **Customizable Parameters**: Control quality steps, guidance scale, image dimensions, and more
- **Negative Prompts**: Specify what you don't want in your images

### 🖼️ Image Editing & Processing
- **Image Upscaling**: Upscale images 2x or 4x with high-quality resampling
- **Photo Filters**: Adjust brightness, contrast, saturation, and sharpness
- **Crop & Resize**: Crop images with precise controls or resize with aspect ratio preservation
- **Watermark Removal**: Remove watermarks from generated images
- **Fullscreen Viewer**: Click any image to view in fullscreen lightbox mode

### 🚀 Advanced Features
- **Prompt Variations**: Auto-generate multiple prompt variations with style-aware modifiers
- **Favorites System**: Bookmark your favorite generated images
- **Image Gallery**: Browse generation history with filtering and sorting
- **Dark Mode**: Toggle between light and dark themes
- **Batch Generation**: Generate multiple images at once
- **Metadata Tracking**: All images saved with prompt and generation parameters

### 💡 User Experience
- **Prompt Templates**: Quick-start templates organized by category
- **Real-time Progress**: Visual progress indicators with time estimates
- **Character Counter**: Smart prompt length validation
- **Responsive Design**: Works on desktop and tablet devices
- **Session Persistence**: Your history and favorites persist during the session

## 📋 Prerequisites

- **Python 3.8+**
- **CUDA-capable GPU** (recommended) or CPU
- **8GB+ RAM** (16GB+ recommended)
- **5GB+ free disk space** (for models)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/AI_image_generator.git
cd AI_image_generator
```

### 2. Create Virtual Environment

**Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. (Optional) HuggingFace Authentication

For gated models (like `stabilityai/stable-diffusion-2-1`), you'll need a HuggingFace token:

1. Get your token from [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Accept the model license on the model's HuggingFace page
3. Enter the token in the app's authentication section, or set it as an environment variable:

**Windows:**
```powershell
$env:HF_TOKEN = "your_token_here"
```

**Linux/Mac:**
```bash
export HF_TOKEN="your_token_here"
```

See [AUTHENTICATION.md](AUTHENTICATION.md) for detailed authentication instructions.

## 🎮 Usage

### Starting the Application

```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`

### Basic Workflow

1. **Load a Model**: Click "🔄 Load Model" in the sidebar (first time may take a few minutes)
2. **Enter Prompt**: Describe the image you want to generate
3. **Customize Settings**: Adjust style, quality, size, and other parameters
4. **Generate**: Click "🚀 Generate Images"
5. **Edit & Download**: Use the editing tools or download your images

### Quick Tips

- **Better Prompts**: Be specific and descriptive. Include style, lighting, and composition details
- **Negative Prompts**: Use to exclude unwanted elements (e.g., "blurry, distorted, low quality")
- **Style Presets**: Choose a preset that matches your desired aesthetic
- **Quality vs Speed**: More steps = better quality but slower generation
- **GPU vs CPU**: GPU is 4-10x faster. The app auto-detects your hardware

## 📁 Project Structure

```
AI_image_generator/
│
├── app.py                 # Main Streamlit application
├── image_generator.py     # Core image generation module
├── image_processor.py     # Image editing and processing utilities
├── prompt_utils.py        # Prompt variation and enhancement tools
├── batch_generator.py     # Batch generation script
├── utils.py               # Utility functions
├── requirements.txt        # Python dependencies
├── AUTHENTICATION.md      # HuggingFace authentication guide
├── README.md              # This file
│
├── generated_images/      # Output directory for generated images
└── samples/               # Sample images (optional)
```

## 🔧 Configuration

### Supported Models

| Model | Auth Required | Quality | Best For |
|-------|--------------|---------|----------|
| `CompVis/stable-diffusion-v1-4` | ❌ No | Good | Quick testing |
| `runwayml/stable-diffusion-v1-5` | ✅ Yes | Better | General use |
| `stabilityai/stable-diffusion-2-1` | ✅ Yes | Best | High quality |
| `stabilityai/stable-diffusion-2-1-base` | ✅ Yes | Great | Balanced |

### Generation Parameters

- **Quality Steps**: 20-100 (50 recommended)
- **Guidance Scale**: 1.0-20.0 (7.5 recommended)
- **Image Sizes**: 512x512, 768x768, 1024x1024, or custom
- **Number of Images**: 1-4 per generation

## 🛠️ Advanced Features

### Prompt Variations

Click "🔄 Generate Prompt Variations" to automatically create multiple prompt variations with:
- Style-aware modifiers
- Quality enhancements
- Lighting and composition suggestions
- Mood modifiers

### Image Editing

Each generated image includes an editing panel with:
- **Upscale**: Increase resolution 2x or 4x
- **Filters**: Adjust brightness, contrast, saturation, sharpness
- **Crop**: Precise cropping with coordinate controls
- **Resize**: Resize with or without aspect ratio preservation
- **Remove Watermark**: One-click watermark removal

### Batch Generation

Use `batch_generator.py` to generate multiple images from a JSON file:

```bash
python batch_generator.py
```

Create a `prompts.json` file with your prompts (see `batch_generator.py` for format).

## 🐛 Troubleshooting

### Model Loading Issues

**Problem**: Model fails to load
- **Solution**: Check your internet connection and HuggingFace authentication
- **Alternative**: Use `CompVis/stable-diffusion-v1-4` (no auth required)

### Out of Memory Errors

**Problem**: CUDA out of memory
- **Solution**: Reduce number of images, image size, or quality steps
- **Alternative**: Use CPU mode (slower but works)

### Slow Generation

**Problem**: Images take too long to generate
- **Solution**: Use GPU if available, reduce quality steps or image size
- **Check**: Verify GPU is detected (should show "🟢 GPU" in header)

### Authentication Errors

**Problem**: 401 or authentication errors
- **Solution**: See [AUTHENTICATION.md](AUTHENTICATION.md) for detailed help
- **Quick Fix**: Use `CompVis/stable-diffusion-v1-4` model

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Output
<img width="1917" height="906" alt="Screenshot 2026-01-08 192000" src="https://github.com/user-attachments/assets/26dd3c37-bf8c-4f4c-b204-49f7fbe44f11" />

<img width="1916" height="873" alt="Screenshot 2026-01-08 194008" src="https://github.com/user-attachments/assets/91713e55-6ae2-4924-b409-9ff92dcb562d" />

<img width="1918" height="900" alt="Screenshot 2026-01-08 194100" src="https://github.com/user-attachments/assets/bfa240ff-ff30-4cbd-be56-690d33d6c99e" />

<img width="1622" height="859" alt="Screenshot 2026-01-08 194118" src="https://github.com/user-attachments/assets/99b11a6f-93c8-475f-bb2a-222477a21ef4" />




## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Stable Diffusion** models by Stability AI, CompVis, and RunwayML
- **Diffusers** library by HuggingFace
- **Streamlit** for the amazing web framework
- **PyTorch** for deep learning capabilities

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/AI_image_generator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/AI_image_generator/discussions)

## 🎯 Roadmap

- [ ] Image-to-Image (img2img) support
- [ ] Inpainting and outpainting features
- [ ] Model comparison tool
- [ ] Export/import generation presets
- [ ] User accounts and cloud storage
- [ ] API endpoints
- [ ] Mobile app support

## ⚠️ Disclaimer

This tool is for creative and educational purposes. Users are responsible for:
- Respecting copyright and intellectual property
- Not generating harmful or inappropriate content
- Using generated images ethically and legally
- Complying with model licenses and terms of service

---

**Made with ❤️ using Python, Streamlit, and Stable Diffusion**


