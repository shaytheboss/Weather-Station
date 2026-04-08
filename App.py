import streamlit as st
import requests

# UI/UX Setup
st.set_page_config(page_title="SkyCast Elite", page_icon="📡", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; font-family: 'Inter', sans-serif; }
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px; padding: 20px; text-align: center;
    }
    .stButton>button {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        color: white; border-radius: 12px; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

def get_weather(icao):
    token = "_uQltLt28HcleET_j3ys_OOlLJdnzmwQS5hqJQ3b9t0"
    url = f"https://avwx.rest/api/metar/{icao}"
    try:
        res = requests.get(url, headers={"Authorization": f"Bearer {token}"})
        return res.json() if res.status_code == 200 else None
    except: return None

st.markdown("<h1 style='text-align: center;'>SKYCAST <span style='color: #4facfe;'>ELITE</span></h1>", unsafe_allow_html=True)

cities = {"Tel Aviv": "LLBG", "London": "EGLL", "New York": "KJFK", "Paris": "LFPG", "Larnaca": "LCLK"}
sel_city = st.selectbox("", list(cities.keys()))
if st.button("RECALIBRATE"): st.rerun()

data = get_weather(cities[sel_city])

if data:
    temp, press, wind, raw = data['temperature']['value'], data['altimeter']['value'], data['wind_speed']['value'], data['raw']
    
    # Image Logic
    img = "https://images.unsplash.com/photo-1504608524841-42fe6f032b4b?w=800"
    if any(x in raw.lower() for x in ['ra', 'dz', 'sh']): img = "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?w=800"
    
    st.image(img, use_container_width=True)
    
    # Metrics
    m1, m2, m3 = st.columns(3)
    m1.markdown(f"<div class='metric-card'><small>TEMP</small><h2>{temp}°C</h2></div>", unsafe_allow_html=True)
    m2.markdown(f"<div class='metric-card'><small>PRESSURE</small><h2>{press} hPa</h2></div>", unsafe_allow_html=True)
    m3.markdown(f"<div class='metric-card'><small>WIND</small><h2>{wind} KT</h2></div>", unsafe_allow_html=True)

    st.markdown(f"### 🛡️ System Analysis")
    if press < 1010: st.warning("Low Pressure: Instability detected.")
    else: st.success("Stable High Pressure.")
    
    with st.expander("RAW METAR"): st.code(raw)
        
