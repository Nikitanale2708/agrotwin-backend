import os
import shutil
import random

# ✅ FIX: raw string (r"...") use karo
source_dir = r"E:\OneDrive\Documents\dt"
train_dir  = r"E:\OneDrive\Documents\Digital_Twin\dataset\train"
val_dir    = r"E:\OneDrive\Documents\Digital_Twin\dataset\val"

split_ratio = 0.8

for cls in os.listdir(source_dir):
    cls_path = os.path.join(source_dir, cls)

    # ✅ skip non-folder files
    if not os.path.isdir(cls_path):
        continue

    images = os.listdir(cls_path)
    random.shuffle(images)

    split = int(len(images) * split_ratio)

    train_imgs = images[:split]
    val_imgs = images[split:]

    os.makedirs(os.path.join(train_dir, cls), exist_ok=True)
    os.makedirs(os.path.join(val_dir, cls), exist_ok=True)

    for img in train_imgs:
        shutil.copy(
            os.path.join(cls_path, img),
            os.path.join(train_dir, cls, img)
        )

    for img in val_imgs:
        shutil.copy(
            os.path.join(cls_path, img),
            os.path.join(val_dir, cls, img)
        )

print("✅ Dataset split done!")