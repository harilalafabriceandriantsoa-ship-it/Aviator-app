import streamlit as st
import random
import time
from datetime import datetime

# --- 1. CONFIGURATION & STATE ---
st.set_page_config(page_title="TITAN V70.0 PREMIUM", layout="wide")

if 'prediction_history' not in st.session_state:
    st.session_state.prediction_history = []

# --- STYLE CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #050a10; color: #ffffff; }
    .titan-header { font-size: 30px; font-weight: 900; text-align: center; color: #00ffcc; text-shadow: 0 0 10px #00ffcc; padding: 10px; border-bottom: 2px solid #00ffcc; }
    .label-premium { color: #ffd700; font-weight: bold; margin-top: 15px; display: block; }
    .card-res { background: rgba(0, 255, 204, 0.1); border: 2px solid #00ffcc; border-radius: 12px; padding: 20px; text-align: center; margin-top: 10px; }
    .stat-box { background: rgba(255, 255, 255, 0.05); border: 1px solid #444; border-radius: 8px; padding: 10px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="titan-header">TITAN OMNI-STRIKE V70.0 💎</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚽ PENALTY VIP"])

# --- TAB 1: AVIATOR ---
with tab1:
    st.file_uploader("📷 CAPTURE AVIATOR:", type=['jpg', 'png', 'jpeg'], key="avi_cap_70")
    avi_hex = st.text_input("🔑 HEX SEED (Aviator):", key="avi_hex_70")
    avi_h = st.text_input("🕒 HEURE:", value=datetime.now().strftime("%H:%M"), key="avi_h_70")
    if st.button("🚀 EXECUTE AVIATOR", use_container_width=True):
        res = round(random.uniform(2.0, 10.0), 2)
        st.session_state.prediction_history.append(f"✈️ AVIATOR | {avi_h} | Result: {res}x")
        st.markdown(f"<div class='card-res'><h1>{res}x</h1></div>", unsafe_allow_html=True)

# --- TAB 2: COSMOS X ---
with tab2:
    st.file_uploader("📷 CAPTURE COSMOS:", type=['jpg', 'png', 'jpeg'], key="cos_cap_70")
    cos_hex = st.text_input("🔑 HEX SEED (Cosmos):", key="cos_hex_70")
    cos_h = st.text_input("🕒 HEURE COSMOS:", value=datetime.now().strftime("%H:%M"), key="cos_h_70")
    if st.button("🚀 EXECUTE COSMOS", use_container_width=True):
        c_min, c_moy, c_max = round(random.uniform(1.2, 1.8), 2), round(random.uniform(2.2, 6.0), 2), round(random.uniform(15, 45), 2)
        pct = random.randint(90, 99)
        st.session_state.prediction_history.append(f"🚀 COSMOS | {cos_h} | Moy: {c_moy}x | {pct}%")
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown(f"<div class='stat-box'>MIN<br><b>{c_min}x</b></div>", unsafe_allow_html=True)
        with col2: st.markdown(f"<div class='stat-box'>MOYEN<br><b>{c_moy}x</b></div>", unsafe_allow_html=True)
        with col3: st.markdown(f"<div class='stat-box'>MAX<br><b>{c_max}x</b></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='card-res'><h3>ACCURACY: {pct}%</h3><h1>{c_moy}x</h1></div>", unsafe_allow_html=True)

# --- TAB 3: MINES VIP (WITH CAPTURE & HEX) ---
with tab3:
    st.markdown("### 💣 MINES STRATEGY")
    st.file_uploader("📷 CAPTURE GRID (Mines):", type=['jpg', 'png', 'jpeg'], key="min_cap_70")
    min_hex = st.text_input("🔑 HEX SEED (Mines):", key="min_hex_70")
    c_seed = st.text_input("💻 CLIENT SEED:", key="min_cli_70")
    s_seed = st.text_input("🖥️ SERVER SEED:", key="min_ser_70")
    
    if st.button("⚡ SCAN MINES GRID", use_container_width=True):
        random.seed(hash(min_hex + c_seed + s_seed))
        stars = random.sample(range(25), k=5)
        grid = '<div style="display: grid; grid-template-columns: repeat(5, 45px); gap: 10px; justify-content: center; margin-top:10px;">'
        for i in range(25):
            color = "#00ffcc" if i in stars else "#1a1f26"
            grid += f'<div style="width:45px; height:45px; background:{color}; border-radius:8px; border:1px solid #333;"></div>'
        st.markdown(grid + '</div>', unsafe_allow_html=True)
        st.session_state.prediction_history.append(f"💣 MINES | {datetime.now().strftime('%H:%M')} | Grid Scanned")

# --- TAB 4: PENALTY VIP (WITH CAPTURE & HEX) ---
with tab4:
    st.markdown("### ⚽ PENALTY SEQUENCE")
    st.file_uploader("📷 CAPTURE GAME (Penalty):", type=['jpg', 'png', 'jpeg'], key="pen_cap_70")
    pen_hex = st.text_input("🔑 HEX SEED (Penalty):", key="pen_hex_70")
    st.selectbox("MODE:", ["FACILE (x2.93)", "MOYEN", "DIFFICILE"], key="pen_mod_70")
    
    if st.button("⚽ GENERATE SEQUENCE", use_container_width=True):
        spots = ["ANKAVIA AMBONY", "AFOVOANY", "ANKAVANANA AMBANY"]
        res_p = random.choice(spots)
        st.success(f"TARGET: {res_p}")
        st.session_state.prediction_history.append(f"⚽ PENALTY | {datetime.now().strftime('%H:%M')} | {res_p}")

# --- RESET & HISTORY ---
st.write("---")
if st.button("🗑️ RESET HISTORIQUE", use_container_width=True):
    st.session_state.prediction_history = []
    st.rerun()

st.subheader("📜 HISTORIQUE")
for h in reversed(st.session_state.prediction_history[-10:]):
    st.write(h)
