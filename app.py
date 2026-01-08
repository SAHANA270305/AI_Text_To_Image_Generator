"""
AI Image Generator - Enhanced Streamlit Web Interface
Modern, interactive interface for text-to-image generation
"""

import streamlit as st
from image_generator import ImageGenerator
from image_processor import ImageProcessor
from prompt_utils import PromptVariator
import torch
from PIL import Image
import time
import os
import json
from datetime import datetime
from io import BytesIO
import base64

# Page configuration
st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    /* Main styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Header styling */
    h1 {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    
    /* Card styling */
    .prompt-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: transform 0.2s;
    }
    
    .prompt-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Button enhancements */
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Image container */
    .image-container {
        position: relative;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        transition: transform 0.3s;
        margin-bottom: 1rem;
    }
    
    .image-container:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 30px rgba(0,0,0,0.2);
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    
    .status-success {
        background-color: #10b981;
        color: white;
    }
    
    .status-warning {
        background-color: #f59e0b;
        color: white;
    }
    
    .status-info {
        background-color: #3b82f6;
        color: white;
    }
    
    /* Prompt template buttons */
    .template-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        cursor: pointer;
        font-size: 0.9rem;
        margin: 0.25rem;
        transition: all 0.2s;
    }
    
    .template-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Character counter */
    .char-counter {
        text-align: right;
        color: #6b7280;
        font-size: 0.85rem;
        margin-top: -0.5rem;
    }
    
    /* Metadata display */
    .metadata-box {
        background: #f3f4f6;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 0.5rem;
        font-size: 0.85rem;
    }
    
    /* Animation for loading */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .loading-animation {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    
    /* Dark mode styles */
    [data-theme="dark"] {
        background-color: #1e1e1e;
        color: #e0e0e0;
    }
    
    [data-theme="dark"] .main {
        background-color: #1e1e1e;
    }
    
    [data-theme="dark"] .metadata-box {
        background: #2d2d2d;
        color: #e0e0e0;
    }
    
    /* Lightbox/Modal styles */
    .lightbox {
        display: none;
        position: fixed;
        z-index: 9999;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0,0,0,0.9);
        overflow: auto;
    }
    
    .lightbox-content {
        margin: auto;
        display: block;
        max-width: 90%;
        max-height: 90%;
        margin-top: 5%;
    }
    
    .lightbox-close {
        position: absolute;
        top: 15px;
        right: 35px;
        color: #f1f1f1;
        font-size: 40px;
        font-weight: bold;
        cursor: pointer;
    }
    
    .lightbox-close:hover {
        color: #bbb;
    }
    
    /* Favorite button */
    .favorite-btn {
        background: transparent;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
        transition: transform 0.2s;
    }
    
    .favorite-btn:hover {
        transform: scale(1.2);
    }
    
    .favorite-active {
        color: #ff6b6b;
    }
    
    .favorite-inactive {
        color: #ccc;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generator' not in st.session_state:
    st.session_state.generator = None
if 'generated_images' not in st.session_state:
    st.session_state.generated_images = []
if 'image_history' not in st.session_state:
    st.session_state.image_history = []
if 'current_prompt' not in st.session_state:
    st.session_state.current_prompt = ""
if 'current_negative_prompt' not in st.session_state:
    st.session_state.current_negative_prompt = ""
if 'favorites' not in st.session_state:
    st.session_state.favorites = []
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'selected_image' not in st.session_state:
    st.session_state.selected_image = None
if 'viewer_open' not in st.session_state:
    st.session_state.viewer_open = False
if 'processor' not in st.session_state:
    st.session_state.processor = ImageProcessor()

# Prompt templates
PROMPT_TEMPLATES = {
    "Realistic": [
        "A golden retriever puppy playing in a flower field, professional photography, natural lighting",
        "Modern minimalist living room with large windows, natural lighting, cozy atmosphere",
        "Majestic lion in a savanna at sunset, photorealistic, detailed fur, golden hour"
    ],
    "Artistic": [
        "Portrait of a cat in the style of Van Gogh's Starry Night, vibrant colors, artistic",
        "Abstract representation of human emotions, vibrant colors, flowing forms",
        "Surreal landscape with floating islands and waterfalls, dreamlike atmosphere"
    ],
    "Fantasy": [
        "A floating castle in the clouds with waterfalls, magical atmosphere, epic fantasy art",
        "Dragon flying over a medieval city at dusk, epic fantasy art, detailed scales",
        "Enchanted forest with glowing mushrooms and fairy lights, mystical atmosphere"
    ],
    "Cyberpunk": [
        "Neon-lit street in Tokyo at night, rain reflections, cyberpunk aesthetic, futuristic",
        "Futuristic robot bartender in a high-tech bar, neon lights, cyberpunk style",
        "Flying car in a futuristic cityscape, neon signs, cyberpunk atmosphere"
    ],
    "Anime": [
        "Anime style character with colorful hair, detailed eyes, vibrant background",
        "Magical girl transformation scene, anime style, sparkles and effects",
        "Anime style landscape with cherry blossoms, peaceful atmosphere"
    ]
}

# App header with dark mode toggle
col_header1, col_header2, col_header3, col_header4 = st.columns([2, 1, 1, 1])
with col_header1:
    st.title("🎨 AI-Powered Image Generator")
    st.markdown("""
    <div style='color: #6b7280; margin-bottom: 2rem;'>
        Transform your imagination into stunning visuals using Stable Diffusion AI
    </div>
    """, unsafe_allow_html=True)

with col_header2:
    if st.session_state.generator is not None:
        st.markdown('<div class="status-badge status-success">Model Ready</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-badge status-warning">Model Not Loaded</div>', unsafe_allow_html=True)

with col_header3:
    device_status = "🟢 GPU" if torch.cuda.is_available() else "🟡 CPU"
    st.markdown(f'<div class="status-badge status-info">{device_status}</div>', unsafe_allow_html=True)

with col_header4:
    dark_mode_label = "🌙 Dark" if not st.session_state.dark_mode else "☀️ Light"
    if st.button(dark_mode_label, key="dark_mode_toggle"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Model status indicator
    if st.session_state.generator is not None:
        st.success("✅ Model Loaded")
        st.caption(f"Model: {st.session_state.generator.model_id}")
    else:
        st.warning("⚠️ Model Not Loaded")
    
    st.divider()
    
    # HuggingFace Token
    with st.expander("🔑 Authentication", expanded=False):
        hf_token = st.text_input(
            "HuggingFace Token",
            type="password",
            help="Required for gated models. Get your token from https://huggingface.co/settings/tokens"
        )
        st.caption("💡 Leave empty if token is set in environment")
    
    # Model selection
    model_choice = st.selectbox(
        "🤖 Select Model",
        [
            "CompVis/stable-diffusion-v1-4",
            "runwayml/stable-diffusion-v1-5",
            "stabilityai/stable-diffusion-2-1",
            "stabilityai/stable-diffusion-2-1-base"
        ],
        help="Choose the Stable Diffusion model"
    )
    
    # Authentication status
    requires_auth = model_choice.startswith("stabilityai/") or model_choice.startswith("runwayml/")
    if requires_auth:
        if hf_token or os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN"):
            st.success("✅ Auth available")
        else:
            st.warning("⚠️ Token required")
    
    # Load model button
    load_col1, load_col2 = st.columns([2, 1])
    with load_col1:
        if st.button("🔄 Load Model", use_container_width=True, type="primary"):
            with st.spinner("Loading model... This may take a few minutes."):
                try:
                    st.session_state.generator = ImageGenerator(
                        model_id=model_choice,
                        device="cuda" if torch.cuda.is_available() else "cpu",
                        hf_token=hf_token if hf_token else None
                    )
                    st.success("✅ Model loaded!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")
    
    with load_col2:
        if st.button("🔄", help="Reload page"):
            st.rerun()
    
    st.divider()
    
    # Generation parameters
    st.header("🎛️ Generation Settings")
    
    num_images = st.slider(
        "Number of Images", 
        1, 4, 1, 
        help="How many images to generate"
    )
    
    style = st.selectbox(
        "🎨 Style Preset",
        ["realistic", "artistic", "cartoon", "anime", "cyberpunk", "fantasy"],
        help="Predefined style enhancements"
    )
    
    num_steps = st.slider(
        "Quality Steps",
        20, 100, 50,
        help="More steps = better quality but slower"
    )
    
    guidance_scale = st.slider(
        "Guidance Scale",
        1.0, 20.0, 7.5, 0.5,
        help="How closely to follow the prompt"
    )
    
    # Image dimensions with presets
    st.subheader("📐 Image Size")
    size_preset = st.radio(
        "Preset",
        ["Square (512x512)", "Portrait (512x768)", "Landscape (768x512)", "Large (1024x1024)", "Custom"],
        horizontal=True,
        help="Quick size presets"
    )
    
    if size_preset == "Square (512x512)":
        width, height = 512, 512
    elif size_preset == "Portrait (512x768)":
        width, height = 512, 768
    elif size_preset == "Landscape (768x512)":
        width, height = 768, 512
    elif size_preset == "Large (1024x1024)":
        width, height = 1024, 1024
    else:
        col1, col2 = st.columns(2)
        with col1:
            width = st.selectbox("Width", [512, 768, 1024], index=0)
        with col2:
            height = st.selectbox("Height", [512, 768, 1024], index=0)
    
    # Advanced settings
    with st.expander("🔧 Advanced Settings"):
        use_seed = st.checkbox("Use Fixed Seed", help="For reproducible results")
        seed = st.number_input("Seed", 0, 999999, 42, disabled=not use_seed)
        add_watermark = st.checkbox("Add Watermark", value=True)
    
    st.divider()
    
    # History
    if st.session_state.image_history:
        with st.expander(f"📚 History ({len(st.session_state.image_history)} items)"):
            for idx, item in enumerate(reversed(st.session_state.image_history[-10:])):  # Show last 10
                if st.button(f"📷 {item['prompt'][:50]}...", key=f"hist_{idx}", use_container_width=True):
                    st.session_state.current_prompt = item['prompt']
                    st.session_state.current_negative_prompt = item.get('negative_prompt', '')
                    st.rerun()
    
    st.divider()
    
    # Responsible AI
    with st.expander("📋 Responsible AI"):
        st.markdown("""
        **Guidelines:**
        - Use for creative purposes
        - Respect copyright
        - Avoid harmful content
        - Images are watermarked
        """)

# Main content area
tab1, tab2, tab3 = st.tabs(["🎨 Generate", "📸 Gallery", "⭐ Favorites"])

with tab1:
    # Prompt input section
    st.header("📝 Create Your Image")
    
    # Prompt templates
    st.subheader("💡 Quick Templates")
    template_category = st.selectbox("Category", list(PROMPT_TEMPLATES.keys()), key="template_cat")
    
    template_cols = st.columns(3)
    for idx, template in enumerate(PROMPT_TEMPLATES[template_category]):
        with template_cols[idx % 3]:
            if st.button(f"📌 {template[:40]}...", key=f"template_{idx}", use_container_width=True):
                st.session_state.current_prompt = template
                st.rerun()
    
    st.divider()
    
    # Prompt variations section
    if st.session_state.current_prompt:
        with st.expander("🔄 Generate Prompt Variations", expanded=False):
            var_col1, var_col2 = st.columns([3, 1])
            with var_col1:
                num_variations = st.slider("Number of variations", 3, 10, 5)
            with var_col2:
                if st.button("Generate", key="gen_variations"):
                    variations = PromptVariator.generate_variations(
                        st.session_state.current_prompt, 
                        num_variations=num_variations,
                        style=style
                    )
                    st.session_state.prompt_variations = variations
            
            if 'prompt_variations' in st.session_state:
                st.write("**Variations:**")
                for idx, var in enumerate(st.session_state.prompt_variations):
                    var_col1, var_col2 = st.columns([4, 1])
                    with var_col1:
                        st.text_area("", value=var, height=50, key=f"var_text_{idx}", disabled=True)
                    with var_col2:
                        if st.button("Use", key=f"use_var_{idx}"):
                            st.session_state.current_prompt = var
                            st.rerun()
    
    st.divider()
    
    # Main prompt input
    col_input1, col_input2 = st.columns([2, 1])
    
    with col_input1:
        prompt = st.text_area(
            "✨ Describe your image",
            value=st.session_state.current_prompt,
            placeholder="e.g., A majestic lion in a savanna at sunset, photorealistic",
            height=120,
            help="Be specific and descriptive for best results",
            key="main_prompt"
        )
        
        # Character counter
        char_count = len(prompt)
        char_color = "#10b981" if 20 <= char_count <= 200 else "#f59e0b" if char_count > 200 else "#ef4444"
        st.markdown(f'<div class="char-counter">Characters: <span style="color: {char_color}">{char_count}</span></div>', unsafe_allow_html=True)
    
    with col_input2:
        negative_prompt = st.text_area(
            "🚫 Negative Prompt",
            value=st.session_state.current_negative_prompt,
            placeholder="e.g., blurry, distorted, low quality",
            height=120,
            help="Describe what you DON'T want"
        )
        
        # Quick negative prompts
        st.caption("Quick options:")
        neg_cols = st.columns(3)
        quick_negatives = ["blurry", "distorted", "low quality"]
        for idx, neg in enumerate(quick_negatives):
            with neg_cols[idx]:
                if st.button(neg, key=f"neg_{idx}"):
                    if negative_prompt:
                        negative_prompt = f"{negative_prompt}, {neg}"
                    else:
                        negative_prompt = neg
                    st.session_state.current_negative_prompt = negative_prompt
                    st.rerun()
    
    # Generate button with status
    generate_col1, generate_col2, generate_col3 = st.columns([1, 2, 1])
    with generate_col2:
        generate_btn = st.button(
            "🚀 Generate Images", 
            type="primary", 
            use_container_width=True,
            disabled=st.session_state.generator is None
        )
        
        if st.session_state.generator is None:
            st.caption("⚠️ Please load the model first")
    
    # Generation process
    if generate_btn and st.session_state.generator is not None:
        if not prompt.strip():
            st.error("❌ Please enter a prompt!")
        else:
            # Content filtering
            inappropriate_keywords = ["nude", "nsfw", "explicit", "gore", "violence"]
            if any(keyword in prompt.lower() for keyword in inappropriate_keywords):
                st.error("❌ Inappropriate content detected. Please modify your prompt.")
            else:
                # Enhanced progress tracking
                progress_container = st.container()
                with progress_container:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    time_elapsed = st.empty()
                    
                    try:
                        # Initialize
                        status_text.markdown("### 🔄 Initializing generation...")
                        progress_bar.progress(5)
                        time.sleep(0.1)
                        
                        # Estimate time
                        est_time = num_steps * num_images * (0.5 if torch.cuda.is_available() else 2)
                        status_text.markdown(f"### ⏳ Generating... Estimated time: {est_time:.0f}s")
                        progress_bar.progress(15)
                        
                        start_time = time.time()
                        
                        # Simulate progress updates
                        def update_progress(step, total):
                            progress = 15 + int((step / total) * 70)
                            progress_bar.progress(min(progress, 85))
                            elapsed = time.time() - start_time
                            time_elapsed.markdown(f"⏱️ Elapsed: {elapsed:.1f}s")
                        
                        # Generate images
                        images = st.session_state.generator.generate_images(
                            prompt=prompt,
                            negative_prompt=negative_prompt,
                            num_images=num_images,
                            style=style,
                            num_inference_steps=num_steps,
                            guidance_scale=guidance_scale,
                            height=height,
                            width=width,
                            seed=seed
                        )
                        
                        progress_bar.progress(90)
                        status_text.markdown("### 💾 Saving images...")
                        
                        # Save images
                        saved_paths = st.session_state.generator.save_images(
                            images,
                            prompt,
                            add_watermark=add_watermark
                        )
                        
                        progress_bar.progress(100)
                        
                        # Calculate time
                        elapsed_time = time.time() - start_time
                        status_text.markdown(f"### ✅ Complete! Generated in {elapsed_time:.1f}s")
                        time_elapsed.empty()
                        
                        # Store in session state
                        st.session_state.generated_images = list(zip(images, saved_paths))
                        
                        # Add to history
                        history_item = {
                            'prompt': prompt,
                            'negative_prompt': negative_prompt,
                            'images': saved_paths,
                            'timestamp': datetime.now().isoformat(),
                            'style': style,
                            'num_steps': num_steps,
                            'guidance_scale': guidance_scale,
                            'width': width,
                            'height': height
                        }
                        st.session_state.image_history.append(history_item)
                        
                        # Success notification
                        st.balloons()
                        st.success(f"🎉 Generated {len(images)} image(s) successfully!")
                        
                        # Clear progress after a moment
                        time.sleep(2)
                        progress_bar.empty()
                        status_text.empty()
                        time_elapsed.empty()
                        
                    except Exception as e:
                        progress_bar.empty()
                        status_text.empty()
                        time_elapsed.empty()
                        st.error(f"❌ Error during generation: {e}")
                        st.info("💡 Try: (1) Reducing number of images, (2) Using fewer steps, or (3) Checking your GPU memory")

with tab2:
    st.header("📸 Image Gallery")
    
    if not st.session_state.image_history:
        st.info("👈 Generate some images first to see them here!")
    else:
        # Filter options
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        with filter_col1:
            filter_style = st.selectbox("Filter by Style", ["All"] + list(set([h.get('style', 'unknown') for h in st.session_state.image_history])))
        with filter_col2:
            sort_by = st.selectbox("Sort by", ["Newest First", "Oldest First"])
        with filter_col3:
            if st.button("🗑️ Clear History"):
                st.session_state.image_history = []
                st.session_state.generated_images = []
                st.rerun()
        
        # Filter history
        filtered_history = st.session_state.image_history
        if filter_style != "All":
            filtered_history = [h for h in filtered_history if h.get('style') == filter_style]
        
        if sort_by == "Oldest First":
            filtered_history = list(reversed(filtered_history))
        
        # Display gallery
        for idx, item in enumerate(filtered_history):
            with st.expander(f"📷 {item['prompt'][:60]}... | {item.get('timestamp', '')[:10]}", expanded=(idx == 0)):
                # Load images
                images_to_show = []
                for img_path in item.get('images', []):
                    if os.path.exists(img_path):
                        images_to_show.append(Image.open(img_path))
                
                if images_to_show:
                    # Display images in grid
                    cols = st.columns(min(len(images_to_show), 3))
                    for img_idx, image in enumerate(images_to_show):
                        with cols[img_idx % len(cols)]:
                            st.image(image, use_container_width=True)
                            
                            # Download button
                            with open(item['images'][img_idx], "rb") as file:
                                st.download_button(
                                    label=f"⬇️ Download",
                                    data=file,
                                    file_name=os.path.basename(item['images'][img_idx]),
                                    mime="image/png",
                                    key=f"dl_{idx}_{img_idx}"
                                )
                    
                    # Metadata
                    with st.container():
                        st.markdown('<div class="metadata-box">', unsafe_allow_html=True)
                        col_meta1, col_meta2 = st.columns(2)
                        with col_meta1:
                            st.caption(f"**Prompt:** {item['prompt']}")
                            if item.get('negative_prompt'):
                                st.caption(f"**Negative:** {item['negative_prompt']}")
                        with col_meta2:
                            st.caption(f"**Style:** {item.get('style', 'N/A')}")
                            st.caption(f"**Steps:** {item.get('num_steps', 'N/A')} | **Guidance:** {item.get('guidance_scale', 'N/A')}")
                            st.caption(f"**Size:** {item.get('width', 'N/A')}x{item.get('height', 'N/A')}")
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Action buttons
                        action_col1, action_col2, action_col3 = st.columns(3)
                        with action_col1:
                            # Favorite button
                            fav_icon = "❤️" if is_favorited(item['images'][0]) else "🤍"
                            if st.button(fav_icon, key=f"fav_gallery_{idx}", use_container_width=True):
                                toggle_favorite(item['images'][0], item['prompt'], item)
                                st.rerun()
                        with action_col2:
                            # Regenerate button
                            if st.button(f"🔄 Regenerate", key=f"regen_{idx}", use_container_width=True):
                                st.session_state.current_prompt = item['prompt']
                                st.session_state.current_negative_prompt = item.get('negative_prompt', '')
                                st.info("💡 Switch to 'Generate' tab to regenerate with these settings")
                                st.rerun()
                        with action_col3:
                            # View button
                            if st.button("👁️ View", key=f"view_{idx}", use_container_width=True):
                                st.session_state.selected_image = item['images'][0]
                                st.session_state.viewer_open = True
                                st.rerun()

with tab3:
    st.header("⭐ Favorites")
    
    if not st.session_state.favorites:
        st.info("🌟 No favorites yet! Click the ❤️ button on any image to add it to favorites.")
    else:
        # Clear favorites button
        if st.button("🗑️ Clear All Favorites"):
            st.session_state.favorites = []
            st.rerun()
        
        st.write(f"**{len(st.session_state.favorites)} favorite(s)**")
        
        # Display favorites
        fav_cols = st.columns(min(len(st.session_state.favorites), 3))
        for idx, fav in enumerate(st.session_state.favorites):
            with fav_cols[idx % len(fav_cols)]:
                if os.path.exists(fav['path']):
                    fav_image = Image.open(fav['path'])
                    st.image(fav_image, use_container_width=True)
                    
                    # Favorite info
                    st.caption(f"**Prompt:** {fav.get('prompt', 'N/A')[:50]}...")
                    st.caption(f"**Date:** {fav.get('timestamp', '')[:10]}")
                    
                    # Actions
                    fav_action_col1, fav_action_col2 = st.columns(2)
                    with fav_action_col1:
                        with open(fav['path'], "rb") as file:
                            st.download_button("⬇️", data=file, file_name=os.path.basename(fav['path']), 
                                            mime="image/png", use_container_width=True, key=f"fav_dl_{idx}")
                    with fav_action_col2:
                        if st.button("❌ Remove", key=f"remove_fav_{idx}", use_container_width=True):
                            toggle_favorite(fav['path'], "")
                            st.rerun()
                else:
                    st.warning("Image file not found")
                    if st.button("Remove", key=f"remove_missing_{idx}"):
                        st.session_state.favorites = [f for f in st.session_state.favorites if f != fav]
                        st.rerun()

# Helper function to check if image is favorited
def is_favorited(image_path):
    return any(fav.get('path') == image_path for fav in st.session_state.favorites)

def toggle_favorite(image_path, prompt, metadata=None):
    if is_favorited(image_path):
        st.session_state.favorites = [f for f in st.session_state.favorites if f.get('path') != image_path]
    else:
        fav_item = {'path': image_path, 'prompt': prompt, 'timestamp': datetime.now().isoformat()}
        if metadata:
            fav_item.update(metadata)
        st.session_state.favorites.append(fav_item)

# Display current generated images with editing features
if st.session_state.generated_images:
    st.divider()
    st.header("✨ Latest Results")
    
    # Display images in grid with enhanced styling
    num_cols = min(len(st.session_state.generated_images), 3)
    cols = st.columns(num_cols)
    
    for idx, (image, path) in enumerate(st.session_state.generated_images):
        with cols[idx % num_cols]:
            # Image display with viewer
            image_key = f"img_{idx}"
            img_base64 = ImageProcessor.image_to_base64(image)
            
            # Clickable image for lightbox
            st.markdown(f'''
            <div class="image-container" onclick="openLightbox('{image_key}')" style="cursor: pointer;">
                <img src="data:image/png;base64,{img_base64}" style="width: 100%; border-radius: 15px;" />
            </div>
            ''', unsafe_allow_html=True)
            
            # Lightbox HTML (will be shown when clicked)
            st.markdown(f'''
            <div id="lightbox_{image_key}" class="lightbox" onclick="closeLightbox('{image_key}')">
                <span class="lightbox-close">&times;</span>
                <img class="lightbox-content" src="data:image/png;base64,{img_base64}" onclick="event.stopPropagation()" />
            </div>
            <script>
            function openLightbox(key) {{
                document.getElementById('lightbox_' + key).style.display = 'block';
            }}
            function closeLightbox(key) {{
                document.getElementById('lightbox_' + key).style.display = 'none';
            }}
            </script>
            ''', unsafe_allow_html=True)
            
            # Action buttons row 1
            action_col1, action_col2, action_col3 = st.columns(3)
            with action_col1:
                # Favorite button
                fav_icon = "❤️" if is_favorited(path) else "🤍"
                if st.button(fav_icon, key=f"fav_{idx}", use_container_width=True):
                    # Get prompt from history if available
                    prompt_text = "Generated image"
                    for hist_item in st.session_state.image_history:
                        if path in hist_item.get('images', []):
                            prompt_text = hist_item.get('prompt', 'Generated image')
                            break
                    toggle_favorite(path, prompt_text)
                    st.rerun()
            with action_col2:
                with open(path, "rb") as file:
                    st.download_button(
                        label="⬇️",
                        data=file,
                        file_name=os.path.basename(path),
                        mime="image/png",
                        use_container_width=True,
                        key=f"download_{idx}"
                    )
            with action_col3:
                if st.button("🔄", key=f"regenerate_{idx}", use_container_width=True, help="Regenerate"):
                    # Get prompt from history
                    for hist_item in st.session_state.image_history:
                        if path in hist_item.get('images', []):
                            st.session_state.current_prompt = hist_item.get('prompt', '')
                            st.session_state.current_negative_prompt = hist_item.get('negative_prompt', '')
                            break
                    st.rerun()
            
            # Image editing section
            with st.expander(f"🛠️ Edit Image {idx + 1}", expanded=False):
                edit_tab1, edit_tab2, edit_tab3, edit_tab4 = st.tabs(["Upscale", "Filters", "Crop/Resize", "Other"])
                
                current_image = image.copy()
                
                with edit_tab1:
                    st.subheader("🔍 Upscale Image")
                    upscale_factor = st.radio("Scale Factor", [2, 4], horizontal=True)
                    if st.button("Upscale", key=f"upscale_{idx}"):
                        upscaled = st.session_state.processor.upscale_image(current_image, upscale_factor)
                        st.image(upscaled, use_container_width=True)
                        # Save upscaled
                        upscaled_path = path.replace(".png", f"_upscaled_{upscale_factor}x.png")
                        upscaled.save(upscaled_path)
                        with open(upscaled_path, "rb") as f:
                            st.download_button("Download Upscaled", f, file_name=os.path.basename(upscaled_path), mime="image/png")
                
                with edit_tab2:
                    st.subheader("🎨 Apply Filters")
                    brightness = st.slider("Brightness", 0.0, 2.0, 1.0, 0.1, key=f"bright_{idx}")
                    contrast = st.slider("Contrast", 0.0, 2.0, 1.0, 0.1, key=f"contrast_{idx}")
                    saturation = st.slider("Saturation", 0.0, 2.0, 1.0, 0.1, key=f"sat_{idx}")
                    sharpness = st.slider("Sharpness", 0.0, 2.0, 1.0, 0.1, key=f"sharp_{idx}")
                    
                    if st.button("Apply Filters", key=f"apply_filters_{idx}"):
                        filtered = st.session_state.processor.apply_brightness(current_image, brightness)
                        filtered = st.session_state.processor.apply_contrast(filtered, contrast)
                        filtered = st.session_state.processor.apply_saturation(filtered, saturation)
                        filtered = st.session_state.processor.apply_sharpness(filtered, sharpness)
                        st.image(filtered, use_container_width=True)
                        # Save filtered
                        filtered_path = path.replace(".png", "_filtered.png")
                        filtered.save(filtered_path)
                        with open(filtered_path, "rb") as f:
                            st.download_button("Download Filtered", f, file_name=os.path.basename(filtered_path), mime="image/png")
                
                with edit_tab3:
                    st.subheader("✂️ Crop & Resize")
                    img_width, img_height = current_image.size
                    
                    crop_col1, crop_col2 = st.columns(2)
                    with crop_col1:
                        st.write("**Crop**")
                        left = st.slider("Left", 0, img_width, 0, key=f"crop_l_{idx}")
                        top = st.slider("Top", 0, img_height, 0, key=f"crop_t_{idx}")
                        right = st.slider("Right", 0, img_width, img_width, key=f"crop_r_{idx}")
                        bottom = st.slider("Bottom", 0, img_height, img_height, key=f"crop_b_{idx}")
                        if st.button("Crop", key=f"crop_btn_{idx}"):
                            cropped = st.session_state.processor.crop_image(current_image, left, top, right, bottom)
                            st.image(cropped, use_container_width=True)
                            cropped_path = path.replace(".png", "_cropped.png")
                            cropped.save(cropped_path)
                            with open(cropped_path, "rb") as f:
                                st.download_button("Download Cropped", f, file_name=os.path.basename(cropped_path), mime="image/png")
                    
                    with crop_col2:
                        st.write("**Resize**")
                        new_width = st.number_input("Width", 100, 2048, img_width, key=f"resize_w_{idx}")
                        new_height = st.number_input("Height", 100, 2048, img_height, key=f"resize_h_{idx}")
                        maintain_aspect = st.checkbox("Maintain Aspect", True, key=f"aspect_{idx}")
                        if st.button("Resize", key=f"resize_btn_{idx}"):
                            resized = st.session_state.processor.resize_image(current_image, new_width, new_height, maintain_aspect)
                            st.image(resized, use_container_width=True)
                            resized_path = path.replace(".png", "_resized.png")
                            resized.save(resized_path)
                            with open(resized_path, "rb") as f:
                                st.download_button("Download Resized", f, file_name=os.path.basename(resized_path), mime="image/png")
                
                with edit_tab4:
                    st.subheader("🔧 Other Tools")
                    if st.button("Remove Watermark", key=f"remove_wm_{idx}"):
                        no_wm = st.session_state.processor.remove_watermark(current_image)
                        st.image(no_wm, use_container_width=True)
                        no_wm_path = path.replace(".png", "_no_watermark.png")
                        no_wm.save(no_wm_path)
                        with open(no_wm_path, "rb") as f:
                            st.download_button("Download (No Watermark)", f, file_name=os.path.basename(no_wm_path), mime="image/png")
    
    # Clear button
    if st.button("🗑️ Clear Results", use_container_width=True):
        st.session_state.generated_images = []
        st.rerun()

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #6b7280; padding: 2rem 0;'>
    <p style='font-size: 0.9rem;'>Built with ❤️ using Streamlit and Stable Diffusion</p>
    <p style='font-size: 0.85rem;'>⚠️ Use responsibly and ethically | All images are AI-generated</p>
</div>
""", unsafe_allow_html=True)
