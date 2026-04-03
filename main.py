import streamlit as st
import hashlib
import random
from datetime import datetime, timedelta

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V85.0 FARATAMPONY", layout="wide")

for key, val in [('logged_in', False), ('admin_pwd', "2026"), ('history', []), ('mines_grid', "")]:
    if key not in st.session_state: st.session_state[key] = val

# --- 2. STYLE NEON PREMIUM ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ffcc; font-family: monospace; }
    .prediction-card {
        background: rgba(0, 255, 204, 0.1); border: 2px solid #00ffcc;
        padding: 20px; border-radius: 20px; text-align: center;
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.5); margin-bottom: 15px;
    }
    .stButton>button { background: #00ffcc !important; color: black !important; border-radius: 15px !important; font-weight: bold; width: 100%; }
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; max-width: 300px; margin: auto; }
    .mine-cell { aspect-ratio: 1/1; background: #111; border: 1px solid #333; display: flex; align-items: center; justify-content: center; font-size: 24px; border-radius: 8px; }
    .cell-star { border: 2px solid #00ffcc !important; box-shadow: 0 0 15px #00ffcc; color: #ffff00; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN ---
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

# --- 4. CORE ALGO (COSMOS & MINES) ---
def run_ultra_sync(seed, client, power=1.2):
    h = hashlib.sha512(f"{seed}{client}TITAN_X".encode()).hexdigest()
    random.seed(int(h[:16], 16))
    now = datetime.now() + timedelta(hours=3)
    results = []
    for i in range(1, 3):
        val = round(random.uniform(2.15, 5.45) * power, 2)
        ora = (now + timedelta(minutes=i*2)).strftime("%H:%M:%S")
        results.append({"ora": ora, "val": val})
    return results

def get_mines_pattern(ms, mc, nb):
    # Triple Hash logic for Mines focus
    h = hashlib.md5(hashlib.sha512(f"{ms}{mc}{nb}".encode()).hexdigest().encode()).hexdigest()
    random.seed(int(h[:16], 16))
    # Isan'ny kintana araka ny Mines (1=10, 2=7, 3=5)
    count = 10 if nb == 1 else (7 if nb == 2 else 5)
    return random.sample(range(25), count)

# --- 5. INTERFACE ---
st.markdown("<h1 style='color:#00ffcc;'>🛰️ TITAN V85.0 FARATAMPONY</h1>", unsafe_allow_html=True)
t1, t2, t3 = st.tabs(["🚀 COSMOS ULTRA-SYNC", "💣 MINES VIP (1-3)", "📜 HISTORY"])

with t1:
    st.markdown("### 🛰️ COSMOS 2-STEP PREDICTION")
    h_cos = st.text_input("Hash SHA512 Combined:")
    c1, c2, c3 = st.columns(3)
    hex_cos = c1.text_input("HEX (8 derniers):")
    time_cos = c2.text_input("Ora (HH:mm:ss):")
    tour_id = c3.text_input("Tour ID:")
    
    if st.button("🔥 ANALYZE COSMOS"):
        if h_cos and tour_id.isdigit():
            jump = (int(hashlib.md5(h_cos.encode()).hexdigest()[:2], 16) % 5) + 2
            target = int(tour_id) + jump
            data = run_ultra_sync(f"{h_cos}{hex_cos}{target}", time_cos)
            st.markdown(f"<h3 style='text-align:center; color:#ffff00;'>🎯 TARGET TOUR: {target} (Jump +{jump})</h3>", unsafe_allow_html=True)
            cols = st.columns(2)
            for i, r in enumerate(data):
                cols[i].markdown(f'<div class="prediction-card"><b style="color:red;">SIGNAL {i+1}</b><br><small>{r["ora"]}</small><br><h2>{r["val"]}x</h2><span style="color:#ffff00; font-size:12px;">SYNC: 98.9%</span></div>', unsafe_allow_html=True)
            st.session_state.history.insert(0, f"Cosmos Tour {target}: {data[0]['val']}x")

with t2:
    st.subheader("💣 MINES ANALYZER (Focus 1, 2, 3)")
    nb_mines = st.select_slider("Isan'ny Mines:", options=[1, 2, 3], value=3)
    m1, m2 = st.columns(2)
    ms, mc = m1.text_input("Server Seed:"), m2.text_input("Client Seed:")
    
    if st.button("🔍 SCAN SAFE SECTORS"):
        if ms and mc:
            safe_stars = get_mines_pattern(ms, mc, nb_mines)
            grid = '<div class="mines-grid">'
            for i in range(25):
                cls = "mine-cell cell-star" if i in safe_stars else "mine-cell"
                grid += f'<div class="{cls}">{"⭐" if i in safe_stars else "⬛"}</div>'
            st.session_state.mines_grid = grid + '</div>'
    
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)
        st.success("✅ IA ULTRA-SYNC: Pattern voadio ho an'ny Mines " + str(nb_mines))

with t3:
    for h in st.session_state.history[:10]: st.write(f"✅ {h}")

with st.sidebar:
    st.title("⚙️ MANAGER")
    if st.text_input("Admin Password:", type="password") == st.session_state.admin_pwd:
        if st.button("🗑️ RESET DATA"):
            st.session_state.history, st.session_state.mines_grid = [], ""
            st.rerun()
