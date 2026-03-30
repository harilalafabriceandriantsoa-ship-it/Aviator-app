import streamlit as st
import hashlib
import random
from datetime import datetime, timedelta

# --- CONFIGURATION ---
st.set_page_config(page_title="TITAN V85.0 ULTRA-SYNC", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'admin_pwd' not in st.session_state: st.session_state.admin_pwd = "2026"
if 'history' not in st.session_state: st.session_state.history = []
if 'manche_screenshots' not in st.session_state: st.session_state.manche_screenshots = []
if 'mines_grid' not in st.session_state: st.session_state.mines_grid = ""

# --- STYLE ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ffcc; font-family: 'Courier New', monospace; }
    .prediction-card {
        background: rgba(0, 255, 204, 0.05);
        border: 2px solid #00ffcc;
        padding: 20px; border-radius: 20px; text-align: center;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.4); margin-bottom: 15px;
    }
    .mines-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 8px;
        max-width: 350px;
        margin: 20px auto;
        padding: 10px;
        background: #111;
        border-radius: 10px;
        border: 1px solid #333;
    }
    .mine-cell {
        aspect-ratio: 1/1;
        background: #1a1a1a;
        border: 1px solid #444;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
    }
    .cell-star { border: 2px solid #ffff00 !important; box-shadow: 0 0 8px #ffff00; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIN ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🛰️ TITAN V85.0 LOGIN</h1>", unsafe_allow_html=True)
    pwd_input = st.text_input("Admin Key:", type="password")
    if st.button("HAMPIDITRA"):
        if pwd_input == st.session_state.admin_pwd:
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- ALGORITHM ---
def get_predictions(seed, client, game, hex_val=None):
    now = datetime.now() + timedelta(hours=3)
    results = []
    final_seed = hex_val if hex_val else seed
    random.seed(int(hashlib.sha256(f"{final_seed}{client}{random.random()}".encode()).hexdigest()[:8], 16))
    for i in range(1, 4):
        moyen = round(random.uniform(1.50, 4.50), 2)
        ora = (now + timedelta(minutes=i*2)).strftime("%H:%M")
        p = {"game": game, "ora": ora, "moyen": moyen}
        results.append(p)
        st.session_state.history.insert(0, p)
    return results

# --- MAIN INTERFACE ---
st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🛰️ TITAN V85.0 ULTRA-SYNC</h1>", unsafe_allow_html=True)
t1, t2, t3, t4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS ULTRA PRO", "💣 MINES VIP", "📸 HISTORY"])

# AVIATOR
with t1:
    st.markdown("### 📸 Screenshot AVIATOR:")
    st.file_uploader("Drag and drop file here", type=['png','jpg'], key="f_avi")
    c1, c2 = st.columns(2)
    s_avi = c1.text_input("Server Seed (Hex):")
    c_avi = c2.text_input("Lera / Client Seed (HH:MM):")
    if st.button("🔥 ANALYZE AVIATOR"):
        preds = get_predictions(s_avi, c_avi, "AVIATOR")
        cols = st.columns(3)
        for i, r in enumerate(preds):
            with cols[i]:
                st.markdown(f'<div class="prediction-card"><b>TOUR {i+1}</b><br>{r["ora"]}<br><span style="font-size:30px; color:#00ffcc;">{r["moyen"]}x</span></div>', unsafe_allow_html=True)

# COSMOS
with t2:
    st.file_uploader("📸 Screenshot COSMOS:", type=['png','jpg'], key="f_cos")
    col_h, col_t = st.columns(2)
    h_hex = col_h.text_input("HEX (8 derniers caractères):")
    h_time = col_t.text_input("Ora (HH:mm:ss):")
    if st.button("🔥 ANALYZE COSMOS"):
        preds = get_predictions("", h_time, "COSMOS", hex_val=h_hex)
        cols = st.columns(3)
        for i, r in enumerate(preds):
            with cols[i]:
                st.markdown(f'<div class="prediction-card"><b>TOUR {i+1}</b><br>{r["ora"]}<br><span style="font-size:30px; color:#00ffcc;">{r["moyen"]}x</span></div>', unsafe_allow_html=True)

# MINES VIP (Ultra Visual Update)
with t3:
    st.markdown("### 💣 MINES VIP 8/10")
    m_col1, m_col2 = st.columns(2)
    m_seed = m_col1.text_input("Seed du serveur (Hex):")
    m_client = m_col2.text_input("Seed du client (Ora):")
    
    if st.button("🔍 SCAN MINES"):
        # Ny algorithm-nao efa nisy:
        random.seed(int(hashlib.sha256(f"{m_seed}{m_client}".encode()).hexdigest()[:10], 16))
        stars_indices = random.sample(range(25), 5) # Manao scan kintana 5
        
        grid_html = '<div class="mines-grid">'
        for i in range(25):
            if i in stars_indices:
                grid_html += f'<div class="mine-cell cell-star">⭐</div>'
            else:
                grid_html += f'<div class="mine-cell">⬛</div>'
        grid_html += '</div>'
        st.session_state.mines_grid = grid_html
        
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)
        st.success("Scan vita! Araho ireo kintana ireo.")

# HISTORY
with t4:
    st.subheader("📜 LAST PREDICTIONS")
    for h in st.session_state.history[:10]:
        st.write(f"🎮 {h['game']} | {h['ora']} | {h['moyen']}x")
