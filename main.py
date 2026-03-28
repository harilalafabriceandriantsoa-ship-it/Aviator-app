import streamlit as st
import random
import time
from datetime import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V63.5 NEURAL STRIKE", layout="wide")

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def check_password():
    if st.session_state["password"] == "TITAN2026": 
        st.session_state.authenticated = True
    else:
        st.error("❌ CODE ERRONÉ.")

# --- LOGIN ---
if not st.session_state.authenticated:
    st.markdown("<style>.stApp { background-color: #050a10; }</style>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; padding:40px; border:2px solid #00ffcc; border-radius:20px; margin-top:80px;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='color:#00ffcc;'>⚡ TITAN NEURAL STRIKE V63.5</h1>", unsafe_allow_html=True)
    st.text_input("Security Password:", type="password", key="password", on_change=check_password)
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- CSS STYLE ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; color: #e0e0e0; }
    .titan-header { font-size: 40px; font-weight: 900; text-align: center; color: #00ffcc; text-shadow: 0 0 20px #00ffcc; }
    .prediction-card { background: rgba(0, 255, 204, 0.05); border: 2px solid #00ffcc; border-radius: 20px; padding: 25px; text-align: center; }
    .timer-text { font-size: 30px; color: #ffd700; font-weight: bold; }
    .step-box { background: rgba(255,255,255,0.05); border-left: 5px solid #00ffcc; padding: 15px; margin: 10px 0; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="titan-header">TITAN NEURAL STRIKE V63.5</h1>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS", "💣 MINES", "⚽ PENALTY"])

# --- AVIATOR, COSMOS, MINES (Tsy niova) ---
with tab1:
    st.text_input("🔑 HEX SEED:", key="avi_h")
    if st.button("🚀 START AVIATOR", use_container_width=True):
        v_moy = round(random.uniform(4.0, 15.0), 2)
        st.markdown(f"<div class='prediction-card'><h1>{v_moy}x</h1></div>", unsafe_allow_html=True)

with tab2:
    st.text_input("🔑 HEX SEED:", key="cos_h")
    if st.button("🚀 START COSMOS", use_container_width=True):
        v_moy = round(random.uniform(2.0, 8.0), 2)
        st.markdown(f"<div class='prediction-card'><h1 style='color:#ffd700;'>{v_moy}x</h1></div>", unsafe_allow_html=True)

with tab3:
    st.file_uploader("📷 Capture History:", type=['jpg','png','jpeg'], key="mines_cap")
    if st.button("⚡ GENERATE MINES SCHEMA", use_container_width=True):
        stars = random.sample(range(25), k=6)
        grid = '<div style="display: grid; grid-template-columns: repeat(5, 45px); gap: 8px; justify-content: center;">'
        for i in range(25):
            color = "#ffd700" if i in stars else "#1a1f26"
            grid += f'<div style="width:45px; height:45px; background:{color}; border-radius:5px;"></div>'
        st.markdown(grid + '</div>', unsafe_allow_html=True)

# --- TAB 4: PENALTY FULL SYNC + TIMER ---
with tab4:
    st.subheader("⚽ PENALTY VIP PREDICTOR")
    mode_p = st.selectbox("Fidio ny Mode:", ["FACILE (Daka 1 -> x2.93)", "MOYEN (Daka 3 -> x12.13)"])
    
    if st.button("⚡ START NEURAL ANALYSIS", use_container_width=True):
        nb_shots = 1 if "FACILE" in mode_p else 3
        targets = ["ANKAVIA AMBONY", "ANKAVANANA AMBONY", "AFOVOANY", "ANKAVIA AMBANY", "ANKAVANANA AMBANY"]
        sequence = random.sample(targets, k=nb_shots)
        
        for i, shot in enumerate(sequence):
            st.markdown(f"<div class='step-box'><b>DAKA {i+1}:</b> <span style='color:#00ffcc; font-size:22px;'>{shot}</span></div>", unsafe_allow_html=True)
            
            # TIMER 5 SECONDS
            with st.empty():
                for seconds in range(5, 0, -1):
                    st.markdown(f"<p class='timer-text'>⏳ Dakaona afaka: {seconds}s</p>", unsafe_allow_html=True)
                    time.sleep(1)
                st.markdown("<p style='color:#00ffcc; font-weight:bold;'>🔥 DAKAO IZAO!</p>", unsafe_allow_html=True)
            time.sleep(1)
        
        st.success("SEQUENCE FINIE! Manaova Cashout izao.")

st.write("---")
with st.expander("📖 CONSIGNES & FAMPIANARANA (Vakio tsara)"):
    st.markdown("""
    1. **Fidio ny firenena**: Arzantina no tsara indrindra ho an'ny algorithm.
    2. **Araho ny Timer**: Rehefa mipoitra ny teny hoe 'DAKAO IZAO', vao manindry ny baolina ianao. Io no mampitovy ny server sy ny app.
    3. **Mode Moyen**: Aza dakaona haingana loatra ireo daka 3. Miandrasa foana ny app hiteny 'Dakaona'.
    4. **Reset Algorithm**: Raha vao mahazo 'Win' lehibe (x12.13), mivoaha amin'ny lalao (Exit), miandrasa 2 minitra, vao miverina.
    5. **Mise**: Ampiasao ny 500 MGA na 5000 MGA araka ny teti-bolanao.
    """)
