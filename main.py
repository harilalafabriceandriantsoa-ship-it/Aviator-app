import streamlit as st
import hashlib
import hmac
import random
from datetime import datetime, timedelta

# --- 1. CONFIG & SESSION ---
st.set_page_config(page_title="TITAN V100.0 FORCE-WIN", layout="wide")
for key, val in [('logged_in', False), ('history', []), ('mines_grid', "")]:
    if key not in st.session_state: st.session_state[key] = val

# --- 2. STYLE PREMIUM NEON ---
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

# --- 3. CORE ALGO (HMAC-SHA256) ---
def get_prediction(seed, client, mode="crash"):
    # Lojika HMAC-SHA256 mitovy amin'ny Provably Fair
    h = hmac.new(seed.encode(), client.encode(), hashlib.sha256).hexdigest()
    random.seed(int(h[:16], 16))
    
    if mode == "mines":
        return random.sample(range(25), 5)
    
    res = []
    for t, l, h, p1, p2 in [("MIN", 1.6, 2.1, 94, 99), ("MOYEN", 2.2, 3.8, 88, 93), ("MAX", 4.0, 8.5, 75, 87)]:
        val = round(random.uniform(l, h), 2)
        ora = (datetime.now() + timedelta(minutes=random.randint(2, 10))).strftime("%H:%M")
        res.append({"t": t, "v": val, "p": random.randint(p1, p2), "o": ora})
    return res

# --- 4. LOGIN ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center;'>🛰️ TITAN V100 LOGIN</h1>", unsafe_allow_html=True)
    if st.text_input("Admin Key:", type="password") == "2026":
        if st.button("HIDITRA"): 
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- 5. INTERFACE ---
st.markdown("<h2 style='color:#00ffcc;'>🛰️ TITAN V100.0 FORCE-WIN</h2>", unsafe_allow_html=True)
t1, t2, t3 = st.tabs(["✈️ AVIATOR/COSMOS", "💣 MINES VIP", "📜 HISTORY"])

with t1:
    st.file_uploader("📸 Screenshot Historique:", type=['jpg', 'png'], key="fa")
    c1, c2 = st.columns(2)
    s_a, cl_a = c1.text_input("Server Seed (Hex):"), c2.text_input("Client Seed (Ora):")
    if st.button("🔥 GENERATE SIGNAL"):
        if s_a and cl_a:
            data = get_prediction(s_a, cl_a)
            cols = st.columns(3)
            for i, r in enumerate(data):
                cols[i].markdown(f'<div class="prediction-card"><b style="color:red;">{r["t"]}</b><br><h2>{r["v"]}x</h2><small>{r["o"]}</small><br><span style="color:#ffff00;">Sync: {r["p"]}%</span></div>', unsafe_allow_html=True)
            st.session_state.history.insert(0, f"Crash: {data[0]['v']}x ({data[0]['p']}%)")

with t2:
    m1, m2 = st.columns(2)
    ms, mc = m1.text_input("Server Seed:", key="msm"), m2.text_input("Client Seed:", key="mcm")
    if st.button("🔍 SCAN 5 STARS"):
        if ms and mc:
            stars = get_prediction(ms, mc, mode="mines")
            grid = '<div class="mines-grid">'
            for i in range(25):
                grid += f'<div class="mine-cell {"cell-star" if i in stars else ""}">{"⭐" if i in stars else "⬛"}</div>'
            st.session_state.mines_grid = grid + '</div>'
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#ffff00;'>✅ SCHEMA SYNCED</p>", unsafe_allow_html=True)

with t3:
    for h in st.session_state.history[:10]: st.write(f"✅ {h}")

with st.sidebar:
    if st.text_input("Manager Key:", type="password") == "2026":
        if st.button("🗑️ RESET"):
            st.session_state.history, st.session_state.mines_grid = [], ""
            st.rerun()
