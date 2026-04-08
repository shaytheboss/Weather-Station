import streamlit as st
import requests
from datetime import datetime

# הגדרות עיצוב UI/UX Expert
st.set_page_config(page_title="SkyCast Pro", page_icon="✈️", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    div[data-testid="stImage"] img { border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

def get_weather(icao):
    token = "_uQltLt28HcleET_j3ys_OOlLJdnzmwQS5hqJQ3b9t0"
    url = f"https://avwx.rest/api/metar/{icao}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        res = requests.get(url, headers=headers)
        return res.json() if res.status_code == 200 else None
    except:
        return None

st.title("✈️ SkyCast Pro Station")
st.write("ניטור אטמוספרי בזמן אמת מנתוני מטוסים")

cities = {
    "תל אביב (LLBG)": "LLBG",
    "לונדון (EGLL)": "EGLL",
    "ניו יורק (KJFK)": "KJFK",
    "פריז (LFPG)": "LFPG",
    "לרנקה (LCLK)": "LCLK"
}

col_sel, col_ref = st.columns([3, 1])
with col_sel:
    selected_city = st.selectbox("בחר עיר:", list(cities.keys()))
with col_ref:
    st.write(" ") # מרווח
    refresh = st.button("🔄 רענן")

icao = cities[selected_city]
data = get_weather(icao)

if data:
    temp = data['temperature']['value']
    press = data['altimeter']['value']
    wind = data['wind_speed']['value']
    raw = data['raw']
    
    # בחירת תמונה לפי מזג אוויר
    raw_l = raw.lower()
    if any(x in raw_l for x in ['ra', 'dz', 'sh']): 
        img = "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?w=500"
        status = "גשום 🌧️"
    elif any(x in raw_l for x in ['fg', 'br']):
        img = "https://images.unsplash.com/photo-1487621167305-5d248087c724?w=500"
        status = "ערפל 🌫️"
    elif 'ovc' in raw_l or 'bkn' in raw_l:
        img = "https://images.unsplash.com/photo-1483977399921-6cf3832f7c44?w=500"
        status = "מעונן ☁️"
    else:
        img = "https://images.unsplash.com/photo-1592210633469-a15766827030?w=500"
        status = "בהיר ☀️"

    st.image(img, use_container_width=True)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("טמפרטורה", f"{temp}°C")
    c2.metric("לחץ", f"{press} hPa")
    c3.metric("רוח", f"{wind} KT")

    st.info(f"📊 **סטטוס:** {status}")
    with st.expander("נתוני METAR גולמיים"):
        st.code(raw)
else:
    st.error("שגיאה במשיכת נתונים.")
  
