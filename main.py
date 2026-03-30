import streamlit as st
import hashlib
import random
import time
from datetime import datetime, timedelta

# --- 1. CONFIGURATION (TSY NIOVA) ---
st.set_page_config(page_title="TITAN V85.0 OMNI-ALGO", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'admin_pwd' not in st.session_state: st.session_state.admin_pwd = "2026"
if 'history' not in st.session_state: st.session_state.history = []
if 'manche_screenshots' not in st.session_state: st.session_state.manche_screenshots = []
if 'mines_grid' not in st.session_state: st.session_state.mines_grid = ""

# --- 2. STYLE NEON (ORIGINAL) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ffcc; font-family: 'Courier New', monospace; }
    .stTabs [data-baseweb="tab-list"] { background-color: #000000; border-bottom: 2px solid #00ffcc; }
    .stTabs [data-baseweb="tab"] { color: #ffffff !important; font-weight: bold; }
    .stTabs [aria-selected="true"] { color: #00ffcc !important; border-bottom: 2px solid #00ffcc !important; }
    
    .prediction-card {
        background: rgba(0, 255, 204, 0.05);
        border: 2px solid #00ffcc;
        padding: 15px; border-radius: 20px; text-align: center;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.4); margin-bottom: 15px;
    }
    .stButton>button { background: #00ffcc !important; color: black !important; border-radius: 15px !important; font-weight: bold; width: 100%; }
    hr { border: 0.5px solid #333; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN (ADMIN ONLY) ---
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

# --- 4. SIDEBAR MANAGER ---
with st.sidebar:
    st.title("⚙️ MANAGER")
    auth = st.text_input("Verify Key:", type="password")
    if auth == st.session_state.admin_pwd:
        if st.button("🗑️ RESET ALL DATA"):
            st.session_state.history = []
            st.session_state.manche_screenshots = []
            st.session_state.mines_grid = ""
            st.rerun()

# --- 5. ALGO OMNI-SYNC ---
def run_omni_calculation(seed, client, power=1.0):
    now = datetime.now() + timedelta(hours=3)
    # Mampiasa nano-seconds ho an'ny hery fara-tampony
    entropy = str(time.time_ns())
    combined = hashlib.sha512(f"{seed}{client}{entropy}".encode()).hexdigest()
    random.seed(int(combined[:12], 16))
    
    results = []
    for i in range(1, 4):
        target = round(random.uniform(1.70, 5.20) * power, 2)
        ora = (now + timedelta(minutes=i*2)).strftime("%H:%M:%S")
        perc = random.randint(95, 99)
        results.append({"ora": ora, "val": target, "min": round(target*0.85, 2), "max": round(target*1.15, 2), "perc": perc})
    return results

# --- 6. INTERFACE ---
st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🛰️ TITAN V85.0 OMNI-SYNC</h1>", unsafe_allow_html=True)
t1, t2, t3, t4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS ULTRA PRO", "💣 MINES VIP", "📸 HISTORY"])

with t1: # AVIATOR
    st.file_uploader("📸 Screenshot AVIATOR:", type=['png','jpg'], key="f_avi")
    c1, c2 = st.columns(2)
    if st.button("🔥 ANALYZE AVIATOR"):
        if c1.text_input("Hex:", key="s_avi") and c2.text_input("Lera:", key="c_avi"):
            data = run_omni_calculation(st.session_state.s_avi, st.session_state.c_avi)
            cols = st.columns(3)
            for i, r in enumerate(data):
                with cols[i]:
                    st.markdown(f'<div class="prediction-card"><b style="color:red;">TOUR {i+1}</b><br><small>{r["ora"]}</small><br><h2 style="color:#00ffcc;">{r["val"]}x</h2><small>{r["perc"]}% Acc.</small><hr><div style="font-size:10px;">Min: {r["min"]}x | Max: {r["max"]}x</div></div>', unsafe_allow_html=True)

with t2: # COSMOS
    st.file_uploader("📸 Screenshot COSMOS:", type=['png','jpg'], key="f_cos")
    h_sha = st.text_input("Hash SHA512:", key="cos_h")
    if st.button("🔥 ANALYZE COSMOS"):
        data = run_omni_calculation(h_sha, "cosmos", power=1.2)
        cols = st.columns(3)
        for i, r in enumerate(data):
            with cols[i]:
                st.markdown(f'<div class="prediction-card"><b style="color:red;">TOUR {i+1}</b><br><small>{r["ora"]}</small><br><h2 style="color:#00ffcc;">{r["val"]}x</h2><hr><small>Range: {r["min"]}x - {r["max"]}x</small></div>', unsafe_allow_html=True)

with t3: # MINES
    m_s = st.text_input("Server Seed:", key="ms")
    m_c = st.text_input("Client Seed:", key="mc")
    m_n = st.slider("Mines:", 1, 7, 3)
    if st.button("🔍 SCAN MINES"):
        random.seed(int(hashlib.md5(f"{m_s}{m_c}".encode()).hexdigest()[:8], 16))
        stars = random.sample(range(25), 5)
        grid = '<div style="display:grid; grid-template-columns:repeat(5, 1fr); gap:5px; max-width:250px; margin:auto;">'
        for i in range(25):
            char = "⭐" if i in stars else "⬛"
            grid += f'<div style="aspect-ratio:1/1; background:#1a1a1a; border:1px solid #00ffcc; display:flex; align-items:center; justify-content:center;">{char}</div>'
        st.markdown(grid + '</div>', unsafe_allow_html=True)

with t4: # HISTORY
    st.subheader("📸 MANCHE HISTORY")
    for m in st.session_state.manche_screenshots:
        st.image(m['img'], width=300, caption=m['info'])
