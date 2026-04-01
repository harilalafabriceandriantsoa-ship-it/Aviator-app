import streamlit as st
import hashlib
import random
import time
from datetime import datetime, timedelta
from PIL import Image

# --- 1. CONFIGURATION & SESSION STATE ---
st.set_page_config(page_title="TITAN V85.0 ULTRA-SYNC", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'admin_pwd' not in st.session_state: st.session_state.admin_pwd = "2026"
if 'history' not in st.session_state: st.session_state.history = []
if 'screenshots' not in st.session_state: st.session_state.screenshots = [] # Naverina ity
if 'mines_grid' not in st.session_state: st.session_state.mines_grid = ""

# --- 2. STYLE DARK "CHARME" NEON ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ffcc; font-family: 'Courier New', monospace; }
    .prediction-card {
        background: rgba(0, 255, 204, 0.05);
        border: 2px solid #00ffcc;
        padding: 15px; border-radius: 20px; text-align: center;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.4); margin-bottom: 15px;
    }
    .multiplier-text { font-size: 42px; color: #00ffcc; font-weight: bold; }
    .luck-text { color: #ffff00; font-weight: bold; font-style: italic; font-size: 13px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN PAGE ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🛰️ TITAN V85.0 LOGIN</h1>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1, 1])
    with col:
        pwd_input = st.text_input("Admin Key:", type="password")
        if st.button("HIDITRA"):
            if pwd_input == st.session_state.admin_pwd:
                st.session_state.logged_in = True
                st.rerun()
    st.stop()

# --- 4. CORE ALGO IA (TSY NOKITIHANA) ---
def run_prediction(seed, client, power=1.0):
    now = datetime.now() + timedelta(hours=3)
    entropy = str(time.time_ns())
    combined = hashlib.sha512(f"{seed}{client}{entropy}".encode()).hexdigest()
    random.seed(int(combined[:12], 16))
    results = []
    for i in range(1, 4):
        target = round(random.uniform(1.68, 5.25) * power, 2)
        results.append({"val": target, "min": round(target*0.82, 2), "max": round(target*1.15, 2)})
    return results

# --- 5. MAIN INTERFACE ---
st.markdown("<h1 style='text-align:left; color:#00ffcc;'>« TITAN V85.0 ULTRA-SYNC</h1>", unsafe_allow_html=True)
t1, t2, t3, t4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS PRO", "💣 MINES VIP", "📸 HISTORY"])

# AVIATOR
with t1:
    f_avi = st.file_uploader("📸 Screenshot Historique Aviator:", type=['png','jpg'], key="f_avi")
    if f_avi:
        st.session_state.screenshots.insert(0, {"name": f"Aviator {datetime.now().strftime('%H:%M')}", "img": f_avi})
    
    c1, c2 = st.columns(2)
    s_avi = c1.text_input("Server Seed (Hex):", key="s_avi_in")
    cl_avi = c2.text_input("Lera / Client Seed (HH:MM):", key="c_avi_in")
    
    if st.button("🔥 ANALYZE AVIATOR"):
        if s_avi and cl_avi:
            data = run_prediction(s_avi, cl_avi)
            cols = st.columns(3)
            for i, r in enumerate(data):
                with cols[i]:
                    st.markdown(f'<div class="prediction-card"><b>TOUR {i+1}</b><div class="multiplier-text">{r["val"]}x</div><div class="luck-text">Patricia Luck</div></div>', unsafe_allow_html=True)

# COSMOS
with t2:
    f_cos = st.file_uploader("📸 Screenshot Historique Cosmos:", type=['png','jpg'], key="f_cos")
    if f_cos:
        st.session_state.screenshots.insert(0, {"name": f"Cosmos {datetime.now().strftime('%H:%M')}", "img": f_cos})
        
    h_cos = st.text_input("Hash SHA512 Combined:", key="h_cos_in")
    col_a, col_b = st.columns(2)
    hex_cos = col_a.text_input("HEX (8 derniers):", key="hex_cos_in")
    tour_id = col_b.text_input("Numéro de Tour (ID):", key="tour_id_in")
    
    if st.button("🔥 ANALYZE COSMOS"):
        if h_cos and tour_id:
            r = run_prediction(h_cos[:32], hex_cos, power=1.4)[0]
            st.markdown(f'<div class="prediction-card"><div class="multiplier-text">{r["val"]}x</div></div>', unsafe_allow_html=True)

# MINES
with t3:
    if st.button("🔍 SCAN MINES"):
        st.session_state.mines_grid = "Grid Loaded" # Simplified for space
    if st.session_state.mines_grid:
        st.write("💣 Mines Grid Active")

# HISTORY (Miverina ny Screenshot ato)
with t4:
    st.subheader("📸 SCREENSHOTS & RESULTS HISTORY")
    for item in st.session_state.screenshots[:5]:
        with st.expander(f"🖼️ {item['name']}"):
            st.image(item['img'], use_container_width=True)
    
    st.markdown("---")
    for h in st.session_state.history[:10]:
        st.write(f"✅ {h}")
