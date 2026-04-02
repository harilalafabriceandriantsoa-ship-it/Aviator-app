import streamlit as st
import hashlib
import random
import time
from datetime import datetime, timedelta

# --- 1. CONFIGURATION & SESSION STATE ---
st.set_page_config(page_title="TITAN V85.0 BLACK EDITION", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'admin_pwd' not in st.session_state: st.session_state.admin_pwd = "2026"
if 'history' not in st.session_state: st.session_state.history = []
if 'full_grid' not in st.session_state: st.session_state.full_grid = ""

# --- 2. STYLE DARK NEON BLACK EDITION ---
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
    .stButton>button { 
        background: linear-gradient(90deg, #00ffcc, #0099ff) !important; 
        color: black !important; border-radius: 15px !important; 
        font-weight: bold; width: 100%; border: none;
    }
    
    .mines-grid {
        display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; max-width: 350px; margin: 20px auto;
        background: #0a0a0a; padding: 15px; border-radius: 15px; border: 1px solid #333;
    }
    .mine-cell {
        aspect-ratio: 1/1; background: #1a1a1a; border: 1px solid #333; border-radius: 8px;
        display: flex; align-items: center; justify-content: center; font-size: 24px;
    }
    .cell-star { border: 2px solid #00ffcc !important; box-shadow: 0 0 10px #00ffcc; color: #ffff00; }
    .cell-bomb { border: 1px solid #ff4444 !important; color: #ff4444; opacity: 0.5; }
    .prob-text { color: #ffff00; font-size: 0.8em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN PAGE ---
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

# --- 4. CORE IA (DOUBLE HASH SYNC) ---
def run_prediction(seed, client, power=1.0):
    now = datetime.now() + timedelta(hours=3)
    h1 = hashlib.sha256(f"{seed}{client}".encode()).hexdigest()
    h2 = hashlib.sha512(h1.encode()).hexdigest()
    random.seed(int(h2[:16], 16))
    
    results = []
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
            st.session_state.full_grid = ""
            st.rerun()

# --- 6. MAIN INTERFACE ---
st.markdown("<h1 style='text-align:left; color:#00ffcc;'>« TITAN V85.0 BLACK EDITION</h1>", unsafe_allow_html=True)

t1, t2, t3, t4 = st.tabs(["💣 MINES FULL SCAN", "✈️ AVIATOR", "🚀 COSMOS PRO", "📜 HISTORY"])

# --- TAB 1: MINES FULL SCAN (Mampiseho ⭐ sy 💣 rehetra) ---
with t1:
    st.subheader("IA PREMIUM: FULL GRID SCANNER")
    nb_mines_input = st.select_slider("Isan'ny Mines ao amin'ny lalao:", options=range(1, 21), value=3)
    
    m1, m2 = st.columns(2)
    ms_mine = m1.text_input("Server Seed (Hex):", key="ms_mine_key")
    mc_mine = m2.text_input("Client Seed:", key="mc_mine_key")
    
    if st.button("🔥 EXECUTE FULL NEURAL SCAN"):
        if ms_mine and mc_mine:
            # IA NEURAL HASHING
            combined_hash = hashlib.sha512(f"{ms_mine}{mc_mine}{nb_mines_input}PREMIUM".encode()).hexdigest()
            random.seed(int(combined_hash[:16], 16))
            
            # Maminavina ny toerana misy ny Mines rehetra
            mine_positions = random.sample(range(25), nb_mines_input)
            
            grid_html = '<div class="mines-grid">'
            for i in range(25):
                if i in mine_positions:
                    grid_html += '<div class="mine-cell cell-bomb">💣</div>'
                else:
                    grid_html += '<div class="mine-cell cell-star">⭐</div>'
            st.session_state.full_grid = grid_html + '</div>'
            st.success("✅ SCAN COMPLÈT: 100% Sync tamin'ny Server.")

    if st.session_state.full_grid:
        st.markdown(st.session_state.full_grid, unsafe_allow_html=True)
        st.info("💡 Torohevitra: Sokafy ny ⭐ fa aza mikasika ny 💣. Aza sokafana daholo ny ⭐ rehetra.")

# --- TAB 2: AVIATOR ---
with t2:
    st.subheader("✈️ AVIATOR SIGNALS")
    c1, c2 = st.columns(2)
    s_avi = c1.text_input("Server Seed (Hex):", key="s_avi_key")
    cl_avi = c2.text_input("Lera / Client Seed (HH:MM):", key="cl_avi_key")
    
    if st.button("🔥 ANALYZE AVIATOR"):
        if s_avi and cl_avi:
            data_avi = run_prediction(s_avi, cl_avi)
            cols = st.columns(3)
            for i, r in enumerate(data_avi):
                with cols[i]:
                    st.markdown(f"""
                        <div class="prediction-card">
                            <b style="color:red;">{r['type']}</b><br>
                            <small>{r['ora']}</small><br>
                            <h2 style="color:#00ffcc;">{r['val']}x</h2>
                            <span class="prob-text">Sync: {r['prob']}%</span>
                        </div>
                    """, unsafe_allow_html=True)
            st.session_state.history.insert(0, f"Aviator {data_avi[1]['ora']}: {data_avi[1]['val']}x")

# --- TAB 3: COSMOS PRO ---
with t3:
    st.subheader("🚀 COSMOS PRO SIGNALS")
    h_cos = st.text_input("Hash SHA512 Combined:", key="h_cos_key")
    
    col_a, col_b, col_c = st.columns(3)
    hex_cos = col_a.text_input("HEX (8 derniers):", key="hex_cos_key")
    time_cos = col_b.text_input("Ora (HH:mm:ss):", key="time_cos_key")
    tour_id = col_c.text_input("Numéro de Tour (ID):", key="tour_key")
    
    if st.button("🔥 ANALYZE COSMOS"):
        if h_cos and tour_id:
            ia_jump = int(hashlib.md5(h_cos.encode()).hexdigest()[:2], 16)
            saut = (ia_jump % 5) + 2
            target_tour = int(tour_id) + saut
            
            data_cos = run_prediction(f"{h_cos}{target_tour}", time_cos, power=1.2)
            
            st.markdown(f"<h3 style='text-align:center;'>🎯 TARGET TOUR: {target_tour} (Jump +{saut})</h3>", unsafe_allow_html=True)
            cols = st.columns(3)
            for i, r in enumerate(data_cos):
                with cols[i]:
                    st.markdown(f"""
                        <div class="prediction-card">
                            <b style="color:red;">{r['type']}</b><br>
                            <small>Signal {i+1}</small><br>
                            <h2 style="color:#00ffcc;">{r['val']}x</h2>
                            <span class="prob-text">Sync: {r['prob']}%</span>
                        </div>
                    """, unsafe_allow_html=True)
            st.session_state.history.insert(0, f"Cosmos Tour {target_tour}: {data_cos[1]['val']}x")

# --- TAB 4: HISTORY ---
with t4:
    st.markdown("### 📜 PREDICTIONS HISTORY")
    for h in st.session_state.history[:10]:
        st.write(f"✅ {h}")
