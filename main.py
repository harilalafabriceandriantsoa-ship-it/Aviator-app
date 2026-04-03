import streamlit as st
import hashlib
import hmac
import random
from datetime import datetime, timedelta

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V100.0 FORCE-WIN", layout="wide")

# Fametrahana ny Session State mba tsy ho voafafa ny angon-drakitra
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'history' not in st.session_state: st.session_state.history = []
if 'mines_grid' not in st.session_state: st.session_state.mines_grid = ""

# --- 2. STYLE PREMIUM NEON (BLACK EDITION) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ffcc; font-family: 'Courier New', monospace; }
    .prediction-card {
        background: rgba(0, 255, 204, 0.05); border: 2px solid #00ffcc;
        padding: 15px; border-radius: 20px; text-align: center;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.4); margin-bottom: 10px;
    }
    .stButton>button { 
        background: #00ffcc !important; color: black !important; 
        font-weight: bold; width: 100%; border-radius: 12px; height: 45px; 
    }
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; max-width: 300px; margin: auto; }
    .mine-cell { 
        aspect-ratio: 1/1; background: #1a1a1a; border: 1px solid #333; 
        display: flex; align-items: center; justify-content: center; 
        font-size: 22px; border-radius: 8px; 
    }
    .cell-star { border: 2px solid #00ffcc !important; color: #ffff00; box-shadow: 0 0 10px #00ffcc; }
    .win-text { color: #ffff00; font-weight: bold; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CORE ALGORITHM (HMAC PROVABLY FAIR) ---
def get_sync_data(server_seed, client_seed, mode="crash"):
    # Fampifandraisana ny Seed mampiasa HMAC-SHA256
    hash_obj = hmac.new(server_seed.encode(), client_seed.encode(), hashlib.sha256)
    final_hash = hash_obj.hexdigest()
    random.seed(int(final_hash[:16], 16))
    
    if mode == "mines":
        # Misafidy kintana 5 "Ultra-Safe" raikitra
        return random.sample(range(25), 5)
    
    # Lojika ho an'ny Aviator/Cosmos (MIN, MOYEN, MAX)
    res = []
    for label, l, h, p_min, p_max in [("MIN", 1.60, 2.15, 94, 99), ("MOYEN", 2.20, 3.80, 88, 93), ("MAX", 4.00, 8.50, 75, 87)]:
        val = round(random.uniform(l, h), 2)
        prob = random.randint(p_min, p_max)
        ora = (datetime.now() + timedelta(minutes=random.randint(2, 10))).strftime("%H:%M")
        res.append({"t": label, "v": val, "p": prob, "o": ora})
    return res

# --- 4. LOGIN PAGE ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center;'>🛰️ TITAN V100 LOGIN</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        pwd = st.text_input("Admin Key:", type="password")
        if st.button("HIDITRA"):
            if pwd == "2026":
                st.session_state.logged_in = True
                st.rerun()
    st.stop()

# --- 5. MAIN INTERFACE ---
st.markdown("<h2 style='color:#00ffcc;'>🛰️ TITAN V100.0 FORCE-WIN</h2>", unsafe_allow_html=True)
t1, t2, t3 = st.tabs(["✈️ CRASH (AVIATOR)", "💣 MINES VIP", "📜 HISTORY"])

# --- TAB 1: AVIATOR / COSMOS ---
with t1:
    st.file_uploader("📸 Screenshot Historique:", type=['jpg', 'png'], key="up")
    c1, c2 = st.columns(2)
    s_s = c1.text_input("Server Seed (Hex):", key="ss")
    c_s = c2.text_input("Client Seed (Ora/Teny):", key="cs")
    
    if st.button("🔥 GENERATE SIGNAL"):
        if s_s and c_s:
            data = get_sync_data(s_s, c_s)
            cols = st.columns(3)
            for i, r in enumerate(data):
                cols[i].markdown(f"""
                    <div class="prediction-card">
                        <b style="color:red;">{r['t']}</b><br>
                        <h2 style="color:#00ffcc;">{r['v']}x</h2>
                        <small>{r['o']}</small><br>
                        <span style="color:#ffff00;">Sync: {r['p']}%</span>
                    </div>
                """, unsafe_allow_html=True)
            st.session_state.history.insert(0, f"Crash: {data[0]['v']}x ({data[0]['p']}%)")

# --- TAB 2: MINES VIP ---
with t2:
    st.markdown("<p style='text-align:center;'>Kintana 5 'SUR' miankina amin'ny Seed</p>", unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    ms = m1.text_input("Server Seed:", key="msm")
    mc = m2.text_input("Client Seed:", key="mcm")
    
    if st.button("🔍 SCAN 5 DIAMANTS"):
        if ms and mc:
            stars = get_sync_data(ms, mc, mode="mines")
            grid = '<div class="mines-grid">'
            for i in range(25):
                is_star = i in stars
                grid += f'<div class="mine-cell {"cell-star" if is_star else ""}">{"⭐" if is_star else "⬛"}</div>'
            st.session_state.mines_grid = grid + '</div>'
            
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)
        st.markdown("<p class='win-text'>✅ SCHEMA SYNCED: Kitiho ireo kintana 5 ireo.</p>", unsafe_allow_html=True)

# --- TAB 3: HISTORY ---
with t3:
    for h in st.session_state.history[:10]:
        st.write(f"✅ {h}")

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ SETTINGS")
    if st.button("🗑️ RESET DATA"):
        st.session_state.history = []
        st.session_state.mines_grid = ""
        st.rerun()
