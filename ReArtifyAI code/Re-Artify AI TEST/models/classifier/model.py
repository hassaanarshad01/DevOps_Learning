#!/usr/bin/env python
# coding: utf-8

# In[31]:


import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
from PIL import Image

categories = ['Blur', 'Clear', 'Discoloured', 'Inpainting', 'Scratches', 'Smudged']
image_size = (256, 256) 

class PaintingDamageClassifier:
    def __init__(self, checkpoint_path, num_classes=6, device=None):
        self.device = device if device else torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.num_classes = num_classes
        self.model = self._build_model().to(self.device)
        self.load_weights(checkpoint_path)
        
        self.transform = transforms.Compose([
            transforms.Resize(image_size),    
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))  
        ])

        
    def _build_model(self):
        class CNNModel(nn.Module):
            def __init__(self, num_classes):
                super(CNNModel, self).__init__()
                self.conv1 = nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1)
                self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
                self.dropout1 = nn.Dropout(0.2)
                self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
                self.dropout2 = nn.Dropout(0.3)
                self.conv3 = nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1)
                self.dropout3 = nn.Dropout(0.4)
                self.conv4 = nn.Conv2d(128, 256, kernel_size=3, stride=1, padding=1)
                self.dropout4 = nn.Dropout(0.5)
                self.fc1 = nn.Linear(256 * (256 // 16) * (256 // 16), 64)  # Adjust image size as per your input
                self.dropout5 = nn.Dropout(0.5)
                self.fc2 = nn.Linear(64, num_classes)

            def forward(self, x):
                x = self.pool(F.relu(self.conv1(x)))
                x = self.dropout1(x)
                x = self.pool(F.relu(self.conv2(x)))
                x = self.dropout2(x)
                x = self.pool(F.relu(self.conv3(x)))
                x = self.dropout3(x)
                x = self.pool(F.relu(self.conv4(x)))
                x = self.dropout4(x)
                x = x.view(x.size(0), -1)
                x = F.relu(self.fc1(x))
                x = self.dropout5(x)
                x = self.fc2(x)
                return x

        return CNNModel(self.num_classes)

    def load_weights(self, weights_path):
        """Load the model weights from a file."""
        self.model.load_state_dict(torch.load(weights_path, map_location=self.device))
        self.model.eval()  # Set the model to evaluation mode
        return

    def preprocess_image(self, image_path):
        img = Image.open(image_path).convert('RGB')
        img = self.transform(img)
        img = img.unsqueeze(0)  # Add batch dimension
        return img.to(self.device)

    def classify(self, image_path):
        """
        Classify the input image tensor.
        Args:
            image_tensor: A tensor representing the image (after applying transforms).
        Returns:
            The predicted class index.
        """
        
        image_tensor = self.preprocess_image(image_path)
        self.model.eval()  
        with torch.no_grad():  
            outputs = self.model(image_tensor)  
            _, predicted_class = torch.max(outputs.data, 1)
            predicted_class_name = categories[predicted_class.item()]
            return predicted_class_name


