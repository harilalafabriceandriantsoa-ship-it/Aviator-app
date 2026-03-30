import streamlit as st
import hashlib
import random
import time
from datetime import datetime, timedelta

# --- 1. CONFIGURATION & SESSION STATE ---
st.set_page_config(page_title="TITAN V85.0 ULTRA-SYNC", layout="wide")

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
    .cell-star { border: 2px solid #00ffcc !important; box-shadow: 0 0 10px #00ffcc; color: #ffff00; }
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

# --- 4. CORE ALGO ---
def run_prediction(seed, client, power=1.0):
    now = datetime.now() + timedelta(hours=3)
    entropy = str(time.time_ns())
    combined = hashlib.sha256(f"{seed}{client}{entropy}".encode()).hexdigest()
    random.seed(int(combined[:8], 16))
    
    results = []
    for i in range(1, 4):
        target = round(random.uniform(1.65, 5.15) * power, 2)
        ora = (now + timedelta(minutes=i*2)).strftime("%H:%M:%S")
        results.append({"ora": ora, "val": target, "min": round(target*0.85, 2), "max": round(target*1.18, 2)})
    return results

# --- 5. MAIN INTERFACE ---
st.markdown("<h1 style='text-align:left; color:#00ffcc;'>« TITAN V85.0 ULTRA-SYNC</h1>", unsafe_allow_html=True)

t1, t2, t3, t4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS ULTRA PRO", "💣 MINES VIP", "📸 HISTORY"])

# COSMOS (DYNAMIC IA JUMP - MIHAZONA NY LITERA REHETRA)
with t2:
    st.file_uploader("📸 Screenshot COSMOS:", type=['png','jpg'], key="f_cos")
    h_cos = st.text_input("Hash SHA512 Combined (ID):", key="h_cos_in")
    
    col_a, col_b = st.columns(2)
    hex_cos = col_a.text_input("HEX (8 derniers):", key="hex_cos_in")
    time_cos = col_b.text_input("Ora (HH:mm:ss):", key="time_cos_in")
    tour_id = st.text_input("Numéro de Tour (ID manomboka amin'ny 8):", key="tour_id_in", placeholder="Ohatra: 8113638")
    
    if st.button("🔥 ANALYZE COSMOS"):
        if h_cos and tour_id:
            # IA DYNAMIC JUMP: Mikajy elanelana miankina amin'ny Hash
            ia_val = int(hashlib.md5(h_cos.encode()).hexdigest()[:2], 16)
            sauts_ia = [(ia_val % 5) + 3, (ia_val % 8) + 9, (ia_val % 12) + 18]
            
            cols = st.columns(3)
            for i, saut in enumerate(sauts_ia):
                target_tour = int(tour_id) + saut
                seed_ia = hashlib.sha512(f"{h_cos}{target_tour}".encode()).hexdigest()
                res_ia = run_prediction(seed_ia[:32], time_cos, power=1.45)[0]
                
                with cols[i]:
                    st.markdown(f"""
                        <div class="prediction-card">
                            <b style="color:red;">TOUR {target_tour}</b><br>
                            <small style="color:#00ffcc;">AI Jump: +{saut}</small><br>
                            <h2 style="color:#00ffcc;">{res_ia['val']}x</h2>
                            <hr>
                            <div style="font-size:10px;">Lera: {time_cos} (Sync)</div>
                        </div>
                    """, unsafe_allow_html=True)

# MINES
with t3:
    st.markdown("### 💣 MINES VIP 8/10")
    m1, m2 = st.columns(2)
    ms = m1.text_input("Server Seed (Hex):", key="ms_in")
    mc = m2.text_input("Client Seed:", key="mc_in")
    if st.button("🔍 SCAN MINES"):
        if ms and mc:
            random.seed(int(hashlib.md5(f"{ms}{mc}".encode()).hexdigest()[:8], 16))
            stars = random.sample(range(25), 5)
            grid = '<div class="mines-grid">'
            for i in range(25):
                char = "⭐" if i in stars else "⬛"
                cls = "mine-cell cell-star" if i in stars else "mine-cell"
                grid += f'<div class="{cls}">{char}</div>'
            st.session_state.mines_grid = grid + '</div>'
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)

# HISTORY
with t4:
    st.markdown("### 📜 PREDICTIONS HISTORY")
    for h in st.session_state.history[:5]:
        st.write(f"✅ {h}")
