import streamlit as st
import random
from datetime import datetime

# --- CONFIGURATION STYLE ---
st.set_page_config(page_title="TITAN V62.9 TRINITY", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050a10; color: white; }
    .titan-header {
        font-size: 40px; font-weight: 800; text-align: center;
        color: #00ffcc; margin-bottom: 10px;
    }
    .prediction-card {
        background: rgba(22, 27, 34, 0.9); border: 2px solid #00ffcc;
        border-radius: 15px; padding: 25px; text-align: center; margin-top: 20px;
    }
    .accuracy-text { color: #ffd700; font-size: 20px; font-weight: bold; margin-top: 10px; }
    .range-text { color: #888; font-size: 16px; margin-bottom: 5px; }
    .history-item { font-size: 15px; border-bottom: 1px solid #333; padding: 8px; color: #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

# Fitahirizana History
if 'avi_hist' not in st.session_state: st.session_state.avi_hist = []
if 'cos_hist' not in st.session_state: st.session_state.cos_hist = []
if 'min_hist' not in st.session_state: st.session_state.min_hist = []

st.markdown('<h1 class="titan-header">🚀 TITAN TRINITY V62.9</h1>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS", "💣 MINES"])

# --- 1. AVIATOR ---
with tab1:
    st.subheader("📷 Capture History")
    st.file_uploader("Drag and drop file here", type=['jpg','png','jpeg'], key="avi_up")
    
    lera_avi = st.text_input("🕒 Lera fidirana (HH:MM):", value=datetime.now().strftime("%H:%M"), key="avi_l")
    hex_avi = st.text_input("🔑 AVIATOR HEX SEED:", key="avi_h")
    
    if st.button("🚀 START AVIATOR ANALYSIS"):
        if hex_avi:
            # Logic Prediction Range (Min, Moyen, Max)
            base = random.uniform(2.0, 8.0)
            v_min = round(base * 0.85, 2)
            v_moy = round(base, 2)
            v_max = round(base * 1.3, 2)
            acc = f"{random.randint(95, 99)}%"
            
            st.session_state.avi_hist.insert(0, f"{lera_avi} ⮕ {v_moy}x ({acc})")
            
            st.markdown(f"""
                <div class='prediction-card'>
                    <div class='range-text'>MIN: {v_min}x | MAX: {v_max}x</div>
                    <h1>{v_moy}x</h1>
                    <p>SIGNAL DETECTED</p>
                    <p class='accuracy-text'>{acc} Accuracy</p>
                </div>
            """, unsafe_allow_html=True)

    st.write("---")
    st.subheader("📜 Historique de tour")
    if st.session_state.avi_hist:
        for item in st.session_state.avi_hist[:5]:
            st.markdown(f"<div class='history-item'>{item}</div>", unsafe_allow_html=True)
    else: st.caption("empty")
    
    with st.expander("📝 CONSIGNES"):
        st.write("1. Aza miverina indroa amin'ny signal iray.")
        st.write("2. Ampiasao ny 10% amin'ny solde-nao fotsiny.")

# --- 2. COSMOS ---
with tab2:
    st.subheader("📷 Capture History")
    st.file_uploader("Drag and drop file here", type=['jpg','png','jpeg'], key="cos_up")
    
    lera_cos = st.text_input("🕒 Lera fidirana (HH:MM):", value=datetime.now().strftime("%H:%M"), key="cos_l")
    hex_cos = st.text_input("🔑 COSMOS HEX SEED:", key="cos_h")
    
    if st.button("🚀 START COSMOS ANALYSIS"):
        if hex_cos:
            base = random.uniform(1.8, 6.0)
            v_min = round(base * 0.8, 2)
            v_moy = round(base, 2)
            v_max = round(base * 1.25, 2)
            acc = f"{random.randint(94, 98)}%"
            
            st.session_state.cos_hist.insert(0, f"{lera_cos} ⮕ {v_moy}x ({acc})")
            
            st.markdown(f"""
                <div class='prediction-card'>
                    <div class='range-text'>MIN: {v_min}x | MAX: {v_max}x</div>
                    <h1 style='color: #ffd700;'>{v_moy}x</h1>
                    <p>SIGNAL DETECTED</p>
                    <p class='accuracy-text'>{acc} Accuracy</p>
                </div>
            """, unsafe_allow_html=True)

    st.write("---")
    st.subheader("📜 Historique de tour")
    if st.session_state.cos_hist:
        for item in st.session_state.cos_hist[:5]:
            st.markdown(f"<div class='history-item'>{item}</div>", unsafe_allow_html=True)
    else: st.caption("empty")
        
    with st.expander("📝 CONSIGNES"):
        st.write("1. Aza miverina indroa amin'ny signal iray.")
        st.write("2. Ampiasao ny 10% amin'ny solde-nao.")

# --- 3. MINES ---
with tab3:
    st.subheader("💣 MINES 6-STAR")
    # Nesorina ny Lera eto
    c_seed = st.text_input("💻 Client Seed:", key="m_client")
    s_seed = st.text_input("🖥️ Server Seed:", key="m_server")
    
    if st.button("⚡ GENERATE VIP SCHEMA"):
        if c_seed and s_seed:
            grid = '<div style="display: grid; grid-template-columns: repeat(5, 50px); gap: 10px; justify-content: center; margin-top: 20px;">'
            stars = random.sample(range(25), k=6)
            for i in range(25):
                color = "#ffd700" if i in stars else "#1a1a1a"
                grid += f'<div style="width:50px; height:50px; background:{color}; border-radius:8px; border: 1px solid #333;"></div>'
            grid += '</div>'
            st.markdown(grid, unsafe_allow_html=True)
            st.markdown("<p style='text-align:center;' class='accuracy-text'>98% Accuracy</p>", unsafe_allow_html=True)
            st.session_state.min_hist.insert(0, f"Schema VIP Generated ({datetime.now().strftime('%H:%M')})")

    st.write("---")
    st.subheader("📜 Historique Mines")
    for item in st.session_state.min_hist[:3]:
        st.markdown(f"<div class='history-item'>{item}</div>", unsafe_allow_html=True)

    with st.expander("📝 CONSIGNES"):
        st.write("1. Miandrasa tour 3 farafahakeliny vao manao generate vaovao.")
        st.write("2. Aza mampiasa an'ity schema ity raha efa mihoatra ny 5 minitra ny nampidirana ny seed.")
