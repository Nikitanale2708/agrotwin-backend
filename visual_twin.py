import cv2
import numpy as np
import os
import uuid

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# 🔥 REALISTIC DISEASE EFFECT
def apply_disease_effect(image, intensity, seed):

    img = image.copy()

    h, w, _ = img.shape

    # ✅ SAME pattern every time (IMPORTANT)
    np.random.seed(seed)

    # 🔥 number of spots based on intensity
    num_spots = int(intensity * 80)

    for _ in range(num_spots):

        x = np.random.randint(0, w)
        y = np.random.randint(0, h)

        radius = int(3 + intensity * 10)

        # 🔴 color changes with severity
        color = (
            int(20 * intensity),   # blue
            int(40 * intensity),   # green
            int(150 + 50 * intensity)  # red
        )

        cv2.circle(img, (x, y), radius, color, -1)

    # 🔥 blur for realism
    if intensity > 0.3:
        img = cv2.GaussianBlur(img, (5, 5), 0)

    return img


# 🔥 MAIN FUNCTION
def generate_visual_twin(image_path, disease_curve):

    img = cv2.imread(image_path)

    if img is None:
        return []

    # 🔥 Resize huge phone camera images to prevent Render Free Tier Timeouts
    h, w = img.shape[:2]
    max_dim = 800
    if max(h, w) > max_dim:
        scale = max_dim / max(h, w)
        img = cv2.resize(img, (int(w * scale), int(h * scale)))

    outputs = []

    # ✅ unique id for each request
    unique_id = str(uuid.uuid4())

    for day_data in disease_curve:

        day = day_data["day"]
        intensity = day_data["spread"] / 100

        # 🔥 stable seed (same pattern progression)
        seed = day * 10

        new_img = apply_disease_effect(img, intensity, seed)

        filename = f"{unique_id}_day_{day}.jpg"
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        cv2.imwrite(filepath, new_img)

        outputs.append({
            "day": day,
            "image": f"/images/{filename}"   # ✅ Android friendly URL
        })

    return outputs