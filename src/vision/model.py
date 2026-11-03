"""
Module 1: Medical Vision & Radiography Preprocessing (ResNet-50)
Part of Multimodal Fused Clinical Decision Support System (CDSS)
VTU 5th Sem Mini Project - Dept. of CSE (Data Science)
"""

import os
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import numpy as np
import cv2


class CDSSVisionModel(nn.Module):
    """
    Fine-tuned ResNet-50 architecture for Thoracic Radiography Screening.
    Predicts:
      0: Normal
      1: Pneumonia
      2: Tuberculosis (from D:/X-RAY)
    """
    def __init__(self, num_classes: int = 3, pretrained: bool = True):
        super(CDSSVisionModel, self).__init__()
        weights = models.ResNet50_Weights.DEFAULT if pretrained else None
        self.backbone = models.resnet50(weights=weights)
        
        # Replace the final fully connected layer (FC) for multi-class triage
        in_features = self.backbone.fc.in_features
        self.backbone.fc = nn.Sequential(
            nn.Dropout(p=0.3),
            nn.Linear(in_features, 128),
            nn.ReLU(),
            nn.Dropout(p=0.2),
            nn.Linear(128, num_classes)
        )
        if num_classes == 3:
            self.classes = ["Normal", "Pneumonia", "Tuberculosis"]
        else:
            self.classes = ["Normal", "Pulmonary Opacity / Pneumonia"]

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.backbone(x)


def apply_clahe(image: Image.Image) -> Image.Image:
    """
    Contrast Limited Adaptive Histogram Equalization (CLAHE).
    Enhances contrast in thoracic radiographs to reveal subtle lung infiltrates.
    """
    # Convert PIL to Grayscale OpenCV image
    np_img = np.array(image.convert("L"))
    
    # Create CLAHE object with 2.0 clip limit and 8x8 tile grid
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(np_img)
    
    # Convert back to 3-channel RGB image for ResNet-50 input
    rgb_enhanced = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2RGB)
    return Image.fromarray(rgb_enhanced)


def get_inference_transforms():
    """Standard transformations matching ImageNet requirements."""
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])


def load_model(weights_path: str = None, device: str = None) -> CDSSVisionModel:
    """Instantiate and load the ResNet-50 model with dynamic class detection."""
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    
    target_weights = weights_path or "models/weights/cdss_resnet50.pth"
    num_classes = 3
    
    if os.path.exists(target_weights):
        state_dict = torch.load(target_weights, map_location=device)
        fc_weight_keys = [k for k in state_dict.keys() if "backbone.fc" in k and "weight" in k]
        if fc_weight_keys:
            num_classes = state_dict[fc_weight_keys[-1]].shape[0]
            
        model = CDSSVisionModel(num_classes=num_classes, pretrained=False)
        model.load_state_dict(state_dict)
        print(f"[*] Loaded weights from: {target_weights} ({num_classes} classes: {model.classes})")
    else:
        model = CDSSVisionModel(num_classes=num_classes, pretrained=True)
        print(f"[i] Running with pre-trained ImageNet backbone ({num_classes} classes).")
    
    model.to(device)
    model.eval()
    return model


class CDSSPredictionResult(dict):
    """
    Polymorphic result object:
    Acts as a dict: res['predicted_class'], res['confidence']
    Can be unpacked as a 2-tuple: p_class, p_conf = predict_xray(...)
    Can be indexed by int: res[0], res[1]
    """
    def __iter__(self):
        return iter((self.get("predicted_class", "Normal"), self.get("confidence", 90.0)))
    
    def __getitem__(self, item):
        if isinstance(item, int):
            if item == 0:
                return self.get("predicted_class", "Normal")
            elif item == 1:
                return self.get("confidence", 90.0)
            elif item == 2:
                return self.get("probabilities", {})
        return super().__getitem__(item)


def predict_xray(*args, **kwargs):
    """
    Runs end-to-end inference on a single chest X-ray.
    Polymorphic signature accepts:
      - predict_xray(model, image)
      - predict_xray(image, model)
      - predict_xray(model=model, image=image)
      - predict_xray(image, model=model)
    Returns:
      CDSSPredictionResult (dict & unpackable as (predicted_class, confidence))
    """
    model = kwargs.get("model")
    image = kwargs.get("image")
    device = kwargs.get("device")

    for a in args:
        if isinstance(a, Image.Image):
            image = a
        elif hasattr(a, "eval") or hasattr(a, "forward") or isinstance(a, torch.nn.Module):
            model = a
        elif isinstance(a, str) and a in ("cuda", "cpu"):
            device = a
        elif isinstance(a, np.ndarray):
            image = Image.fromarray(a)

    if model is None:
        model = load_model()
    if image is None:
        raise ValueError("predict_xray requires a valid PIL Image")

    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
    enhanced_img = apply_clahe(image)
    transform = get_inference_transforms()
    input_tensor = transform(enhanced_img).unsqueeze(0).to(device)
    
    with torch.no_grad():
        logits = model(input_tensor)
        probs = torch.softmax(logits, dim=1)[0].cpu().numpy()
        
    pred_idx = int(np.argmax(probs))
    pred_class = model.classes[pred_idx]
    confidence = float(probs[pred_idx] * 100.0)
    
    prob_dict = {model.classes[i]: float(probs[i] * 100.0) for i in range(len(model.classes))}
    
    return CDSSPredictionResult({
        "predicted_class": pred_class,
        "confidence": confidence,
        "class_index": pred_idx,
        "probabilities": prob_dict,
        "enhanced_image": enhanced_img,
        "input_tensor": input_tensor
    })
