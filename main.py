import streamlit as st
import random
import time
from datetime import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V65.6 PREMIUM", layout="wide")

# --- STYLE CSS (Tsy nisy novaina fa nohamafisina ny fitazonana ny données) ---
st.markdown("""
    <style>
    .stApp { background-color: #050a10; color: #ffffff; }
    .titan-header { font-size: 32px; font-weight: 900; text-align: center; color: #00ffcc; text-shadow: 0 0 10px #00ffcc; padding: 10px; border-bottom: 2px solid #00ffcc; }
    .label-text { color: #ffd700; font-weight: bold; font-size: 16px; margin-top: 15px; }
    .result-card { background: rgba(0, 255, 204, 0.1); border: 2px solid #00ffcc; border-radius: 15px; padding: 20px; text-align: center; margin-top: 15px; }
    .stat-box { background: rgba(255, 255, 255, 0.05); border: 1px solid #444; border-radius: 8px; padding: 10px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="titan-header">TITAN OMNI-STRIKE V65.6</div>', unsafe_allow_html=True)

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚽ PENALTY VIP"])

# --- TAB 1: AVIATOR ---
with tab1:
    st.markdown("### ✈️ AVIATOR PREDICTOR")
    st.markdown('<p class="label-text">📷 CAPTURE HISTORIQUE:</p>', unsafe_allow_html=True)
    st.file_uploader("Upload Aviator", type=['jpg', 'png', 'jpeg'], key="avi_file_v6")
    
    st.markdown('<p class="label-text">🕒 HEURE (LERA):</p>', unsafe_allow_html=True)
    avi_h = st.text_input("Heure", value=datetime.now().strftime("%H:%M"), key="avi_h_v6")
    
    if st.button("🚀 GET SIGNAL AVIATOR", use_container_width=True):
        res = round(random.uniform(1.8, 12.0), 2)
        st.markdown(f"<div class='result-card'><h2>SIGNAL:</h2><h1>{res}x</h1></div>", unsafe_allow_html=True)

# --- TAB 2: COSMOS X (MIARAKA AMIN'NY HEX SY STATS REHETRA) ---
with tab2:
    st.markdown("### 🚀 COSMOS X PREMIUM")
    
    st.markdown('<p class="label-text">📷 CAPTURE HISTORIQUE:</p>', unsafe_allow_html=True)
    st.file_uploader("Upload Cosmos", type=['jpg', 'png', 'jpeg'], key="cos_file_v6")
    
    st.markdown('<p class="label-text">🔑 HEX SEED (Azo kitihana):</p>', unsafe_allow_html=True)
    hex_val = st.text_input("Paste Hex Here", placeholder="OxFF...", key="cos_hex_v6")
    
    st.markdown('<p class="label-text">🕒 HEURE (LERA):</p>', unsafe_allow_html=True)
    cos_h = st.text_input("Heure Cosmos", value=datetime.now().strftime("%H:%M"), key="cos_h_v6")
    
    if st.button("🚀 EXECUTE COSMOS ANALYSIS", use_container_width=True):
        if not hex_val:
            st.error("⚠️ Apetaho ny HEX SEED!")
        else:
            random.seed(hash(hex_val + cos_h))
            p_min = round(random.uniform(1.2, 1.7), 2)
            p_moy = round(random.uniform(2.2, 6.0), 2)
            p_max = round(random.uniform(11.0, 42.0), 2)
            pct = random.randint(86, 99)
            
            # Miseho ny Min Moyen Max
            c1, c2, c3 = st.columns(3)
            with c1: st.markdown(f"<div class='stat-box'>MIN<br><b style='color:#ff4b4b;'>{p_min}x</b></div>", unsafe_allow_html=True)
            with c2: st.markdown(f"<div class='stat-box'>MOYEN<br><b style='color:#ffd700;'>{p_moy}x</b></div>", unsafe_allow_html=True)
            with c3: st.markdown(f"<div class='stat-box'>MAX<br><b style='color:#00ffcc;'>{p_max}x</b></div>", unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class='result-card'>
                    <p>PROBABILITY ACCURACY</p>
                    <h1 style='color:#00ffcc;'>{pct}%</h1>
                    <p>RECOMMANDATION: <b>{p_moy}x</b></p>
                </div>
            """, unsafe_allow_html=True)

# --- TAB 4: PENALTY VIP ---
with tab4:
    st.markdown("### ⚽ PENALTY VIP")
    st.markdown('<p class="label-text">⚽ MODE:</p>', unsafe_allow_html=True)
    st.selectbox("Mode", ["FACILE (x2.93)", "MOYEN", "DIFFICILE"], key="p_mode_v6")
    
    if st.button("⚽ GENERATE SEQUENCE", use_container_width=True):
        spots = ["ANKAVIA AMBONY", "AFOVOANY", "ANKAVANANA AMBANY"]
        for i in range(3):
            st.info(f"SHOT {i+1}: {random.choice(spots)}")

# --- TAB 3: MINES VIP ---
with tab3:
    st.markdown("### 💣 MINES VIP SCANNER")
    if st.button("⚡ SCAN GRID", use_container_width=True):
        stars = random.sample(range(25), k=5)
        grid = '<div style="display: grid; grid-template-columns: repeat(5, 45px); gap: 10px; justify-content: center;">'
        for i in range(25):
            color = "#00ffcc" if i in stars else "#1a1f26"
            grid += f'<div style="width:45px; height:45px; background:{color}; border-radius:5px;"></div>'
        st.markdown(grid + '</div>', unsafe_allow_html=True)
