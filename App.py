import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime

# הגדרות מערכת
st.set_page_config(page_title="SkyCast Analytics", page_icon="📈", layout="wide")

# CSS מתקדם ל-Dashboard כהה
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: #e6edf3; }
    .stMetric { background: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 15px; }
    .status-box { padding: 20px; border-radius: 15px; margin-bottom: 20px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

def get_weather(icao):
    token = "_uQltLt28HcleET_j3ys_OOlLJdnzmwQS5hqJQ3b9t0"
    url = f"https://avwx.rest/api/metar/{icao}"
    try:
        res = requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=10)
        return res.json() if res.status_code == 200 else None
    except: return None

# כותרת
st.title("📡 SKYCAST ANALYTICS PRO")
st.markdown("---")

# תפריט צדדי לבחירה
with st.sidebar:
    st.header("Settings")
    cities = {"Tel Aviv": "LLBG", "London": "EGLL", "New York": "KJFK", "Paris": "LFPG", "Larnaca": "LCLK", "Tokyo": "RJTT"}
    sel_name = st.selectbox("Select Target Station", list(cities.keys()))
    icao = cities[sel_name]
    refresh = st.button("FORCE REFRESH 🔄")

data = get_weather(icao)

if data:
    # שליפת נתונים
    temp = data.get('temperature', {}).get('value', 0)
    press = data.get('altimeter', {}).get('value', 1013)
    wind = data.get('wind_speed', {}).get('value', 0)
    raw = data.get('raw', '')
    lat = data.get('meta', {}).get('latitude', 32.0)
    lon = data.get('meta', {}).get('longitude', 34.8)

    # לוגיקת תמונה ותצוגה חכמה
    raw_l = raw.lower()
    img = "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1200" # Default Mountain
    status_msg = "STABLE"
    
    if any(x in raw_l for x in ['ra', 'dz', 'sh', 'sn']): 
        img = "https://images.unsplash.com/photo-1534274988757-a28bf1a57c17?w=1200"
        status_msg = "PRECIPITATION"
    elif any(x in raw_l for x in ['fg', 'br', 'hz']):
        img = "https://images.unsplash.com/photo-1485236715598-c8879a636a81?w=1200"
        status_msg = "LOW VISIBILITY"
    elif 'ts' in raw_l:
        img = "https://images.unsplash.com/photo-1605727216801-e27ce1d0cc28?w=1200"
        status_msg = "STORM CELL"

    # תצוגה ראשית: תמונה ומדדים
    st.image(img, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("TEMPERATURE", f"{temp}°C")
    col2.metric("PRESSURE", f"{press} hPa", delta=f"{round(press-1013.25, 2)} vs Std")
    col3.metric("WIND SPEED", f"{wind} KT")

    st.markdown("---")

    # פיצ'ר חדש: מפת מיקום השדה
    st.subheader(f"📍 Station Location: {sel_name}")
    map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})
    st.map(map_data, zoom=10)

    # פיצ'ר חדש: גרף סימולציית מגמה (Trend Analysis)
    # מכיוון שה-API החינמי לא נותן היסטוריה, אנחנו יוצרים סימולציה של ה-24 שעות האחרונות המבוססת על הלחץ הנוכחי
    st.subheader("📊 24h Pressure Trend (Analytical Simulation)")
    chart_data = pd.DataFrame(
        np.random.randn(24, 1) * 0.5 + press,
        columns=['Pressure (hPa)']
    )
    st.line_chart(chart_data)

    # ניתוח מערכת
    st.subheader("🔍 AI Tactical Analysis")
    with st.container():
        if press < 1005:
            st.error(f"CRITICAL: Extreme Low Pressure detected at {icao}. Expected heavy turbulence and rapid weather deterioration.")
        elif press < 1010:
            st.warning("CAUTION: Frontal system approaching. Watch for wind shear.")
        else:
            st.success("NOMINAL: High pressure dominance. Clear operational conditions.")

    with st.expander("TECHNICAL RAW DATA"):
        st.code(raw)

else:
    st.error("Connection Timeout: Unable to reach Aviation Servers.")
    
