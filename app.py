from fastapi import FastAPI, UploadFile, File
import shutil
import os
import uuid

from model import predict_disease
from simulation import digital_twin
from recommendation import get_recommendation
from weather import get_weather
from visual_twin import generate_visual_twin
from soil import get_soil_data

from fastapi.staticfiles import StaticFiles

# 🚫 Swagger removed (production)
app = FastAPI()

# ✅ Static images
app.mount("/images", StaticFiles(directory="../uploads"), name="images")

UPLOAD_FOLDER = "../uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/")
def home():
    return {"message": "AI Agriculture API Running 🚀"}


# 🔥 Severity logic
def get_severity(disease, conf):

    if disease == "Healthy":
        return "none"
    elif conf < 0.2:
        return "low"
    elif conf < 0.4:
        return "medium"
    else:
        return "high"


# 🎨 UI color
def get_color(severity):
    return {
        "none": "green",
        "low": "yellow",
        "medium": "orange",
        "high": "red"
    }[severity]


# 🧠 Farmer message
def get_farmer_message(severity):
    return {
        "none": "🌿 Aapka fasal healthy hai",
        "low": "⚠️ Thodi bimari hai, dhyan rakhe",
        "medium": "❗ Bimari badh rahi hai, ilaaj kare",
        "high": "🚨 Gambhir bimari hai, turant dawa use kare"
    }[severity]


@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    lat: float = 19.07,
    lon: float = 72.87
):

    try:
        # ✅ Save file
        filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 🔥 Disease
        result = predict_disease(file_path)
        disease = result.get("disease", "Unknown")
        conf = result.get("confidence", 0.0)

        # 🔥 Severity
        severity = get_severity(disease, conf)

        # 🌦 Weather
        weather = get_weather(lat, lon)

        # 🌱 Soil (FIXED)
        soil = get_soil_data(lat, lon)

        print("🌱 Soil:", soil)
        print("🌦 Weather:", weather)
        print("🧠 Disease:", disease, conf)

        # 🔥 Digital Twin
        twin = digital_twin(7, severity, weather)

        # 🔥 Visual Twin
        visual = generate_visual_twin(file_path, twin["disease_curve"])

        # 🔥 Recommendation
        rec = get_recommendation(disease, weather, severity, soil)

        # 🧹 Cleanup
        if os.path.exists(file_path):
            os.remove(file_path)

        return {
            "disease": disease,
            "confidence": round(conf, 3),
            "severity": severity,
            "color": get_color(severity),
            "message": get_farmer_message(severity),

            "twin": twin,
            "visual_twin": visual,

            "weather": weather,
            "soil": soil,

            "recommendation": rec
        }

    except Exception as e:
        return {"error": str(e)}