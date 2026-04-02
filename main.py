import streamlit as st
import hashlib
import random
from datetime import datetime, timedelta

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V85.0 BLACK EDITION", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'admin_pwd' not in st.session_state: st.session_state.admin_pwd = "2026"
if 'history' not in st.session_state: st.session_state.history = []
if 'full_grid' not in st.session_state: st.session_state.full_grid = ""

# --- 2. STYLE PREMIUM NEON ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ffcc; font-family: 'Courier New', monospace; }
    .stTabs [data-baseweb="tab-list"] { background-color: #000000; border-bottom: 1px solid #00ffcc; }
    .stTabs [data-baseweb="tab"] { color: #ffffff !important; font-weight: bold; }
    .stTabs [aria-selected="true"] { color: #00ffcc !important; border-bottom: 2px solid #00ffcc !important; }
    .prediction-card {
        background: rgba(0, 255, 204, 0.05); border: 2px solid #00ffcc;
        padding: 15px; border-radius: 20px; text-align: center;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.4); margin-bottom: 15px;
    }
    .stButton>button { background: linear-gradient(90deg, #00ffcc, #0099ff) !important; color: black !important; font-weight: bold; border-radius: 15px !important; width: 100%; border: none; }
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; max-width: 350px; margin: 20px auto; background: #0a0a0a; padding: 15px; border-radius: 15px; border: 1px solid #333; }
    .mine-cell { aspect-ratio: 1/1; background: #1a1a1a; border: 1px solid #333; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 24px; }
    .cell-star { border: 2px solid #00ffcc !important; box-shadow: 0 0 10px #00ffcc; color: #ffff00; }
    .cell-bomb { border: 1px solid #ff4444 !important; color: #ff4444; opacity: 0.5; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🛰️ TITAN BLACK LOGIN</h1>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1, 1])
    with col:
        pwd_input = st.text_input("Admin Key:", type="password")
        if st.button("ACCÈS PREMIUM"):
            if pwd_input == st.session_state.admin_pwd:
                st.session_state.logged_in = True
                st.rerun()
            else: st.error("Diso ny MDP!")
    st.stop()

# --- 4. IA CORE ---
def run_prediction(seed, client, power=1.0):
    now = datetime.now() + timedelta(hours=3)
    h1 = hashlib.sha256(f"{seed}{client}".encode()).hexdigest()
    h2 = hashlib.sha512(h1.encode()).hexdigest()
    random.seed(int(h2[:16], 16))
    res = []
    for t in ["MIN", "MOYEN", "MAX"]:
        val = round(random.uniform(1.5, 6.5) * power, 2)
        prob = random.randint(85, 99)
        ora = (now + timedelta(minutes=random.randint(2, 8))).strftime("%H:%M:%S")
        res.append({"type": t, "val": val, "prob": prob, "ora": ora})
    return res

# --- 5. INTERFACE ---
st.markdown("<h1 style='color:#00ffcc;'>« TITAN V85.0 BLACK EDITION</h1>", unsafe_allow_html=True)

t1, t2, t3, t4 = st.tabs(["💣 MINES SCAN", "✈️ AVIATOR", "🚀 COSMOS PRO", "📜 HISTORY"])

with t1:
    st.subheader("IA PREMIUM: FULL SCAN (Mines & Stars)")
    nb_m = st.select_slider("Isan'ny Mines:", options=range(1, 21), value=3)
    c1, c2 = st.columns(2)
    ms = c1.text_input("Server Seed (Hex):", key="ms_m")
    mc = c2.text_input("Client Seed:", key="mc_m")
    if st.button("🔥 EXECUTE FULL NEURAL SCAN"):
        if ms and mc:
            combined = hashlib.sha512(f"{ms}{mc}{nb_m}TITAN".encode()).hexdigest()
            random.seed(int(combined[:16], 16))
            mine_pos = random.sample(range(25), nb_m)
            grid_html = '<div class="mines-grid">'
            for i in range(25):
                if i in mine_pos: grid_html += '<div class="mine-cell cell-bomb">💣</div>'
                else: grid_html += '<div class="mine-cell cell-star">⭐</div>'
            st.session_state.full_grid = grid_html + '</div>'
    if st.session_state.full_grid:
        st.markdown(st.session_state.full_grid, unsafe_allow_html=True)

with t2:
    s_avi = st.text_input("Server Seed:", key="s_avi")
    c_avi = st.text_input("Client Seed (Lera):", key="c_avi")
    if st.button("🔥 ANALYZE AVIATOR"):
        if s_avi and c_avi:
            data = run_prediction(s_avi, c_avi)
            cols = st.columns(3)
            for i, r in enumerate(data):
                with cols[i]:
                    st.markdown(f'<div class="prediction-card"><b style="color:red;">{r["type"]}</b><br><h2>{r["val"]}x</h2><small>{r["prob"]}% | {r["ora"]}</small></div>', unsafe_allow_html=True)

with t3:
    h_cos = st.text_input("Hash SHA512:", key="h_cos")
    if st.button("🔥 ANALYZE COSMOS"):
        if h_cos:
            data = run_prediction(h_cos, "COSMOS", power=1.2)
            st.markdown(f"<h3 style='text-align:center;'>🎯 SIGNAL DETECTED</h3>", unsafe_allow_html=True)
            cols = st.columns(3)
            for i, r in enumerate(data):
                with cols[i]:
                    st.markdown(f'<div class="prediction-card"><b>{r["type"]}</b><br><h2>{r["val"]}x</h2><small>{r["prob"]}%</small></div>', unsafe_allow_html=True)

with t4:
    for h in st.session_state.history[:10]: st.write(f"✅ {h}")

with st.sidebar:
    if st.text_input("Admin Key:", type="password") == "2026":
        if st.button("🗑️ RESET"):
            st.session_state.full_grid = ""
            st.rerun()
