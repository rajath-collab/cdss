"""
Explainable AI (XAI): Gradient-weighted Class Activation Mapping (Grad-CAM)
Part of Multimodal Fused Clinical Decision Support System (CDSS)

Features:
- Dual DenseNet-121 support (targets features.norm5)
- Fallback ResNet-50 support (targets layer4)
- Tensor-level backward hooks to avoid PyTorch autograd inplace view conflicts
- Jet colormap overlay with optional clinical badge annotation
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import cv2
from PIL import Image


class GradCAM:
    """
    Computes Grad-CAM saliency heatmaps for DenseNet-121 or ResNet-50.
    """
    def __init__(self, model, target_layer=None):
        self.model = model
        
        # Resolve target layer
        if hasattr(model, "nih_model"):
            self.net = model.nih_model
            self.target_layer = self.net.backbone.features.norm5 if target_layer is None else target_layer
        elif hasattr(model, "backbone") and hasattr(model.backbone, "features") and hasattr(model.backbone.features, "norm5"):
            self.net = model
            self.target_layer = model.backbone.features.norm5 if target_layer is None else target_layer
        elif hasattr(model, "features") and hasattr(model.features, "norm5"):
            self.net = model
            self.target_layer = model.features.norm5 if target_layer is None else target_layer
        elif hasattr(model, "backbone") and hasattr(model.backbone, "layer4"):
            self.net = model
            self.target_layer = model.backbone.layer4[-1].conv3 if target_layer is None else target_layer
        else:
            self.net = model
            self.target_layer = target_layer

        self.net.eval()
        
        # Ensure no inplace ReLUs corrupt autograd graph
        for m in self.net.modules():
            if isinstance(m, nn.ReLU):
                m.inplace = False

        self.gradients = None
        self.activations = None
        self._register_hooks()

    def _register_hooks(self):
        def forward_hook(module, input, output):
            self.activations = output.detach().clone()
            def backward_hook(grad):
                self.gradients = grad.detach().clone()
            output.register_hook(backward_hook)

        self.target_layer.register_forward_hook(forward_hook)

    def generate_heatmap(self, input_tensor: torch.Tensor, class_idx: int = None) -> np.ndarray:
        """Generates a 2D normalized Grad-CAM heatmap [0, 1]."""
        self.net.eval()
        self.net.zero_grad()
        self.gradients = None
        self.activations = None

        output = self.net(input_tensor)
        
        if class_idx is None:
            class_idx = int(torch.argmax(output, dim=1).item())
            
        target_score = output[0, class_idx]
        target_score.backward(retain_graph=True)
        
        if self.gradients is None or self.activations is None:
            # Fallback uniform saliency if hooks uncaptured
            return np.zeros((224, 224), dtype=np.float32)

        weights = torch.mean(self.gradients, dim=[2, 3], keepdim=True)
        cam = torch.sum(weights * self.activations, dim=1).squeeze()
        cam = F.relu(cam)
        
        cam_np = cam.detach().cpu().numpy()
        cam_min, cam_max = np.min(cam_np), np.max(cam_np)
        if cam_max - cam_min > 1e-8:
            cam_np = (cam_np - cam_min) / (cam_max - cam_min)
        else:
            cam_np = np.zeros_like(cam_np)
            
        return cam_np

    def overlay_heatmap(
        self,
        original_image: Image.Image,
        heatmap: np.ndarray,
        alpha: float = 0.45,
        colormap: int = cv2.COLORMAP_JET,
        draw_legend: bool = True
    ) -> Image.Image:
        """Overlays the Grad-CAM heatmap on the original radiograph."""
        orig_w, orig_h = original_image.size
        resized_heatmap = cv2.resize(heatmap, (orig_w, orig_h))
        
        # Colorize
        heatmap_color = cv2.applyColorMap(np.uint8(255 * resized_heatmap), colormap)
        heatmap_color = cv2.cvtColor(heatmap_color, cv2.COLOR_BGR2RGB)
        
        orig_np = np.array(original_image.convert("RGB"))
        blended = np.uint8((1.0 - alpha) * orig_np + alpha * heatmap_color)
        
        if draw_legend:
            cv2.putText(
                blended, "DenseNet-121 Grad-CAM Saliency", (15, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA
            )
            
        return Image.fromarray(blended)
