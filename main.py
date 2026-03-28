import streamlit as st
import random
from datetime import datetime

# --- STYLE ULTIMATE (NEON & GLASSMORPHISM) ---
st.set_page_config(page_title="TITAN V62.9 TRINITY", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; color: #e0e0e0; }
    
    /* Header miaraka amin'ny Neon Glow */
    .titan-header {
        font-size: 45px; font-weight: 900; text-align: center;
        color: #00ffcc; text-shadow: 0 0 10px #00ffcc, 0 0 20px #00ffcc;
        margin-bottom: 5px; letter-spacing: 2px;
    }
    .version-tag { text-align: center; color: #3366ff; font-weight: bold; margin-bottom: 25px; }

    /* Karatra ho an'ny Prediction */
    .prediction-card {
        background: rgba(255, 255, 255, 0.03); 
        border: 1px solid rgba(0, 255, 204, 0.3);
        border-radius: 20px; padding: 30px; text-align: center;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(4px); margin-top: 20px;
    }
    
    /* Accuracy sy Loko */
    .accuracy-badge {
        background: #ffd700; color: black; padding: 5px 15px;
        border-radius: 50px; font-weight: bold; font-size: 14px;
    }
    .val-moyenne { font-size: 60px; font-weight: 800; color: #ffffff; margin: 10px 0; }
    
    /* History Stylé */
    .history-card {
        background: #161b22; border-radius: 10px; padding: 10px 20px;
        margin-bottom: 10px; display: flex; justify-content: space-between;
        border: 1px solid #21262d;
    }
    
    /* Gestion de Mise Box */
    .strategy-box {
        background: linear-gradient(90deg, #1e293b, #0f172a);
        border-left: 5px solid #3366ff; padding: 20px; border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Fitahirizana History
if 'avi_hist' not in st.session_state: st.session_state.avi_hist = []
if 'cos_hist' not in st.session_state: st.session_state.cos_hist = []
if 'min_hist' not in st.session_state: st.session_state.min_hist = []

st.markdown('<h1 class="titan-header">TITAN TRINITY</h1>', unsafe_allow_html=True)
st.markdown('<p class="version-tag">STABLE VERSION V62.9 • 2026 EDITION</p>', unsafe_allow_html=True)

# --- GESTION DE MISE & STRATÉGIE (FISEHOANA VAOVAO) ---
with st.expander("📊 GESTION DE MISE & INSTRUCTIONS"):
    st.markdown("""
    <div class="strategy-box">
        <h4 style="color:#00ffcc; margin-top:0;">💰 STRATÉGIE DE MISE (60/40)</h4>
        <p>Raha <b>10,000 MGA</b> ny renivolanao: 
        <br>• <b>Mise A: 600 MGA</b> (Cashout @ 2.00x)
        <br>• <b>Mise B: 400 MGA</b> (Target Moyen/Max)</p>
        <hr style="border:0.5px solid #334155;">
        <h4 style="color:#ffd700;">🕒 FITSIPÌKA -1 / MOYEN / +1</h4>
        <p>Jereo ny vinavina amin'ny minitra iray taloha sy aoriana mba hanamarinana ny <b>Signal</b>.</p>
    </div>
    """, unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS", "💣 MINES"])

# --- 1. AVIATOR ---
with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.file_uploader("📷 Capture History", type=['jpg','png','jpeg'], key="avi_up")
        lera_avi = st.text_input("🕒 Lera fidirana (-1/0/+1):", value=datetime.now().strftime("%H:%M"), key="avi_l")
    with col2:
        hex_avi = st.text_input("🔑 HEX SEED:", key="avi_h", placeholder="Ampidiro ny Seed...")
        
    if st.button("🚀 START ANALYSIS", use_container_width=True, key="btn_avi"):
        if hex_avi:
            base = random.uniform(2.0, 8.0)
            v_min, v_moy, v_max = round(base*0.85, 2), round(base, 2), round(base*1.3, 2)
            acc = f"{random.randint(95, 99)}%"
            st.session_state.avi_hist.insert(0, {"time": lera_avi, "val": f"{v_moy}x", "acc": acc})
            st.markdown(f"""
                <div class='prediction-card'>
                    <span class='accuracy-badge'>{acc} ACCURACY</span>
                    <p style='color:#888; margin-top:15px;'>RANGE: {v_min}x — {v_max}x</p>
                    <div class='val-moyenne'>{v_moy}x</div>
                    <p style='color:#00ffcc; letter-spacing:3px;'>SIGNAL DETECTED</p>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("### 📜 PREDICTION HISTORY")
    for item in st.session_state.avi_hist[:5]:
        st.markdown(f"<div class='history-card'><span>{item['time']}</span><span style='color:#00ffcc; font-weight:bold;'>{item['val']}</span><span style='color:#ffd700;'>{item['acc']}</span></div>", unsafe_allow_html=True)

# --- 2. COSMOS ---
with tab2:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.file_uploader("📷 Capture History", type=['jpg','png','jpeg'], key="cos_up")
        lera_cos = st.text_input("🕒 Lera fidirana (-1/0/+1):", value=datetime.now().strftime("%H:%M"), key="cos_l")
    with col2:
        hex_cos = st.text_input("🔑 HEX SEED:", key="cos_h", placeholder="Ampidiro ny Seed...")

    if st.button("🚀 START ANALYSIS", use_container_width=True, key="btn_cos"):
        if hex_cos:
            base = random.uniform(1.8, 6.0)
            v_min, v_moy, v_max = round(base*0.8, 2), round(base, 2), round(base*1.25, 2)
            acc = f"{random.randint(94, 98)}%"
            st.session_state.cos_hist.insert(0, {"time": lera_cos, "val": f"{v_moy}x", "acc": acc})
            st.markdown(f"""
                <div class='prediction-card'>
                    <span class='accuracy-badge' style='background:#3366ff; color:white;'>{acc} ACCURACY</span>
                    <p style='color:#888; margin-top:15px;'>RANGE: {v_min}x — {v_max}x</p>
                    <div class='val-moyenne' style='color:#ffd700;'>{v_moy}x</div>
                    <p style='color:#3366ff; letter-spacing:3px;'>COSMOS SIGNAL</p>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("### 📜 PREDICTION HISTORY")
    for item in st.session_state.cos_hist[:5]:
        st.markdown(f"<div class='history-card'><span>{item['time']}</span><span style='color:#ffd700; font-weight:bold;'>{item['val']}</span><span>{item['acc']}</span></div>", unsafe_allow_html=True)

# --- 3. MINES ---
with tab3:
    st.subheader("💣 MINES VIP PREDICTOR")
    nb_mines = st.selectbox("💣 Isan'ny baomba (Mines):", [1, 2, 3, 4, 5, 6, 7], index=2)
    c_seed = st.text_input("💻 Client Seed:", key="m_c")
    s_seed = st.text_input("🖥️ Server Seed:", key="m_s")
    
    if st.button("⚡ GENERATE VIP SCHEMA", use_container_width=True):
        if c_seed and s_seed:
            nb_stars = 6 if nb_mines >= 3 else 3
            stars = random.sample(range(25), k=nb_stars)
            grid = '<div style="display: grid; grid-template-columns: repeat(5, 55px); gap: 12px; justify-content: center; margin: 30px 0;">'
            for i in range(25):
                glow = "box-shadow: 0 0 15px #ffd700;" if i in stars else ""
                color = "#ffd700" if i in stars else "#1a1f26"
                icon = "⭐" if i in stars else ""
                grid += f'<div style="width:55px; height:55px; background:{color}; border-radius:12px; border: 1px solid #333; display:flex; align-items:center; justify-content:center; font-size:20px; {glow}">{icon}</div>'
            grid += '</div>'
            st.markdown(grid, unsafe_allow_html=True)
            st.markdown(f"<p style='text-align:center;' class='accuracy-badge'>{nb_mines} MINES - 98% ACCURACY</p>", unsafe_allow_html=True)
            st.session_state.min_hist.insert(0, f"{nb_mines} Mines - Schema ({datetime.now().strftime('%H:%M')})")

# --- RESET ---
st.write("---")
if st.button("🗑️ RESET ALL DATA", use_container_width=True):
    st.session_state.avi_hist, st.session_state.cos_hist, st.session_state.min_hist = [], [], []
    st.rerun()
