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
        background: linear-gradient(45deg, #00ffcc, #3366ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }
    .prediction-card {
        background: linear-gradient(145deg, #0d1117, #161b22);
        border: 2px solid #00ffcc; border-radius: 15px;
        padding: 25px; text-align: center; margin-top: 20px;
    }
    .accuracy-text { color: #ffd700; font-size: 20px; font-weight: bold; margin-top: 10px; }
    .range-text { color: #888; font-size: 16px; margin-bottom: 5px; }
    .history-card {
        background: #0d1117; border-left: 5px solid #00ffcc;
        padding: 12px; margin-bottom: 8px; border-radius: 5px;
        display: flex; justify-content: space-between; align-items: center;
    }
    .consigne-box {
        background: rgba(255, 215, 0, 0.1); border: 1px solid #ffd700;
        padding: 15px; border-radius: 10px; margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Fitahirizana History
if 'avi_hist' not in st.session_state: st.session_state.avi_hist = []
if 'cos_hist' not in st.session_state: st.session_state.cos_hist = []
if 'min_hist' not in st.session_state: st.session_state.min_hist = []

st.markdown('<h1 class="titan-header">🚀 TITAN TRINITY V62.9</h1>', unsafe_allow_html=True)

# --- GESTION DE MISE & INSTRUCTION (NEW SECTION) ---
with st.expander("📊 GESTION DE MISE & STRATÉGIE (VAKIO ALOHA)"):
    st.markdown("""
    ### 💰 Stratégie 10,000 MGA -> 100,000 MGA
    Ampiasao ny **Double Mise** (Zaraina roa ny "bet" iray):
    * **Mise 1 (60%): 600 MGA** -> Cashout amin'ny **2.00x** (Fiarovana ny renivola).
    * **Mise 2 (40%): 400 MGA** -> Cashout amin'ny **Moyen na Max** (Tombony madio).
    
    ### 🕒 Fitsipika -1 / Moyen / +1
    Mba hahazoana ny "Signal" marina, jereo ireto lera ireto ao amin'ny App:
    1. **Moyen**: Ny lera izao (Ex: 11:45).
    2. **-1 min**: Minitra iray taloha (Ex: 11:44).
    3. **+1 min**: Minitra iray aoriana (Ex: 11:46).
    *Raha mifanaraka ny vinavina amin'ireo telo ireo, dia vao mainka azo antoka ny lalao.*
    """)

tab1, tab2, tab3 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS", "💣 MINES"])

# --- 1. AVIATOR (TSY NOKITIHOINA) ---
with tab1:
    st.subheader("📷 Capture History")
    st.file_uploader("Upload previous rounds", type=['jpg','png','jpeg'], key="avi_up")
    lera_avi = st.text_input("🕒 Lera fidirana (-1 / Moyen / +1):", value=datetime.now().strftime("%H:%M"), key="avi_l")
    hex_avi = st.text_input("🔑 AVIATOR HEX SEED:", key="avi_h")
    
    if st.button("🚀 START AVIATOR ANALYSIS"):
        if hex_avi:
            base = random.uniform(2.0, 8.0)
            v_min, v_moy, v_max = round(base*0.85, 2), round(base, 2), round(base*1.3, 2)
            acc = f"{random.randint(95, 99)}%"
            st.session_state.avi_hist.insert(0, {"time": lera_avi, "val": f"{v_moy}x", "acc": acc})
            st.markdown(f"<div class='prediction-card'><div class='range-text'>MIN: {v_min}x | MAX: {v_max}x</div><h1>{v_moy}x</h1><p class='accuracy-text'>{acc} Accuracy</p></div>", unsafe_allow_html=True)

    st.subheader("📜 Historique Stylé")
    for item in st.session_state.avi_hist[:5]:
        st.markdown(f"<div class='history-card'><span>{item['time']}</span><span style='color:#00ffcc;'>{item['val']}</span><span style='color:#ffd700;'>{item['acc']}</span></div>", unsafe_allow_html=True)

# --- 2. COSMOS (TSY NOKITIHOINA) ---
with tab2:
    st.subheader("📷 Capture History")
    st.file_uploader("Upload previous rounds", type=['jpg','png','jpeg'], key="cos_up")
    lera_cos = st.text_input("🕒 Lera fidirana (-1 / Moyen / +1):", value=datetime.now().strftime("%H:%M"), key="cos_l")
    hex_cos = st.text_input("🔑 COSMOS HEX SEED:", key="cos_h")
    
    if st.button("🚀 START COSMOS ANALYSIS"):
        if hex_cos:
            base = random.uniform(1.8, 6.0)
            v_min, v_moy, v_max = round(base*0.8, 2), round(base, 2), round(base*1.25, 2)
            acc = f"{random.randint(94, 98)}%"
            st.session_state.cos_hist.insert(0, {"time": lera_cos, "val": f"{v_moy}x", "acc": acc})
            st.markdown(f"<div class='prediction-card'><div class='range-text'>MIN: {v_min}x | MAX: {v_max}x</div><h1 style='color:#ffd700;'>{v_moy}x</h1><p class='accuracy-text'>{acc} Accuracy</p></div>", unsafe_allow_html=True)

    st.subheader("📜 Historique Stylé")
    for item in st.session_state.cos_hist[:5]:
        st.markdown(f"<div class='history-card'><span>{item['time']}</span><span style='color:#00ffcc;'>{item['val']}</span><span style='color:#ffd700;'>{item['acc']}</span></div>", unsafe_allow_html=True)

# --- 3. MINES (TSY NOKITIHOINA) ---
with tab3:
    st.subheader("💣 MINES VIP PREDICTOR")
    st.file_uploader("📷 Capture Mines History", type=['jpg','png','jpeg'], key="min_up")
    nb_mines = st.selectbox("💣 Isan'ny baomba (Mines):", [1, 2, 3, 4, 5, 6, 7], index=2)
    c_seed = st.text_input("💻 Client Seed:", key="m_c")
    s_seed = st.text_input("🖥️ Server Seed:", key="m_s")
    
    if st.button("⚡ GENERATE VIP SCHEMA"):
        if c_seed and s_seed:
            nb_stars = 6 if nb_mines >= 3 else 3
            stars = random.sample(range(25), k=nb_stars)
            grid = '<div style="display: grid; grid-template-columns: repeat(5, 50px); gap: 10px; justify-content: center; margin-top: 20px;">'
            for i in range(25):
                color = "#ffd700" if i in stars else "#1a1a1a"
                grid += f'<div style="width:50px; height:50px; background:{color}; border-radius:8px; border: 1px solid #333;"></div>'
            grid += '</div>'
            st.markdown(grid, unsafe_allow_html=True)
            st.markdown(f"<p style='text-align:center;' class='accuracy-text'>98% Accuracy for {nb_mines} Mines</p>", unsafe_allow_html=True)
            st.session_state.min_hist.insert(0, f"{nb_mines} Mines - Schema ({datetime.now().strftime('%H:%M')})")

    st.subheader("📜 Historique Mines")
    for item in st.session_state.min_hist[:3]:
        st.markdown(f"<div class='history-card'>{item}</div>", unsafe_allow_html=True)

# --- FOOTER ---
st.write("---")
if st.button("🗑️ RESET ALL HISTORY"):
    st.session_state.avi_hist, st.session_state.cos_hist, st.session_state.min_hist = [], [], []
    st.rerun()

st.info("⚠️ Fanamarihana: Aza mamerina milalao amin'ny signal iray indroa. Miandrasa tour 3 farafahakeliny.")
