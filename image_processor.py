"""
Image Processing Module
Handles upscaling, filters, cropping, resizing, and watermark removal
"""

from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
from io import BytesIO
import base64


class ImageProcessor:
    """Handle various image processing operations"""
    
    @staticmethod
    def upscale_image(image, scale_factor=2, method='lanczos'):
        """
        Upscale image using specified method
        
        Args:
            image: PIL Image
            scale_factor: 2 or 4
            method: 'lanczos' (high quality) or 'nearest' (fast)
            
        Returns:
            Upscaled PIL Image
        """
        width, height = image.size
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        
        if method == 'lanczos':
            resample = Image.LANCZOS
        elif method == 'nearest':
            resample = Image.NEAREST
        else:
            resample = Image.LANCZOS
        
        upscaled = image.resize((new_width, new_height), resample=resample)
        return upscaled
    
    @staticmethod
    def apply_brightness(image, factor):
        """
        Adjust image brightness
        
        Args:
            image: PIL Image
            factor: 0.0 (black) to 2.0 (white), 1.0 is original
            
        Returns:
            Adjusted PIL Image
        """
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(factor)
    
    @staticmethod
    def apply_contrast(image, factor):
        """
        Adjust image contrast
        
        Args:
            image: PIL Image
            factor: 0.0 (gray) to 2.0 (high contrast), 1.0 is original
            
        Returns:
            Adjusted PIL Image
        """
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)
    
    @staticmethod
    def apply_saturation(image, factor):
        """
        Adjust image saturation
        
        Args:
            image: PIL Image
            factor: 0.0 (grayscale) to 2.0 (vibrant), 1.0 is original
            
        Returns:
            Adjusted PIL Image
        """
        enhancer = ImageEnhance.Color(image)
        return enhancer.enhance(factor)
    
    @staticmethod
    def apply_sharpness(image, factor):
        """
        Adjust image sharpness
        
        Args:
            image: PIL Image
            factor: 0.0 (blurred) to 2.0 (sharp), 1.0 is original
            
        Returns:
            Adjusted PIL Image
        """
        enhancer = ImageEnhance.Sharpness(image)
        return enhancer.enhance(factor)
    
    @staticmethod
    def crop_image(image, left, top, right, bottom):
        """
        Crop image to specified coordinates
        
        Args:
            image: PIL Image
            left, top, right, bottom: Crop box coordinates
            
        Returns:
            Cropped PIL Image
        """
        return image.crop((left, top, right, bottom))
    
    @staticmethod
    def resize_image(image, width, height, maintain_aspect=True):
        """
        Resize image
        
        Args:
            image: PIL Image
            width: Target width
            height: Target height
            maintain_aspect: If True, maintain aspect ratio
            
        Returns:
            Resized PIL Image
        """
        if maintain_aspect:
            image.thumbnail((width, height), Image.LANCZOS)
            return image
        else:
            return image.resize((width, height), Image.LANCZOS)
    
    @staticmethod
    def remove_watermark(image):
        """
        Attempt to remove watermark by inpainting the bottom-right corner
        
        Args:
            image: PIL Image
            
        Returns:
            Image with watermark area filled
        """
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        width, height = image.size
        
        # Estimate watermark area (bottom-right corner, ~15% of image)
        watermark_width = int(width * 0.15)
        watermark_height = int(height * 0.1)
        
        left = width - watermark_width - 10
        top = height - watermark_height - 10
        right = width
        bottom = height
        
        # Get pixels around watermark area for color matching
        sample_left = max(0, left - 50)
        sample_top = max(0, top - 50)
        sample_right = left
        sample_bottom = top
        
        if sample_right > sample_left and sample_bottom > sample_top:
            # Sample background color
            sample_region = image.crop((sample_left, sample_top, sample_right, sample_bottom))
            sample_array = np.array(sample_region)
            
            # Calculate average color
            avg_color = tuple(np.mean(sample_array.reshape(-1, 3), axis=0).astype(int))
            
            # Create a copy and fill watermark area
            result = image.copy()
            from PIL import ImageDraw
            draw = ImageDraw.Draw(result)
            draw.rectangle([left, top, right, bottom], fill=avg_color)
            
            # Apply slight blur to blend
            result = result.filter(ImageFilter.GaussianBlur(radius=1))
            
            return result
        
        return image
    
    @staticmethod
    def apply_filter(image, filter_name):
        """
        Apply a named filter
        
        Args:
            image: PIL Image
            filter_name: 'blur', 'sharpen', 'smooth', 'edge_enhance', 'emboss'
            
        Returns:
            Filtered PIL Image
        """
        filter_map = {
            'blur': ImageFilter.BLUR,
            'sharpen': ImageFilter.SHARPEN,
            'smooth': ImageFilter.SMOOTH,
            'edge_enhance': ImageFilter.EDGE_ENHANCE,
            'emboss': ImageFilter.EMBOSS,
        }
        
        if filter_name in filter_map:
            return image.filter(filter_map[filter_name])
        return image
    
    @staticmethod
    def image_to_base64(image, format='PNG'):
        """Convert PIL Image to base64 string for display"""
        buffered = BytesIO()
        image.save(buffered, format=format)
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return img_str

