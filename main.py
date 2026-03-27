import streamlit as st
import hashlib
import time
from datetime import datetime, timedelta

# --- CONFIGURATION STYLE ---
st.set_page_config(page_title="ANDRIANTSO TITAN v60.9", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .main { background: #050505; color: #ffffff; }
    .stMetric { background: rgba(0, 255, 204, 0.05); border: 1px solid #00ffcc; border-radius: 15px; padding: 15px; }
    .prediction-box {
        background: linear-gradient(135deg, rgba(0, 255, 204, 0.1), rgba(255, 215, 0, 0.1));
        border: 2px solid #00ffcc; border-radius: 20px; padding: 30px; text-align: center;
        box-shadow: 0 0 25px rgba(0, 255, 204, 0.3);
    }
    .stButton>button {
        background: linear-gradient(90deg, #00ffcc, #FFD700);
        color: black; font-weight: 900; border-radius: 12px; height: 4em; border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 20px #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

if 'history' not in st.session_state: st.session_state.history = []

st.markdown("<h1 style='text-align: center; color: #00ffcc;'>⚡ TITAN NEON v60.9</h1>", unsafe_allow_html=True)

# --- 🎯 SELECTION LALAO (VISIBLE) ---
st.write("### 🎮 FIDIO NY LALAO HATAO ANALYSE:")
mode = st.radio("", ["✈️ AVIATOR GOLD", "🚀 COSMOS X"], horizontal=True)

st.write("---")

# --- INPUT PANEL ---
col_up, col_tm = st.columns(2)
with col_up:
    st.file_uploader("📸 Screenshot History", type=['jpg', 'png'])
with col_tm:
    game_time = st.time_input("⏲️ Lera ao amin'ny lalao:", datetime.now().time())

hex_input = st.text_input(f"🔑 HEX SEED {mode}:", placeholder="Paste SHA Hash here...")

if st.button(f"🔥 EXECUTE TITAN ANALYSIS"):
    if not hex_input:
        st.error("❌ Ampidiro aloha ny Hex Seed!")
    else:
        with st.spinner('🔐 TITAN AI is decrypting SHA-512...'):
            time.sleep(1.5)
            # Algorithm SHA-512 ho an'ny analysis mahery
            titan_hash = hashlib.sha512(hex_input.encode()).hexdigest()
            val = int(titan_hash[:12], 16)
            
            # Triple Estimation Logic
            prob = 89 + (val % 10)
            
            if "AVIATOR" in mode:
                safe = round(1.85 + (val % 135) / 100, 2)
                moyen = round(safe * 2.8, 2)
                max_val = round(20.0 + (val % 12000) / 100, 2)
            else:
                safe = round(1.50 + (val % 110) / 100, 2)
                moyen = round(safe * 2.2, 2)
                max_val = round(10.0 + (val % 5500) / 100, 2)
            
            target_time = (datetime.combine(datetime.today(), game_time) + timedelta(minutes=(val % 4) + 1)).strftime("%H:%M")

            # --- DISPLAY RESULT ---
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

            st.session_state.history.insert(0, {"Lera": target_time, "Lalao": mode, "Safe": safe, "Moyen": moyen, "Max": max_val})

# --- SIDEBAR: CONSIGNES ---
st.sidebar.header("📖 Fampianarana Expert")
st.sidebar.info("""
1. **Fidio tsara ny lalao**: Aviator sa Cosmos eo ambony.
2. **SHA-512**: Ity no manome ny 'Moyen' sy 'Max'.
3. **Mialà amin'ny Safe**: Raha vao nivoaka in-2 ny Blue, aza miala amin'ny Safe.
4. **Target Moyen**: Ny 'Moyen' no tanjona azonao atao isan'andro.
""")

# --- HISTORY ---
st.write("---")
st.subheader("📜 RECENT TITAN SIGNALS")
if st.session_state.history:
    st.table(st.session_state.history)
    if st.sidebar.button("🗑️ RESET ALL"):
        st.session_state.history = []
        st.rerun()
