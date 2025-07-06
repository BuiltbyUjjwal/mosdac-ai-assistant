import openai
import requests
import streamlit as st
import pandas as pd

# -------------------- API Setup --------------------
openai.api_key = st.secrets["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"]

openai.api_base = "https://openrouter.ai/api/v1"

def ask_bot(prompt):
    response = openai.ChatCompletion.create(
        model="mistralai/mistral-7b-instruct",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message['content']

# -------------------- Weather Info --------------------
def get_weather(city):
    coords = {
        "mumbai": (19.0760, 72.8777),
        "delhi": (28.6139, 77.2090),
        "nagpur": (21.1458, 79.0882),
        "chennai": (13.0827, 80.2707),
        "kolkata": (22.5726, 88.3639),
        "pune": (18.5204, 73.8567)
    }
    city = city.lower()
    if city not in coords:
        return "City not found in the database."
    lat, lon = coords[city]
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,precipitation,windspeed_10m"
    r = requests.get(url)
    if r.status_code != 200:
        return "Weather data not available."
    data = r.json()['current']
    return f"🌤️ Weather in {city.title()}:\n- Temperature: {data['temperature_2m']}°C\n- Precipitation: {data['precipitation']} mm\n- Wind: {data['windspeed_10m']} km/h"

# -------------------- App Interface --------------------
st.set_page_config(page_title="MOSDAC AI Assistant", page_icon="🛰️")

st.title("🛰️ MOSDAC AI Assistant")
st.write("Ask anything about satellites, rainfall, or weather!")

user_input = st.text_input("Your Question:")

if st.button("Ask"):
    if "weather" in user_input.lower():
        for city in ["mumbai", "delhi", "nagpur", "chennai", "kolkata", "pune"]:
            if city in user_input.lower():
                weather = get_weather(city)
                st.success(weather)
                break
        else:
            st.info("Please mention a supported city for weather info.")
    elif "rainfall" in user_input.lower():
        df = pd.read_csv("rainfall_sample.csv")
        st.subheader("📊 Rainfall Data")
        st.dataframe(df)
    elif "satellite image" in user_input.lower():
        st.image("satellite_image.png", caption="Sample Satellite Image", use_column_width=True)
    elif "mosdac" in user_input.lower() or "insat" in user_input.lower() or "megha-tropiques" in user_input.lower():
        with open("mosdac_knowledge.txt", "r") as file:
            context = file.read()
        full_prompt = f"{context}\n\nUser: {user_input}\nAssistant:"
        answer = ask_bot(full_prompt)
        st.write(answer)
    else:
        answer = ask_bot(user_input)
        st.write(answer)
