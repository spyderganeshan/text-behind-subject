from backend.LayerEstimator import LayerEstimator
from backend.TextOverlay    import TextOverlay
from PIL                    import Image
from loguru                 import logger
import timm
import numpy as np

class ModelProcessor:
    def __init__(self):
        self.depth_estimator    = None
        self.depth_normalized   = None
        self.text_overlay       = TextOverlay()
        self.image_pil          = None
        self.f_mask             = None
        self.model_map          = {
            "Small": "MiDaS_small",
            "Hybrid": "DPT_Hybrid",
            "Large": "DPT_Large"
        }
        logger.success('Initialized ModelProcessor')
    
    def set_model(self, model_name,image_pil):
        self.layer_estimator    = LayerEstimator(model_name=self.model_map.get(model_name))
        self.image_pil          = image_pil
        logger.info("model set for processing")
        
    def generate_depth_map(self,):
        self.depth_normalized   = self.layer_estimator.estimate_depth(self.image_pil)
        
    def process_foreground(self,):
        self.f_mask             =self.layer_estimator.extract_foreground(self.depth_normalized, np.array(self.image_pil))
        logger.info("successfully processed foreground")
        
    def process_text(self,text, text_size, text_position,text_color, font_name):
        self.text_overlay.set_text_input(text, text_size, text_position,text_color, font_name)
        final_image_output      =self.text_overlay.apply_text_overlay(image_pil=self.image_pil,foreground_mask=self.f_mask)
        logger.info("text_overlay completed")
        return final_image_output
        