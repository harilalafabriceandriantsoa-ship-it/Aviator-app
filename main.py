import streamlit as st
import hashlib
import time
from datetime import datetime, timedelta, timezone

# 1. SETUP SY LERA
if 'history' not in st.session_state:
    st.session_state.history = []

st.set_page_config(page_title="SNIPER FIXED v29.0", layout="wide")

now_mg = datetime.now(timezone(timedelta(hours=3)))
lera_izao = now_mg.time()

# 2. STYLE DESIGN
st.markdown("""
    <style>
    .main { background-color: #050505; }
    .stButton>button { 
        background: linear-gradient(90deg, #ffcc00 0%, #ff9900 100%); 
        color: black; font-weight: 900; border-radius: 15px; height: 55px; width: 100%; border: none;
    }
    .main-card { 
        padding: 30px; border: 1px solid #333; border-radius: 25px; 
        text-align: center; background: #111; color: white;
    }
    .est-container { display: flex; justify-content: space-between; margin-top: 25px; gap: 10px; }
    .est-card { flex: 1; padding: 15px; border-radius: 15px; text-align: center; }
    .min-card { border: 2px solid #00ff44; background: rgba(0, 255, 68, 0.1); }
    .moyen-card { border: 2px solid #ffcc00; background: rgba(255, 204, 0, 0.1); }
    .max-card { border: 2px solid #ff3300; background: rgba(255, 51, 0, 0.1); }
    .time-target { font-size: 55px; color: #00ff44; font-weight: 900; border: 2px dashed #00ff44; padding: 10px; border-radius: 15px; margin: 15px 0; }
    h1, h2, h3 { color: #ffcc00 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR
st.sidebar.title("📜 SIGNAL RECENT")
for item in st.session_state.history[:5]:
    st.sidebar.markdown(f"<div style='background:#222; padding:8px; border-radius:5px; margin-bottom:5px; border-left:4px solid #ffcc00;'>🚀 {item['max']}x | {item['time']}</div>", unsafe_allow_html=True)

# 4. DASHBOARD ENGINE
st.title("🛡️ SNIPER PRO v29.0")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### ⚙️ SETUP")
    hex_input = st.text_input("INPUT HEX SEED:", placeholder="Paste SHA-256 here...")
    time_now_input = st.time_input("LERA AO AMIN'NY LALAO:", value=lera_izao)
    
    if st.button("🔥 GENERATE SIGNAL NOW"):
        if hex_input:
            hash_obj = hashlib.sha256(hex_input.encode())
            hash_hex = hash_obj.hexdigest()
            val_base = int(hash_hex[:8], 16)
            
            # KAJY ESTIMATION
            est_min = 2.03 
            est_moyen = round(4.00 + (val_base % 350) / 100, 2)
            est_max = round(8.00 + (val_base % 1800) / 100, 2)
            
            interval = 1 + (int(hash_hex[-8:], 16) % 4)
            prob = 60 + (int(hash_hex[12:14], 16) % 40)
            entry_time = (datetime.combine(datetime.today(), time_now_input) + timedelta(minutes=interval)).strftime("%H:%M")
            
            st.session_state.history.insert(0, {"min": est_min, "moyen": est_moyen, "max": est_max, "time": entry_time, "prob": prob})
            st.rerun()

with col2:
    if st.session_state.history:
        latest = st.session_state.history[0]
        # Logic Consigne (Tsy misy Syntax Error intsony)
        if latest['prob'] >= 85:
            txt = "SIGNAL EXPERT: Afaka mitady cote MAX ianao, nefa mivoaha amin'ny MOYEN raha te hahazo antoka."
            color = "#00ff44"
        elif latest['prob'] >= 70:
            txt = "SIGNAL TSARA: Mivoaha amin'ny 2.03x na MOYEN. Aza miandry MAX loatra."
            color = "#ffcc00"
        else:
            txt = "SIGNAL RISQUÉ: Mivoaha haingana amin'ny 2.03x ihany. Tandremo ny fahaverezana."
            color = "#ff3300"
        
        st.markdown(f"""
        <div class="main-card">
            <h3>LERA FIDIRANA:</h3>
            <div class="time-target">{latest['time']}</div>
            <p style="color:{color}; font-weight:bold;">PROBABILITÉ: {latest['prob']}%</p>
            <div class="est-container">
                <div class="est-card min-card"><span>💰</span><br><small>SAFE</small><br><b>{latest['min']}x</b></div>
                <div class="est-card moyen-card"><span>🚀</span><br><small>MOYEN</small><br><b>{latest['moyen']}x</b></div>
                <div class="est-card max-card"><span>🔥</span><br><small>MAX</small><br><b>{latest['max']}x</b></div>
            </div>
            <div style="margin-top:20px; padding:15px; background:rgba(255,255,255,0.05); border-radius:15px; border-left:5px solid {color};">
                <p style="color:#ddd; text-align:left; margin:0;"><b>📋 TOROLALANA:</b><br>{txt}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
