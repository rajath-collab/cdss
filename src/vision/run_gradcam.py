# run_gradcam.py - FIXED for your vision_predict.py
import torch
import sys
from PIL import Image
from torchvision import transforms

from gradcam import GradCAM
from vision_predict import load_model

img_path = sys.argv[1] if len(sys.argv) > 1 else "02-01-Infiltrat_pa.png"

# Load model - returns (model, classes, device)
model, classes, device = load_model()
print("Classes:", classes)

# Same preprocessing as vision_predict.py
tf = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
])

img = Image.open(img_path).convert("RGB")
x = tf(img).unsqueeze(0).to(device)

# FIX: plain ResNet50 has layer4 directly, not .backbone.layer4
target_layer = model.layer4[-1].conv3
cam = GradCAM(model, target_layer=target_layer)

heatmap = cam.generate_heatmap(x)
out = cam.overlay_heatmap(img, heatmap)
out.save("gradcam_output.jpg")
print("Saved gradcam_output.jpg - OPEN IT!")