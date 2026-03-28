import streamlit as st
import random
import time
from datetime import datetime

# --- 1. CONFIGURATION & STATE ---
st.set_page_config(page_title="TITAN V65.2 PREMIUM", layout="wide")

# Ity no mitahiry ny tantaran'ny prediction rehetra
if 'master_history' not in st.session_state:
    st.session_state.master_history = []

# --- STYLE CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #050a10; color: #ffffff; }
    .titan-header { font-size: 30px; font-weight: 900; text-align: center; color: #00ffcc; text-shadow: 0 0 10px #00ffcc; }
    .hist-card { 
        background: rgba(255, 255, 255, 0.05); 
        border-left: 5px solid #00ffcc; 
        padding: 10px; 
        margin-bottom: 5px; 
        border-radius: 5px;
    }
    .stat-box { background: rgba(0, 255, 204, 0.1); border: 1px solid #00ffcc; border-radius: 10px; padding: 10px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="titan-header">TITAN OMNI-STRIKE V65.2</div>', unsafe_allow_html=True)

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚽ PENALTY VIP"])

# --- TAB 2: COSMOS X (Miaraka amin'ny Historique) ---
with tab2:
    st.subheader("🚀 COSMOS X ANALYZER")
    cap_cos = st.file_uploader("📷 Capture Historique:", type=['jpg', 'png', 'jpeg'], key="c_cap")
    hex_input = st.text_input("🔑 HEX SEED:", placeholder="OxFF...", key="c_hex")
    time_input = st.text_input("🕒 Heure:", value=datetime.now().strftime("%H:%M"), key="c_h")
    
    if st.button("🚀 EXECUTE COSMOS", use_container_width=True):
        if hex_input:
            random.seed(hash(hex_input + time_input))
            p_moy = round(random.uniform(2.1, 6.5), 2)
            # Ampidirina ao anaty historique
            entry = f"🚀 COSMOS | {time_input} | Result: {p_moy}x | Hex: {hex_input[:10]}..."
            st.session_state.master_history.append(entry)
            
            # Fampisehoana ny vokatra
            st.markdown(f"<div class='stat-box'><h1>{p_moy}x</h1></div>", unsafe_allow_html=True)
        else:
            st.error("⚠️ Apetaho ny HEX SEED!")

# --- TAB 1: AVIATOR ---
with tab1:
    st.subheader("✈️ AVIATOR")
    avi_h = st.text_input("🕒 Heure Aviator:", value=datetime.now().strftime("%H:%M"), key="a_h")
    if st.button("🚀 GET AVIATOR SIGNAL", use_container_width=True):
        res = round(random.uniform(1.8, 8.0), 2)
        st.session_state.master_history.append(f"✈️ AVIATOR | {avi_h} | Result: {res}x")
        st.success(f"Prediction: {res}x")

# --- TAB 4: PENALTY ---
with tab4:
    st.subheader("⚽ PENALTY VIP")
    if st.button("⚽ GENERATE SEQUENCE", use_container_width=True):
        seq = random.choice(["ANKAVIA", "AFOVOANY", "ANKAVANANA"])
        st.session_state.master_history.append(f"⚽ PENALTY | {datetime.now().strftime('%H:%M')} | Shot: {seq}")
        st.info(f"Target: {seq}")

# --- SECTION HISTORIQUE (REHETRA) ---
st.write("---")
st.subheader("📜 HISTORIQUE DES PRÉDICTIONS")

if st.button("🗑️ Effacer l'historique"):
    st.session_state.master_history = []
    st.rerun()

if not st.session_state.master_history:
    st.write("Tsy mbola misy historique eo.")
else:
    # Mampiseho ny 10 farany, ny vaovao indrindra no eo ambony
    for h in reversed(st.session_state.master_history[-10:]):
        st.markdown(f"<div class='hist-card'>{h}</div>", unsafe_allow_html=True)
