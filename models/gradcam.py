"""
Explainable AI (XAI): Gradient-weighted Class Activation Mapping (Grad-CAM)
Part of Multimodal Fused Clinical Decision Support System (CDSS)
VTU 5th Sem Mini Project - Dept. of CSE (Data Science)

Reference:
R. R. Selvaraju et al., "Grad-CAM: Visual Explanations from Deep Networks via
Gradient-Based Localization," ICCV 2017.
"""

import torch
import numpy as np
import cv2
from PIL import Image


class GradCAM:
    """
    Computes Grad-CAM saliency heatmaps for ResNet-50.
    Attaches forward and backward hooks to the final convolutional bottleneck layer (layer4).
    """
    def __init__(self, model, target_layer=None):
        self.model = model
        self.model.eval()
        
        # Default to the final bottleneck block of ResNet-50 layer4
        if target_layer is None:
            self.target_layer = self.model.backbone.layer4[-1].conv3
        else:
            self.target_layer = target_layer

        self.gradients = None
        self.activations = None
        self._register_hooks()

    def _register_hooks(self):
        def forward_hook(module, input, output):
            self.activations = output.detach()

        def backward_hook(module, grad_input, grad_output):
            self.gradients = grad_output[0].detach()

        self.target_layer.register_forward_hook(forward_hook)
        self.target_layer.register_full_backward_hook(backward_hook)

    def generate_heatmap(self, input_tensor: torch.Tensor, class_idx: int = None) -> np.ndarray:
        """
        Generates a 2D normalized Grad-CAM heatmap [0, 1] for the specified class index.
        """
        # Ensure gradients are enabled for the backward hook
        self.model.zero_grad()
        
        # Forward pass
        input_tensor.requires_grad = True
        output = self.model(input_tensor)
        
        if class_idx is None:
            class_idx = torch.argmax(output, dim=1).item()
            
        # Target score for backpropagation
        target_score = output[0, class_idx]
        target_score.backward(retain_graph=True)
        
        # Global Average Pooling of gradients across spatial dimensions (H, W)
        # self.gradients: [1, Channels, H, W]
        pooled_gradients = torch.mean(self.gradients, dim=[0, 2, 3])
        
        # Weight the activations by their respective pooled gradients
        activations = self.activations[0] # [Channels, H, W]
        for i in range(len(pooled_gradients)):
            activations[i, :, :] *= pooled_gradients[i]
            
        # Average channel activations and apply ReLU (we only care about positive influences)
        heatmap = torch.mean(activations, dim=0).cpu().numpy()
        heatmap = np.maximum(heatmap, 0)
        
        # Normalize between 0 and 1
        max_val = np.max(heatmap)
        if max_val > 0:
            heatmap /= max_val
            
        return heatmap

    def overlay_heatmap(
        self,
        original_image: Image.Image,
        heatmap: np.ndarray,
        alpha: float = 0.5,
        colormap: int = cv2.COLORMAP_JET,
        draw_legend: bool = True
    ) -> Image.Image:
        """
        Resizes and blends the Grad-CAM heatmap over the original radiograph.
        - alpha: Opacity of heatmap (0.0 = only original image, 1.0 = only heatmap)
        - draw_legend: Annotates an intuitive color interpretation badge in the image corner.
        """
        orig_w, orig_h = original_image.size
        
        # Resize heatmap to match original image dimensions
        resized_heatmap = cv2.resize(heatmap, (orig_w, orig_h))
        
        # Convert heatmap to 8-bit unsigned integer and apply false-color colormap
        heatmap_uint8 = np.uint8(255 * resized_heatmap)
        colored_heatmap = cv2.applyColorMap(heatmap_uint8, colormap)
        colored_heatmap = cv2.cvtColor(colored_heatmap, cv2.COLOR_BGR2RGB)
        
        # Blend original image and colored heatmap
        orig_np = np.array(original_image.convert("RGB"))
        blended = cv2.addWeighted(colored_heatmap, alpha, orig_np, 1.0 - alpha, 0)
        
        if draw_legend:
            # Draw a sleek semi-transparent clinical legend card in the top-right corner
            legend_w, legend_h = min(220, int(orig_w * 0.42)), 115
            margin_x, margin_y = orig_w - legend_w - 12, 12
            
            # Semi-transparent dark background card
            sub_rect = blended[margin_y:margin_y + legend_h, margin_x:margin_x + legend_w]
            dark_card = np.zeros_like(sub_rect)
            blended[margin_y:margin_y + legend_h, margin_x:margin_x + legend_w] = cv2.addWeighted(
                dark_card, 0.72, sub_rect, 0.28, 0
            )
            # Subtle card border
            cv2.rectangle(
                blended,
                (margin_x, margin_y),
                (margin_x + legend_w, margin_y + legend_h),
                (180, 180, 180),
                1
            )
            
            # Title
            cv2.putText(
                blended, "GRAD-CAM COLOR KEY",
                (margin_x + 10, margin_y + 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 255, 255), 1, cv2.LINE_AA
            )
            
            # Items: (Color RGB, Label)
            items = [
                ((255, 40, 40), "Red: High Abnormality Focus"),
                ((255, 215, 0), "Yellow: Moderate Infiltration"),
                ((60, 140, 255), "Blue: Normal / Clear Tissue")
            ]
            
            for idx, (rgb, label) in enumerate(items):
                y_pos = margin_y + 44 + (idx * 24)
                # Colored indicator dot
                cv2.circle(blended, (margin_x + 18, y_pos - 4), 5, rgb, -1)
                cv2.circle(blended, (margin_x + 18, y_pos - 4), 6, (255, 255, 255), 1)
                # Label text
                cv2.putText(
                    blended, label,
                    (margin_x + 32, y_pos),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.36, (240, 240, 240), 1, cv2.LINE_AA
                )
        
        return Image.fromarray(blended)
