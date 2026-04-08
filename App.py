import streamlit as st
import requests

# UI Setup
st.set_page_config(page_title="SkyCast Tactical", layout="wide")

st.markdown("""
    <style>
    .metric-card {
        border: 2px solid #4facfe;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

def get_data(icao):
    tkn = "_uQltLt28HcleET_j3ys_OOlLJdnzmwQS5hqJQ3b9t0"
    url = f"https://avwx.rest/api/metar/{icao}"
    try:
        r = requests.get(url, headers={"Authorization": f"Bearer {tkn}"})
        return r.json() if r.status_code == 200 else None
    except: return None

# Sidebar
st.sidebar.title("STATION SELECT")
cities = {"Tel Aviv": "LLBG", "London": "EGLL", "NY": "KJFK", "Larnaca": "LCLK"}
sel = st.sidebar.selectbox("City", list(cities.keys()))
if st.sidebar.button("REFRESH"): st.rerun()

data = get_data(cities[sel])

if data:
    # Basic Specs
    val = lambda k: data.get(k, {}).get('value', 'N/A')
    temp, press, wind = val('temperature'), val('altimeter'), val('wind_speed')
    vis, dew, hum = val('visibility'), val('dewpoint'), data.get('relative_humidity', 'N/A')
    raw = data.get('raw', '').lower()

    # Weather Logic (Short lines to avoid errors)
    if 'ts' in raw: icon, status = "⛈️", "STORM"
    elif 'ra' in raw or 'dz' in raw: icon, status = "🌧️", "RAIN"
    elif 'fg' in raw or 'br' in raw: icon, status = "🌫️", "FOG"
    elif 'ovc' in raw or 'bkn' in raw: icon, status = "☁️", "CLOUDY"
    else: icon, status = "☀️", "CLEAR"

    # Display
    st.markdown(f"<h1 style='text-align:center;'>{icon} {status}</h1>", unsafe_allow_html=True)
    
    # Grid System
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"<div class='metric-card'><h3>TEMP</h3><h2>{temp}°C</h2></div>", True)
    c2.markdown(f"<div class='metric-card'><h3>PRESS</h3><h2>{press} hPa</h2></div>", True)
    c3.markdown(f"<div class='metric-card'><h3>WIND</h3><h2>{wind} KT</h2></div>", True)

    st.markdown("### 📊 Advanced Sensors")
    a1, a2, a3 = st.columns(3)
    a1.metric("Visibility", f"{vis} m")
    a2.metric("Humidity", f"{round(hum, 1) if hum != 'N/A' else 'N/A'}%")
    a3.metric("Dew Point", f"{dew}°C")

    # Analysis
    st.info(f"Flight Rules: {data.get('flight_rules', 'N/A')}")
    if press < 1010: st.warning("Low pressure detected. Frontal activity likely.")
    
    with st.expander("RAW DATA"): st.code(data.get('raw', ''))
else:
    st.error("Sensor Offline.")
    
