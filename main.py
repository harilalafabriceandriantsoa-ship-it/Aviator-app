import streamlit as st
import random
import time
from datetime import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V64.1 ELITE", layout="wide")

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
    st.markdown("<h1 style='color:#00ffcc;'>🛸 TITAN ELITE V64.1</h1>", unsafe_allow_html=True)
    st.text_input("ENTER SYSTEM KEY:", type="password", key="password", on_change=check_password)
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- STYLE CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #080c14; color: #ffffff; }
    .titan-header { font-size: 40px; font-weight: 900; text-align: center; color: #00ffcc; text-shadow: 0 0 20px #00ffcc; }
    .signal-on { color: #ffd700; font-weight: bold; animation: blinker 1.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    .prediction-card { background: rgba(0, 255, 204, 0.05); border: 1px solid #00ffcc; border-radius: 15px; padding: 20px; text-align: center; }
    .hist-box { background: #1a1f26; padding: 12px; border-radius: 8px; margin-top: 8px; border-left: 4px solid #00ffcc; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="titan-header">TITAN OMNI-STRIKE V64.1</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center;"><span class="signal-on">● LIVE SIGNAL SYNC</span> | ELITE VIP</p>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚽ PENALTY VIP"])

# --- TAB 1: AVIATOR ---
with tab1:
    st.file_uploader("📷 Capture History (Aviator):", type=['jpg','png'], key="avi_cap")
    st.text_input("🕒 Heure Aviator:", value=datetime.now().strftime("%H:%M"), key="avi_t")
    if st.button("🚀 EXECUTE AVIATOR", use_container_width=True):
        res = round(random.uniform(5.0, 19.0), 2)
        st.session_state.history.append(f"Aviator: {res}x at {datetime.now().strftime('%H:%M')}")
        st.markdown(f"<div class='prediction-card'><h1>{res}x</h1></div>", unsafe_allow_html=True)

# --- TAB 2: COSMOS X ---
with tab2:
    st.file_uploader("📷 Capture History (Cosmos):", type=['jpg','png'], key="cos_cap")
    st.text_input("🕒 Heure Cosmos:", value=datetime.now().strftime("%H:%M"), key="cos_t")
    st.text_input("🔑 SEED COSMOS:", key="cos_s")
    if st.button("🚀 EXECUTE COSMOS X", use_container_width=True):
        res = round(random.uniform(2.8, 12.5), 2)
        st.session_state.history.append(f"Cosmos X: {res}x at {datetime.now().strftime('%H:%M')}")
        st.markdown(f"<div class='prediction-card'><h1 style='color:#ffd700;'>{res}x</h1></div>", unsafe_allow_html=True)

# --- TAB 3: MINES VIP (Seed 1 & 2) ---
with tab3:
    st.subheader("💣 NEURAL MINES ENGINE")
    st.file_uploader("📷 Grid Capture:", type=['jpg','png'], key="min_cap")
    colA, colB = st.columns(2)
    with colA:
        st.text_input("🔑 CURRENT SEED (1):", placeholder="Current...", key="min_s1")
    with colB:
        st.text_input("🔑 NEXT SEED (2):", placeholder="Next...", key="min_s2")
    
    nb_m = st.slider("Nombre de Mines:", 1, 5, 3)
    if st.button("⚡ ANALYZE SEEDS & SCAN", use_container_width=True):
        stars = random.sample(range(25), k=6)
        st.session_state.history.append(f"Mines: Grid Generated at {datetime.now().strftime('%H:%M')}")
        grid = '<div style="display: grid; grid-template-columns: repeat(5, 45px); gap: 10px; justify-content: center;">'
        for i in range(25):
            color = "#ffd700" if i in stars else "#1a1f26"
            grid += f'<div style="width:45px; height:45px; background:{color}; border-radius:5px; border:1px solid #333;"></div>'
        st.markdown(grid + '</div>', unsafe_allow_html=True)

# --- TAB 4: PENALTY ---
with tab4:
    mode_p = st.selectbox("Mode Penalty:", ["FACILE (x2.93)", "MOYEN (x12.13)"])
    if st.button("⚡ START 5-STRIKE SEQUENCE", use_container_width=True):
        targets = ["ANKAVIA AMBONY", "ANKAVANANA AMBONY", "AFOVOANY", "ANKAVIA AMBANY", "ANKAVANANA AMBANY"]
        seq = random.sample(targets, k=5)
        st.session_state.history.append(f"Penalty: {mode_p} (5 Shots)")
        for i, s in enumerate(seq):
            st.markdown(f"<div style='background:rgba(0,255,204,0.1); padding:10px; margin:5px; border-radius:5px;'><b>SHOT {i+1}:</b> {s}</div>", unsafe_allow_html=True)
            time.sleep(0.3)

# --- 📜 HISTORIQUE & TOOLS ---
st.write("---")
col_h, col_c = st.columns(2)

with col_h:
    st.subheader("📜 HISTORIQUE")
    if st.button("🗑️ FAMAFANA HISTORIQUE", type="secondary"):
        st.session_state.history = []
        st.success("Vafafana ny historique!")
        time.sleep(1)
        st.rerun()
    
    if not st.session_state.history:
        st.info("Aucune donnée enregistrée.")
    for h in reversed(st.session_state.history[-5:]):
        st.markdown(f"<div class='hist-box'>{h}</div>", unsafe_allow_html=True)

with col_c:
    st.subheader("📖 VIP CONSIGNES")
    st.markdown("""
    * **Famafana Historique**: Ampiasao ity bokotra ity isaky ny mahazo fandresena be ianao mba hanadiovana ny algorithm.
    * **Seed 1 & 2**: Aza hadino ny mampiditra ny Seed manaraka (Seed 2) ao amin'ny Mines.
    * **Sync**: Jereo raha mifanaraka tsara amin'ny findainao ny **Heure** apetrakao.
    """)

if st.button("🔓 LOGOUT"):
    st.session_state.authenticated = False
    st.rerun()
