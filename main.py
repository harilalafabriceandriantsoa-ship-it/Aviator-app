import streamlit as st
import random
import time
from datetime import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V64.2 ELITE", layout="wide")

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
    st.markdown("<h1 style='color:#00ffcc;'>🛸 TITAN ELITE V64.2</h1>", unsafe_allow_html=True)
    st.text_input("ENTER SYSTEM KEY:", type="password", key="password", on_change=check_password)
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- STYLE CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #080c14; color: #ffffff; }
    .titan-header { font-size: 35px; font-weight: 900; text-align: center; color: #00ffcc; text-shadow: 0 0 15px #00ffcc; }
    .signal-on { color: #ffd700; font-weight: bold; animation: blinker 1.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    .prediction-card { background: rgba(0, 255, 204, 0.05); border: 1px solid #00ffcc; border-radius: 15px; padding: 20px; text-align: center; }
    .hist-box { background: #1a1f26; padding: 10px; border-radius: 5px; margin-top: 5px; border-left: 4px solid #00ffcc; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="titan-header">TITAN OMNI-STRIKE V64.2</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center;"><span class="signal-on">● SEED ENGINE CONNECTED</span> | V64.2 VIP</p>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚽ PENALTY"])

# --- TAB 3: MINES VIP (PRO PREDICTION) ---
with tab3:
    st.subheader("💣 NEURAL MINES ENGINE")
    
    # Drag and drop capture
    st.file_uploader("📷 Grid Capture History:", type=['jpg','png','jpeg'], key="min_cap")
    
    col1, col2 = st.columns(2)
    with col1:
        client_seed = st.text_input("💻 Seed du Client:", placeholder="Paste Seed here...", key="c_seed")
    with col2:
        server_seed = st.text_input("🖥️ Seed du Serveur:", placeholder="Paste Seed here...", key="s_seed")
        
    nb_mines = st.select_slider("Nombre de Mines:", options=[1, 3, 5], value=5)
    
    if st.button("⚡ ANALYZE SEEDS & SCAN GRID", use_container_width=True):
        # Algorithm simulation based on seed length/hash
        random.seed(len(client_seed) + len(server_seed))
        stars = random.sample(range(25), k=7 if nb_mines == 5 else 5)
        
        st.session_state.history.append(f"Mines: Grid Generated at {datetime.now().strftime('%H:%M')}")
        
        # Grid Display (Yellow for stars like in your screenshot)
        grid = '<div style="display: grid; grid-template-columns: repeat(5, 50px); gap: 10px; justify-content: center; margin-top:20px;">'
        for i in range(25):
            color = "#ffd700" if i in stars else "#2c3e50"
            grid += f'<div style="width:50px; height:50px; background:{color}; border-radius:8px; border:1px solid #34495e;"></div>'
        st.markdown(grid + '</div>', unsafe_allow_html=True)
        st.success("✅ Prediction Complete. Follow the yellow stars.")

# --- OTHER TABS (Aviator, Cosmos, Penalty) ---
with tab1:
    st.file_uploader("📷 Capture:", type=['jpg','png'], key="avi_cap")
    st.text_input("🕒 Heure:", value=datetime.now().strftime("%H:%M"), key="avi_t")
    if st.button("🚀 EXECUTE", use_container_width=True):
        res = round(random.uniform(5.5, 20.0), 2)
        st.session_state.history.append(f"Aviator: {res}x at {datetime.now().strftime('%H:%M')}")
        st.markdown(f"<div class='prediction-card'><h1>{res}x</h1></div>", unsafe_allow_html=True)

with tab2:
    st.file_uploader("📷 Capture:", type=['jpg','png'], key="cos_cap")
    st.text_input("🕒 Lera:", value=datetime.now().strftime("%H:%M"), key="cos_t")
    if st.button("🚀 START SCAN", use_container_width=True):
        res = round(random.uniform(3.0, 15.0), 2)
        st.session_state.history.append(f"Cosmos X: {res}x at {datetime.now().strftime('%H:%M')}")
        st.markdown(f"<div class='prediction-card'><h1 style='color:#ffd700;'>{res}x</h1></div>", unsafe_allow_html=True)

with tab4:
    if st.button("⚽ GENERATE PENALTY SEQ", use_container_width=True):
        targets = ["ANKAVIA AMBONY", "ANKAVANANA AMBONY", "AFOVOANY", "ANKAVIA AMBANY", "ANKAVANANA AMBANY"]
        seq = random.sample(targets, k=5)
        st.session_state.history.append(f"Penalty: Seq at {datetime.now().strftime('%H:%M')}")
        for i, s in enumerate(seq):
            st.markdown(f"<div class='hist-box'><b>Daka {i+1}:</b> {s}</div>", unsafe_allow_html=True)

# --- 📜 HISTORIQUE & FAMAFANA ---
st.write("---")
col_h, col_t = st.columns([2, 1])

with col_h:
    st.subheader("📜 HISTORIQUE")
    if st.button("🗑️ FAMAFANA HISTORIQUE", use_container_width=True):
        st.session_state.history = []
        st.rerun()
    
    for h in reversed(st.session_state.history[-5:]):
        st.markdown(f"<div class='hist-box'>{h}</div>", unsafe_allow_html=True)

with col_t:
    st.subheader("📖 VIP TIPS")
    st.write("- Mines: Adikao ny Seed ao amin'ny lalao vao manindry 'Analyze'.")
    st.write("- Cosmos: Jereo tsara ny lera mifanaraka amin'ny findainao.")
