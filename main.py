import streamlit as st
import hashlib
import time
from datetime import datetime, timedelta, timezone

# 1. SETUP SY LERA (Tsy miova ny fototra)
if 'history' not in st.session_state:
    st.session_state.history = []

st.set_page_config(page_title="SNIPER ULTRA v28.0", layout="wide")

# Lera Madagasikara (EAT - UTC+3)
now_mg = datetime.now(timezone(timedelta(hours=3)))
lera_izao = now_mg.time()

# 2. STYLE PRO (NOHATSARAINA NY LOKO SY NY ICON)
st.markdown("""
    <style>
    .main { background-color: #050505; }
    .stButton>button { 
        background: linear-gradient(90deg, #ffcc00 0%, #ff9900 100%); 
        color: black; font-weight: 900; border-radius: 15px; height: 60px; width: 100%; border: none;
        box-shadow: 0px 5px 20px rgba(255, 204, 0, 0.3);
    }
    .main-card { 
        padding: 35px; border: 1px solid #333; border-radius: 30px; 
        text-align: center; background: linear-gradient(145deg, #111, #1a1a1a); color: white;
    }
    .est-container {
        display: flex; justify-content: space-between; margin-top: 30px; gap: 15px;
    }
    .est-card {
        flex: 1; padding: 20px; border-radius: 20px; text-align: center; transition: 0.3s;
    }
    .min-card { border: 2px solid #00ff44; background: rgba(0, 255, 68, 0.05); }
    .moyen-card { border: 2px solid #ffcc00; background: rgba(255, 204, 0, 0.05); }
    .max-card { border: 2px solid #ff3300; background: rgba(255, 51, 0, 0.05); }
    
    .time-target { 
        font-size: 60px; color: #00ff44; font-weight: 900; 
        background: rgba(0, 255, 68, 0.1); padding: 15px; border-radius: 20px; 
        border: 2px dashed #00ff44; margin: 20px 0;
    }
    .prob-text { font-size: 22px; font-weight: bold; margin-bottom: 10px; }
    h1, h2, h3 { color: #ffcc00 !important; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR (HISTORIQUE)
st.sidebar.title("📜 SIGNAL RECENT")
for item in st.session_state.history[:8]:
    st.sidebar.markdown(f"""
    <div style='background:#1a1a1a; padding:10px; border-radius:10px; margin-bottom:10px; border-left:5px solid #ffcc00;'>
        <b style='color:#ffcc00; font-size:16px;'>🚀 {item['max']}x</b><br>
        <small style='color:#888;'>🕒 {item['time']} | 🔥 {item['prob']}%</small>
    </div>
    """, unsafe_allow_html=True)

# 4. DASHBOARD LEHIBE
st.title("🛡️ SNIPER PRO DASHBOARD")
st.write(f"🌍 **SERVER MADAGASCAR** | 🕒 **{now_mg.strftime('%H:%M:%S')}**")

col1, col2 = st.columns([1, 2.2])

with col1:
    st.markdown("### 🛠️ CONFIGURATION")
    hex_input = st.text_input("INPUT HEX SEED:", placeholder="8ebe8e80...")
    time_now_input = st.time_input("LERA AO AMIN'NY LALAO:", value=lera_izao)
    
    if st.button("🔥 GENERATE TRIPLE SIGNAL"):
        if hex_input:
            hash_obj = hashlib.sha256(hex_input.encode())
            hash_hex = hash_obj.hexdigest()
            val_base = int(hash_hex[:8], 16)
            
            # KAJY ESTIMATION (Mitovy amin'ny teo aloha fa hatsaraina ny sanda)
            est_min = 2.03 
            est_moyen = round(4.00 + (val_base % 350) / 100, 2)
            est_max = round(8.00 + (val_base % 1800) / 100, 2)
            
            interval = 1 + (int(hash_hex[-8:], 16) % 4)
            prob = 60 + (int(hash_hex[12:14], 16) % 40)
            
            entry_time = (datetime.combine(datetime.today(), time_now_input) + timedelta(minutes=interval)).strftime("%H:%M")
            
            st.session_state.history.insert(0, {
                "min": est_min, "moyen": est_moyen, "max": est_max, 
                "time": entry_time, "prob": prob
            })
            st.rerun()

with col2:
    if st.session_state.history:
        latest = st.session_state.history[0]
        prob_color = "#00ff44" if latest['prob'] >= 85 else "#ffcc00" if latest['prob'] >= 70 else "#ff3300"
        
        st.markdown(f"""
        <div class="main-card">
            <h3 style='color:#888; margin-bottom:0;'>🎯 LERA FIDIRANA (STRIKE)</h3>
            <div class="time-target">{latest['time']}</div>
            <div class="prob-text" style="color:{prob_color};">⚡ PROBABILITÉ: {latest['prob']}%</div>
            
            <div class="est-container">
                <div class="est-card min-card">
                    <span style="font-size:25px;">💰</span><br>
                    <small style="color:#00ff44;">SAFE</small><br>
                    <b style="font-size:30px;">{latest['min']}x</b>
                </div>
                <div class="est-card moyen-card">
                    <span style="font-size:25px;">🚀</span><br>
                    <small style="color:#ffcc00;">MOYEN</small><br>
                    <b style="font-size:30px;">{latest['moyen']}x</b>
                </div>
                <div class="est-card max-card">
                    <span style="font-size:25px;">🔥</span><br>
                    <small style="color:#ff3300;">MAX</small><br>
                    <b style="font-size:30px;">{latest['max']}x</b>
                </div>
            </div>
            
            <div style="margin-top:25px; padding:20px; background:rgba(255,255,255,0.03); border-radius:20px; border:1px solid #333;">
                <h4 style="color:#ffcc00; margin-top:0;">📋 TOROLALANA (CONSIGNE)</h4>
                <p style="color:#bbb; font-size:18px;">
                    {
                        "<b>SIGNAL EXPERT:</b> Afaka mitady cote <b>MAX</b> ianao nefa mivoaha amin'ny <b>MOYEN</b> raha te hahazo antoka." if latest['prob'] >= 85 
                        else "
