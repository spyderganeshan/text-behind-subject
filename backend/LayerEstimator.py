from torchvision    import transforms
from loguru         import logger
import torch
import numpy        as np
import cv2

class LayerEstimator:
    def __init__(self, model_name, device=None):
        """Initialize MiDaS model and transformations."""
        self.device     =   device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model      =   torch.hub.load("intel-isl/MiDaS", model_name).to(self.device)
        self.model.eval()
        
        self.transform  =   transforms.Compose([                                                    # Transformation for MiDaS
                            transforms.Resize((384, 384)),
                            transforms.ToTensor(),
                            transforms.Normalize(mean=[0.5], std=[0.5])])
        logger.success(f'Initialized LayerEstimator:DEVICE={self.device}:MODEL={type(self.model)}')

    def estimate_depth(self, image_pil):
        """Predict depth map from an image."""
        input_tensor    =   self.transform(image_pil).unsqueeze(0).to(self.device)
        with torch.no_grad():                                                                       # Predict depth
            depth_map   =   self.model(input_tensor).squeeze().cpu().numpy()            
        original_w, original_h  = image_pil.size                                                    # Resize depth map to original size
        depth_map  = cv2.resize(depth_map, (original_w, original_h))
        depth_normalized  = cv2.normalize(depth_map, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8) # Normalize depth map
        
        return depth_normalized
    
    def extract_foreground(self,depth_normalized,image):
        """Process foreground image."""
        _, foreground_mask  = cv2.threshold(depth_normalized, 128, 255, cv2.THRESH_BINARY)           # Threshold depth to create a foreground mask
        foreground_mask     = cv2.GaussianBlur(foreground_mask, (5, 5), 0)                           # Smooth edges
        foreground          = cv2.bitwise_and(image, image, mask=foreground_mask)                    # Create foreground-only image (Apply mask to original image)
        foreground_mask     = cv2.bitwise_not(foreground_mask)                                       # Invert mask (foreground in white, background in black)
        return foreground_mask