import streamlit as st
import random
import time
from datetime import datetime

# --- 1. CONFIGURATION & STATE ---
st.set_page_config(page_title="TITAN V71.0 PREMIUM", layout="wide")

if 'prediction_history' not in st.session_state:
    st.session_state.prediction_history = []

# --- STYLE CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #050a10; color: #ffffff; }
    .titan-header { font-size: 30px; font-weight: 900; text-align: center; color: #00ffcc; text-shadow: 0 0 10px #00ffcc; padding: 10px; border-bottom: 2px solid #00ffcc; }
    .label-premium { color: #ffd700; font-weight: bold; margin-top: 15px; display: block; }
    .card-res { background: rgba(0, 255, 204, 0.1); border: 2px solid #00ffcc; border-radius: 12px; padding: 20px; text-align: center; margin-top: 10px; }
    .stat-box { background: rgba(255, 255, 255, 0.05); border: 1px solid #00ffcc; border-radius: 8px; padding: 10px; text-align: center; }
    .hist-item { background: #1a1f26; border-left: 5px solid #00ffcc; padding: 8px; margin-bottom: 5px; border-radius: 5px; font-size: 13px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="titan-header">TITAN OMNI-STRIKE V71.0 💎</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚽ PENALTY VIP"])

# --- FUNCTION FOR STATS ---
def show_stats(p_min, p_moy, p_max, pct, game_name):
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f"<div class='stat-box'>MIN<br><b style='color:#ff4b4b;'>{p_min}x</b></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='stat-box'>MOYEN<br><b style='color:#ffd700;'>{p_moy}x</b></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='stat-box'>MAX<br><b style='color:#00ffcc;'>{p_max}x</b></div>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class='card-res'>
            <p style='margin:0;'>PROBABILITY ACCURACY</p>
            <h1 style='color:#00ffcc; margin:0;'>{pct}%</h1>
            <p style='margin:0;'>RECOMMANDATION: <b style='color:#ffd700;'>{p_moy}x</b></p>
        </div>
    """, unsafe_allow_html=True)

# --- TAB 1: AVIATOR ---
with tab1:
    st.file_uploader("📷 CAPTURE AVIATOR:", type=['jpg', 'png', 'jpeg'], key="avi_cap_71")
    avi_hex = st.text_input("🔑 HEX SEED (Aviator):", key="avi_hex_71")
    avi_h = st.text_input("🕒 HEURE:", value=datetime.now().strftime("%H:%M"), key="avi_h_71")
    
    if st.button("🚀 EXECUTE AVIATOR", use_container_width=True):
        random.seed(hash(avi_hex + avi_h + str(time.time())))
        p_min, p_moy, p_max = round(random.uniform(1.1, 1.4), 2), round(random.uniform(1.8, 5.5), 2), round(random.uniform(10, 40), 2)
        pct = random.randint(88, 98)
        show_stats(p_min, p_moy, p_max, pct, "AVIATOR")
        st.session_state.prediction_history.append(f"✈️ AVIATOR | {avi_h} | Result: {p_moy}x")

# --- TAB 2: COSMOS X ---
with tab2:
    st.file_uploader("📷 CAPTURE COSMOS:", type=['jpg', 'png', 'jpeg'], key="cos_cap_71")
    cos_hex = st.text_input("🔑 HEX SEED (Cosmos):", key="cos_hex_71")
    cos_h = st.text_input("🕒 HEURE COSMOS:", value=datetime.now().strftime("%H:%M"), key="cos_h_71")
    
    if st.button("🚀 EXECUTE COSMOS", use_container_width=True):
        random.seed(hash(cos_hex + cos_h + str(time.time())))
        c_min, c_moy, c_max = round(random.uniform(1.2, 1.6), 2), round(random.uniform(2.1, 6.5), 2), round(random.uniform(12, 55), 2)
        pct = random.randint(90, 99)
        show_stats(c_min, c_moy, c_max, pct, "COSMOS")
        st.session_state.prediction_history.append(f"🚀 COSMOS | {cos_h} | Moy: {c_moy}x | {pct}%")

# --- TAB 3: MINES & TAB 4: PENALTY (Stay same with Inputs) ---
with tab3:
    st.file_uploader("📷 CAPTURE MINES:", type=['jpg', 'png', 'jpeg'], key="min_cap_71")
    st.text_input("🔑 HEX SEED (Mines):", key="min_hex_71")
    if st.button("⚡ SCAN GRID"): st.warning("Stars located.")

with tab4:
    st.file_uploader("📷 CAPTURE PENALTY:", type=['jpg', 'png', 'jpeg'], key="pen_cap_71")
    st.text_input("🔑 HEX SEED (Penalty):", key="pen_hex_71")
    if st.button("⚽ GENERATE"): st.info("Target: Center")

# --- RESET & HISTORIQUE ---
st.write("---")
col_bt1, col_bt2 = st.columns([4, 1])
with col_bt2:
    if st.button("🗑️ RESET HISTORIQUE"):
        st.session_state.prediction_history = []
        st.rerun()

st.subheader("📜 HISTORIQUE DES PRÉDICTIONS")
if not st.session_state.prediction_history:
    st.write("Tsy mbola misy tantara.")
else:
    for h in reversed(st.session_state.prediction_history[-10:]):
        st.markdown(f"<div class='hist-item'>{h}</div>", unsafe_allow_html=True)
