import streamlit as st
import hashlib
from datetime import datetime, timedelta, timezone

if 'history' not in st.session_state:
    st.session_state.history = []

st.set_page_config(page_title="SNIPER TREND v30.0", layout="wide")

now_mg = datetime.now(timezone(timedelta(hours=3)))

# 1. STYLE DESIGN
st.markdown("""
    <style>
    .main { background-color: #050505; }
    .stButton>button { background: linear-gradient(90deg, #ffcc00 0%, #ff9900 100%); color: black; font-weight: 900; border-radius: 12px; height: 50px; width: 100%; border: none; }
    .main-card { padding: 25px; border: 1px solid #333; border-radius: 20px; text-align: center; background: #111; color: white; }
    .trend-box { background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 10px; margin-top: 10px; border-left: 5px solid #ffcc00; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ SNIPER PRO: TREND ANALYSER")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### ⚙️ CONFIG & TREND")
    hex_input = st.text_input("INPUT HEX SEED:", placeholder="Paste SHA-256...")
    
    # --- FIDIRANA NY COTE FARANY ---
    last_cotes = st.text_input("HISTORIQUE (Cotes farany 3):", placeholder="Ohatra: 1.20, 1.45, 1.08")
    
    time_now_input = st.time_input("LERA AO AMIN'NY LALAO:", value=now_mg.time())
    
    if st.button("🔥 GENERATE SMART SIGNAL"):
        if hex_input:
            hash_obj = hashlib.sha256(hex_input.encode())
            hash_hex = hash_obj.hexdigest()
            val_base = int(hash_hex[:8], 16)
            
            # KAJY ESTIMATION
            est_min = 2.03 
            est_moyen = round(4.00 + (val_base % 350) / 100, 2)
            est_max = round(8.00 + (val_base % 1800) / 100, 2)
            
            # ANALYSE TREND (Miankina amin'ny cote nampidirinao)
            bonus_prob = 0
            if last_cotes:
                try:
                    cotes_list = [float(c.strip()) for c in last_cotes.split(",")]
                    # Raha latsaky ny 2.00x daholo ny 3 farany, dia mampitombo probabilité
                    if all(c < 2.0 for c in cotes_list):
                        bonus_prob = 15 
                except:
                    pass

            prob = min(99, 60 + (int(hash_hex[12:14], 16) % 25) + bonus_prob)
            interval = 1 + (int(hash_hex[-8:], 16) % 4)
            entry_time = (datetime.combine(datetime.today(), time_now_input) + timedelta(minutes=interval)).strftime("%H:%M")
            
            st.session_state.history.insert(0, {"min": est_min, "moyen": est_moyen, "max": est_max, "time": entry_time, "prob": prob, "trend": bonus_prob > 0})
            st.rerun()

with col2:
    if st.session_state.history:
        latest = st.session_state.history[0]
        color = "#00ff44" if latest['prob'] >= 85 else "#ffcc00" if latest['prob'] >= 75 else "#ff3300"
        
        st.markdown(f"""
        <div class="main-card">
            <h3>LERA FIDIRANA:</h3>
            <h1 style="font-size:60px; color:#00ff44; margin:0;">🎯 {latest['time']} 🎯</h1>
            <p style="color:{color}; font-size:20px; font-weight:bold;">PROBABILITÉ: {latest['prob']}%</p>
            
            <div style="display: flex; justify-content: space-around; margin-top: 20px;">
                <div style="border:1px solid #00ff44; padding:10px; border-radius:10px;"><b>SAFE</b><br>{latest['min']}x</div>
                <div style="border:1px solid #ffcc00; padding:10px; border-radius:10px;"><b>MOYEN</b><br>{latest['moyen']}x</div>
                <div style="border:1px solid #ff3300; padding:10px; border-radius:10px;"><b>MAX</b><br>{latest['max']}x</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if latest['trend']:
            st.markdown("""
            <div class="trend-box">
                <b style="color:#00ff44;">📈 TREND DETECTED:</b><br>
                Nahatsikaritra ny AI fa nifanesy ny cote ambany. Niakatra ny probabilité fa efa akaiky hivoaka ny cote tsara!
            </div>
            """, unsafe_allow_html=True)
