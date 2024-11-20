#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import torch
import cv2
import os
from PIL import Image
import numpy as np

from .blur.BlurModel import BlurRemoverModel
from .classifier.model import PaintingDamageClassifier
from .coloring.ColoringModel import ColorationModel
from .scratches.ScratchModel import ScratchRemoverModel
from .smudges.SmudgeModel import SmudgeModel
from .inpainting.InpaintingModel import StableDiffusionInpainting 



class ModelPackage:
    def __init__(self):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print('device in __init: ', self.device)
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.classifier = PaintingDamageClassifier(os.path.join(base_dir, 'classifier', 'checkpoint.pth'))
        self.blur = BlurRemoverModel(os.path.join(base_dir, 'blur', 'checkpoint.pth'))
        self.scratches = ScratchRemoverModel(os.path.join(base_dir, 'scratches', 'checkpoint.pth'))
        self.coloring = ColorationModel(os.path.join(base_dir, 'coloring', 'checkpoint.pth'))
        self.smudges = SmudgeModel(os.path.join(base_dir, 'smudges', 'checkpoint.pth'))

        #self.inpainting = StableDiffusionInpainting()
        
    def classify(self, image_path):
        return self.classifier.classify(image_path)

    def predict(self, image_path, model_name):
        
        if model_name == 'blur':
            return self.blur.predict(image_path)
        elif model_name == 'scratches':
            return self.scratches.predict(image_path)
        elif model_name == 'coloring':
            o1, o2 = self.coloring.predict_dualpass(image_path)
            return o2
        elif model_name == 'smudges':
            o1, o2 = self.smudges.predict_dualpass(image_path)
            return o2
        else:
            raise ValueError(f"Model '{model_name}' not recognized.")

    def save_image(self, image, save_path):
        """Save the image to the specified path."""
        image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(save_path, image_bgr)  

    """def inpaint_image(self, image_path, prompt):
        
        
        painting = Image.open(image_path)

        edited_prompt = prompt + ", old painting"
        # Inpaint the image
        inpainted_image = self.inpainting.inpaint_image_with_path(image_path, edited_prompt)
        
        # Get the masks
        eroded_mask, clear_mask = self.inpainting.get_mask(painting)
    
        # Convert inpainted_image and masks to PIL Image if they are not already
        if isinstance(inpainted_image, np.ndarray):
            inpainted_image = Image.fromarray(inpainted_image)
            
        if isinstance(eroded_mask, np.ndarray):
            eroded_mask = Image.fromarray(eroded_mask)
    
        if isinstance(clear_mask, np.ndarray):
            clear_mask = Image.fromarray(clear_mask)

        images_list = [painting, clear_mask, eroded_mask, inpainted_image]
        self.inpainting.save_image_grid(images_list, rows=1, cols=4, output_dir='./_Images/Output/result_grids')

        return inpainted_image, eroded_mask, clear_mask"""


# In[ ]:




