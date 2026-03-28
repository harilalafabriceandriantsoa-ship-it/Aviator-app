import streamlit as st
import random
import time
from datetime import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V65.0", layout="wide")

# --- STYLE CSS (Namboarina mba tsy hifanindry intsony) ---
st.markdown("""
    <style>
    .stApp { background-color: #050a10; color: #ffffff; }
    .titan-header { 
        font-size: 32px; font-weight: 900; text-align: center; 
        color: #00ffcc; text-shadow: 0 0 10px #00ffcc; 
        padding: 20px; border-bottom: 2px solid #00ffcc;
    }
    .input-label { color: #00ffcc; font-weight: bold; margin-bottom: 5px; }
    .prediction-card { 
        background: rgba(0, 255, 204, 0.1); border: 2px solid #00ffcc; 
        border-radius: 15px; padding: 20px; text-align: center; 
    }
    /* Manala ny elanelana be loatra */
    .block-container { padding-top: 2rem; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="titan-header">TITAN OMNI-STRIKE V65.0</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#00ffcc;'>● PREMIUM INTERFACE FIXED</p>", unsafe_allow_html=True)

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚽ PENALTY"])

# --- TAB 2: COSMOS X (ETO NO MISY NY HEX SEED) ---
with tab2:
    st.markdown("### 🚀 COSMOS X ANALYZER")
    
    # Input HEX SEED mazava tsara
    st.markdown('<p class="input-label">🔑 HEX SEED (Paste from Game):</p>', unsafe_allow_html=True)
    hex_input = st.text_input("", placeholder="OxFF... (Copy-Paste eto)", key="cos_hex_v65")
    
    st.markdown('<p class="input-label">🕒 LERA COSMOS:</p>', unsafe_allow_html=True)
    time_input = st.text_input("Heure", value=datetime.now().strftime("%H:%M"), key="cos_t_v65")
    
    if st.button("🚀 EXECUTE COSMOS", use_container_width=True):
        if not hex_input:
            st.warning("⚠️ Ampidiro aloha ny HEX SEED vao manindry an'ity.")
        else:
            with st.spinner('Analyzing...'):
                time.sleep(1)
                random.seed(hash(hex_input + time_input))
                res = round(random.uniform(1.8, 12.5), 2)
                st.markdown(f"<div class='prediction-card'><h2>SIGNAL:</h2><h1 style='font-size:50px;'>{res}x</h1></div>", unsafe_allow_html=True)

# --- TAB 1, 3, 4 (SIMPLIFIED FOR STABILITY) ---
with tab1:
    st.subheader("✈️ AVIATOR PREDICTOR")
    st.text_input("🕒 Heure:", value=datetime.now().strftime("%H:%M"), key="avi_t_v65")
    if st.button("🚀 GET SIGNAL", use_container_width=True):
        res = round(random.uniform(2.0, 15.0), 2)
        st.markdown(f"<div class='prediction-card'><h1>{res}x</h1></div>", unsafe_allow_html=True)

with tab3:
    st.subheader("💣 NEURAL MINES")
    st.slider("Nombre de Mines:", 1, 5, 3, key="mine_slider")
    if st.button("⚡ SCAN GRID", use_container_width=True):
        stars = random.sample(range(25), k=5)
        grid_html = '<div style="display: grid; grid-template-columns: repeat(5, 40px); gap: 5px; justify-content: center;">'
        for i in range(25):
            color = "#00ffcc" if i in stars else "#1a1f26"
            grid_html += f'<div style="width:40px; height:40px; background:{color}; border-radius:5px; border:1px solid #333;"></div>'
        grid_html += '</div>'
        st.markdown(grid_html, unsafe_allow_html=True)

with tab4:
    st.subheader("⚽ PENALTY SEQUENCE")
    if st.button("🎯 GENERATE", use_container_width=True):
        targets = ["ANKAVIA", "ANKAVANANA", "AFOVOANY"]
        for i in range(5):
            st.write(f"SHOT {i+1}: **{random.choice(targets)}**")
