import streamlit as st
import hashlib
import time
from datetime import datetime, timedelta, timezone

if 'history' not in st.session_state:
    st.session_state.history = []

st.set_page_config(page_title="SNIPER PRO v24.0", layout="wide")

# Lera Madagasikara (UTC+3)
now_mg = datetime.now(timezone(timedelta(hours=3)))
lera_izao = now_mg.time()

# STYLE DASHBOARD
st.markdown("""
    <style>
    .main { background-color: #050505; }
    .stButton>button { 
        background: linear-gradient(90deg, #ffcc00 0%, #ff9900 100%); 
        color: black; font-weight: 900; border-radius: 12px; height: 60px; width: 100%; border: none;
        box-shadow: 0px 4px 15px rgba(255, 204, 0, 0.4);
    }
    .main-card { 
        padding: 30px; border: 2px solid #333; border-radius: 25px; 
        text-align: center; background-color: #111; color: white;
    }
    .time-target { 
        font-size: 50px; color: #00ff44; font-weight: 900; 
        border: 2px dashed #00ff44; padding: 15px; border-radius: 20px; margin: 15px 0;
    }
    .prob-badge {
        padding: 10px 20px; border-radius: 50px; font-weight: bold; font-size: 20px;
    }
    h1, h2, h3 { color: #ffcc00 !important; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# SIDEBAR HISTORY
st.sidebar.title("📜 PREDICTIONS VITA")
for item in st.session_state.history[:10]:
    st.sidebar.markdown(f"""
    <div style='background:#222; padding:10px; border-radius:8px; margin-bottom:8px; border-left:5px solid #ffcc00;'>
        <b style='color:#ffcc00; font-size:18px;'>🚀 {item['val']}x</b><br>
        <small style='color:#bbb;'>🕒 Lera: {item['time']}</small><br>
        <small style='color:#00ff44;'>🔥 Probabilité: {item['prob']}%</small>
    </div>
    """, unsafe_allow_html=True)

# MAIN ENGINE
st.title("⚡ AVIATOR SNIPER PRO v24.0")
st.write(f"🟢 **SERVER:** ACTIVE | 🕒 **TIME:** {now_mg.strftime('%H:%M:%S')}")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### ⚙️ SETUP")
    hex_input = st.text_input("INPUT HEX SEED:", placeholder="8ebe8e80...")
    time_now_input = st.time_input("LERA AO AMIN'NY LALAO:", value=lera_izao)
    
    if st.button("🚀 GENERATE SIGNAL NOW"):
        if hex_input:
            with st.spinner('AI Scanning...'):
                time.sleep(1)
            
            # SHA-256 LOGIC
            hash_obj = hashlib.sha256(hex_input.encode())
            hash_hex = hash_obj.hexdigest()
            
            # Multiplier & Interval
            val_m = int(hash_hex[:8], 16)
            result = max(1.1, round(100 / (1 + (val_m % 78)), 2))
            interval = 1 + (int(hash_hex[-8:], 16) % 4)
            
            # Percentage Logic
            prob = 60 + (int(hash_hex[12:14], 16) % 40) 
            
            entry_time = (datetime.combine(datetime.today(), time_now_input) + timedelta(minutes=interval)).strftime("%H:%M")
            
            st.session_state.history.insert(0, {"val": result, "time": entry_time, "prob": prob})
            st.rerun()
        else:
            st.error("Ampidiro ny HEX Seed!")

with col2:
    if st.session_state.history:
        latest = st.session_state.history[0]
        
        # Color Logic for Probability
        prob_color = "#00ff44" if latest['prob'] >= 90 else "#ffcc00" if latest['prob'] >= 70 else "#ff3300"
        status_msg = "🔥 SIGNAL MAHERY VAIKA!" if latest['prob'] >= 90 else "⚠️ SIGNAL ANTONONY" if latest['prob'] >= 70 else "❌ MITANDREMA BE!"
        
        st.markdown(f"""
        <div class="main-card">
            <h3 style='color:#888;'>LERA FIDIRANA MANARAKA:</h3>
            <div class="time-target">🎯 {latest['time']} 🎯</div>
            <span class="prob-badge" style="background: {prob_color}22; color: {prob_color}; border: 1px solid {prob_color};">
                PROBABILITÉ: {latest['prob']}%
            </span>
            <br><br>
            <h3 style='color:#888;'>EXPECTED MULTIPLIER:</h3>
            <h1 style="font-size:90px; margin:0; color:#fff;">{latest['val']}x</h1>
            <p style="color:{prob_color}; font-weight:bold; font-size:20px; margin-top:15px;">{status_msg}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<div class='main-card'><h3>MIANDRY DATA...</h3><p>Ampidiro ny HEX hahazoana ny Strike voalohany.</p></div>", unsafe_allow_html=True)
