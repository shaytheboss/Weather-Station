import streamlit as st
import requests
import pandas as pd
import time

# הגדרות דף
st.set_page_config(page_title="SkyCast Tactical v4", layout="wide")

# CSS לשיפור ניגודיות ועיצוב מקצועי (עובד מעולה גם בבהיר וגם בכהה)
st.markdown("""
    <style>
    .metric-box {
        border: 2px solid #edeff2;
        border-radius: 15px;
        padding: 20px;
        background-color: rgba(255, 255, 255, 0.05);
        text-align: center;
    }
    .main { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# ניהול היסטוריה בזיכרון של האפליקציה (כדי שהגרף לא יהיה קו ישר)
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
    st.title("控制台 Control") # מראה טכנולוגי
    cities = {"Tel Aviv": "LLBG", "London": "EGLL", "New York": "KJFK", "Larnaca": "LCLK", "Tokyo": "RJTT"}
    sel_name = st.selectbox("Select Station", list(cities.keys()))
    icao = cities[sel_name]
    refresh = st.button("UPDATE SENSORS 🔄")

data = get_weather(icao)

if data:
    # שליפת נתונים מורחבת
    temp = data.get('temperature', {}).get('value', 0)
    press = data.get('altimeter', {}).get('value', 1013)
    wind = data.get('wind_speed', {}).get('value', 0)
    vis = data.get('visibility', {}).get('value', "N/A")
    raw = data.get('raw', '')
    
    # עדכון היסטוריה לגרף (מוסיף נקודה בכל רענון)
    new_entry = pd.DataFrame([[datetime.now().strftime("%H:%M:%S"), press, temp]], columns=['Time', 'Pressure', 'Temp'])
    st.session_state.history = pd.concat([st.session_state.history, new_entry]).tail(20)

    # לוגיקת מצב שמיים ואייקונים
    raw_l = raw.lower()
    if 'ts' in raw_l: icon, status, color = "⛈️", "THUNDERSTORM", "#ff4b4b"
    elif any(x in raw_l for x in ['ra', 'dz', 'sh']): icon, status, color = "🌧️", "RAINY", "#007bff"
    elif any(x in raw_l for x in ['fg', 'br']): icon, status, color = "🌫️", "FOG/MIST", "#6c757d"
    elif 'ovc' in raw_l: icon, status, color = "☁️", "OVERCAST", "#555"
    else: icon, status, color = "☀️", "CLEAR SKIES", "#ffa500"

    # תצוגה ראשית
    st.markdown(f"<h1 style='text-align: center; color: {color};'>{icon} {status}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>Station: {sel_name} ({icao}) | Live Data Stream</p>", unsafe_allow_html=True)

    # מדדים בשורה אחת
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("TEMP", f"{temp}°C")
    c2.metric("PRESSURE", f"{press} hPa")
    c3.metric("WIND", f"{wind} KT")
    c4.metric("VISIBILITY", f"{vis} m")

    st.markdown("---")

    # גרפים אמיתיים (נבנים עם כל רענון)
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.subheader("Pressure Trend (Live)")
        if len(st.session_state.history) > 1:
            st.line_chart(st.session_state.history.set_index('Time')['Pressure'])
        else:
            st.info("Collecting data points... Press 'Update' to build the trend.")
    
    with col_g2:
        st.subheader("Temperature Stability")
        if len(st.session_state.history) > 1:
            st.area_chart(st.session_state.history.set_index('Time')['Temp'])
        else:
            st.info("Wait for next update...")

    # נתונים טכניים נוספים מה-API
    st.subheader("🛠️ Tactical Specs")
    t1, t2 = st.columns(2)
    with t1:
        flight_rules = data.get('flight_rules', 'N/A')
        st.markdown(f"**Flight Rules:** {flight_rules}")
        st.caption("VFR = Visual, IFR = Instrument (Low Visibility)")
    with t2:
        dew = data.get('dewpoint', {}).get('value', 'N/A')
        st.markdown(f"**Dew Point:** {dew}°C")
        st.caption("Cloud formation probability indicator")

    with st.expander("RAW AVIATION METAR"):
        st.code(raw)

else:
    st.error("Station Offline or API Limit reached.")
    
