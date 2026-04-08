import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# הגדרות דף - עיצוב אדפטיבי (Adaptive UI)
st.set_page_config(page_title="SkyCast Tactical v5", layout="wide")

# CSS לשיפור נראות ב-Light/Dark Mode וכרטיסים מעוצבים
st.markdown("""
    <style>
    .reportview-container { background: #f0f2f6; }
    .metric-card {
        border: 1px solid #d1d5db;
        border-radius: 12px;
        padding: 15px;
        background-color: rgba(128, 128, 128, 0.05);
    }
    h1 { margin-bottom: 0px; }
    </style>
    """, unsafe_allow_html=True)

# אתחול היסטוריה בזיכרון (Session State)
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=['Time', 'Pressure', 'Temp'])

def get_weather(icao):
    token = "_uQltLt28HcleET_j3ys_OOlLJdnzmwQS5hqJQ3b9t0"
    url = f"https://avwx.rest/api/metar/{icao}"
    try:
        res = requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=10)
        return res.json() if res.status_code == 200 else None
    except: return None

# תפריט צד
with st.sidebar:
    st.header("SENSORS CONTROL")
    cities = {
        "Tel Aviv (Ben Gurion)": "LLBG",
        "London (Heathrow)": "EGLL",
        "New York (JFK)": "KJFK",
        "Larnaca (Cyprus)": "LCLK",
        "Tokyo (Haneda)": "RJTT"
    }
    sel_name = st.selectbox("Select Station", list(cities.keys()))
    icao = cities[sel_name]
    refresh = st.button("EXECUTE DATA REFRESH 🔄")

data = get_weather(icao)

if data:
    # שליפת נתונים
    temp = data.get('temperature', {}).get('value', 0)
    press = data.get('altimeter', {}).get('value', 1013)
    wind = data.get('wind_speed', {}).get('value', 0)
    vis = data.get('visibility', {}).get('value', "N/A")
    raw = data.get('raw', '')
    flight_rules = data.get('flight_rules', 'VFR')
    
    # עדכון היסטוריה (כדי שהגרף יתחיל לזוז)
    current_time = datetime.now().strftime("%H:%M:%S")
    new_entry = pd.DataFrame([[current_time, press, temp]], columns=['Time', 'Pressure', 'Temp'])
    st.session_state.history = pd.concat([st.session_state.history, new_entry], ignore_index=True).tail(15)

    # לוגיקת סטטוס ויזואלי (Icons & Colors)
    raw_l = raw.lower()
    if 'ts' in raw_l: icon, status, color = "⛈️", "THUNDERSTORM", "#FF4B4B"
    elif any(x in raw_l for x in ['ra
                                  
