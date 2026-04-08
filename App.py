import streamlit as st
import requests
from datetime import datetime

# הגדרות דף ברמת פרימיום
st.set_page_config(page_title="SkyCast Pro Dashboard", page_icon="🌤️", layout="wide")

# CSS מתקדם של מומחה UI/UX לעיצוב אדפטיבי ומודרני
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stMetric {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(128, 128, 128, 0.1);
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    
    .main-header {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0px;
    }
    
    div[data-testid="stImage"] img {
        border-radius: 20px;
        box-shadow: 0 10px 15px rgba(0,0,0,0.1);
    }
    
    .stSelectbox {
        margin-top: -20px;
    }
    
    </style>
    """, unsafe_allow_html=True)

def get_weather_data(icao):
    token = "_uQltLt28HcleET_j3ys_OOlLJdnzmwQS5hqJQ3b9t0"
    url = f"https://avwx.rest/api/metar/{icao}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        return res.json() if res.status_code == 200 else None
    except: return None

# כותרת האפליקציה בראש המסך
st.markdown("<h1 class='main-header'>SKYCAST <span style='color: #4facfe;'>PRO</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>ניטור אטמוספרי מתקדם מנתוני תעופה</p>", unsafe_allow_html=True)

# בחירת עיר - ממוקמת בתוך המסך הראשי
cities = {
    "תל אביב (נתבג)": "LLBG",
    "לונדון (היתרו)": "EGLL",
    "ניו יורק (JFK)": "KJFK",
    "פריז (שארל דה גול)": "LFPG",
    "קפריסין (לרנקה)": "LCLK",
    "טוקיו (האנדה)": "RJTT",
    "ברלין (ברנדנבורג)": "EDDB",
    "מוסקבה (שרמטייבו)": "UUEE",
    "דובאי (DBX)": "OMDB",
    "רומא (פיומיצינו)": "LIRF"
}

# שורת שליטה מרכזית
c_sel, c_ref = st.columns([3, 1])
with c_sel:
    selected_name = st.selectbox("בחר יעד:", list(cities.keys()), label_visibility="collapsed")
    icao = cities[selected_name]
with c_ref:
    refresh = st.button("🔄 רענן נתונים")

# משיכת הנתונים
with st.spinner('מתחבר לחיישני המטוסים...'):
    data = get_weather_data(icao)

if data:
    # שליפת נתונים מורחבת
    temp = data['temperature']['value']
    press = data['altimeter']['value']
    wind = data['wind_speed']['value']
    vis = data['visibility']['value']
    dew = data['dewpoint']['value']
    hum = data.get('relative_humidity', 'N/A')
    raw = data['raw']
    
    # --- לוגיקת תמונה דינמית (The Visual UX) ---
    raw_l = raw.lower()
    
    # ברירת מחדל: בהיר/נעים
    img_url = "https://images.unsplash.com/photo-1592210633469-a15766827030?w=1200&q=80"
    weather_desc = "בהיר/נוח"

    if any(x in raw_l for x in ['ra', 'dz', 'sh']): # גשם/טפטוף/ממטרים
        img_url = "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?w=1200&q=80"
        weather_desc = "גשום 🌧️"
    elif 'ts' in raw_l: # סופות רעמים
        img_url = "https://images.unsplash.com/photo-1605727216801-e27ce1d0cc28?w=1200&q=80"
        weather_desc = "סופות רעמים ⛈️"
    elif 'sn' in raw_l or 'sg' in raw_l: # שלג
        img_url = "https://images.unsplash.com/photo-1547366155-2e0617b70366?w=1200&q=80"
        weather_desc = "מושלג ❄️"
    elif any(x in raw_l for x in ['fg', 'br', 'hz']): # ערפל/אובך
        img_url = "https://images.unsplash.com/photo-1487621167305-5d248087c724?w=1200&q=80"
        weather_desc = "ראות מוגבלת/ערפל 🌫️"
    elif 'ovc' in raw_l or 'bkn' in raw_l: # מעונן חלקית עד מלא
        img_url = "https://images.unsplash.com/photo-1483977399921-6cf3832f7c44?w=1200&q=80"
        weather_desc = "מעונן ☁️"

    # הצגת התמונה הדינמית
    st.image(img_url, caption=f"מצב נוכחי ב-{selected_name}: {weather_desc}", use_container_width=True)

    st.markdown("---")

    # דאשבורד מטריקות (Data Visualisation)
    # שימוש ב-3 קולונות עם כרטיסים מעוצבים
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🌡️ טמפרטורה", f"{temp}°C", delta=f"{dew}°C נקודת טל")
    with col2:
        # צבע הלחץ משתנה לפי המצב (שקע/רמה)
        st.metric("⏲️ לחץ ברומטרי", f"{press} hPa", delta=f"{round(press-1013.25, 2)} hPa vs Std")
    with col3:
        st.metric("💨 מהירות רוח", f"{wind} Knots")

    # נתונים מתקדמים בשורה שנייה
    st.markdown("### 📊 נתונים פיזיקליים נוספים")
    a1, a2, a3 = st.columns(3)
    a1.metric("🌫️ ראות", f"{vis} מטרים")
    a2.metric("💧 לחות יחסית", f"{round(hum, 1) if hum != 'N/A' else 'N/A'}%")
    a3.metric("✈️ חוקי טיסה", data.get('flight_rules', 'VFR'))

    st.markdown("---")
    
    # ניתוח "המומחה" (Expert Insight)
    st.subheader("🔍 ניתוח אסטרטגי")
    if press < 1010:
        st.error(f"אזהרה: לחץ ברומטרי נמוך ב-{selected_name}. מערכת שקע ברומטרי עשויה להוביל לשינוי מהיר במזג האוויר ולהיווצרות עננות חזקה.")
    else:
        st.success(f"יציבות אטמוספרית: לחץ גבוה ב-{selected_name}. תנאים יציבים וראות טובה.")

    # הצגת הדיווח הגולמי בתחתית
    with st.expander("לצפייה בדיווח ה-METAR הגולמי (Aviation Raw Data)"):
        st.code(raw)

else:
    st.error("לא ניתן למשוך נתונים כרגע. וודא שהחיבור לאינטרנט תקין.")

st.caption("הנתונים מתבססים על חיישני מטוסים ותחנות שדה תעופה בזמן אמת. Powered by AVWX.")
