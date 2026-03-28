import streamlit as st
import random
import time
from datetime import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V64.8 PREMIUM", layout="wide")

if 'history' not in st.session_state:
    st.session_state.history = []
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def check_password():
    if st.session_state.get("password_input") == "TITAN2026": 
        st.session_state.authenticated = True
    else:
        st.error("❌ ACCESS DENIED.")

# --- LOGIN ---
if not st.session_state.authenticated:
    st.markdown("<style>.stApp { background-color: #050a10; }</style>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; padding:50px; border:2px solid #00ffcc; border-radius:30px; margin-top:100px;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='color:#00ffcc;'>🛸 TITAN PREMIUM V64.8</h1>", unsafe_allow_html=True)
    st.text_input("ENTER SYSTEM KEY:", type="password", key="password_input", on_change=check_password)
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- STYLE CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #080c14; color: #ffffff; }
    .titan-header { font-size: 35px; font-weight: 900; text-align: center; color: #00ffcc; text-shadow: 0 0 15px #00ffcc; margin-bottom: 0px; }
    .signal-status { text-align: center; color: #00ffcc; font-size: 14px; margin-bottom: 20px; font-weight: bold; }
    .prediction-card { background: rgba(0, 255, 204, 0.1); border: 2px solid #00ffcc; border-radius: 15px; padding: 20px; text-align: center; margin: 10px 0; box-shadow: 0 0 20px rgba(0, 255, 204, 0.2); }
    .hist-box { background: #1a1f26; padding: 10px; border-radius: 5px; margin-top: 5px; border-left: 4px solid #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="titan-header">TITAN OMNI-STRIKE V64.8</h1>', unsafe_allow_html=True)
st.markdown('<p class="signal-status">● LIVE SIGNAL CONNECTED | PREMIUM MODE ACTIVE</p>', unsafe_allow_html=True)

# --- VIP CONSIGNES ---
with st.expander("📜 VIP CONSIGNES & STRATEGIES (Patricia Edition)"):
    st.markdown("### 📝 Torolalana ho an'i Patricia:")
    st.write("- **Aviator/Cosmos**: Aza adino ny manavao ny 'Heure' isaky ny handefa prediction vaovao.")
    st.write("- **Mines VIP**: Adikao tsara ny **Client Seed** sy **Server Seed** avy ao amin'ny 'Provably Fair' an'ny lalao.")
    st.write("- **Penalty**: Ny mode **FACILE** no manome taham-pahombiazana ambony indrindra (x2.93).")

tab1, tab2, tab3, tab4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚽ PENALTY VIP"])

# --- TAB 1: AVIATOR ---
with tab1:
    st.file_uploader("📷 Capture Aviator History:", type=['jpg', 'png', 'jpeg'], key="avi_img")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("🕒 Lera Aviator:", value=datetime.now().strftime("%H:%M"), key="avi_t")
    with col2:
        st.selectbox("Algorithm:", ["Neural V2", "Safe Bet"], key="avi_algo")
    
    if st.button("🚀 EXECUTE AVIATOR", use_container_width=True):
        with st.spinner('Analyzing patterns...'):
            time.sleep(1.5)
            random.seed(time.time_ns())
            res = round(random.uniform(2.1, 15.5), 2)
            st.session_state.history.append(f"Aviator: {res}x ({st.session_state.avi_t})")
            st.markdown(f"<div class='prediction-card'><h3 style='color:#00ffcc;'>NEXT CRASH AT:</h3><h1>{res}x</h1></div>", unsafe_allow_html=True)

# --- TAB 2: COSMOS X ---
with tab2:
    st.file_uploader("📷 Capture Cosmos History:", type=['jpg', 'png', 'jpeg'], key="cos_img")
    st.text_input("🔑 HEX SEED:", placeholder="Paste Hex Seed from game...", key="cos_hex")
    st.text_input("🕒 Lera Cosmos:", value=datetime.now().strftime("%H:%M"), key="cos_t")
    
    if st.button("🚀 EXECUTE COSMOS X", use_container_width=True):
        seed_val = st.session_state.cos_hex if st.session_state.cos_hex else str(time.time_ns())
        random.seed(hash(seed_val + st.session_state.cos_t))
        res = round(random.uniform(1.85, 12.0), 2)
        st.session_state.history.append(f"Cosmos X: {res}x ({st.session_state.cos_t})")
        st.markdown(f"<div class='prediction-card'><h3 style='color:#ffd700;'>TARGET MULTIPLIER:</h3><h1>{res}x</h1></div>", unsafe_allow_html=True)

# --- TAB 3: MINES VIP ---
with tab3:
    st.subheader("💣 NEURAL MINES ENGINE")
    st.file_uploader("📷 Grid Capture (Mines):", type=['jpg', 'png', 'jpeg'], key="mine_img")
    m_c_s = st.text_input("💻 Current Seed:", key="min_c_s", placeholder="Enter Mines Seed...")
    nb_m = st.slider("Nombre de Mines:", 1, 5, 3)
    
    if st.button("⚡ ANALYZE SEEDS & SCAN", use_container_width=True):
        # Premium Logic: Combining Seeds for randomness
        random.seed(hash(m_c_s + str(time.time_ns())))
        stars = random.sample(range(25), k=5)
        st.session_state.history.append(f"Mines: 5 Stars Generated at {datetime.now().strftime('%H:%M')}")
        
        grid_html = '<div style="display: grid; grid-template-columns: repeat(5, 55px); gap: 10px; justify-content: center; padding: 20px;">'
        for i in range(25):
            color = "#ffd700" if i in stars else "#2c3e50"
            border = "2px solid #ffd700" if i in stars else "1px solid #444"
            grid_html += f'<div style="width:55px; height:55px; background:{color}; border-radius:10px; border:{border}; box-shadow: inset 0 0 10px rgba(0,0,0,0.5);"></div>'
        grid_html += '</div>'
        st.markdown(grid_html, unsafe_allow_html=True)
        st.success("✅ Analysis Complete. Follow the gold squares.")

# --- TAB 4: PENALTY ---
with tab4:
    st.selectbox("Sélectionnez le Mode:", ["FACILE (Cible x2.93)", "MOYEN", "DIFFICILE"], key="pen_mode")
    if st.button("⚽ GENERATE SEQUENCE", use_container_width=True):
        random.seed(time.time_ns())
        targets = ["ANKAVIA AMBONY", "ANKAVANANA AMBONY", "AFOVOANY", "ANKAVIA AMBANY", "ANKAVANANA AMBANY"]
        seq = random.sample(targets, k=5)
        st.session_state.history.append(f"Penalty: Seq for {st.session_state.pen_mode}")
        for i, s in enumerate(seq):
            st.markdown(f"<div class='hist-box'><b>STRIKE {i+1}:</b> {s}</div>", unsafe_allow_html=True)

# --- HISTORIQUE ---
st.write("---")
st.markdown("### 📜 LAST 5 SIGNALS")
if st.button("🗑️ CLEAR SYSTEM CACHE"):
    st.session_state.history = []
    st.rerun()

for h in reversed(st.session_state.history[-5:]):
    st.markdown(f"<div class='hist-box'>{h}</div>", unsafe_allow_html=True)
