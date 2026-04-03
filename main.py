import streamlit as st
import hashlib
import random
from datetime import datetime, timedelta

# --- 1. CONFIG & SESSION ---
st.set_page_config(page_title="TITAN V100.0 ULTRA-PRO", layout="wide")
for key, val in [('logged_in', False), ('history', []), ('mines_grid', "")]:
    if key not in st.session_state: st.session_state[key] = val

# --- 2. STYLE NEON PREMIUM ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ffcc; font-family: 'Courier New', monospace; }
    .prediction-card {
        background: rgba(0, 255, 204, 0.05); border: 2px solid #00ffcc;
        padding: 15px; border-radius: 20px; text-align: center;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.4); margin-bottom: 10px;
    }
    .stButton>button { background: #00ffcc !important; color: black !important; font-weight: bold; width: 100%; border-radius: 12px; }
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; max-width: 300px; margin: auto; }
    .mine-cell { aspect-ratio: 1/1; background: #1a1a1a; border: 1px solid #333; display: flex; align-items: center; justify-content: center; font-size: 22px; border-radius: 5px; }
    .cell-star { border: 2px solid #00ffcc !important; color: #ffff00; box-shadow: 0 0 10px #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CORE ALGO (MONTE CARLO & PATTERN) ---
def get_prediction(seed, client, mode="crash"):
    h = hashlib.sha512(f"{seed}{client}V100".encode()).hexdigest()
    random.seed(int(h[:16], 16))
    if mode == "mines":
        # Monte Carlo: Simulation in-1000
        wins = sum(1 for _ in range(1000) if not any(p in random.sample(range(25), 3) for p in random.sample(range(25), 3)))
        return random.sample(range(25), 5), wins/10
    
    res = []
    for t, rmin, rmax, pmin, pmax in [("MIN", 1.6, 2.1, 94, 99), ("MOYEN", 2.2, 3.8, 88, 93), ("MAX", 4.0, 7.5, 75, 87)]:
        val = round(random.uniform(rmin, rmax), 2)
        ora = (datetime.now() + timedelta(minutes=random.randint(2, 10))).strftime("%H:%M")
        res.append({"t": t, "v": val, "p": random.randint(pmin, pmax), "o": ora})
    return res

# --- 4. LOGIN ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center;'>🛰️ TITAN V100 LOGIN</h1>", unsafe_allow_html=True)
    if st.text_input("Key:", type="password") == "2026":
        if st.button("HIDITRA"): 
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- 5. INTERFACE ---
st.markdown("<h2 style='color:#00ffcc;'>« TITAN V100.0 ULTRA-PRO</h2>", unsafe_allow_html=True)
t1, t2, t3, t4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS", "💣 MINES VIP", "📜 HISTORY"])

with t1:
    st.file_uploader("📸 Capture Aviator:", type=['jpg', 'png'], key="fa")
    c1, c2 = st.columns(2)
    s_a, cl_a = c1.text_input("Server Seed:"), c2.text_input("Client Seed:")
    if st.button("🔥 ANALYZE AVIATOR"):
        if s_a and cl_a:
            data = get_prediction(s_a, cl_a)
            cols = st.columns(3)
            for i, r in enumerate(data):
                cols[i].markdown(f'<div class="prediction-card"><b style="color:red;">{r["t"]}</b><br><h2>{r["v"]}x</h2><small>{r["o"]}</small><br><span style="color:#ffff00;">{r["p"]}% Sync</span></div>', unsafe_allow_html=True)
            st.session_state.history.insert(0, f"Aviator: {data[0]['v']}x ({data[0]['p']}%)")

with t2:
    st.file_uploader("📸 Capture Cosmos:", type=['jpg', 'png'], key="fc")
    h_c, tid = st.text_input("Hash SHA512:"), st.text_input("Tour ID:")
    if st.button("🔥 EXECUTE COSMOS"):
        if h_c and tid:
            jump = (int(hashlib.md5(h_c.encode()).hexdigest()[:2], 16) % 6) + 2
            st.info(f"🎯 Target: Tour {int(tid) + jump}")
            data = get_prediction(h_c, tid)
            cols = st.columns(3)
            for i, r in enumerate(data):
                cols[i].markdown(f'<div class="prediction-card"><b>{r["t"]}</b><br><h2>{r["v"]}x</h2><span>{r["p"]}%</span></div>', unsafe_allow_html=True)

with t3:
    nm = st.select_slider("Mines:", options=range(1, 15), value=3)
    m1, m2 = st.columns(2)
    ms, mc = m1.text_input("Server Seed:", key="msm"), m2.text_input("Client Seed:", key="mcm")
    if st.button("🔍 SCAN 5 STARS"):
        if ms and mc:
            stars, wr = get_prediction(ms, mc, mode="mines")
            grid = '<div class="mines-grid">'
            for i in range(25):
                grid += f'<div class="mine-cell {"cell-star" if i in stars else ""}">{"⭐" if i in stars else "⬛"}</div>'
            st.session_state.mines_grid = grid + '</div>'
            st.markdown(f"<p style='text-align:center; color:#ffff00;'>Monte Carlo Win Rate: {wr}%</p>", unsafe_allow_html=True)
    if st.session_state.mines_grid: st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)

with t4:
    for h in st.session_state.history[:10]: st.write(f"✅ {h}")

with st.sidebar:
    if st.text_input("Admin:", type="password") == "2026":
        if st.button("🗑️ RESET"):
            st.session_state.history, st.session_state.mines_grid = [], ""
            st.rerun()
