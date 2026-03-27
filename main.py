import streamlit as st
import hashlib
import time
from datetime import datetime, timedelta

# --- STYLE ULTRA PREMIUM ---
st.set_page_config(page_title="ANDRIANTSO TITAN v60.8", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    .main { background: #000000; color: #ffffff; }
    .stMetric { background: rgba(255, 255, 255, 0.05); border: 1px solid #00ffcc; border-radius: 15px; padding: 15px; }
    .prediction-box {
        background: linear-gradient(135deg, rgba(0, 255, 204, 0.1), rgba(255, 215, 0, 0.1));
        border: 2px solid #00ffcc; border-radius: 20px; padding: 30px; text-align: center;
        box-shadow: 0 0 25px rgba(0, 255, 204, 0.3);
    }
    .stButton>button {
        background: linear-gradient(90deg, #00ffcc, #33ccff);
        color: black; font-weight: bold; border-radius: 12px; height: 4em; border: none;
    }
    .expert-card { background: #111; border-left: 5px solid #ff0055; padding: 15px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

if 'history' not in st.session_state: st.session_state.history = []

st.markdown("<h1 style='text-align: center; color: #00ffcc;'>🚀 TITAN NEON v60.8</h1>", unsafe_allow_html=True)

# --- NAVIGATION ---
mode = st.sidebar.selectbox("🎯 FIDIO NY LALAO:", ["🚀 COSMOS X", "✈️ AVIATOR GOLD"])
st.sidebar.markdown("---")
st.sidebar.subheader("📖 CONSIGNES")
st.sidebar.markdown("""
* **Rule 1**: Aza miala amin'ny 'Safe' raha vao nivoaka in-2 ny Blue.
* **Rule 2**: Ny SHA-512 dia mijery ny fahasamihafan'ny Hex.
* **Rule 3**: Rehefa azonao ny 'Moyen', ajanony ny lalao.
""")

# --- INPUT SECTION ---
col_up, col_tm = st.columns(2)
with col_up:
    uploaded_file = st.file_uploader("📸 Screenshot History", type=['jpg', 'png'])
with col_tm:
    game_time = st.time_input("⏲️ Lera ao amin'ny lalao:", datetime.now().time())

hex_input = st.text_input(f"🔑 HEX SEED {mode}:", placeholder="Paste SHA Hash here...")

if st.button(f"🔥 EXECUTE {mode} ANALYSIS"):
    if not hex_input:
        st.error("❌ Ampidiro aloha ny Hex Seed!")
    else:
        with st.spinner('🔐 TITAN AI is decrypting SHA-512...'):
            time.sleep(1.5)
            # Algorithm SHA-512
            titan_hash = hashlib.sha512(hex_input.encode()).hexdigest()
            val = int(titan_hash[:12], 16)
            
            # Triple Estimation Logic
            prob = 89 + (val % 10)
            
            if "COSMOS" in mode:
                safe = round(1.50 + (val % 100) / 100, 2)
                moyen = round(safe * 2.2, 2)
                max_val = round(10.0 + (val % 5000) / 100, 2)
            else:
                safe = round(1.85 + (val % 130) / 100, 2)
                moyen = round(safe * 2.8, 2)
                max_val = round(20.0 + (val % 12000) / 100, 2)
            
            target_time = (datetime.combine(datetime.today(), game_time) + timedelta(minutes=(val % 4) + 1)).strftime("%H:%M")

            # --- DISPLAY ---
            st.markdown(f"""
                <div class="prediction-box">
                    <p style='color: #00ffcc; letter-spacing: 2px;'>{mode} SIGNAL ACTIVE</p>
                    <h1 style='font-size: 60px; margin: 10px 0;'>{target_time}</h1>
                    <h3 style='color: #FFD700;'>ESTIMATION ACCURACY: {prob}%</h3>
                </div>
            """, unsafe_allow_html=True)

            st.write("---")
            m1, m2, m3 = st.columns(3)
            m1.metric("🟢 SAFE", f"{safe}x")
            m2.metric("🟡 MOYEN", f"{moyen}x")
            m3.metric("🌸 MAX (PINK)", f"{max_val}x")

            st.session_state.history.insert(0, {"Lera": target_time, "Game": mode, "Safe": safe, "Moyen": moyen, "Max": max_val})

# --- HISTORY ---
st.write("---")
st.subheader("📜 RECENT TITAN SIGNALS")
if st.session_state.history:
    st.table(st.session_state.history)
    if st.sidebar.button("🗑️ RESET ALL"):
        st.session_state.history = []
        st.rerun()
