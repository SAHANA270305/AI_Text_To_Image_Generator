"""
Prompt Utilities Module
Handles prompt variations and enhancements
"""

import random
import re


class PromptVariator:
    """Generate variations of prompts"""
    
    # Quality enhancers
    QUALITY_TAGS = [
        "high quality", "detailed", "4K", "8K", "ultra detailed",
        "professional", "masterpiece", "best quality", "sharp focus"
    ]
    
    # Style modifiers
    STYLE_MODIFIERS = {
        "realistic": ["photorealistic", "realistic", "professional photography", "DSLR"],
        "artistic": ["artistic", "oil painting", "watercolor", "digital art", "concept art"],
        "fantasy": ["fantasy art", "magical", "ethereal", "epic", "legendary"],
        "cyberpunk": ["cyberpunk", "neon", "futuristic", "dystopian", "sci-fi"],
        "anime": ["anime style", "manga", "japanese animation", "cel shaded"],
        "cartoon": ["cartoon style", "animated", "vibrant colors", "illustration"]
    }
    
    # Lighting modifiers
    LIGHTING_MODIFIERS = [
        "natural lighting", "golden hour", "sunset", "sunrise", "dramatic lighting",
        "soft lighting", "studio lighting", "rim lighting", "backlit", "ambient light"
    ]
    
    # Composition modifiers
    COMPOSITION_MODIFIERS = [
        "wide angle", "close-up", "macro", "panoramic", "bird's eye view",
        "low angle", "dutch angle", "rule of thirds", "centered composition"
    ]
    
    # Mood modifiers
    MOOD_MODIFIERS = [
        "peaceful", "dramatic", "mysterious", "vibrant", "serene", "energetic",
        "melancholic", "joyful", "epic", "intimate", "grandiose"
    ]
    
    @staticmethod
    def generate_variations(prompt, num_variations=5, style=None):
        """
        Generate variations of a prompt
        
        Args:
            prompt: Original prompt string
            num_variations: Number of variations to generate
            style: Optional style to emphasize
            
        Returns:
            List of prompt variations
        """
        variations = []
        base_prompt = prompt.strip()
        
        # Extract main subject (first part before comma if exists)
        parts = base_prompt.split(',')
        main_subject = parts[0].strip()
        existing_modifiers = [p.strip() for p in parts[1:]] if len(parts) > 1 else []
        
        for i in range(num_variations):
            variation_parts = [main_subject]
            
            # Add style modifiers if specified
            if style and style in PromptVariator.STYLE_MODIFIERS:
                style_mods = PromptVariator.STYLE_MODIFIERS[style]
                variation_parts.append(random.choice(style_mods))
            
            # Add quality tags (50% chance)
            if random.random() > 0.5:
                variation_parts.append(random.choice(PromptVariator.QUALITY_TAGS))
            
            # Add lighting modifier (40% chance)
            if random.random() > 0.6:
                variation_parts.append(random.choice(PromptVariator.LIGHTING_MODIFIERS))
            
            # Add composition modifier (30% chance)
            if random.random() > 0.7:
                variation_parts.append(random.choice(PromptVariator.COMPOSITION_MODIFIERS))
            
            # Add mood modifier (30% chance)
            if random.random() > 0.7:
                variation_parts.append(random.choice(PromptVariator.MOOD_MODIFIERS))
            
            # Keep some existing modifiers (random selection)
            if existing_modifiers:
                keep_count = random.randint(0, min(2, len(existing_modifiers)))
                kept = random.sample(existing_modifiers, keep_count)
                variation_parts.extend(kept)
            
            variations.append(", ".join(variation_parts))
        
        return variations
    
    @staticmethod
    def enhance_prompt(prompt, add_quality=True, add_lighting=True):
        """
        Enhance a prompt with quality and lighting modifiers
        
        Args:
            prompt: Original prompt
            add_quality: Add quality tags
            add_lighting: Add lighting modifiers
            
        Returns:
            Enhanced prompt
        """
        enhanced = prompt.strip()
        
        if add_quality and not any(tag in enhanced.lower() for tag in PromptVariator.QUALITY_TAGS):
            enhanced += f", {random.choice(PromptVariator.QUALITY_TAGS)}"
        
        if add_lighting and not any(light in enhanced.lower() for light in PromptVariator.LIGHTING_MODIFIERS):
            enhanced += f", {random.choice(PromptVariator.LIGHTING_MODIFIERS)}"
        
        return enhanced
    
    @staticmethod
    def create_negative_prompt_variations(negative_prompt=""):
        """
        Generate variations of negative prompts
        
        Args:
            negative_prompt: Original negative prompt
            
        Returns:
            List of negative prompt variations
        """
        base_negatives = [
            "blurry", "low quality", "distorted", "deformed", "ugly",
            "bad anatomy", "bad proportions", "watermark", "text", "signature"
        ]
        
        variations = []
        
        # Start with base if provided
        if negative_prompt:
            base_list = [n.strip() for n in negative_prompt.split(',')]
        else:
            base_list = []
        
        # Generate variations
        for i in range(3):
            variation = base_list.copy()
            
            # Add random negatives
            add_count = random.randint(2, 4)
            additional = random.sample(base_negatives, min(add_count, len(base_negatives)))
            variation.extend(additional)
            
            variations.append(", ".join(variation))
        
        return variations

