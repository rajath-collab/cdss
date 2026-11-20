# src/vision/train_colab.py
# CDSS Vision Training - Run in Google Colab
# Usage in Colab:
# !python src/vision/train_colab.py --data_dir /content/drive/MyDrive/cdss_data --epochs 10

import argparse
import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms
from sklearn.metrics import classification_report, confusion_matrix

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
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    val_tf = transforms.Compose([
        transforms.Resize((args.img_size, args.img_size)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])

    train_ds = datasets.ImageFolder(os.path.join(args.data_dir, "train"), transform=train_tf)
    val_ds = datasets.ImageFolder(os.path.join(args.data_dir, "val"), transform=val_tf)
    print(f"Classes: {train_ds.classes}")
    print(f"Train: {len(train_ds)} | Val: {len(val_ds)}")

    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=args.batch_size)

    model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
    model.fc = nn.Linear(model.fc.in_features, len(train_ds.classes))
    model = model.to(device)

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
            total_loss += loss.item()
            correct += (out.argmax(1) == y).sum().item()
            total += y.size(0)
        print(f"Epoch {epoch+1}/{args.epochs} - Loss: {total_loss/len(train_loader):.4f} - Train Acc: {correct/total:.4f}")

        # Validation
        model.eval()
        all_pred, all_true = [], []
        with torch.no_grad():
            for x, y in val_loader:
                pred = model(x.to(device)).argmax(1).cpu()
                all_pred.extend(pred.tolist())
                all_true.extend(y.tolist())
        print(classification_report(all_true, all_pred, target_names=train_ds.classes))
        print(confusion_matrix(all_true, all_pred))

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    torch.save({"model": model.state_dict(), "classes": train_ds.classes}, args.out)
    print(f"Saved to {args.out}")

if __name__ == "__main__":
    main()
