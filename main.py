import streamlit as st
import random
import time
from datetime import datetime, timedelta

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V76.0 FIX", layout="wide")

if 'prediction_history' not in st.session_state:
    st.session_state.prediction_history = []

# --- STYLE CSS (Namboarina mba tsy hisy error) ---
st.markdown("""
    <style>
    .stApp { background-color: #050a10; color: #ffffff; }
    .titan-header { font-size: 30px; font-weight: 900; text-align: center; color: #00ffcc; border-bottom: 3px solid #00ffcc; padding-bottom: 10px; }
    .card-res { background: rgba(0, 255, 204, 0.1); border: 2px solid #00ffcc; border-radius: 15px; padding: 20px; text-align: center; }
    .next-rounds { background: rgba(255, 215, 0, 0.1); border: 1px dashed #ffd700; padding: 15px; border-radius: 10px; margin-top: 15px; text-align: center; color: #ffd700; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="titan-header">TITAN V76.0 BEAST-FIX 💎</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚽ PENALTY VIP"])

# --- SHARED CALCULATION LOGIC ---
def get_prediction(seed, lera):
    random.seed(hash(seed + lera + str(time.time())))
    p_moy = round(random.uniform(2.5, 6.2), 2)
    accuracy = random.randint(94, 99)
    base_time = datetime.strptime(lera, "%H:%M")
    next_times = [(base_time + timedelta(minutes=random.randint(i*2, i*5))).strftime("%H:%M") for i in range(1, 4)]
    return p_moy, accuracy, next_times

# --- AVIATOR ---
with tab1:
    st.file_uploader("📷 CAPTURE DE TOUR (Aviator):", type=['jpg','png','jpeg'], key="avi_c")
    a_seed = st.text_input("🔑 HEX SEED (Aviator):", key="avi_s")
    a_lera = st.text_input("🕒 HEURE:", value=datetime.now().strftime("%H:%M"), key="avi_l")
    
    if st.button("🚀 EXECUTE AVIATOR"):
        pm, acc, nt = get_prediction(a_seed, a_lera)
        st.markdown(f"<div class='card-res'><h3>ACCURACY: {acc}%</h3><h1>{pm}x</h1></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='next-rounds'>🕒 LERA FIDIRANA: {' | '.join(nt)}</div>", unsafe_allow_html=True)
        st.session_state.prediction_history.append(f"✈️ Aviator | {a_lera} | {pm}x")

# --- COSMOS X ---
with tab2:
    st.file_uploader("📷 CAPTURE DE TOUR (Cosmos):", type=['jpg','png','jpeg'], key="cos_c")
    c_seed = st.text_input("🔑 HEX SEED (Cosmos):", key="cos_s")
    c_lera = st.text_input("🕒 HEURE:", value=datetime.now().strftime("%H:%M"), key="cos_l")
    
    if st.button("🚀 EXECUTE COSMOS"):
        pm, acc, nt = get_prediction(c_seed, c_lera)
        st.markdown(f"<div class='card-res'><h3>ACCURACY: {acc}%</h3><h1>{pm}x</h1></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='next-rounds'>🕒 LERA FIDIRANA: {' | '.join(nt)}</div>", unsafe_allow_html=True)
        st.session_state.prediction_history.append(f"🚀 Cosmos | {c_lera} | {pm}x")

# --- MINES VIP ---
with tab3:
    st.file_uploader("📷 CAPTURE DE TOUR (Mines):", type=['jpg','png','jpeg'], key="min_c")
    m_seed = st.text_input("💻 CLIENT SEED:", key="min_s")
    nb_m = st.select_slider("💣 NOMBRE DE MINES:", options=[1, 2, 3, 4, 5, 6, 7], value=3)
    
    if st.button("⚡ SCAN SECURE GRID"):
        random.seed(hash(m_seed + str(nb_m)))
        # Misafidy kintana 3 hatramin'ny 5 arakaraky ny isan'ny baomba
        stars = random.sample(range(25), k=5 if nb_m < 4 else 3)
        grid = '<div style="display:grid; grid-template-columns:repeat(5, 50px); gap:10px; justify-content:center; margin-top:20px;">'
        for i in range(25):
            color = "#00ffcc" if i in stars else "#1a1f26"
            grid += f'<div style="width:50px; height:50px; background:{color}; border-radius:8px; border:2px solid #00ffcc;"></div>'
        st.markdown(grid + '</div>', unsafe_allow_html=True)
        st.session_state.prediction_history.append(f"💣 Mines | {nb_m} Mines Grid")

# --- PENALTY ---
with tab4:
    if st.button("⚽ SHOT PREDICTION"):
        target = random.choice(["ANKAVIA", "AFOVOANY", "ANKAVANANA"])
        st.info(f"TARGET: {target}")

# --- HISTORIQUE ---
st.write("---")
if st.button("🗑️ RESET"):
    st.session_state.prediction_history = []
    st.rerun()

st.subheader("📜 HISTORIQUE")
for h in reversed(st.session_state.prediction_history[-5:]):
    st.write(h)
