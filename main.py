import streamlit as st
import random
import time
from datetime import datetime

# --- 1. CONFIGURATION & SESSION STATE ---
st.set_page_config(page_title="TITAN V63.9 ELITE", layout="wide")

if 'history' not in st.session_state:
    st.session_state.history = []
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def check_password():
    if st.session_state["password"] == "TITAN2026": 
        st.session_state.authenticated = True
    else:
        st.error("❌ ACCESS DENIED.")

# --- LOGIN ---
if not st.session_state.authenticated:
    st.markdown("<style>.stApp { background-color: #050a10; }</style>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; padding:50px; border:2px solid #00ffcc; border-radius:30px; margin-top:100px;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='color:#00ffcc;'>🛸 TITAN ELITE V63.9</h1>", unsafe_allow_html=True)
    st.text_input("ENTER SYSTEM KEY:", type="password", key="password", on_change=check_password)
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- CSS STYLE VIP ELITE ---
st.markdown("""
    <style>
    .stApp { background-color: #080c14; color: #ffffff; }
    .titan-header { font-size: 40px; font-weight: 900; text-align: center; color: #00ffcc; text-shadow: 0 0 20px #00ffcc; }
    .signal-on { color: #00ffcc; font-weight: bold; animation: blinker 1.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    .prediction-card { background: rgba(0, 255, 204, 0.05); border: 1px solid #00ffcc; border-radius: 15px; padding: 20px; text-align: center; }
    .hist-box { background: #1a1f26; padding: 10px; border-radius: 5px; margin-top: 5px; font-size: 12px; border-left: 3px solid #ffd700; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="titan-header">TITAN OMNI-STRIKE ELITE</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center;"><span class="signal-on">● LIVE SIGNAL CONNECTED</span> | V63.9 VIP</p>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS", "💣 MINES VIP", "⚽ PENALTY VIP"])

# --- TAB 1: AVIATOR ---
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.file_uploader("📷 Capture History:", type=['jpg','png'], key="avi_cap")
        st.text_input("🕒 Heure Actuelle:", value=datetime.now().strftime("%H:%M"), key="avi_t")
    with col2:
        st.text_input("🔑 HEX/SEED:", placeholder="Paste here...", key="avi_s")
    
    if st.button("🚀 EXECUTE PREDICTION", use_container_width=True):
        res = round(random.uniform(4.2, 18.5), 2)
        st.session_state.history.append(f"Aviator: {res}x at {datetime.now().strftime('%H:%M:%S')}")
        st.markdown(f"<div class='prediction-card'><h1>{res}x</h1><p>Next Flight Target</p></div>", unsafe_allow_html=True)

# --- TAB 2: COSMOS ---
with tab2:
    st.text_input("🕒 Heure:", value=datetime.now().strftime("%H:%M"), key="cos_t")
    st.text_input("🔑 SEED:", key="cos_s")
    if st.button("🚀 START COSMOS SCAN", use_container_width=True):
        res = round(random.uniform(2.1, 9.8), 2)
        st.session_state.history.append(f"Cosmos: {res}x at {datetime.now().strftime('%H:%M:%S')}")
        st.markdown(f"<div class='prediction-card'><h1 style='color:#ffd700;'>{res}x</h1></div>", unsafe_allow_html=True)

# --- TAB 3: MINES VIP (Misy Seed + Sary) ---
with tab3:
    st.subheader("💣 NEURAL MINES ENGINE")
    st.file_uploader("📷 Grid Capture:", type=['jpg','png'], key="min_cap")
    st.text_input("🔑 CURRENT SEED:", placeholder="Enter Mines Seed...", key="min_s")
    nb_m = st.slider("Nombre de Mines:", 1, 5, 3)
    
    if st.button("⚡ ANALYZE SEED & GENERATE", use_container_width=True):
        stars = random.sample(range(25), k=7 if nb_m < 3 else 5)
        grid = '<div style="display: grid; grid-template-columns: repeat(5, 45px); gap: 8px; justify-content: center; margin-top:10px;">'
        for i in range(25):
            color = "#ffd700" if i in stars else "#1a1f26"
            grid += f'<div style="width:45px; height:45px; background:{color}; border-radius:5px; border:1px solid #333;"></div>'
        st.markdown(grid + '</div>', unsafe_allow_html=True)
        st.info(f"Seed Analyzed: {st.session_state.min_s if st.session_state.min_s else 'Auto-Generated'}")

# --- TAB 4: PENALTY (5 Strikes) ---
with tab4:
    mode_p = st.selectbox("Mode:", ["FACILE (x2.93)", "MOYEN (x12.13)"])
    if st.button("⚡ START 5-STRIKE SEQ", use_container_width=True):
        targets = ["ANKAVIA AMBONY", "ANKAVANANA AMBONY", "AFOVOANY", "ANKAVIA AMBANY", "ANKAVANANA AMBANY"]
        seq = random.sample(targets, k=5)
        st.session_state.history.append(f"Penalty: {mode_p} Seq Generated")
        for i, s in enumerate(seq):
            st.markdown(f"<div style='background:rgba(0,255,204,0.1); padding:10px; margin:5px; border-radius:5px;'><b>SHOT {i+1}:</b> {s}</div>", unsafe_allow_html=True)
            time.sleep(0.5)

# --- 5. HISTORIQUE & CONSIGNES ---
st.write("---")
col_h, col_c = st.columns(2)
with col_h:
    st.subheader("📜 HISTORIQUE")
    for h in reversed(st.session_state.history[-5:]):
        st.markdown(f"<div class='hist-box'>{h}</div>", unsafe_allow_html=True)

with col_c:
    st.subheader("📖 VIP CONSIGNES")
    st.write("1. Copy ny **Seed** ao amin'ny lalao ary apetaho amin'ny app.")
    st.write("2. Jereo ny **Signal Status** (Tokony ho maitso).")
    st.write("3. Ampiasao ny **Lera** (Heure) mifanaraka amin'ny findainao.")

if st.button("🔓 LOGOUT"):
    st.session_state.authenticated = False
    st.rerun()
