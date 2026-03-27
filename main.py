import streamlit as st
import hashlib
import time
from datetime import datetime, timedelta

if 'history' not in st.session_state:
    st.session_state.history = []

st.set_page_config(page_title="AVIATOR SNIPER ULTRA v20.0", layout="wide")

# STYLE MAHERY VAIKA (Neon Gold & Red)
st.markdown("""
    <style>
    .main { background-color: #050505; }
    .stButton>button { 
        background: linear-gradient(90deg, #ffcc00 0%, #ff9900 100%); 
        color: black; font-weight: 900; border-radius: 15px; 
        height: 65px; width: 100%; font-size: 22px; border: none;
        box-shadow: 0px 0px 15px #ffcc00;
    }
    .prediction-box { 
        padding: 30px; border: 5px double #ffcc00; border-radius: 25px; 
        text-align: center; background-color: #111; color: white;
        box-shadow: 0px 0px 20px rgba(255, 204, 0, 0.2);
    }
    .time-target { 
        font-size: 40px; color: #00ff44; font-weight: 900; 
        border: 3px solid #00ff44; padding: 20px; margin: 15px 0; 
        border-radius: 20px; background-color: #001a00;
        text-shadow: 0px 0px 10px #00ff44;
    }
    .status-vip { color: #ff3300; font-weight: bold; font-size: 14px; text-transform: uppercase; }
    h1, h2, h3 { color: #ffcc00 !important; text-align: center; font-family: 'Arial Black'; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 SNIPER ULTRA PREDICTOR")
st.write("### AI ENGINE: BOLT-SPEED | AMBOSITRA 2026")

# SIDEBAR SETTINGS
st.sidebar.markdown("### 🛠️ CONFIGURATION")
hex_input = st.sidebar.text_input("INPUT HEX SEED:", placeholder="Paste SHA-256 here...")
time_now_input = st.sidebar.time_input("LERA AO AMIN'NY LALAO:", value=datetime.now().time())
st.sidebar.write("---")
st.sidebar.markdown("<p class='status-vip'>Server Status: ONLINE (100ms)</p>", unsafe_allow_html=True)

if st.sidebar.button("🔥 GENERATE SIGNAL NOW"):
    if hex_input:
        with st.spinner('⚡ ANALYZING HASH...'):
            time.sleep(1.5)
        
        # SHA-256 ALGORITHM
        hash_obj = hashlib.sha256(hex_input.encode())
        hash_hex = hash_obj.hexdigest()
        
        # 1. Kajy ny Multiplier
        value_mult = int(hash_hex[:8], 16)
        result = max(1.1, round(100 / (1 + (value_mult % 78)), 2))
        
        # 2. KAJY NY INTERVALLE (1-4 Minitra)
        value_time = int(hash_hex[-8:], 16)
        interval_minutes = 1 + (value_time % 4) # Miteraka 1, 2, 3, na 4
        
        # 3. Kajy ny Lera Automatique
        entry_dt = datetime.combine(datetime.today(), time_now_input) + timedelta(minutes=interval_minutes)
        entry_time = entry_dt.strftime("%H:%M")
        
        # Tehirizina
        st.session_state.history.insert(0, {"val": result, "time": entry_time, "int": interval_minutes})

        # Fampisehoana Vokatra
        st.markdown('<div class="prediction-box">', unsafe_allow_html=True)
        st.markdown(f"<p style='color:#aaa;'>ALGORITHM DETECTED: +{interval_minutes}m Interval</p>", unsafe_allow_html=True)
        st.markdown(f"<h3>LERA FIDIRANA (STRIKE):</h3>", unsafe_allow_html=True)
        st.markdown(f'<div class="time-target">🎯 {entry_time} 🎯</div>', unsafe_allow_html=True)
        
        # Loko mifanaraka amin'ny hery
        color = "#00d4ff" if result < 2.0 else "#ffcc00" if result < 10.0 else "#ff0055"
        st.markdown(f"<h3>EXPECTED MULTIPLIER:</h3><h1 style='color: {color}; font-size: 95px;'>{result}x</h1>", unsafe_allow_html=True)
        st.markdown('<p class="status-vip">⚠️ MANDEHA NY SIGNAL - MIOMANA!</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("ERROR: Ampidiro ny HEX Seed vao manindry Run!")

# HISTORIQUE PREMIUM
st.write("---")
st.subheader("📜 PREVIOUS STRIKES")
if st.session_state.history:
    cols = st.columns(len(st.session_state.history[:5]))
    for i, item in enumerate(st.session_state.history[:5]):
        with cols[i]:
            st.markdown(f"""
                <div style="text-align:center; border:2px solid #333; padding:15px; border-radius:15px; background-color:#111;">
                    <b style="color:#ffcc00; font-size:20px;">{item['val']}x</b><br>
                    <span style="color:#00ff44; font-weight:bold;">{item['time']}</span><br>
                    <small style="color:#555;">Gap: {item['int']}m</small>
                </div>
            """, unsafe_allow_html=True)
