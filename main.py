import streamlit as st
import hashlib
import random

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V85.0 ULTRA-SYNC", layout="wide")

if 'history' not in st.session_state: st.session_state.history = []
if 'mines_grid' not in st.session_state: st.session_state.mines_grid = ""

# --- 2. STYLE ORIGINAL (TSY NIOVA NA LITERA RAY) ---
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

# AVIATOR (Original)
with t1:
    s_avi = st.text_input("Server Seed (Hex):", key="s_avi")
    c_avi = st.text_input("Client Seed:", key="c_avi")
    if st.button("🔥 ANALYZE AVIATOR"):
        if s_avi and c_avi:
            random.seed(int(hashlib.sha256(f"{s_avi}{c_avi}".encode()).hexdigest()[:8], 16))
            cols = st.columns(3)
            for i in range(3):
                val = round(random.uniform(1.30, 3.80), 2)
                with cols[i]:
                    st.markdown(f'<div class="prediction-card"><b>TOUR {i+1}</b><br><span style="font-size:38px; color:#00ffcc;">{val}x</span></div>', unsafe_allow_html=True)

# COSMOS ULTRA PRO (Ity ihany no nampiana Hash sy HEX)
with t2:
    st.subheader("Kajy Cosmos Provably Fair (Ultra Pro)")
    st.info("Ampidiro ny Hash sy Hex avy amin'ny lalao (Provably Fair) ho an'ny prédiction mafy.")
    
    c_hash = st.text_input("Hash SHA512 Combined:", placeholder="f81f7076664b3571812c4925110deccfc9752745c13dc940998f6a8...")
    h_hex = st.text_input("HEX (8 derniers caractères):", placeholder="d265709a")
    
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

# MINES VIP (Original)
with t3:
    st.subheader("💣 MINES VIP 8/10")
    m_s = st.text_input("Seed du serveur:", key="m_s")
    m_c = st.text_input("Seed du client:", key="m_c")
    if st.button("🔍 SCAN MINES"):
        if m_s and m_c:
            random.seed(int(hashlib.sha256(f"{m_s}{m_c}".encode()).hexdigest()[:8], 16))
            stars = random.sample(range(25), 5)
            grid = '<div class="mines-grid">'
            for i in range(25):
                cls = "mine-cell cell-star" if i in stars else "mine-cell"
                char = "⭐" if i in stars else "⬛"
                grid += f'<div class="{cls}">{char}</div>'
            grid += '</div>'
            st.session_state.mines_grid = grid
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;'>🍀 Bonne chance à tous !</p>", unsafe_allow_html=True)

# HISTORY
with t4:
    st.subheader("📜 LAST PREDICTIONS")
    for h in st.session_state.history[:10]:
        st.write(f"✅ {h}")

st.markdown("---")
st.button("🛠️ Manage app", use_container_width=True)
