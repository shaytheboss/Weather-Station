import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timezone

# הגדרות דף Elite
st.set_page_config(page_title="SKYCAST ELITE | OSINT Weather", page_icon="⚡", layout="wide")

# CSS מתקדם ל-UI/UX ברמה הגבוהה ביותר
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;600&display=swap');
    
    .stApp { background-color: #05070a; color: #e6edf3; }
    .metric-container {
        background: rgba(23, 27, 33, 0.8);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
    }
    .main-title {
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 5px;
        background: linear-gradient(90deg, #58a6ff, #bc8cff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
    }
    .status-bar {
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

def get_weather_data(icao):
    token = "_uQltLt28HcleET_j3ys_OOlLJdnzmwQS5hqJQ3b9t0"
    url = f"https://avwx.rest/api/metar/{icao}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        res = requests.get(url, headers=headers)
        return res.json() if res.status_code == 200 else None
    except: return None

# ניהול מצב (State) למעקב אחר מגמת לחץ
if 'last_press' not in st.session_state:
    st.session_state.last_press = {}

# Header
st.markdown("<h1 class='main-title'>SKYCAST ELITE</h1>", unsafe_allow_html=True)
utc_now = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")
st.markdown(f"<p style='text-align: center; color: #8b949e;'>SYSTEM TIME: {utc_now} | SECURE DATA LINK ACTIVE</p>", unsafe_allow_html=True)

# Sidebar Control
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2503/2503508.png", width=100)
    st.markdown("### COMMAND CENTER")
    cities = {
        "TEL AVIV (LLBG)": "LLBG",
        "LONDON (EGLL)": "EGLL",
        "NEW YORK (KJFK)": "KJFK",
        "TOKYO (RJTT)": "RJTT",
        "LARNACA (LCLK)": "LCLK"
    }
    selected_city = st.selectbox("TARGET LOCATION", list(cities.keys()))
    icao = cities[selected_city]
    refresh = st.button("SYNC SENSORS")

data = get_weather_data(icao)

if data:
    temp = data['temperature']['value']
    press = data['altimeter']['value']
    wind = data['wind_speed']['value']
    raw = data['raw']
    
    # 1. חישוב מגמת לחץ (Trend)
    trend_icon = "➡️"
    if icao in st.session_state.last_press:
        prev = st.session_state.last_press[icao]
        if press > prev: trend_icon = "📈 RISING"
        elif press < prev: trend_icon = "📉 DROPPING"
    st.session_state.last_press[icao] = press

    # 2. ניתוח חכם (Expert Analysis)
    raw_l = raw.lower()
    if 'ts' in raw_l: status, color = "THUNDERSTORM ALERT ⛈️", "#ff4b4b"
    elif 'ra' in raw_l: status, color = "PRECIPITATION ACTIVE 🌧️", "#37a0ea"
    elif 'fg' in raw_l: status, color = "LOW VISIBILITY / FOG 🌫️", "#8b949e"
    else: status, color = "OPTIMAL CONDITIONS ☀️", "#00d4ff"

    st.markdown(f"<div class='status-bar' style='background: {color}22; color: {color}; border: 1px solid {color};'>{status}</div>", unsafe_allow_html=True)

    # 3. תצוגת מדדים (Metrics Dashboard)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='metric-container'><small>TEMPERATURE</small><h2>{temp}°C</h2></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-container'><small>PRESSURE</small><h2>{press} h
        
