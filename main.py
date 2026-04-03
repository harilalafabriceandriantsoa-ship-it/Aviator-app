import streamlit as st
import hashlib
import random
import time
from datetime import datetime, timedelta

# --- 1. CONFIGURATION & SESSION STATE ---
st.set_page_config(page_title="TITAN V85.0 ULTRA-SYNC", layout="wide")

# Fanombohana ny session state rehetra
for key, val in [('logged_in', False), ('admin_pwd', "2026"), ('history', []), ('mines_grid', "")]:
    if key not in st.session_state: st.session_state[key] = val

# --- 2. STYLE DARK NEON ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #00ffcc; font-family: monospace; }
    .prediction-card {
        background: rgba(0, 255, 204, 0.05); border: 2px solid #00ffcc;
        padding: 15px; border-radius: 20px; text-align: center;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.4); margin-bottom: 15px;
    }
    .stButton>button { background: #00ffcc !important; color: #000 !important; font-weight: bold; width: 100%; border-radius: 15px; }
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; max-width: 300px; margin: auto; }
    .mine-cell { aspect-ratio: 1/1; background: #111; border: 1px solid #333; display: flex; align-items: center; justify-content: center; font-size: 24px; border-radius: 5px; }
    .cell-star { border: 2px solid #00ffcc !important; box-shadow: 0 0 15px #00ffcc; color: #ff0; }
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
            else: st.error("Diso ny MDP!")
    st.stop()

# --- 4. CORE ALGO ---
def run_prediction(seed, client, power=1.0):
    now = datetime.now() + timedelta(hours=3)
    combined = hashlib.sha512(f"{seed}{client}".encode()).hexdigest()
    random.seed(int(combined[:16], 16))
    results = []
    for i in range(1, 4):
        target = round(random.uniform(1.85, 4.95) * power, 2)
        ora = (now + timedelta(minutes=i*2)).strftime("%H:%M:%S")
        results.append({"ora": ora, "val": target})
    return results

# --- 5. MAIN INTERFACE ---
st.markdown("<h1 style='color:#00ffcc;'>🛰️ TITAN V85.0 ULTRA-SYNC</h1>", unsafe_allow_html=True)
t1, t2, t3, t4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS PRO", "💣 MINES VIP", "📜 HISTORY"])

with t1:
    st.file_uploader("📸 Screenshot Aviator:", type=['png','jpg'], key="f_avi")
    c1, c2 = st.columns(2)
    s_avi, cl_avi = c1.text_input("Server Seed:", key="s1"), c2.text_input("Client Seed (Ora):", key="c1")
    if st.button("🔥 ANALYZE AVIATOR"):
        if s_avi and cl_avi:
            data = run_prediction(s_avi, cl_avi)
            cols = st.columns(3)
            for i, r in enumerate(data):
                cols[i].markdown(f'<div class="prediction-card"><b style="color:red;">TOUR {i+1}</b><br><small>{r["ora"]}</small><br><h2>{r["val"]}x</h2></div>', unsafe_allow_html=True)
            st.session_state.history.insert(0, f"Aviator {data[0]['ora']}: {data[0]['val']}x")

with t2:
    st.file_uploader("📸 Screenshot Cosmos:", type=['png','jpg'], key="f_cos")
    h_cos = st.text_input("Hash SHA512:", key="h2")
    col_a, col_b, col_c = st.columns(3)
    hex_cos, time_cos, tour_id = col_a.text_input("HEX:"), col_b.text_input("Ora:"), col_c.text_input("Tour ID:")
    if st.button("🔥 ANALYZE COSMOS"):
        if h_cos and tour_id.isdigit():
            ia_jump = int(hashlib.md5(h_cos.encode()).hexdigest()[:2], 16)
            sauts = [(ia_jump % 4) + 2, (ia_jump % 7) + 8, (ia_jump % 12) + 16]
            cols = st.columns(3)
            for i, s in enumerate(sauts):
                target_tour = int(tour_id) + s
                r = run_prediction(hashlib.sha512(f"{h_cos}{target_tour}".encode()).hexdigest()[:32], time_cos, 1.25)[0]
                cols[i].markdown(f'<div class="prediction-card"><b style="color:red;">TOUR {target_tour}</b><br><small>Jump: +{s}</small><br><h2>{r["val"]}x</h2></div>', unsafe_allow_html=True)

with t3:
    nb_m = st.select_slider("Mines:", options=range(1, 13), value=3)
    m1, m2 = st.columns(2)
    ms, mc = m1.text_input("Server Seed:", key="ms_in"), m2.text_input("Client Seed:", key="mc_in")
    if st.button("🔍 SCAN MINES"):
        if ms and mc:
            # Algorithm deterministe (Fixed per seed)
            random.seed(int(hashlib.sha256(f"{ms}{mc}{nb_m}".encode()).hexdigest()[:16], 16))
            safe_stars = random.sample(range(25), 5)
            grid = '<div class="mines-grid">'
            for i in range(25):
                char, cls = ("⭐", "mine-cell cell-star") if i in safe_stars else ("⬛", "mine-cell")
                grid += f'<div class="{cls}">{char}</div>'
            st.session_state.mines_grid = grid + '</div>'
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)
        st.success("✅ SCHEMA SYNCED")

with t4:
    st.markdown("### 📜 HISTORY")
    for h in st.session_state.history[:10]:
        st.write(f"✅ {h}")

with st.sidebar:
    st.title("⚙️ MANAGER")
    if st.text_input("Admin Password:", type="password", key="admin_key") == st.session_state.admin_pwd:
        if st.button("🗑️ RESET ALL"):
            st.session_state.history = []
            st.session_state.mines_grid = ""
            st.rerun()
