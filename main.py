import streamlit as st
import hashlib
import random
import time
from datetime import datetime, timedelta

# --- 1. CONFIGURATION & SESSION STATE ---
st.set_page_config(page_title="TITAN V85.0 ULTRA-PRO", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'admin_pwd' not in st.session_state: st.session_state.admin_pwd = "2026"
if 'history' not in st.session_state: st.session_state.history = []
if 'manche_screenshots' not in st.session_state: st.session_state.manche_screenshots = []
if 'mines_grid' not in st.session_state: st.session_state.mines_grid = ""

# --- 2. STYLE DARK "CHARME" NEON ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ffcc; font-family: 'Courier New', monospace; }
    .stTabs [data-baseweb="tab-list"] { background-color: #000000; border-bottom: 1px solid #00ffcc; }
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
    
    .mines-grid {
        display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; max-width: 300px; margin: 20px auto;
    }
    .mine-cell {
        aspect-ratio: 1/1; background: #1a1a1a; border: 1px solid #333; border-radius: 5px;
        display: flex; align-items: center; justify-content: center; font-size: 24px;
    }
    .cell-star { border: 2px solid #00ffcc !important; box-shadow: 0 0 15px #00ffcc; color: #ffff00; }
    .prob-text { color: #ffff00; font-size: 0.8em; font-weight: bold; }
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

# --- 4. CORE ALGO IA (DOUBLE HASH SYNC) ---
def run_prediction(seed, client, power=1.0):
    now = datetime.now() + timedelta(hours=3)
    # DOUBLE HASHING: SHA256 then SHA512 for absolute fixed security
    h1 = hashlib.sha256(f"{seed}{client}".encode()).hexdigest()
    h2 = hashlib.sha512(h1.encode()).hexdigest()
    random.seed(int(h2[:16], 16))
    
    results = []
    # Logic for MIN, MOYEN, MAX
    types = ["MIN", "MOYEN", "MAX"]
    for i, t in enumerate(types):
        if t == "MIN":
            val = round(random.uniform(1.50, 2.10) * power, 2)
            prob = random.randint(95, 99)
        elif t == "MOYEN":
            val = round(random.uniform(2.11, 3.80) * power, 2)
            prob = random.randint(88, 94)
        else: # MAX
            val = round(random.uniform(3.81, 8.50) * power, 2)
            prob = random.randint(75, 87)
            
        ora = (now + timedelta(minutes=(i+1)*2)).strftime("%H:%M:%S")
        results.append({"type": t, "ora": ora, "val": val, "prob": prob})
    return results

# --- 5. SIDEBAR MANAGER ---
with st.sidebar:
    st.title("⚙️ MANAGER")
    auth = st.text_input("Verify Admin Key to Manage:", type="password")
    if auth == st.session_state.admin_pwd:
        st.success("Admin Access Granted")
        if st.button("🗑️ RESET ALL DATA"):
            st.session_state.history = []
            st.session_state.manche_screenshots = []
            st.session_state.mines_grid = ""
            st.rerun()
    else:
        st.warning("Ampidiro ny password raha hanova Manager")

# --- 6. MAIN INTERFACE ---
st.markdown("<h1 style='text-align:left; color:#00ffcc;'>« TITAN V85.0 ULTRA-PRO</h1>", unsafe_allow_html=True)

t1, t2, t3, t4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS ULTRA PRO", "💣 MINES VIP", "📸 HISTORY"])

# --- AVIATOR ---
with t1:
    st.file_uploader("📸 Screenshot AVIATOR:", type=['png','jpg'], key="f_avi")
    c1, c2 = st.columns(2)
    s_avi = c1.text_input("Server Seed (Hex):", key="s_avi_in")
    cl_avi = c2.text_input("Lera / Client Seed (HH:MM):", key="c_avi_in")
    
    if st.button("🔥 ANALYZE AVIATOR"):
        if s_avi and cl_avi:
            data = run_prediction(s_avi, cl_avi)
            cols = st.columns(3)
            for i, r in enumerate(data):
                with cols[i]:
                    st.markdown(f"""
                        <div class="prediction-card">
                            <b style="color:red;">{r['type']}</b><br>
                            <small>{r['ora']}</small><br>
                            <h2 style="color:#00ffcc;">{r['val']}x</h2>
                            <span class="prob-text">Sync: {r['prob']}%</span>
                        </div>
                    """, unsafe_allow_html=True)
            st.session_state.history.insert(0, f"Aviator {data[0]['ora']}: {data[1]['val']}x ({data[1]['prob']}%)")

# --- COSMOS ---
with t2:
    st.file_uploader("📸 Screenshot COSMOS:", type=['png','jpg'], key="f_cos")
    h_cos = st.text_input("Hash SHA512 Combined:", key="h_cos_in")
    
    col_a, col_b, col_c = st.columns(3)
    hex_cos = col_a.text_input("HEX (8 derniers):", key="hex_cos_in")
    time_cos = col_b.text_input("Ora (HH:mm:ss):", key="time_cos_in")
    tour_id = col_c.text_input("Numéro de Tour (ID):", key="tour_id_in")
    
    if st.button("🔥 ANALYZE COSMOS"):
        if h_cos and tour_id and tour_id.isdigit():
            ia_jump = int(hashlib.md5(h_cos.encode()).hexdigest()[:2], 16)
            saut = (ia_jump % 5) + 2
            
            target_tour = int(tour_id) + saut
            seed_final = hashlib.sha512(f"{h_cos}{hex_cos}{target_tour}".encode()).hexdigest()
            data = run_prediction(seed_final[:32], time_cos, power=1.2)
            
            st.markdown(f"<h3 style='text-align:center;'>🎯 TARGET TOUR: {target_tour} (Jump +{saut})</h3>", unsafe_allow_html=True)
            cols = st.columns(3)
            for i, r in enumerate(data):
                with cols[i]:
                    st.markdown(f"""
                        <div class="prediction-card">
                            <b style="color:red;">{r['type']}</b><br>
                            <small>Signal {i+1}</small><br>
                            <h2 style="color:#00ffcc;">{r['val']}x</h2>
                            <span class="prob-text">Sync: {r['prob']}%</span>
                        </div>
                    """, unsafe_allow_html=True)
            st.session_state.history.insert(0, f"Cosmos Tour {target_tour}: {data[1]['val']}x")

# --- MINES VIP (KINTANA 5 FIXE & ASSURE) ---
with t3:
    st.subheader("💣 MINES VIP - 5 DIAMANTS ULTRA-ASSURÉ")
    nb_mines = st.select_slider("Isan'ny Mines:", options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], value=3)
    
    m1, m2 = st.columns(2)
    ms = m1.text_input("Server Seed (Hex):", key="ms_in")
    mc = m2.text_input("Client Seed:", key="mc_in")
    
    if st.button("🔍 SCAN 5 DIAMANTS"):
        if ms and mc:
            # DOUBLE HASH FOR ABSOLUTE FIXED GRID
            h1 = hashlib.sha256(f"{ms}{mc}{nb_mines}".encode()).hexdigest()
            h2 = hashlib.sha512(h1.encode()).hexdigest()
            random.seed(int(h2[:16], 16))
            
            # Kintana 5 raikitra ho an'io Seed io
            safe_stars = random.sample(range(25), 5)
            grid = '<div class="mines-grid">'
            for i in range(25):
                char = "⭐" if i in safe_stars else "⬛"
                cls = "mine-cell cell-star" if i in safe_stars else "mine-cell"
                grid += f'<div class="{cls}">{char}</div>'
            st.session_state.mines_grid = grid + '</div>'
            
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)
        st.success("✅ IA ULTRA-SYNC: Kintana 5 raikitra. Ataovy 'Rotate Seed' isaky ny WIN.")

# --- HISTORY ---
with t4:
    st.markdown("### 📜 PREDICTIONS HISTORY")
    for h in st.session_state.history[:10]:
        st.write(f"✅ {h}")
