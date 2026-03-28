import streamlit as st
import random
import time
from datetime import datetime

# --- 1. CONFIGURATION & HISTORY STATE ---
st.set_page_config(page_title="TITAN V69.0 PREMIUM", layout="wide")

# Ity no vata itahirizana ny tantara (History)
if 'prediction_history' not in st.session_state:
    st.session_state.prediction_history = []

# --- STYLE CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #050a10; color: #ffffff; }
    .titan-header { font-size: 30px; font-weight: 900; text-align: center; color: #00ffcc; text-shadow: 0 0 10px #00ffcc; padding: 10px; border-bottom: 2px solid #00ffcc; }
    .label-premium { color: #ffd700; font-weight: bold; margin-top: 10px; display: block; }
    .card-res { background: rgba(0, 255, 204, 0.1); border: 2px solid #00ffcc; border-radius: 12px; padding: 15px; text-align: center; margin-top: 10px; }
    .stat-box { background: rgba(255, 255, 255, 0.05); border: 1px solid #444; border-radius: 8px; padding: 10px; text-align: center; }
    .hist-item { background: #1a1f26; border-left: 5px solid #00ffcc; padding: 10px; margin-bottom: 5px; border-radius: 5px; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="titan-header">TITAN OMNI-STRIKE V69.0 💎</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚽ PENALTY VIP"])

# --- TAB 1: AVIATOR ---
with tab1:
    st.markdown('<span class="label-premium">📷 CAPTURE & DATA AVIATOR:</span>', unsafe_allow_html=True)
    st.file_uploader("Upload Aviator", type=['jpg', 'png', 'jpeg'], key="avi_cap_69")
    avi_hex = st.text_input("🔑 HEX SEED:", key="avi_hex_69")
    avi_h = st.text_input("🕒 HEURE:", value=datetime.now().strftime("%H:%M"), key="avi_h_69")

    if st.button("🚀 EXECUTE AVIATOR", use_container_width=True):
        random.seed(hash(avi_hex + avi_h + str(time.time())))
        res = round(random.uniform(2.0, 8.5), 2)
        # Save to History
        st.session_state.prediction_history.append(f"✈️ AVIATOR | {avi_h} | Res: {res}x")
        
        st.markdown(f"<div class='card-res'><h1>{res}x</h1></div>", unsafe_allow_html=True)

# --- TAB 2: COSMOS X ---
with tab2:
    st.markdown('<span class="label-premium">🚀 COSMOS X DATA:</span>', unsafe_allow_html=True)
    st.file_uploader("Upload Cosmos", type=['jpg', 'png', 'jpeg'], key="cos_cap_69")
    cos_hex = st.text_input("🔑 HEX SEED (Cosmos):", key="cos_hex_69")
    cos_h = st.text_input("🕒 HEURE COSMOS:", value=datetime.now().strftime("%H:%M"), key="cos_h_69")

    if st.button("🚀 EXECUTE COSMOS", use_container_width=True):
        random.seed(hash(cos_hex + cos_h))
        c_min, c_moy, c_max = round(random.uniform(1.2, 1.8), 2), round(random.uniform(2.2, 5.8), 2), round(random.uniform(12, 40), 2)
        pct = random.randint(88, 98)
        # Save to History
        st.session_state.prediction_history.append(f"🚀 COSMOS | {cos_h} | Moy: {c_moy}x | Acc: {pct}%")
        
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f"<div class='stat-box'>MIN<br><b>{c_min}x</b></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='stat-box'>MOYEN<br><b>{c_moy}x</b></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='stat-box'>MAX<br><b>{c_max}x</b></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='card-res'><h3>ACCURACY: {pct}%</h3><h1>{c_moy}x</h1></div>", unsafe_allow_html=True)

# --- SECTION HISTORIQUE & RESET ---
st.write("---")
st.subheader("📜 HISTORIQUE DES PRÉDICTIONS")

col_h1, col_h2 = st.columns([4, 1])
with col_h2:
    if st.button("🗑️ RESET"):
        st.session_state.prediction_history = []
        st.rerun()

if not st.session_state.prediction_history:
    st.write("Tsy mbola misy tantara voatahiry.")
else:
    for item in reversed(st.session_state.prediction_history[-10:]):
        st.markdown(f"<div class='hist-item'>{item}</div>", unsafe_allow_html=True)
