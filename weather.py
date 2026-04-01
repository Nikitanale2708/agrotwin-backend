import requests

API_KEY = "ae1a0d0abff5b8cbe38cfa4bc3743ead"

def get_weather(lat, lon):

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

    res = requests.get(url)
    data = res.json()

    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    rainfall = data.get("rain", {}).get("1h", 0)

    return {
        "temperature": temperature,
        "humidity": humidity,
        "rainfall": rainfall
    }