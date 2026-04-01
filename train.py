import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
import timm
from collections import Counter

import os

# ---------------- DEVICE ----------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "model")
os.makedirs(MODEL_DIR, exist_ok=True)

# ---------------- PATHS ----------------
train_dir = os.path.join(BASE_DIR, "..", "dataset", "train")
val_dir   = os.path.join(BASE_DIR, "..", "dataset", "val")

# ---------------- TRANSFORMS (FIXED ✅) ----------------
transform_train = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor(),
    transforms.Normalize(   # 🔥 IMPORTANT FIX
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

transform_val = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize(   # 🔥 SAME AS TRAIN
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# ---------------- DATA LOAD ----------------
train_data = datasets.ImageFolder(train_dir, transform=transform_train)
val_data   = datasets.ImageFolder(val_dir, transform=transform_val)

train_loader = torch.utils.data.DataLoader(train_data, batch_size=16, shuffle=True)
val_loader   = torch.utils.data.DataLoader(val_data, batch_size=16)

class_names = train_data.classes
print("Classes:", class_names)

# ---------------- CLASS DISTRIBUTION CHECK ----------------
print("\nClass Distribution:")
print(Counter(train_data.targets))

# ---------------- MODEL ----------------
model = timm.create_model(
    "efficientnet_b0",
    pretrained=True,
    num_classes=len(class_names)
)
model = model.to(device)

# ---------------- LOSS & OPTIMIZER ----------------
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.0003)  # 🔥 FIXED LR

# ---------------- TRAINING ----------------
epochs = 20   # 🔥 FIXED (was 5)

best_val_acc = 0

for epoch in range(epochs):
    model.train()
    total_loss = 0
    correct = 0
    total = 0

    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)

        outputs = model(images)
        loss = criterion(outputs, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

        _, preds = torch.max(outputs, 1)
        correct += (preds == labels).sum().item()
        total += labels.size(0)

    train_acc = correct / total

    # ---------------- VALIDATION ----------------
    model.eval()
    val_correct = 0
    val_total = 0

    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)

            outputs = model(images)
            _, preds = torch.max(outputs, 1)

            val_correct += (preds == labels).sum().item()
            val_total += labels.size(0)

    val_acc = val_correct / val_total

    print(f"\nEpoch {epoch+1}/{epochs}")
    print(f"Loss: {total_loss:.4f}")
    print(f"Train Acc: {train_acc:.4f}")
    print(f"Val Acc: {val_acc:.4f}")
    print("-"*50)

    # 🔥 SAVE BEST MODEL ONLY
    if val_acc > best_val_acc:
        best_val_acc = val_acc
        torch.save(model.state_dict(), os.path.join(MODEL_DIR, "model.pth"))
        print("✅ Best model saved!")

# ---------------- SAVE CLASS NAMES ----------------
with open(os.path.join(MODEL_DIR, "classes.txt"), "w") as f:
    for c in class_names:
        f.write(c + "\n")

print("\n✅ Training complete!")
print(f"Best Validation Accuracy: {best_val_acc:.4f}")