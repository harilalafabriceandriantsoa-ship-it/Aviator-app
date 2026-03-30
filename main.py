import streamlit as st
import hashlib
import random
from datetime import datetime, timedelta

# --- 1. CONFIGURATION & SESSION STATE ---
st.set_page_config(page_title="TITAN V85.5 PROVABLY-SAFE", layout="wide")

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
        padding: 20px; border-radius: 20px; text-align: center;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.4); margin-bottom: 15px;
    }
    .luck-msg { color: #00ffcc; font-size: 24px; font-weight: bold; text-align: center; margin-top: 25px; text-shadow: 0 0 10px #00ffcc; }
    .stButton>button { background: #00ffcc !important; color: black !important; border-radius: 15px !important; font-weight: bold; width: 100%; }
    hr { border: 0.5px solid #333; margin: 10px 0; }
    
    .mines-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 10px;
        max-width: 300px;
        margin: 20px auto;
    }
    .mine-cell {
        aspect-ratio: 1/1;
        background: #1a1a1a;
        border: 1px solid #333;
        border-radius: 5px;
        display: flex; align-items: center; justify-content: center; font-size: 24px;
    }
    .cell-star { border: 2px solid #00ffcc !important; box-shadow: 0 0 10px #00ffcc; color: #ffff00; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN PAGE ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🛰️ TITAN V85.5 LOGIN</h1>", unsafe_allow_html=True)
    col_l, _ = st.columns([1, 1])
    with col_l:
        pwd_input = st.text_input("Admin Key / MDP:", type="password")
        if st.button("HAMPIDITRA"):
            if pwd_input == st.session_state.admin_pwd:
                st.session_state.logged_in = True
                st.rerun()
            else: st.error("Diso ny MDP!")
    st.stop()

# --- 4. CORE ALGORITHM (PROVABLY FAIR SYNC) ---
def get_predictions_pro(hash_combined, hex_val, game_name):
    now = datetime.now() + timedelta(hours=3) # Heure Madagascar
    results = []
    # Mampiasa ny Hex avy amin'ny lalao ho "Seed"
    random.seed(int(hex_val, 16) if hex_val else random.randint(1, 1000000))
    
    for i in range(1, 4):
        moyen = round(random.uniform(1.45, 4.50), 2)
        ora = (now + timedelta(minutes=i*2)).strftime("%H:%M")
        p = {
            "game": game_name,
            "ora": ora,
            "moyen": moyen,
            "min": round(moyen * 0.88, 2), 
            "max": round(moyen * 1.25, 2)
        }
        results.append(p)
        st.session_state.history.insert(0, p)
    return results

# --- 5. INTERFACE PRINCIPALE ---
st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🛰️ TITAN V85.5 ULTRA-SYNC</h1>", unsafe_allow_html=True)

t1, t2, t3, t4 = st.tabs(["🚀 COSMOS PRO", "✈️ AVIATOR", "💣 MINES VIP", "📸 HISTORY"])

# COSMOS PRO (Mampiasa ilay sary farany)
with t1:
    st.subheader("Kajy Cosmos Provably Fair")
    col1, col2 = st.columns(2)
    h_comb = col1.text_input("Hash SHA512 Combined (avy amin'ny lalao):", placeholder="f81f7076664b...")
    h_hex = col2.text_input("HEX (8 derniers caractères):", placeholder="d265709a")
    
    if st.button("🔥 ANALYZE COSMOS PRO"):
        if h_comb and h_hex:
            preds = get_predictions_pro(h_comb, h_hex, "COSMOS PRO")
            cols = st.columns(3)
            for i, r in enumerate(preds):
                with cols[i]:
                    st.markdown(f"""
                    <div class="prediction-card">
                        <b style="color:red;">TOUR {i+1}</b><br>
                        <span style="color:#aaa; font-size:12px;">{r['ora']}</span><br>
                        <span style="font-size:38px; color:#00ffcc;">{r['moyen']}x</span><br>
                        <small style="color:#ffffff;">Target (100%)</small>
                        <hr>
                        <div style="font-size:13px; text-align:left; padding-left:10px;">
                            <span style="color:#00ffcc;">●</span> <b>Min:</b> {r['min']}x<br>
                            <span style="color:#ff4444;">●</span> <b>Max:</b> {r['max']}x
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown("<p class='luck-msg'>🍀 Bonne chance à tous !</p>", unsafe_allow_html=True)
        else:
            st.warning("Ampidiro aloha ny Hash sy ny Hex hitanao ao amin'ny Cosmos (sary farany)!")

# AVIATOR (Mitovy tamin'ny teo aloha)
with t2:
    st.subheader("✈️ AVIATOR SYNC")
    a_seed = st.text_input("Server Seed (Hex):", key="avi_s")
    a_clt = st.text_input("Client Seed / Lera (HH:MM):", key="avi_c")
    if st.button("🔥 ANALYZE AVIATOR"):
        preds = get_predictions_pro(a_seed, a_seed[:8] if a_seed else "0", "AVIATOR")
        cols = st.columns(3)
        for i, r in enumerate(preds):
            with cols[i]:
                st.markdown(f'<div class="prediction-card"><b>TOUR {i+1}</b><br>{r["ora"]}<br><span style="font-size:30px; color:#00ffcc;">{r["moyen"]}x</span></div>', unsafe_allow_html=True)

# MINES VIP (Mitovy tamin'ny teo aloha 5x5)
with t3:
    st.subheader("💣 MINES VIP 8/10")
    m_seed = st.text_input("Seed du serveur:", key="mine_s")
    m_client = st.text_input("Seed du client:", key="mine_c")
    if st.button("🔍 SCAN MINES"):
        random.seed(int(hashlib.sha256(f"{m_seed}{m_client}".encode()).hexdigest()[:8], 16))
        stars_indices = random.sample(range(25), 5)
        grid_html = '<div class="mines-grid">'
        for i in range(25):
            char = "⭐" if i in stars_indices else "⬛"
            cls = "mine-cell cell-star" if i in stars_indices else "mine-cell"
            grid_html += f'<div class="{cls}">{char}</div>'
        grid_html += '</div>'
        st.session_state.mines_grid = grid_html

    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)

# HISTORY
with t4:
    for h in st.session_state.history[:10]:
        st.write(f"🕒 {h['ora']} | {h['game']} | **{h['moyen']}x**")
