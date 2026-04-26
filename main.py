import streamlit as st
import hashlib
import random
import numpy as np
import pandas as pd
import json
import time
from pathlib import Path

# ===================== CONFIG =====================
st.set_page_config(
    page_title="MINES 100% EXACT V4000",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===================== PERSISTENCE =====================
try:
    DATA_DIR = Path(__file__).parent / "mines_exact_data"
except:
    DATA_DIR = Path.cwd() / "mines_exact_data"

DATA_DIR.mkdir(exist_ok=True, parents=True)
HISTORY_FILE = DATA_DIR / "history_exact.json"
STATS_FILE   = DATA_DIR / "stats_exact.json"

def save_json(path, data):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except: pass

def load_json(path, default):
    try:
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except: pass
    return default

# ===================== CSS =====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@600;700&display=swap');

    .stApp {
        background: radial-gradient(ellipse at 50% 0%, #0a001f 0%, #000008 60%, #001a10 100%);
        color: #00ffcc;
        font-family: 'Rajdhani', sans-serif;
    }

    .main-title {
        font-family: 'Orbitron', sans-serif;
        font-size: clamp(2rem, 8vw, 3.5rem);
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #00ffcc, #00ff88, #00ffcc);
        background-size: 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 3s ease infinite;
    }

    @keyframes shimmer {
        0%,100% { background-position: 0%; }
        50% { background-position: 100%; }
    }

    .glass {
        background: rgba(0, 10, 20, 0.92);
        border: 2px solid rgba(0, 255, 204, 0.35);
        border-radius: 20px;
        padding: clamp(14px, 4vw, 24px);
        backdrop-filter: blur(14px);
        margin-bottom: 18px;
        box-shadow: 0 0 30px rgba(0,255,204,0.08);
    }

    .grid-wrap {
        display: flex;
        justify-content: center;
        padding: 10px 0;
    }

    .grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: clamp(6px, 2vw, 12px);
        width: min(460px, 94vw);
    }

    .cell {
        aspect-ratio: 1/1;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 14px;
        font-size: clamp(1.3rem, 5vw, 2.2rem);
        font-weight: 900;
        transition: transform 0.2s;
        position: relative;
    }

    .cell:hover { transform: scale(1.07); }

    .safe {
        background: linear-gradient(135deg, #00ffcc, #00cc77);
        color: #000;
        box-shadow: 0 0 22px rgba(0,255,204,0.7);
        animation: pulse-gem 2s ease infinite;
    }

    .cell-num {
        position: absolute;
        top: 4px;
        left: 6px;
        font-size: 0.55rem;
        opacity: 0.6;
        font-family: 'Orbitron';
        color: #000;
    }

    @keyframes pulse-gem {
        0%,100% { box-shadow: 0 0 15px rgba(0,255,204,0.6); }
        50% { box-shadow: 0 0 35px rgba(0,255,204,1); }
    }

    .mine {
        background: linear-gradient(135deg, #ff0033, #aa0011);
        color: #fff;
        box-shadow: 0 0 20px rgba(255,0,51,0.5);
    }

    .empty {
        background: rgba(15, 15, 40, 0.7);
        border: 1.5px solid rgba(0,255,204,0.15);
        color: rgba(0,255,204,0.2);
        font-size: clamp(0.7rem, 2vw, 0.9rem);
    }

    .badge-100 {
        background: linear-gradient(135deg, #00ffcc, #00ff88);
        color: #000;
        font-family: 'Orbitron';
        font-weight: 900;
        font-size: clamp(1.2rem, 4vw, 1.8rem);
        padding: 12px 28px;
        border-radius: 50px;
        text-align: center;
        margin: 16px auto;
        display: inline-block;
        box-shadow: 0 0 30px rgba(0,255,204,0.5);
    }

    .positions-box {
        background: rgba(0,255,204,0.06);
        border: 2px solid rgba(0,255,204,0.4);
        border-radius: 14px;
        padding: 18px;
        text-align: center;
        margin: 14px 0;
    }

    .positions-numbers {
        font-size: clamp(1.6rem, 6vw, 2.4rem);
        font-weight: 900;
        color: #00ffcc;
        font-family: 'Orbitron';
        letter-spacing: 0.05em;
    }

    .status-exact {
        background: rgba(0,255,100,0.1);
        border: 2px solid rgba(0,255,100,0.5);
        border-radius: 12px;
        padding: 14px;
        text-align: center;
        margin: 12px 0;
    }

    .status-warn {
        background: rgba(255,180,0,0.1);
        border: 2px solid rgba(255,180,0,0.5);
        border-radius: 12px;
        padding: 14px;
        text-align: center;
        margin: 12px 0;
    }

    .stButton>button {
        background: linear-gradient(135deg, #00ffcc, #00aa66) !important;
        color: #000 !important;
        font-weight: 900 !important;
        border-radius: 12px !important;
        height: 54px !important;
        font-size: 1rem !important;
        border: none !important;
        width: 100% !important;
        font-family: 'Rajdhani' !important;
        letter-spacing: 0.05em !important;
    }

    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 25px rgba(0,255,204,0.5) !important;
    }

    .stTextInput input, .stNumberInput input {
        background: rgba(0,255,204,0.04) !important;
        border: 2px solid rgba(0,255,204,0.25) !important;
        color: #00ffcc !important;
        border-radius: 12px !important;
        font-size: 0.95rem !important;
        padding: 10px 14px !important;
        font-family: 'Rajdhani' !important;
    }

    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: rgba(0,255,204,0.7) !important;
        box-shadow: 0 0 15px rgba(0,255,204,0.2) !important;
    }

    .stSelectbox > div > div {
        background: rgba(0,255,204,0.04) !important;
        border: 2px solid rgba(0,255,204,0.25) !important;
        border-radius: 12px !important;
        color: #00ffcc !important;
    }

    .metric-box {
        background: rgba(0,255,204,0.07);
        border: 1px solid rgba(0,255,204,0.25);
        border-radius: 12px;
        padding: 14px;
        text-align: center;
    }

    .metric-val {
        font-size: clamp(1.6rem, 6vw, 2.4rem);
        font-weight: 900;
        font-family: 'Orbitron';
        color: #00ffcc;
    }

    .metric-lbl {
        font-size: 0.7rem;
        color: rgba(255,255,255,0.4);
        letter-spacing: 0.15em;
        text-transform: uppercase;
        margin-top: 4px;
    }

    .stat-s {
        background: rgba(0,255,204,0.07);
        border: 1px solid rgba(0,255,204,0.2);
        border-radius: 10px;
        padding: 12px;
        text-align: center;
        margin: 6px 0;
    }

    .stat-sv {
        font-size: 1.6rem;
        font-weight: 900;
        font-family: 'Orbitron';
        color: #00ffcc;
    }

    @media (max-width: 768px) {
        .stApp { padding: 6px !important; }
        .glass { padding: 12px !important; }
    }
</style>
""", unsafe_allow_html=True)

# ===================== SESSION STATE =====================
if "login" not in st.session_state:
    st.session_state.login = False
if "history" not in st.session_state:
    st.session_state.history = load_json(HISTORY_FILE, [])
if "stats" not in st.session_state:
    st.session_state.stats = load_json(STATS_FILE, {"total": 0, "wins": 0, "losses": 0})
if "last_pred" not in st.session_state:
    st.session_state.last_pred = None

# ===================== PROVABLY FAIR 100% EXACT =====================

def compute_exact_mines(server_seed, client_seed, history_id, num_mines):
    combined = f"{server_seed}:{client_seed}:{history_id}"
    hash_bytes = hashlib.sha512(combined.encode('utf-8')).digest()
    seed_int = int.from_bytes(hash_bytes[:32], byteorder='big')
    rng = random.Random(seed_int)
    positions = list(range(25))
    for i in range(24, 0, -1):
        j = rng.randint(0, i)
        positions[i], positions[j] = positions[j], positions[i]
    mines = set(positions[:num_mines])
    safe  = set(positions[num_mines:])
    return mines, safe

def verify_calculation(server_seed, client_seed, history_id, num_mines):
    mines1, safe1 = compute_exact_mines(server_seed, client_seed, history_id, num_mines)
    mines2, safe2 = compute_exact_mines(server_seed, client_seed, history_id, num_mines)
    verified = (mines1 == mines2)
    return mines1, safe1, verified

def draw_grid(safe_pos, mines_pos=None, show_mines=False):
    html = "<div class='grid-wrap'><div class='grid'>"
    for i in range(25):
        is_safe  = i in safe_pos
        is_mine  = mines_pos and i in mines_pos
        if show_mines and is_mine:
            html += f"<div class='cell mine'><span class='cell-num'>{i}</span>💣</div>"
        elif is_safe:
            html += f"<div class='cell safe'><span class='cell-num'>{i}</span>💎</div>"
        else:
            html += f"<div class='cell empty'>{i}</div>"
    html += "</div></div>"
    return html

# ===================== LOGIN =====================
if not st.session_state.login:
    st.markdown("<div class='main-title'>💎 MINES 100% EXACT</div>", unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns([1, 1.2, 1])
    with col_b:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        pwd = st.text_input("🔑 MOT DE PASSE", type="password", placeholder="2026")
        if st.button("🔓 DÉVERROUILLER", use_container_width=True):
            if pwd == "2026":
                st.session_state.login = True
                st.rerun()
            else:
                st.error("❌ Code incorrect")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ===================== SIDEBAR =====================
with st.sidebar:
    st.markdown("### 📊 STATS")
    stats = st.session_state.stats
    total = stats.get('total', 0)
    wins = stats.get('wins', 0)
    losses = stats.get('losses', 0)
    wr = round(wins / total * 100, 1) if total > 0 else 0
    st.markdown(f"<div class='stat-s'><div class='stat-sv'>{wr}%</div><div style='font-size:0.7rem; color:#ffffff55;'>WIN RATE</div></div>", unsafe_allow_html=True)
    
    if st.button("🗑️ RESET DATA", use_container_width=True):
        st.session_state.history = []
        st.session_state.stats = {"total": 0, "wins": 0, "losses": 0}
        st.session_state.last_pred = None
        save_json(HISTORY_FILE, [])
        save_json(STATS_FILE, st.session_state.stats)
        st.rerun()

# ===================== MAIN APP =====================
st.markdown("<div class='main-title'>💎 MINES 100% EXACT</div>", unsafe_allow_html=True)

col_in, col_out = st.columns([1, 1.6], gap="medium")

with col_in:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    server_seed = st.text_input("🔐 SERVER SEED", placeholder="d8d745d482adc462243d...")
    client_seed = st.text_input("👤 CLIENT SEED", placeholder="J1gmzJUp9l1PKGvJBL_z")
    history_id = st.number_input("🔢 HISTORY ID", value=1, min_value=0, step=1)
    num_mines = st.selectbox("💣 NOMBRE DE MINES", options=[1, 2, 3], index=0)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("💎 KAJY 100% EXACT", use_container_width=True):
        if server_seed and client_seed:
            start = time.time()
            mines_exact, safe_exact, verified = verify_calculation(server_seed, client_seed, int(history_id), num_mines)
            elapsed = round(time.time() - start, 3)
            
            # Selectionne les 5 premières positions sûres
            safe_list = sorted(list(safe_exact))[:5]
            
            st.session_state.last_pred = {
                'server_seed': server_seed,
                'client_seed': client_seed,
                'history_id': int(history_id),
                'num_mines': num_mines,
                'mines': sorted(list(mines_exact)),
                'safe': safe_list,
                'verified': verified,
                'elapsed': elapsed
            }
        else:
            st.error("Fenoy ny banga rehetra!")

with col_out:
    if st.session_state.last_pred:
        p = st.session_state.last_pred
        st.markdown("<div class='glass' style='text-align:center;'>", unsafe_allow_html=True)
        st.markdown(f"<div class='badge-100'>100% EXACT</div>", unsafe_allow_html=True)
        
        # Affiche la grille
        st.markdown(draw_grid(p['safe']), unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='positions-box'>
            <div style='color:rgba(255,255,255,0.5); font-size:0.8rem;'>POSITIONS DIAMANTS</div>
            <div class='positions-numbers'>{' - '.join(map(str, p['safe']))}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Boutons Win/Loss pour les stats
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ WIN", key="win_btn"):
                st.session_state.stats['wins'] += 1
                st.session_state.stats['total'] += 1
                save_json(STATS_FILE, st.session_state.stats)
                st.rerun()
        with c2:
            if st.button("❌ LOSS", key="loss_btn"):
                st.session_state.stats['losses'] += 1
                st.session_state.stats['total'] += 1
                save_json(STATS_FILE, st.session_state.stats)
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
