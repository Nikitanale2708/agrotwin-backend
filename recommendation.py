import joblib

# ✅ Load models
pest_model = joblib.load("../model/pesticide_model.pkl")
fert_model = joblib.load("../model/fertilizer_model.pkl")

# ✅ Load encoders
le_soil = joblib.load("../model/le_soil.pkl")
le_crop = joblib.load("../model/le_crop.pkl")
le_target = joblib.load("../model/le_target.pkl")

# ✅ Disease encoding
disease_map = {
    "Healthy": 0,
    "Rust": 1,
    "Redrot": 2,
    "Mosaic": 3,
    "Yellow": 4
}


# ---------------- PESTICIDE ----------------
def get_pesticide(disease, severity, weather=None):

    if disease not in disease_map:
        return "❓ Data not available"

    if disease == "Healthy":
        return "🌿 No pesticide needed"

    rain = weather.get("rainfall", 0) if weather else 0

    if severity == "low":
        return "⚠️ Monitor crop, no pesticide needed now"

    pest = pest_model.predict([[disease_map[disease]]])[0]

    if rain > 120:
        return f"{pest} (⏳ Apply after rain)"

    if severity == "high":
        return f"{pest} (🚨 Urgent treatment required)"

    return f"{pest} (Recommended)"


# ---------------- FERTILIZER ----------------
def get_fertilizer(weather=None, soil=None):

    try:
        temp = weather.get("temperature", 30) if weather else 30
        rain = weather.get("rainfall", 100) if weather else 100

        N = soil.get("Nitrogen", 50) if soil else 50
        P = soil.get("Phosphorus", 40) if soil else 40
        K = soil.get("Potassium", 40) if soil else 40
        pH = soil.get("pH", 6.5) if soil else 6.5
        soil_type = soil.get("soil_type", "Black") if soil else "Black"

        # 🌦 Adjustment
        if rain > 150:
            N -= 10
        elif rain < 50:
            K += 5

        if temp > 35:
            N += 5

        # Encode
        try:
            soil_encoded = le_soil.transform([soil_type])[0]
        except:
            soil_encoded = le_soil.transform(["Black"])[0]

        crop_encoded = le_crop.transform(["Sugarcane"])[0]

        data = [[
            soil_encoded,
            N,
            P,
            K,
            pH,
            rain,
            temp,
            crop_encoded
        ]]

        pred = fert_model.predict(data)
        fert = le_target.inverse_transform(pred)[0]

        if rain > 120:
            return f"{fert} (Apply after rain)"
        elif temp > 35:
            return f"{fert} (Use with irrigation)"
        else:
            return f"{fert} (Apply as recommended)"

    except:
        return "⚠️ Fertilizer unavailable"


# ---------------- FINAL ----------------
def get_recommendation(disease, weather=None, severity="low", soil=None):

    pesticide = get_pesticide(disease, severity, weather)
    fertilizer = get_fertilizer(weather, soil)

    return {
        "pesticide": pesticide,
        "fertilizer": fertilizer
    }