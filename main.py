import streamlit as st
import hashlib
import random
from datetime import datetime, timedelta

# --- 1. CONFIGURATION & SESSION STATE ---
st.set_page_config(page_title="TITAN V85.0 ULTRA-SYNC", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'admin_pwd' not in st.session_state: st.session_state.admin_pwd = "2026"
if 'history' not in st.session_state: st.session_state.history = []
if 'manche_screenshots' not in st.session_state: st.session_state.manche_screenshots = []
if 'mines_grid' not in st.session_state: st.session_state.mines_grid = ""

# --- 2. STYLE ORIGINAL (TSY NIOVA) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ffcc; font-family: 'Courier New', monospace; }
    .stTabs [data-baseweb="tab-list"] { background-color: #000000; border-bottom: 1px solid #00ffcc; }
    .stTabs [data-baseweb="tab"] { color: #ffffff !important; font-weight: bold; }
    .stTabs [aria-selected="true"] { color: #00ffcc !important; border-bottom: 2px solid #00ffcc !important; }
    
    .prediction-card {
        background: rgba(0, 255, 204, 0.05);
        border: 2px solid #00ffcc;
        padding: 20px; border-radius: 20px; text-align: center;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.4); margin-bottom: 15px;
    }
    .luck-msg { color: #00ffcc; font-size: 24px; font-weight: bold; text-align: center; margin-top: 25px; }
    .stButton>button { background: #00ffcc !important; color: black !important; border-radius: 15px !important; font-weight: bold; width: 100%; }
    hr { border: 0.5px solid #333; margin: 10px 0; }
    
    .mines-grid {
        display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; max-width: 300px; margin: 20px auto;
    }
    .mine-cell {
        aspect-ratio: 1/1; background: #1a1a1a; border: 1px solid #333; border-radius: 5px;
        display: flex; align-items: center; justify-content: center; font-size: 24px;
    }
    .cell-star { border: 2px solid #00ffcc !important; box-shadow: 0 0 10px #00ffcc; color: #ffff00; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN PAGE ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🛰️ TITAN V85.0 LOGIN</h1>", unsafe_allow_html=True)
    pwd_input = st.text_input("Admin Key:", type="password")
    if st.button("HAMPIDITRA"):
        if pwd_input == st.session_state.admin_pwd:
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- 4. ALGORITHM ---
def get_predictions(seed_val, hex_val, game):
    now = datetime.now() + timedelta(hours=3) # UTC+3 Madagascar
    results = []
    # Mampiasa ny Hex raha misy (ho an'ny Cosmos Ultra Pro)
    seed_to_use = hex_val if hex_val else seed_val
    random.seed(int(hashlib.sha256(f"{seed_to_use}{random.random()}".encode()).hexdigest()[:8], 16))
    
    for i in range(1, 4):
        moyen = round(random.uniform(1.45, 4.20), 2)
        ora = (now + timedelta(minutes=i*2)).strftime("%H:%M")
        p = {"game": game, "ora": ora, "moyen": moyen, "min": round(moyen * 0.88, 2), "max": round(moyen * 1.25, 2)}
        results.append(p)
        st.session_state.history.insert(0, p)
    return results

# --- 5. INTERFACE PRINCIPALE ---
st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🛰️ TITAN V85.0 ULTRA-SYNC</h1>", unsafe_allow_html=True)

t1, t2, t3, t4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS ULTRA PRO", "💣 MINES VIP", "📸 HISTORY"])

# AVIATOR (Tsy voakitika)
with t1:
    st.file_uploader("📸 Screenshot Aviator:", type=['png','jpg'], key="f_avi")
    c1, c2 = st.columns(2)
    s_avi = c1.text_input("Server Seed (Hex):", key="s_avi")
    c_avi = c2.text_input("Lera / Client Seed (HH:MM):", key="c_avi")
    if st.button("🔥 ANALYZE AVIATOR"):
        preds = get_predictions(s_avi, "", "AVIATOR")
        cols = st.columns(3)
        for i, r in enumerate(preds):
            with cols[i]:
                st.markdown(f'<div class="prediction-card"><b>TOUR {i+1}</b><br>{r["ora"]}<br><span style="font-size:38px; color:#00ffcc;">{r["moyen"]}x</span></div>', unsafe_allow_html=True)

# COSMOS ULTRA PRO (ITY NO NOVAINA)
with t2:
    st.subheader("Kajy Cosmos Provably Fair (Ultra Pro)")
    st.info("Ampidiro ny Hash sy Hex avy amin'ny lalao (Provably Fair) ho an'ny prédiction mafy.")
    col_a, col_b = st.columns(2)
    h_comb = col_a.text_input("Hash SHA512 Combined:", placeholder="f81f7076664b...", key="h_c")
    h_hex = col_b.text_input("HEX (8 derniers caractères):", placeholder="d265709a", key="h_h")
    
    if st.button("🔥 ANALYZE COSMOS ULTRA PRO"):
        if h_comb and h_hex:
            preds = get_predictions(h_comb, h_hex, "COSMOS ULTRA PRO")
            cols = st.columns(3)
            for i, r in enumerate(preds):
                with cols[i]:
                    st.markdown(f'<div class="prediction-card"><b style="color:red;">TOUR {i+1}</b><br>{r["ora"]}<br><span style="font-size:38px; color:#00ffcc;">{r["moyen"]}x</span><hr>Max: {r["max"]}x</div>', unsafe_allow_html=True)
        else:
            st.warning("Ampidiro aloha ny Hash sy Hex hitanao ao amin'ny lalao!")

# MINES VIP (Tsy voakitika)
with t3:
    st.subheader("💣 MINES VIP 8/10")
    m_col1, m_col2 = st.columns(2)
    m_seed = m_col1.text_input("Seed du serveur:", key="m_s")
    m_client = m_col2.text_input("Seed du client:", key="m_c")
    if st.button("🔍 SCAN MINES"):
        random.seed(int(hashlib.sha256(f"{m_seed}{m_client}".encode()).hexdigest()[:8], 16))
        stars = random.sample(range(25), 5)
        grid = '<div class="mines-grid">'
        for i in range(25):
            char = "⭐" if i in stars else "⬛"
            cls = "mine-cell cell-star" if i in stars else "mine-cell"
            grid += f'<div class="{cls}">{char}</div>'
        grid += '</div>'
        st.session_state.mines_grid = grid
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)

# HISTORY (Tsy voakitika)
with t4:
    for h in st.session_state.history[:10]:
        st.write(f"🕒 {h['ora']} | {h['game']} | **{h['moyen']}x**")
