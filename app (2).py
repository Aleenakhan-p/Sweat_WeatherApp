import streamlit as st
import requests
import os


API_KEY = os.getenv("Weather_App_Key")  # loads from Hugging Face Secrets
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    try:
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"  # Celsius
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if data.get("cod") != 200:
            return None, f"❌ Error: {data.get('message', 'Invalid city')}"

        # Extract weather info
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        weather_desc = data["weather"][0]["description"].capitalize()
        humidity = data["main"]["humidity"]

        # Rain prediction logic
        if "rain" in weather_desc.lower():
            rain_prediction = "☔ High chance of rain!"
        elif humidity > 80:
            rain_prediction = "🌧️ Possible rain (High humidity)."
        else:
            rain_prediction = "☀️ Low chance of rain."

        result = {
            "city": city.title(),
            "temp": temp,
            "feels_like": feels_like,
            "weather_desc": weather_desc,
            "humidity": humidity,
            "rain_prediction": rain_prediction
        }
        return result, None

    except Exception as e:
        return None, f"⚠️ Error: {str(e)}"


# 🎨 Streamlit UI
st.set_page_config(page_title="Weather App", page_icon="🌦️", layout="centered")

st.markdown("<h1 style='text-align: center;'>🌦️Sweat- Simple Weather App</h1>", unsafe_allow_html=True)

city = st.text_input("Enter City", placeholder="e.g., Lahore, London, New York")

if st.button("Get Weather 🌍"):
    weather, error = get_weather(city)
    if error:
        st.error(error)
    else:
        st.success(f"Weather report for **{weather['city']}**")
        st.markdown(f"🌡️ **Temperature:** {weather['temp']}°C (Feels like {weather['feels_like']}°C)")
        st.markdown(f"⛅ **Condition:** {weather['weather_desc']}")
        st.markdown(f"💧 **Humidity:** {weather['humidity']}%")
        st.markdown(f"🔮 **Rain Prediction:** {weather['rain_prediction']}")
