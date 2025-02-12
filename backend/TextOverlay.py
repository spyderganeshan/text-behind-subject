
# from torchvision    import transforms
from PIL            import Image, ImageDraw, ImageFont
from loguru         import logger
from io             import BytesIO
import numpy        as np
import cv2
import requests

class TextOverlay:
    def __init__(self,):
        self.text           = None
        self.text_size      = None
        self.text_position  = None
        self.text_color     = None
        self.font_name      = None
        logger.success('Initialized TextOverlay')
        
    def set_text_input(self,text, text_size, text_position,text_color, font_name):
        self.text           = text
        self.text_size      = text_size
        self.text_position  = text_position
        self.text_color     = text_color
        self.font_name      = font_name
        self.font           = ImageFont.truetype(f"utils/fonts/{self.font_name}.ttf", self.text_size)
        logger.info(f"TextOverlay input set")
        
    def apply_text_overlay(self,image_pil,foreground_mask):
        """Apply text behind detected
        objects using depth map."""
        logger.info(f"applying text overlay...")
        try:
            image           = np.array(image_pil)                                                 # Convert PIL image to NumPy array
            original_h      = image.shape[0]  
            original_w      = image.shape[1]
            text_overlay    = Image.new("RGBA", (original_w, original_h), (0, 0, 0, 0))           # Create text overlay using PIL
            draw            = ImageDraw.Draw(text_overlay)
            # text_size       = draw.textbbox((0, 0), self.text, font=self.font)                    # Get text width/height
        except Exception as e:
            logger.error(f"Error in apply_text API: {e}")
            return {"error": str(e)}
        
        try:
            # text_width          = text_size[2] - text_size[0]
            # text_height         = text_size[3] - text_size[1]
            text_x              = self.text_position[0]
            text_y              = self.text_position[1]
            # fill=(255, 0, 0, 255)
            draw.text((text_x, text_y), self.text, fill=self.text_color, font=self.font)             # Draw text on overlay
        except Exception as e:
            logger.error(f"Error in apply_text API: {e}")
            return {"error": str(e)}
        try:
            text_overlay_np     = np.array(text_overlay)                                              # Convert PIL overlay to NumPy
            text_behind         = cv2.bitwise_and(text_overlay_np, text_overlay_np, mask=foreground_mask)   # Apply text only to background using the mask
            final_image_pil     = Image.fromarray(image)                                              # Convert image back to PIL for merging
            final_overlay_pil   = Image.fromarray(text_behind)
            final_output = Image.alpha_composite(final_image_pil.convert("RGBA"),final_overlay_pil)   # Merge text with the original image
        except Exception as e:
            logger.error(f"Error in apply_text API: {e}")
            return {"error": str(e)}
        
        return final_output
    
    
    
        # def get_google_fonts(self,font_name,text_size):
    #     """Fetch Google Font dynamically for PIL usage."""
    #     base_url = "https://github.com/google/fonts/tree/main/ofl"
    #     font_path = f"{base_url}/{font_name.lower().replace(' ', '')}/{font_name.replace(' ', '')}-Regular.ttf"
    #     response = requests.get(font_path)
    #     if response.status_code == 200:
    #         return ImageFont.truetype(BytesIO(response.content),text_size)
    #     else:
    #         raise ValueError(f"Font '{font_name}' not found!")
        
    