import streamlit as st
import hashlib
import random

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V85.0 ULTRA-SYNC", layout="wide")

if 'history' not in st.session_state: st.session_state.history = []
if 'mines_grid' not in st.session_state: st.session_state.mines_grid = ""

# --- 2. STYLE ORIGINAL ---
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
    .stButton>button { background: #00ffcc !important; color: black !important; border-radius: 15px !important; font-weight: bold; width: 100%; }
    
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

# --- 3. INTERFACE PRINCIPALE ---
st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🛰️ TITAN V85.0 ULTRA-SYNC</h1>", unsafe_allow_html=True)

t1, t2, t3, t4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS ULTRA PRO", "💣 MINES VIP", "📸 HISTORY"])

# --- TAB 1: AVIATOR ---
with t1:
    c1, c2 = st.columns(2)
    s_avi = c1.text_input("Server Seed (Hex):", key="s_avi")
    c_avi = c2.text_input("Client Seed:", key="c_avi")
    if st.button("🔥 ANALYZE AVIATOR"):
        if s_avi and c_avi:
            random.seed(int(hashlib.sha256(f"{s_avi}{c_avi}".encode()).hexdigest()[:8], 16))
            cols = st.columns(3)
            for i in range(3):
                val = round(random.uniform(1.30, 4.50), 2)
                with cols[i]:
                    st.markdown(f'<div class="prediction-card"><b>TOUR {i+1}</b><br><span style="font-size:38px; color:#00ffcc;">{val}x</span></div>', unsafe_allow_html=True)
        else: st.error("Fenoy ny Seeds!")

# --- TAB 2: COSMOS ULTRA PRO (TAHAKA NY AVIATOR + PROVABLY FAIR) ---
with t2:
    st.subheader("Kajy Cosmos Provably Fair (Ultra Pro)")
    
    # Ireo fizarana nampiana avy amin'ny Provably Fair (sary 1.1)
    h_combined = st.text_input("Hash SHA512 Combined:", placeholder="f81f7076664b3571812c4925110deccfc9752745c13dc940998f6a8...")
    h_hex = st.text_input("HEX (8 derniers caractères):", placeholder="d265709a")
    
    if st.button("🔥 ANALYZE COSMOS ULTRA PRO"):
        if h_hex:
            # Mampiasa ny HEX ho "Seed" mba hitovy amin'ny Aviator nefa mafy kokoa
            random.seed(int(h_hex, 16))
            cols = st.columns(3)
            preds = []
            for i in range(3):
                # Ny fomba fikajiana ny valiny (tahaka ny amin'ny sary 1.2)
                val = round(random.uniform(1.40, 5.20), 2)
                preds.append(val)
                with cols[i]:
                    st.markdown(f'<div class="prediction-card"><b style="color:red;">TOUR {i+1}</b><br><span style="font-size:38px; color:#00ffcc;">{val}x</span></div>', unsafe_allow_html=True)
            st.session_state.history.insert(0, f"Cosmos: {preds[0]}x | {preds[1]}x | {preds[2]}x")
        else:
            st.warning("Ampidiro ny HEX avy amin'ny lalao (Provably Fair)!")

# --- TAB 3: MINES VIP ---
with t3:
    st.subheader("💣 MINES VIP 8/10")
    m_s = st.text_input("Seed du serveur:", key="m_s")
    m_c = st.text_input("Seed du client:", key="m_c")
    if st.button("🔍 SCAN MINES"):
        if m_s and m_c:
            random.seed(int(hashlib.sha256(f"{m_s}{m_c}".encode()).hexdigest()[:8], 16))
            stars = random.sample(range(25), 8)
            grid = '<div class="mines-grid">'
            for i in range(25):
                cls = "mine-cell cell-star" if i in stars else "mine-cell"
                char = "⭐" if i in stars else "⬛"
                grid += f'<div class="{cls}">{char}</div>'
            grid += '</div>'
            st.session_state.mines_grid = grid
    
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;'>🍀 Bonne chance !</p>", unsafe_allow_html=True)

# --- TAB 4: HISTORY ---
with t4:
    st.subheader("📜 Last Predictions")
    for h in st.session_state.history[:10]:
        st.write(f"✅ {h}")

st.markdown("---")
st.button("🛠️ Manage app", use_container_width=True)import streamlit as st
import hashlib
import random
from datetime import datetime, timedelta

# --- 1. CONFIGURATION & STATE ---
st.set_page_config(page_title="TITAN V85.0 ULTRA-SYNC", layout="wide")

if 'admin_pwd' not in st.session_state: st.session_state.admin_pwd = "2026"
if 'history' not in st.session_state: st.session_state.history = []
if 'mines_grid' not in st.session_state: st.session_state.mines_grid = ""

# --- 2. STYLE ORIGINAL ---
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
    .stButton>button { background: #00ffcc !important; color: black !important; border-radius: 15px !important; font-weight: bold; width: 100%; }
    
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

# --- 3. INTERFACE PRINCIPALE ---
st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🛰️ TITAN V85.0 ULTRA-SYNC</h1>", unsafe_allow_html=True)

t1, t2, t3, t4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS ULTRA PRO", "💣 MINES VIP", "📜 HISTORY"])

# AVIATOR
with t1:
    c1, c2 = st.columns(2)
    s_avi = c1.text_input("Server Seed (Hex):", key="s_avi")
    c_avi = c2.text_input("Client Seed:", key="c_avi")
    if st.button("🔥 ANALYZE AVIATOR"):
        random.seed(int(hashlib.sha256(f"{s_avi}{c_avi}".encode()).hexdigest()[:8], 16))
        cols = st.columns(3)
        for i in range(3):
            val = round(random.uniform(1.30, 3.80), 2)
            with cols[i]:
                st.markdown(f'<div class="prediction-card"><b>TOUR {i+1}</b><br><span style="font-size:38px; color:#00ffcc;">{val}x</span></div>', unsafe_allow_html=True)

# COSMOS ULTRA PRO (Tsisy Heure)
with t2:
    st.subheader("Kajy Cosmos Provably Fair (Ultra Pro)")
    h_hex = st.text_input("HEX (8 derniers caractères):", placeholder="d265709a", key="h_h")
    if st.button("🔥 ANALYZE COSMOS ULTRA PRO"):
        if h_hex:
            random.seed(int(h_hex, 16))
            cols = st.columns(3)
            for i in range(3):
                val = round(random.uniform(1.50, 4.80), 2)
                with cols[i]:
                    st.markdown(f'<div class="prediction-card"><b style="color:red;">TOUR {i+1}</b><br><span style="font-size:38px; color:#00ffcc;">{val}x</span></div>', unsafe_allow_html=True)
            st.session_state.history.insert(0, f"Cosmos: {val}x")
        else: st.warning("Ampidiro ny HEX!")

# MINES VIP (8/10 ihany)
with t3:
    st.subheader("💣 MINES VIP 8/10")
    m_s = st.text_input("Seed du serveur:", key="m_s")
    m_c = st.text_input("Seed du client:", key="m_c")
    if st.button("🔍 SCAN MINES"):
        if m_s and m_c:
            random.seed(int(hashlib.sha256(f"{m_s}{m_c}".encode()).hexdigest()[:8], 16))
            stars = random.sample(range(25), 8) # 8 kintana foana
            grid = '<div class="mines-grid">'
            for i in range(25):
                cls = "mine-cell cell-star" if i in stars else "mine-cell"
                char = "⭐" if i in stars else "⬛"
                grid += f'<div class="{cls}">{char}</div>'
            grid += '</div>'
            st.session_state.mines_grid = grid
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;'>🍀 Bonne chance !</p>", unsafe_allow_html=True)

# HISTORY
with t4:
    for h in st.session_state.history[:10]:
        st.write(f"✅ {h}")

# --- 4. ADMIN PANEL (MIAFINA ANY AMBANY) ---
st.markdown("---")
with st.expander("🛠️ Manage App (Admin Only)"):
    check_pwd = st.text_input("Teny miafina ho an'ny Admin:", type="password")
    if check_pwd == st.session_state.admin_pwd:
        st.success("Tonga soa Patricia!")
        new_pwd = st.text_input("Hanova ny teny miafina vaovao:")
        if st.button("Hitehirizana ny MDP vaovao"):
            st.session_state.admin_pwd = new_pwd
            st.success("Voatahiry!")
    elif check_pwd != "":
        st.error("Diso ny teny miafina!")
