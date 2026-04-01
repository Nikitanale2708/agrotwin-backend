import requests
import json

def get_soil_data(lat, lon):

    try:
        # 🌍 Reverse geolocation
        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
        res = requests.get(url).json()

        # 🔥 Smart district detection
        district = (
            res["address"].get("state_district") or
            res["address"].get("county") or
            res["address"].get("state")
        )

        # 🔥 Normalize
        district = district.lower().replace(" district", "").strip()

        # 📂 Load soil DB
        with open("soil_data.json") as f:
            soil_db = json.load(f)

        # 🔍 Smart match
        for key in soil_db:
            if key.lower() in district:
                print("🌱 Matched Soil District:", key)
                return soil_db[key]

        print("⚠️ Soil not found, using default")

        # fallback
        return {
            "Nitrogen": 50,
            "Phosphorus": 40,
            "Potassium": 40,
            "pH": 6.5,
            "soil_type": "Black"
        }

    except Exception as e:
        print("❌ Soil Error:", e)

        return {
            "Nitrogen": 50,
            "Phosphorus": 40,
            "Potassium": 40,
            "pH": 6.5,
            "soil_type": "Black"
        }