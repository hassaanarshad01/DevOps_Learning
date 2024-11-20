#!/usr/bin/env python
# coding: utf-8

# In[6]:


from diffusers import StableDiffusionInpaintPipeline
import torch
import cv2
import numpy as np
from PIL import Image
from diffusers.utils import make_image_grid
import os

class StableDiffusionInpainting:
    def __init__(self):
        """
        Initialize the StableDiffusionInpainting class.
        Automatically sets the device to GPU if available, otherwise defaults to CPU.
        The model path is fixed to './Stable_Diffusion_Inpaint_2'.
        """
        
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print('device for inpainter:', self.device)
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, './Stable_Diffusion_Inpaint_2')
        print("Loading model from:", model_path)

        self.pipe = StableDiffusionInpaintPipeline.from_pretrained(
            model_path,
            torch_dtype=torch.float16 if self.device == 'cuda' else torch.float32
        )

        self.pipe.enable_attention_slicing()
        self.pipe = self.pipe.to(self.device)

    def process_mask(self, painting):
        """
        Processes the input image to generate an appropriate inpainting mask.
        :param painting: Input image in PIL format.
        :return: Processed mask image in PIL format.
        """
        if isinstance(painting, Image.Image):
            painting = np.array(painting)

        gray_painting = cv2.cvtColor(painting, cv2.COLOR_BGR2GRAY)
        _, black_mask = cv2.threshold(gray_painting, 10, 255, cv2.THRESH_BINARY_INV)
        white_background = np.ones_like(gray_painting) * 255
        result_mask = cv2.bitwise_and(white_background, white_background, mask=black_mask)
        contours, _ = cv2.findContours(black_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        num_shapes = len(contours)

        if num_shapes > 25:
            kernel_dilate = np.ones((20, 20), np.uint8)
            kernel_erode = np.ones((15, 15), np.uint8)
        else:
            kernel_dilate = np.ones((30, 30), np.uint8)
            kernel_erode = np.ones((25, 25), np.uint8)

        dilated_mask = cv2.dilate(result_mask, kernel_dilate, iterations=1)
        eroded_mask = cv2.erode(dilated_mask, kernel_erode, iterations=1)
        final_mask_resized = cv2.resize(eroded_mask, (512, 512))

        return Image.fromarray(final_mask_resized), result_mask

    def inpaint_image_with_path(self, init_image_path, prompt):
        """
        Inpaint the damaged areas of an image based on a text prompt.
        :param init_image_path: Path to the damaged input image.
        :param prompt: Text prompt describing what should be filled in.
        :return: Inpainted image in PIL format.
        """
        
        init_image = Image.open(init_image_path)
        mask_image, clear_image = self.process_mask(init_image)
        
        inpainted_image = self.pipe(prompt=prompt, image=init_image, mask_image=mask_image).images[0]
        
        #self.save_images(inpainted_image, mask_image, clear_image)
        
        return inpainted_image

    def inpaint_image(self, init_image, prompt):
        """
        Inpaint the damaged areas of an image based on a text prompt.
        :param init_image_path: Path to the damaged input image.
        :param prompt: Text prompt describing what should be filled in.
        :return: Inpainted image in PIL format.
        """
        
        mask_image, clear_mask = self.process_mask(init_image)
        
        inpainted_image = self.pipe(prompt=prompt, image=init_image, mask_image=mask_image).images[0]

        #uncomment this to save immediately to wherever
        #self.save_images(inpainted_image, mask_image, clear_mask)

        return inpainted_image

    def save_images(self, inpainted_image, mask_image, clear_mask):
        """
        Save the inpainted image, mask image, and the processed mask.
        :param inpainted_image: The inpainted output image (PIL).
        :param mask_image: The mask image used for inpainting (PIL).
        :param clear_mask: The raw mask (NumPy array) used for mask processing.
        """
        output_dir = './_Images/Output'
        os.makedirs(output_dir, exist_ok=True)
        
        inpainted_image.save(os.path.join(output_dir, 'inpainted_image.jpg'))
        
        mask_image.save(os.path.join(output_dir, 'mask_image.jpg'))
        
        clear_mask_pil = Image.fromarray(clear_mask)
        clear_mask_pil.save(os.path.join(output_dir, 'clear_mask.jpg'))

        return

    def get_mask(self, Painting):
        eroded_mask, clear_mask = self.process_mask(Painting)
        return eroded_mask, clear_mask

    def image_grid(self, imgs, rows, cols, resize=512):
        if resize is not None:
            imgs = [img.resize((resize, resize)) for img in imgs]
        w, h = imgs[0].size
        grid = Image.new("RGB", size=(cols * w, rows * h))
        grid_w, grid_h = grid.size
    
        for i, img in enumerate(imgs):
            grid.paste(img, box=(i % cols * w, i // cols * h))
        return grid

    def save_image_grid(self, images, rows, cols, output_dir='./_Images/Output/result_grids'):
        os.makedirs(output_dir, exist_ok=True)
        
        existing_files = os.listdir(output_dir)
        
        existing_grids = [f for f in existing_files if f.startswith("grid_") and f.endswith(".png")]
        
        if existing_grids:
            next_number = len(existing_grids) + 1
        else:
            next_number = 1
        
        output_path = os.path.join(output_dir, f"grid_{next_number}.png")
        grid_image = self.image_grid(images, rows=rows, cols=cols)
        
        grid_image.save(output_path)
        print(f"Grid image saved at: {output_path}")
        return

