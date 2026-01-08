"""
Batch Image Generation Script
Generate multiple images from a list of prompts
"""

from image_generator import ImageGenerator
import json
import os
from datetime import datetime

def batch_generate(prompts_file="prompts.json", output_dir="batch_output"):
    """
    Generate images from a JSON file containing prompts
    
    prompts.json format:
    {
        "prompts": [
            {
                "text": "A beautiful sunset over mountains",
                "style": "realistic",
                "num_images": 2,
                "negative_prompt": "blurry, distorted"
            },
            ...
        ]
    }
    """
    
    # Load prompts
    print("Loading prompts...")
    with open(prompts_file, 'r') as f:
        data = json.load(f)
    
    prompts = data.get('prompts', [])
    print(f"Found {len(prompts)} prompts to process")
    
    # Initialize generator
    print("\nInitializing image generator...")
    generator = ImageGenerator()
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Process each prompt
    results = []
    
    for idx, prompt_config in enumerate(prompts, 1):
        print(f"\n{'='*60}")
        print(f"Processing prompt {idx}/{len(prompts)}")
        print(f"{'='*60}")
        
        text = prompt_config.get('text', '')
        style = prompt_config.get('style', 'realistic')
        num_images = prompt_config.get('num_images', 1)
        negative_prompt = prompt_config.get('negative_prompt', '')
        
        print(f"Prompt: {text}")
        print(f"Style: {style}")
        print(f"Number of images: {num_images}")
        
        try:
            # Generate images
            images = generator.generate_images(
                prompt=text,
                negative_prompt=negative_prompt,
                num_images=num_images,
                style=style
            )
            
            # Save images
            saved_paths = generator.save_images(
                images,
                text,
                output_dir=output_dir
            )
            
            results.append({
                "prompt": text,
                "status": "success",
                "num_generated": len(images),
                "paths": saved_paths
            })
            
            print(f"✅ Successfully generated {len(images)} image(s)")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append({
                "prompt": text,
                "status": "failed",
                "error": str(e)
            })
    
    # Save batch results
    results_file = os.path.join(output_dir, f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*60}")
    print("BATCH GENERATION COMPLETE")
    print(f"{'='*60}")
    print(f"Total prompts: {len(prompts)}")
    print(f"Successful: {sum(1 for r in results if r['status'] == 'success')}")
    print(f"Failed: {sum(1 for r in results if r['status'] == 'failed')}")
    print(f"Results saved to: {results_file}")

if __name__ == "__main__":
    # Example: Create a sample prompts file if it doesn't exist
    if not os.path.exists("prompts.json"):
        sample_prompts = {
            "prompts": [
                {
                    "text": "A serene mountain lake at sunrise, professional photography",
                    "style": "realistic",
                    "num_images": 1,
                    "negative_prompt": "blurry, distorted"
                },
                {
                    "text": "Abstract representation of artificial intelligence, vibrant colors",
                    "style": "artistic",
                    "num_images": 1,
                    "negative_prompt": "ugly, low quality"
                },
                {
                    "text": "Cyberpunk city street at night with neon lights",
                    "style": "cyberpunk",
                    "num_images": 1,
                    "negative_prompt": "blurry, low resolution"
                }
            ]
        }
        
        with open("prompts.json", 'w') as f:
            json.dump(sample_prompts, f, indent=2)
        
        print("Created sample prompts.json file")
    
    # Run batch generation
    batch_generate()