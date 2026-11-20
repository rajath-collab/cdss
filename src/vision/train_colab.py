# src/vision/train_colab.py
# CDSS Vision Training - Uses CDSSVisionModel from model.py
# Usage in Colab:
# !python src/vision/train_colab.py --data_dir /content/drive/MyDrive/cdss_data --epochs 10

import argparse
import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from sklearn.metrics import classification_report, confusion_matrix
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from src.vision.model import CDSSVisionModel, apply_clahe

def get_args():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", type=str, default="data/vision",
                   help="Folder with train/ and val/ subfolders, each with class folders inside")
    p.add_argument("--epochs", type=int, default=10)
    p.add_argument("--batch_size", type=int, default=32)
    p.add_argument("--lr", type=float, default=0.001)
    p.add_argument("--out", type=str, default="models/vision_resnet50.pth")
    p.add_argument("--img_size", type=int, default=224)
    return p.parse_args()

def main():
    args = get_args()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    train_tf = transforms.Compose([
        transforms.Resize((args.img_size, args.img_size)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(10),
        transforms.ToTensor(),
        transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
    ])
    val_tf = transforms.Compose([
        transforms.Resize((args.img_size, args.img_size)),
        transforms.ToTensor(),
        transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
    ])

    train_ds = datasets.ImageFolder(os.path.join(args.data_dir, "train"), transform=train_tf)
    val_ds = datasets.ImageFolder(os.path.join(args.data_dir, "val"), transform=val_tf)
    print(f"Classes: {train_ds.classes} | Train: {len(train_ds)} | Val: {len(val_ds)}")

    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=args.batch_size)

    # USE THE REAL PROJECT MODEL - 3 classes, same as model.py
    model = CDSSVisionModel(num_classes=len(train_ds.classes), pretrained=True).to(device)
    print(f"Model classes: {model.classes}")

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)

    for epoch in range(args.epochs):
        model.train()
        total_loss, correct, total = 0, 0, 0
        for x, y in train_loader:
            x, y = x.to(device), y.to(device)
            optimizer.zero_grad()
            out = model(x)
            loss = criterion(out, y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item() * x.size(0)
            correct += (out.argmax(1) == y).sum().item()
            total += x.size(0)
        print(f"Epoch {epoch+1}/{args.epochs} Loss: {total_loss/total:.4f} Acc: {correct/total:.4f}")

    # Evaluation
    model.eval()
    all_true, all_pred = [], []
    with torch.no_grad():
        for x, y in val_loader:
            out = model(x.to(device))
            all_pred.extend(out.argmax(1).cpu().numpy())
            all_true.extend(y.numpy())
    print(classification_report(all_true, all_pred, target_names=train_ds.classes))
    print("Confusion Matrix:\n", confusion_matrix(all_true, all_pred))

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    torch.save(model.state_dict(), args.out)
    print(f"Saved to {args.out} - Compatible with model.py and gradcam.py")

if __name__ == "__main__":
    main()
