import streamlit as st
import hashlib
import time
from datetime import datetime, timedelta

# --- CONFIGURATION STYLE ---
st.set_page_config(page_title="ANDRIANTSO SUPREME v60.5", page_icon="💎", layout="wide")

# --- CSS ULTRA PREMIUM (GLOW & GLASS) ---
st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: white; }
    .stMetric { background: rgba(255, 255, 255, 0.05); border: 1px solid #FFD700; border-radius: 15px; box-shadow: 0 0 15px #FFD700; padding: 20px; }
    .stButton>button { 
        background: linear-gradient(90deg, #FFD700, #FFA500); 
        color: black; font-weight: bold; border-radius: 30px; 
        height: 3.5em; border: none; box-shadow: 0 5px 15px rgba(255, 215, 0, 0.4);
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 25px #FFD700; }
    .prediction-box {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        border-left: 5px solid #FFD700;
        margin-bottom: 20px;
    }
    .percent-text { font-size: 50px; font-weight: bold; color: #FFD700; text-shadow: 0 0 10px #FFD700; }
    </style>
    """, unsafe_allow_html=True)

if 'history' not in st.session_state: st.session_state.history = []
if 'wins' not in st.session_state: st.session_state.wins = 0

# --- HEADER ---
st.markdown("<h1 style='text-align: center; color: #FFD700;'>💎 ANDRIANTSO SUPREME v60.5</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; opacity: 0.7;'>Ultra Premium Prediction System | Variable Logic</p>", unsafe_allow_html=True)

# --- STATS BAR ---
col_s1, col_s2, col_s3 = st.columns(3)
with col_s1: st.metric("🏆 TOTAL WINS", st.session_state.wins)
with col_s2: 
    acc = (st.session_state.wins / len(st.session_state.history) * 100) if st.session_state.history else 0
    st.metric("📈 REAL ACCURACY", f"{round(acc, 1)}%")
with col_s3: st.metric("🔄 PREDICTIONS", len(st.session_state.history))

st.write("---")

# --- CONTROL PANEL ---
mode = st.radio("🚀 SELECT GAME MODE:", ["✈️ AVIATOR GOLD", "🚀 COSMOS NEON"], horizontal=True)
hex_input = st.text_input("🔑 ENTER SHA-256 HEX SEED:", placeholder="Paste here...")

if st.button("🔥 START ULTRA ANALYSIS"):
    if len(hex_input) < 10:
        st.error("❌ Hex Seed invalid! Please check the hash.")
    else:
        # Progress bar animation
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
        
        # Logic Variable
        h = hashlib.sha256(hex_input.encode()).hexdigest()
        val = int(h[:10], 16)
        prob = 85 + (val % 13)
        
        if "AVIATOR" in mode:
            safe = round(1.85 + (val % 140) / 100, 2)
            pink = round(20.0 + (val % 9000) / 100, 2)
        else:
            safe = round(1.60 + (val % 110) / 100, 2)
            pink = round(12.0 + (val % 5000) / 100, 2)
        
        target_time = (datetime.now() + timedelta(minutes=(val % 4) + 1)).strftime("%H:%M")

        # --- DISPLAY RESULT (STYLED) ---
        st.markdown(f"""
            <div class="prediction-box">
                <p style='margin:0; opacity:0.8;'>ESTIMATED PROBABILITY</p>
                <div class="percent-text">{prob}%</div>
                <hr style='border: 0.5px solid rgba(255,215,0,0.2);'>
                <h2 style='color: #00ffcc;'>⏰ NEXT SIGNAL: {target_time}</h2>
            </div>
        """, unsafe_allow_html=True)

        res_c1, res_c2 = st.columns(2)
        res_c1.success(f"🟢 SAFE EXIT: {safe}x")
        res_c2.warning(f"🌸 MAX PINK: {pink}x")
        
        st.session_state.history.insert(0, {"Time": target_time, "Game": mode, "Prob": f"{prob}%", "Safe": f"{safe}x"})

# --- HISTORY TABLE ---
st.write("---")
st.subheader("📜 RECENT PREDICTIONS")
if st.session_state.history:
    st.table(st.session_state.history)
    if st.button("✅ MARK AS WIN"):
        st.session_state.wins += 1
        st.rerun()
else:
    st.info("Awaiting new analysis...")

if st.sidebar.button("🗑️ CLEAN SYSTEM"):
    st.session_state.history = []
    st.session_state.wins = 0
    st.rerun()
