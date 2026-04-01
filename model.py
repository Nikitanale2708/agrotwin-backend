import torch
import timm
from torchvision import transforms
from PIL import Image
import numpy as np

device = torch.device("cpu")

with open("../model/classes.txt", "r") as f:
    class_names = [line.strip() for line in f.readlines()]

model = timm.create_model(
    "efficientnet_b0",
    pretrained=False,
    num_classes=len(class_names)
)

model.load_state_dict(torch.load("../model/model.pth", map_location=device))
model.eval()

# ✅ FIXED TRANSFORM
transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

def predict_disease(img_path):
    try:
        img = Image.open(img_path).convert("RGB")
        img = transform(img).unsqueeze(0)

        with torch.no_grad():
            outputs = model(img)

            probs = torch.softmax(outputs, dim=1)[0].numpy()
            pred_idx = np.argmax(probs)

            confidence = probs[pred_idx]

        return {
            "disease": class_names[pred_idx],
            "confidence": float(confidence)
        }

    except Exception as e:
        return {
            "disease": "Unknown",
            "confidence": 0.0,
            "error": str(e)
        }