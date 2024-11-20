#!/usr/bin/env python
# coding: utf-8

# In[3]:


import torch
import torch.nn as nn
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

class SmudgeModel:
    def __init__(self, model_path, device='cuda' if torch.cuda.is_available() else 'cpu'):
        self.device = device
        self.model = self._build_model().to(self.device)
        self.load_weights(model_path)
        
    def _build_model(self):
        class DehazeNet(nn.Module):
            def __init__(self):
                super(DehazeNet, self).__init__()

                # Initial Convolution
                self.initial_conv = nn.Sequential(
                    nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1),  # Input: 3 channels (RGB)
                    nn.BatchNorm2d(64),
                    nn.ReLU(inplace=True)
                )

                # Encoder
                self.encoder = nn.Sequential(
                    nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1),  # Output: 128x128x128
                    nn.BatchNorm2d(128),
                    nn.ReLU(inplace=True),
                    nn.MaxPool2d(kernel_size=2, stride=2),  # Output: 64x64x128

                    nn.Conv2d(128, 256, kernel_size=3, stride=1, padding=1),  # Output: 64x64x256
                    nn.BatchNorm2d(256),
                    nn.ReLU(inplace=True),
                )

                # Middle layers
                self.middle_conv = nn.Sequential(
                    nn.Conv2d(256, 512, kernel_size=3, padding=1),  # Output: 64x64x512
                    nn.ReLU(inplace=True),
                )

                # Decoder
                self.decoder = nn.Sequential(
                    nn.Conv2d(512, 256, kernel_size=3, padding=1),  # Output: 64x64x256
                    nn.ReLU(inplace=True),
                    nn.Upsample(scale_factor=2, mode='bilinear', align_corners=False),  # Output: 128x128x256

                    nn.Conv2d(256, 128, kernel_size=3, padding=1),  # Output: 128x128x128
                    nn.ReLU(inplace=True),

                    nn.Conv2d(128, 64, kernel_size=3, padding=1),   # Output: 128x128x64
                    nn.ReLU(inplace=True),

                    nn.Conv2d(64, 3, kernel_size=3, padding=1)      # Output: 128x128x3
                )

            def forward(self, x):
                x = self.initial_conv(x)
                x = self.encoder(x)
                x = self.middle_conv(x)
                x = self.decoder(x)
                return x

        return DehazeNet()

    def load_weights(self, model_path):
        """Loads the model weights from the specified path."""
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.eval() 

    def preprocess_image(self, image_paths, desired_shape):
        images = []
        for image_path in image_paths:
            image = cv2.imread(image_path)
            if image is not None:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  
                image = cv2.resize(image, desired_shape[::-1])  
                image = image.astype('float32') / 255.0  
                images.append(image)
        return np.array(images)

    def predict_dualpass(self, image_path, desired_shape=(256, 256)):
        """Generates the deblurred image for the given image path."""
        with torch.no_grad():
            image = self.preprocess_image([image_path], desired_shape)  
            image_tensor = torch.tensor(image).permute(0, 3, 1, 2).to(self.device)
            
            output_tensor = self.model(image_tensor)
            output_tensor_2nd = self.model(output_tensor)
            
            output_image = output_tensor.cpu().numpy().squeeze().transpose(1, 2, 0) 
            output_image = np.clip(output_image * 255.0, 0, 255).astype(np.uint8)  

            output_image_2nd = output_tensor_2nd.cpu().numpy().squeeze().transpose(1, 2, 0)
            output_image_2nd = np.clip(output_image_2nd * 255.0, 0, 255).astype(np.uint8)

            
            return output_image, output_image_2nd
    def predict(self, image_path, desired_shape=(256, 256)):
        """Generates the deblurred image for the given image path."""
        with torch.no_grad():
            image = self.preprocess_image([image_path], desired_shape)  
            image_tensor = torch.tensor(image).permute(0, 3, 1, 2).to(self.device)
            
            output_tensor = self.model(image_tensor)
            
            output_image = output_tensor.cpu().numpy().squeeze().transpose(1, 2, 0)  
            output_image = np.clip(output_image * 255.0, 0, 255).astype(np.uint8)  
            
            return output_image

    def display_result(self, input_image_path, output_image):
        """Displays the input and output images side by side."""
        input_image = cv2.imread(input_image_path)
        input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)

        fig, axes = plt.subplots(1, 2, figsize=(10, 5))
        axes[0].imshow(input_image)
        axes[0].set_title('Input Image')
        axes[0].axis('off')

        axes[1].imshow(output_image)
        axes[1].set_title('Output Image')
        axes[1].axis('off')

        plt.tight_layout()
        plt.show()

    def save_image(self, image, save_path):
        """Saves the image to the specified path."""
        image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(save_path, image_bgr)  


# In[ ]:




