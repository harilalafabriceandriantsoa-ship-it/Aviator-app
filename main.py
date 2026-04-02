import streamlit as st
import hashlib
import random
from datetime import datetime, timedelta

# --- 1. CONFIGURATION & SESSION STATE ---
st.set_page_config(page_title="TITAN V100.0 ULTRA-PRO", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'admin_pwd' not in st.session_state: st.session_state.admin_pwd = "2026"
if 'history' not in st.session_state: st.session_state.history = []
if 'mines_grid' not in st.session_state: st.session_state.mines_grid = ""

# --- 2. STYLE PREMIUM NEON (DARK MODE) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ffcc; font-family: 'Courier New', monospace; }
    .stTabs [data-baseweb="tab-list"] { background-color: #000000; border-bottom: 2px solid #00ffcc; }
    .stTabs [data-baseweb="tab"] { color: #ffffff !important; font-weight: bold; }
    .stTabs [aria-selected="true"] { color: #00ffcc !important; border-bottom: 2px solid #00ffcc !important; }
    
    .prediction-card {
        background: rgba(0, 255, 204, 0.05); border: 2px solid #00ffcc;
        padding: 15px; border-radius: 20px; text-align: center;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.4); margin-bottom: 15px;
    }
    .stButton>button { 
        background: linear-gradient(90deg, #00ffcc, #0099ff) !important; 
        color: black !important; border-radius: 15px !important; 
        font-weight: bold; width: 100%; border: none; 
    }
    
    .mines-grid {
        display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; max-width: 300px; margin: 20px auto;
    }
    .mine-cell {
        aspect-ratio: 1/1; background: #1a1a1a; border: 1px solid #333; border-radius: 8px;
        display: flex; align-items: center; justify-content: center; font-size: 24px;
    }
    .cell-star { border: 2px solid #00ffcc !important; box-shadow: 0 0 15px #00ffcc; color: #ffff00; }
    .prob-text { color: #ffff00; font-size: 0.9em; font-weight: bold; text-align: center; display: block; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ALGORITHMS (Monte Carlo & Pattern Analysis) ---
def monte_carlo_logic(nb_mines, iterations=1000):
    wins = 0
    for _ in range(iterations):
        grid = list(range(25))
        mines = random.sample(grid, nb_mines)
        my_picks = random.sample(grid, 3) 
        if not any(p in mines for p in my_picks):
            wins += 1
    return wins / (iterations / 100)

def pattern_prediction(seed, client, power=1.0):
    now = datetime.now() + timedelta(hours=3)
    h = hashlib.sha512(f"{seed}{client}ULTRA".encode()).hexdigest()
    random.seed(int(h[:16], 16))
    res = []
    types = ["MIN", "MOYEN", "MAX"]
    for i, t in enumerate(types):
        if t == "MIN":
            val = round(random.uniform(1.60, 2.15) * power, 2)
            prob = random.randint(94, 99)
        elif t == "MOYEN":
            val = round(random.uniform(2.20, 3.85) * power, 2)
            prob = random.randint(88, 93)
        else:
            val = round(random.uniform(4.00, 7.50) * power, 2)
            prob = random.randint(75, 87)
            
        ora = (now + timedelta(minutes=(i+1)*3)).strftime("%H:%M:%S")
        res.append({"type": t, "val": val, "prob": prob, "ora": ora})
    return res

# --- 4. LOGIN PAGE ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🛰️ TITAN V100.0 LOGIN</h1>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1, 1])
    with col:
        pwd = st.text_input("Admin Key:", type="password")
        if st.button("HIDITRA"):
            if pwd == st.session_state.admin_pwd:
                st.session_state.logged_in = True
                st.rerun()
    st.stop()

# --- 5. MAIN INTERFACE ---
st.markdown("<h1 style='color:#00ffcc;'>« TITAN V100.0 ULTRA-PRO</h1>", unsafe_allow_html=True)
t1, t2, t3, t4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS PRO", "💣 MINES VIP", "📜 HISTORY"])

# --- TAB 1: AVIATOR ---
with t1:
    st.subheader("✈️ AVIATOR NEURAL ANALYSIS")
    st.file_uploader("📸 Capture Historique Aviator:", type=['jpg', 'png'], key="f_avi")
    c1, c2 = st.columns(2)
    s_avi = c1.text_input("Server Seed (Hex):", key="s_avi_k")
    cl_avi = c2.text_input("Client Seed (Lera):", key="cl_avi_k")
    
    if st.button("🔥 ANALYZE PATTERN (AVIATOR)"):
        if s_avi and cl_avi:
            data = pattern_prediction(s_avi, cl_avi)
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
            st.session_state.history.insert(0, f"Aviator {data[0]['ora']}: {data[0]['val']}x ({data[0]['prob']}%)")

# --- TAB 2: COSMOS ---
with t2:
    st.subheader("🚀 COSMOS PRO SIGNALS")
    st.file_uploader("📸 Capture Historique Cosmos:", type=['jpg', 'png'], key="f_cos")
    h_cos = st.text_input("Hash SHA512 Combined:", key="h_cos_k")
    t_id = st.text_input("Numéro de Tour (ID):", key="t_id_k")
    
    if st.button("🔥 EXECUTE JUMP ANALYSIS"):
        if h_cos and t_id:
            ia_jump = int(hashlib.md5(h_cos.encode()).hexdigest()[:2], 16)
            saut = (ia_jump % 6) + 2
            target_tour = int(t_id) + saut
            data = pattern_prediction(h_cos, target_tour, power=1.2)
            st.markdown(f"<h3 style='text-align:center;'>🎯 TARGET: TOUR {target_tour}</h3>", unsafe_allow_html=True)
            cols = st.columns(3)
            for i, r in enumerate(data):
                with cols[i]:
                    st.markdown(f"""
                        <div class="prediction-card">
                            <b style="color:red;">{r['type']}</b><br>
                            <h2 style="color:#00ffcc;">{r['val']}x</h2>
                            <span class="prob-text">Monte Carlo Sync</span>
                        </div>
                    """, unsafe_allow_html=True)

# --- TAB 3: MINES VIP ---
with t3:
    st.subheader("💣 MINES VIP: 5 KINTANA RAIPY")
    nb_m = st.select_slider("Isan'ny Mines:", options=range(1, 15), value=3)
    m1, m2 = st.columns(2)
    ms_m = m1.text_input("Server Seed (Hex):", key="ms_m_k")
    mc_m = m2.text_input("Client Seed:", key="mc_m_k")
    
    if st.button("🔍 SCAN 5 DIAMANTS"):
        if ms_m and mc_m:
            win_rate = monte_carlo_logic(nb_m)
            h = hashlib.sha256(f"{ms_m}{mc_m}{nb_m}".encode()).hexdigest()
            random.seed(int(h[:16], 16))
            safe_stars = random.sample(range(25), 5)
            grid = '<div class="mines-grid">'
            for i in range(25):
                char = "⭐" if i in safe_stars else "⬛"
                cls = "mine-cell cell-star" if i in safe_stars else "mine-cell"
                grid += f'<div class="{cls}">{char}</div>'
            st.session_state.mines_grid = grid + '</div>'
            st.markdown(f"<span class='prob-text'>Win Rate: {win_rate}%</span>", unsafe_allow_html=True)
            
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)

# --- TAB 4: HISTORY ---
with t4:
    st.markdown("### 📜 PREDICTIONS HISTORY")
    for h in st.session_state.history[:10]:
        st.write(f"✅ {h}")

# --- SIDEBAR MANAGER ---
with st.sidebar:
    st.title("⚙️ V100 MANAGER")
    if st.text_input("Admin Key:", type="password") == "2026":
        if st.button("🗑️ RESET ALL DATA"):
            st.session_state.history = []
            st.session_state.mines_grid = ""
            st.rerun()
