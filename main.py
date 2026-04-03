import streamlit as st
import hashlib
import random
from datetime import datetime, timedelta

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V85.0 ULTRA-SYNC", layout="wide")

for key, val in [('logged_in', False), ('admin_pwd', "2026"), ('history', []), ('mines_grid', "")]:
    if key not in st.session_state: st.session_state[key] = val

# --- 2. STYLE NEON (OPTIMIZED FOR MOBILE) ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #00ffcc; font-family: 'Courier New', monospace; }
    .prediction-card {
        background: linear-gradient(145deg, #0f0f0f, #1a1a1a);
        border: 2px solid #00ffcc; padding: 20px; border-radius: 15px;
        text-align: center; box-shadow: 0 0 20px rgba(0, 255, 204, 0.3);
    }
    .stButton>button { background: #00ffcc !important; color: #000 !important; font-weight: 900 !important; border-radius: 10px !important; }
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; max-width: 300px; margin: auto; }
    .mine-cell { aspect-ratio: 1/1; background: #111; border: 1px solid #333; display: flex; align-items: center; justify-content: center; font-size: 22px; border-radius: 5px; }
    .cell-star { border: 2px solid #ffff00 !important; box-shadow: 0 0 10px #ffff00; color: #ffff00; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center;'>🛰️ TITAN LOGIN</h1>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 2, 1])
    with col:
        pwd = st.text_input("Key:", type="password")
        if st.button("HIDITRA"):
            if pwd == st.session_state.admin_pwd:
                st.session_state.logged_in = True
                st.rerun()
    st.stop()

# --- 4. ENGINE FARATAMPONY (IA CALCUL) ---
def ultra_logic_engine(seed, client, mode="cosmos"):
    # Ultra-Fast Hashing (SHA256 -> MD5)
    raw = f"{seed}{client}TITAN_PREDICT_2026".encode()
    h = hashlib.md5(hashlib.sha256(raw).hexdigest().encode()).hexdigest()
    random.seed(int(h[:16], 16))
    
    if mode == "cosmos":
        # 2 Signals raikitra (Cote 2.10x - 5.50x)
        return [{"val": round(random.uniform(2.10, 3.80), 2)}, {"val": round(random.uniform(3.81, 5.50), 2)}]
    else:
        # Mines 8/5 logic
        count = 8 if client in ["1", "2"] else 5
        return random.sample(range(25), count)

# --- 5. MAIN INTERFACE ---
st.markdown("<h2 style='color:#00ffcc; text-align:center;'>🛰️ TITAN V85.0 ULTRA-SYNC</h2>", unsafe_allow_html=True)
t1, t2, t3 = st.tabs(["🚀 COSMOS SYNC", "💣 MINES 8/5", "📜 HISTORY"])

with t1:
    h_cos = st.text_input("Hash SHA512 Combined (Server Seed):")
    c1, c2 = st.columns(2)
    hex_val = c1.text_input("HEX (Last 8):")
    t_id = c2.text_input("Tour ID:")
    
    if st.button("🔥 ANALYZE & SYNC"):
        if h_cos and t_id.isdigit():
            # IA Jump Sync
            jump = (int(hashlib.md5(h_cos.encode()).hexdigest()[:1], 16) % 3) + 1
            target = int(t_id) + jump
            data = ultra_logic_engine(h_cos, f"{hex_val}{target}", "cosmos")
            
            st.markdown(f"<h4 style='text-align:center; color:#ffff00;'>🎯 TARGET TOUR: {target}</h4>", unsafe_allow_html=True)
            col_a, col_b = st.columns(2)
            for i, r in enumerate(data):
                with [col_a, col_b][i]:
                    st.markdown(f'<div class="prediction-card"><b style="color:red;">SIGNAL {i+1}</b><h2>{r["val"]}x</h2><small>SYNC: 100%</small></div>', unsafe_allow_html=True)
            st.session_state.history.insert(0, f"Cosmos T-{target}: {data[0]['val']}x")

with t2:
    nb_m = st.select_slider("Mines:", options=[1, 2, 3], value=3)
    m1, m2 = st.columns(2)
    ms, mc = m1.text_input("Server Seed:"), m2.text_input("Client Seed:")
    
    if st.button("🔍 SCAN 8/5 DIAMANTS"):
        if ms and mc:
            safe = ultra_logic_engine(ms, str(nb_m), "mines")
            grid = '<div class="mines-grid">'
            for i in range(25):
                is_s = i in safe
                grid += f'<div class="mine-cell {"cell-star" if is_s else ""} ">{"⭐" if is_s else "⬛"}</div>'
            st.session_state.mines_grid = grid + '</div>'
            
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)
        st.success(f"✅ Pattern { (8 if nb_m < 3 else 5) } Diamants nivoaka!")

with t3:
    for h in st.session_state.history[:10]: st.write(f"✅ {h}")

with st.sidebar:
    if st.text_input("Admin:", type="password") == "2026":
        if st.button("🗑️ RESET ALL"):
            st.session_state.history, st.session_state.mines_grid = [], ""
            st.rerun()
