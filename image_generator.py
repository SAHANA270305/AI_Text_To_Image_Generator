"""
AI Image Generator Core Module
Handles Stable Diffusion model loading and image generation
"""

import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime
import json


class ImageGenerator:
    def __init__(self, model_id="stabilityai/stable-diffusion-2-1", device=None, hf_token=None):
        """
        Initialize the image generator with Stable Diffusion model
        
        Args:
            model_id: HuggingFace model identifier
            device: 'cuda' for GPU, 'cpu' for CPU, None for auto-detect
            hf_token: HuggingFace authentication token (for gated models)
        """
        self.model_id = model_id
        self.hf_token = hf_token or os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
        
        # Auto-detect device if not specified
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
            
        print(f"Using device: {self.device}")
        
        # Load model
        self.pipe = None
        self.load_model()
        
    def load_model(self):
        """Load the Stable Diffusion pipeline"""
        print(f"Loading model: {self.model_id}...")
        
        try:
            # Prepare kwargs for loading
            load_kwargs = {
                "torch_dtype": torch.float16 if self.device == "cuda" else torch.float32,
                "safety_checker": None,  # Disable for faster generation
                "requires_safety_checker": False
            }
            
            # Add token if available (required for gated models)
            if self.hf_token:
                load_kwargs["token"] = self.hf_token
                print("Using HuggingFace authentication token")
            
            # Load pipeline with optimizations
            self.pipe = StableDiffusionPipeline.from_pretrained(
                self.model_id,
                **load_kwargs
            )
            
            # Use faster scheduler
            self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
                self.pipe.scheduler.config
            )
            
            # Move to device
            self.pipe = self.pipe.to(self.device)
            
            # Enable memory optimizations for GPU
            if self.device == "cuda":
                self.pipe.enable_attention_slicing()
                # Uncomment if you have limited VRAM
                # self.pipe.enable_vae_slicing()
                # self.pipe.enable_sequential_cpu_offload()
            
            print("Model loaded successfully!")
            
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    
    def enhance_prompt(self, prompt, style="realistic"):
        """
        Enhance prompts with quality descriptors
        
        Args:
            prompt: User's text prompt
            style: Generation style (realistic, artistic, cartoon, etc.)
        """
        style_templates = {
            "realistic": "highly detailed, photorealistic, 4K, professional photography",
            "artistic": "artistic, oil painting, masterpiece, highly detailed",
            "cartoon": "cartoon style, animated, vibrant colors, cel shaded",
            "anime": "anime style, manga, detailed, vibrant",
            "cyberpunk": "cyberpunk style, neon lights, futuristic, dystopian",
            "fantasy": "fantasy art, magical, ethereal, detailed"
        }
        
        enhancement = style_templates.get(style, style_templates["realistic"])
        enhanced_prompt = f"{prompt}, {enhancement}"
        
        return enhanced_prompt
    
    def generate_images(
        self,
        prompt,
        negative_prompt="",
        num_images=1,
        style="realistic",
        num_inference_steps=50,
        guidance_scale=7.5,
        height=512,
        width=512,
        seed=None
    ):
        """
        Generate images from text prompt
        
        Args:
            prompt: Text description of desired image
            negative_prompt: Things to avoid in generation
            num_images: Number of images to generate
            style: Generation style
            num_inference_steps: More steps = higher quality (20-100)
            guidance_scale: How closely to follow prompt (5-15)
            height: Image height (multiples of 8)
            width: Image width (multiples of 8)
            seed: Random seed for reproducibility
            
        Returns:
            List of PIL Images
        """
        # Enhance prompt based on style
        enhanced_prompt = self.enhance_prompt(prompt, style)
        
        # Default negative prompt
        default_negative = "blurry, bad quality, distorted, deformed, ugly, low resolution"
        if negative_prompt:
            negative_prompt = f"{negative_prompt}, {default_negative}"
        else:
            negative_prompt = default_negative
        
        # Set random seed if provided
        generator = None
        if seed is not None:
            generator = torch.Generator(device=self.device).manual_seed(seed)
        
        print(f"Generating {num_images} image(s)...")
        print(f"Enhanced prompt: {enhanced_prompt}")
        
        try:
            # Generate images
            output = self.pipe(
                prompt=enhanced_prompt,
                negative_prompt=negative_prompt,
                num_images_per_prompt=num_images,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                height=height,
                width=width,
                generator=generator
            )
            
            images = output.images
            print(f"Successfully generated {len(images)} image(s)")
            
            return images
            
        except Exception as e:
            print(f"Error generating images: {e}")
            raise
    
    def add_watermark(self, image):
        """Add AI-generated watermark to image"""
        draw = ImageDraw.Draw(image)
        watermark_text = "AI Generated"
        
        # Position watermark at bottom right
        width, height = image.size
        
        # Use default font
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        # Get text bounding box
        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Position
        x = width - text_width - 10
        y = height - text_height - 10
        
        # Draw semi-transparent background
        padding = 5
        draw.rectangle(
            [x - padding, y - padding, x + text_width + padding, y + text_height + padding],
            fill=(0, 0, 0, 128)
        )
        
        # Draw text
        draw.text((x, y), watermark_text, fill=(255, 255, 255), font=font)
        
        return image
    
    def save_images(self, images, prompt, output_dir="generated_images", add_watermark=True):
        """
        Save generated images with metadata
        
        Args:
            images: List of PIL Images
            prompt: Original prompt
            output_dir: Directory to save images
            add_watermark: Whether to add AI watermark
            
        Returns:
            List of saved file paths
        """
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        saved_paths = []
        
        for i, image in enumerate(images):
            # Add watermark if requested
            if add_watermark:
                image = self.add_watermark(image)
            
            # Generate filename
            filename = f"generated_{timestamp}_{i+1}.png"
            filepath = os.path.join(output_dir, filename)
            
            # Save image
            image.save(filepath, "PNG")
            saved_paths.append(filepath)
            
            # Save metadata
            metadata = {
                "prompt": prompt,
                "timestamp": timestamp,
                "filename": filename,
                "model": self.model_id
            }
            
            metadata_file = filepath.replace(".png", "_metadata.json")
            with open(metadata_file, "w") as f:
                json.dump(metadata, f, indent=2)
            
            print(f"Saved: {filepath}")
        
        return saved_paths