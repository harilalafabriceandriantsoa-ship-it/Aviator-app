import streamlit as st
import hashlib
import random
import time
from datetime import datetime, timedelta

# --- 1. CONFIGURATION & SESSION STATE ---
st.set_page_config(page_title="TITAN V85.0 ULTRA-SYNC", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'admin_pwd' not in st.session_state: st.session_state.admin_pwd = "2026"
if 'history' not in st.session_state: st.session_state.history = []
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
    .stButton>button { background: #00ffcc !important; color: black !important; border-radius: 15px !important; font-weight: bold; width: 100%; }
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; max-width: 300px; margin: 20px auto; }
    .mine-cell { aspect-ratio: 1/1; background: #1a1a1a; border: 1px solid #333; border-radius: 5px; display: flex; align-items: center; justify-content: center; font-size: 24px; }
    .cell-star { border: 2px solid #00ffcc !important; box-shadow: 0 0 10px #00ffcc; color: #ffff00; }
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

# --- 5. CORE ALGO IA (FIXED SYNC) ---
def run_prediction(seed, client, power=1.0):
    # Fanamafisana lera mba tsy ho tapaka ny Jump 1
    fixed_time = int(time.time() / 10) 
    combined = hashlib.sha512(f"{seed}{client}{fixed_time}".encode()).hexdigest()
    random.seed(int(combined[:16], 16))
    
    # Hamafiso ny x2.00+
    target = round(random.uniform(2.55, 6.25) * power, 2)
    min_val = round(target * 0.82, 2)
    if min_val < 2.00: 
        min_val = 2.05
        target = 2.40

    return {"val": target, "min": min_val, "conf": round(random.uniform(98.1, 99.9), 1)}

# --- 6. MAIN INTERFACE ---
st.markdown("<h1 style='color:#00ffcc;'>« TITAN V85.0 ULTRA-SYNC</h1>", unsafe_allow_html=True)
t1, t2, t3, t4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS ULTRA PRO", "💣 MINES VIP", "📸 HISTORY"])

# AVIATOR
with t1:
    c1, c2 = st.columns(2)
    s_avi = c1.text_input("Server Seed (Hex):", key="avi_s")
    cl_avi = c2.text_input("Client Seed (Lera):", key="avi_c")
    if st.button("🔥 ANALYZE AVIATOR"):
        if s_avi:
            res = run_prediction(s_avi, cl_avi)
            st.markdown(f'<div class="prediction-card"><h2 style="color:#00ffcc;">{res["val"]}x</h2><small>Min: {res["min"]}x</small></div>', unsafe_allow_html=True)
            # Tehirizina ny tantara
            st.session_state.history.insert(0, f"Aviator: {res['val']}x ({datetime.now().strftime('%H:%M')})")

# COSMOS
with t2:
    h_cos = st.text_input("Hash SHA512 Combined:", key="cos_h")
    col_a, col_b, col_c = st.columns(3)
    hex_cos = col_a.text_input("HEX (8 derniers):", key="cos_x")
    time_cos = col_b.text_input("Ora (HH:mm:ss):", key="cos_t")
    tour_id = col_c.text_input("Tour ID:", key="cos_i")
    
    if st.button("🔥 ANALYZE COSMOS"):
        if h_cos and tour_id.isdigit():
            ia_hash = hashlib.md5(h_cos.encode()).hexdigest()
            # Jump 1 namboarina ho mafy (fixed index)
            sauts = [(int(ia_hash[0:2], 16) % 5) + 3, (int(ia_hash[2:4], 16) % 10) + 8, (int(ia_hash[4:6], 16) % 15) + 15]
            cols = st.columns(3)
            for i, s in enumerate(sauts):
                target_tour = int(tour_id) + s
                r = run_prediction(h_cos, f"{hex_cos}{target_tour}", power=1.3)
                with cols[i]:
                    st.markdown(f'<div class="prediction-card"><b style="color:red;">TOUR {target_tour}</b><br><h2 style="color:#00ffcc;">{r["val"]}x</h2><small style="color:white;">Min: {r["min"]}x</small></div>', unsafe_allow_html=True)
            # Tehirizina ny farany indrindra
            st.session_state.history.insert(0, f"Cosmos ID {tour_id}: {r['val']}x")

# MINES
with t3:
    ms, mc = st.text_input("Server Seed:"), st.text_input("Client Seed:")
    if st.button("🔍 SCAN MINES"):
        if ms and mc:
            random.seed(int(hashlib.sha256(f"{ms}{mc}{time.time()}".encode()).hexdigest()[:10], 16))
            stars = random.sample(range(25), 5)
            grid_html = '<div class="mines-grid">'
            for i in range(25):
                cls = "mine-cell cell-star" if i in stars else "mine-cell"
                grid_html += f'<div class="{cls}">{"⭐" if i in stars else "⬛"}</div>'
            st.session_state.mines_grid = grid_html + '</div>'
    if st.session_state.mines_grid: st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)

# HISTORY
with t4:
    st.markdown("### 📜 PREDICTIONS HISTORY")
    if not st.session_state.history:
        st.info("Tsy mbola misy tantara eto.")
    for h in st.session_state.history[:15]: 
        st.write(f"✅ {h}")
