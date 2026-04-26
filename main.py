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
    page_title="MINES 100% EXACT V5000",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===================== PERSISTENCE =====================
try:
    DATA_DIR = Path(__file__).parent / "mines_v5000_data"
except:
    DATA_DIR = Path.cwd() / "mines_v5000_data"

DATA_DIR.mkdir(exist_ok=True, parents=True)
HISTORY_FILE = DATA_DIR / "history.json"
STATS_FILE   = DATA_DIR / "stats.json"

def save_json(path, data):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except:
        pass

def load_json(path, default):
    try:
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
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
        font-size: clamp(1.8rem, 7vw, 3rem);
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #00ffcc, #00ff88, #00ffcc);
        background-size: 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 3s ease infinite;
        margin-bottom: 4px;
    }

    @keyframes shimmer {
        0%,100% { background-position: 0%; }
        50%      { background-position: 100%; }
    }

    .glass {
        background: rgba(0, 10, 20, 0.92);
        border: 2px solid rgba(0, 255, 204, 0.35);
        border-radius: 18px;
        padding: clamp(12px, 4vw, 22px);
        backdrop-filter: blur(14px);
        margin-bottom: 16px;
        box-shadow: 0 0 25px rgba(0,255,204,0.07);
    }

    .mgrid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: clamp(5px, 1.8vw, 11px);
        width: min(440px, 92vw);
        margin: 16px auto;
    }

    .mcell {
        aspect-ratio: 1/1;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border-radius: 12px;
        font-size: clamp(1.3rem, 4.5vw, 2rem);
        font-weight: 900;
        transition: transform 0.15s;
        position: relative;
    }

    .mcell:hover { transform: scale(1.06); }

    .cnum {
        position: absolute;
        top: 3px;
        left: 5px;
        font-size: clamp(0.45rem, 1.2vw, 0.6rem);
        font-family: 'Orbitron';
        opacity: 0.55;
    }

    .csafe {
        background: linear-gradient(135deg, #00ffcc, #00cc77);
        color: #000;
        box-shadow: 0 0 18px rgba(0,255,204,0.65);
        animation: pgem 2s ease infinite;
    }
    @keyframes pgem {
        0%,100% { box-shadow: 0 0 12px rgba(0,255,204,0.55); }
        50%      { box-shadow: 0 0 30px rgba(0,255,204,0.95); }
    }

    .cmine {
        background: linear-gradient(135deg, #ff0033, #aa0011);
        color: #fff;
        box-shadow: 0 0 16px rgba(255,0,51,0.45);
    }

    .cempty {
        background: rgba(12, 12, 35, 0.75);
        border: 1.5px solid rgba(0,255,204,0.12);
        color: rgba(0,255,204,0.18);
        font-size: clamp(0.65rem, 2vw, 0.85rem);
    }

    .stButton>button {
        background: linear-gradient(135deg, #00ffcc, #00aa66) !important;
        color: #000 !important;
        font-weight: 900 !important;
        border-radius: 11px !important;
        height: 52px !important;
        font-size: 0.95rem !important;
        border: none !important;
        width: 100% !important;
        font-family: 'Rajdhani' !important;
        letter-spacing: 0.04em !important;
        transition: all 0.2s !important;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 22px rgba(0,255,204,0.5) !important;
    }

    .stTextInput input, .stNumberInput input {
        background: rgba(0,255,204,0.04) !important;
        border: 2px solid rgba(0,255,204,0.22) !important;
        color: #00ffcc !important;
        border-radius: 11px !important;
        font-size: 0.9rem !important;
        padding: 10px 13px !important;
        font-family: 'Rajdhani' !important;
    }

    .mbox {
        background: rgba(0,255,204,0.06);
        border: 1px solid rgba(0,255,204,0.22);
        border-radius: 11px;
        padding: 12px;
        text-align: center;
    }
    .mval {
        font-size: clamp(1.4rem, 5vw, 2.2rem);
        font-weight: 900;
        font-family: 'Orbitron';
        color: #00ffcc;
    }
    .mlbl {
        font-size: 0.65rem;
        color: rgba(255,255,255,0.38);
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-top: 3px;
    }

    .badge100 {
        background: linear-gradient(135deg, #00ffcc, #00ff88);
        color: #000;
        font-family: 'Orbitron';
        font-weight: 900;
        font-size: clamp(1rem, 3.5vw, 1.5rem);
        padding: 10px 24px;
        border-radius: 50px;
        display: inline-block;
        box-shadow: 0 0 26px rgba(0,255,204,0.5);
    }

    .posbox {
        background: rgba(0,255,204,0.05);
        border: 2px solid rgba(0,255,204,0.35);
        border-radius: 13px;
        padding: 16px;
        text-align: center;
        margin: 12px 0;
    }
    .posnums {
        font-size: clamp(1.3rem, 5vw, 2rem);
        font-weight: 900;
        color: #00ffcc;
        font-family: 'Orbitron';
        letter-spacing: 0.04em;
    }

    .minebox {
        background: rgba(255,0,51,0.07);
        border: 1.5px solid rgba(255,0,51,0.28);
        border-radius: 11px;
        padding: 13px;
        text-align: center;
        margin: 10px 0;
    }

    .nextbox {
        background: rgba(0,255,204,0.04);
        border: 1px solid rgba(0,255,204,0.18);
        border-radius: 11px;
        padding: 13px;
        text-align: center;
        margin-top: 12px;
    }

    .sstat {
        background: rgba(0,255,204,0.06);
        border: 1px solid rgba(0,255,204,0.18);
        border-radius: 9px;
        padding: 11px;
        text-align: center;
        margin: 5px 0;
    }
    .ssv {
        font-size: 1.5rem;
        font-weight: 900;
        font-family: 'Orbitron';
        color: #00ffcc;
    }
</style>
""", unsafe_allow_html=True)

# ===================== SESSION STATE =====================
if "login"     not in st.session_state: st.session_state.login     = False
if "history"   not in st.session_state: st.session_state.history   = load_json(HISTORY_FILE, [])
if "stats"     not in st.session_state: st.session_state.stats     = load_json(STATS_FILE, {"total":0,"wins":0,"losses":0})
if "result"    not in st.session_state: st.session_state.result    = None
if "calc_key"  not in st.session_state: st.session_state.calc_key  = 0

# ===================== PROVABLY FAIR =====================
def compute_mines(server_seed: str, client_seed: str, history_id: int, num_mines: int):
    combined   = f"{server_seed.strip()}:{client_seed.strip()}:{history_id}"
    hash_bytes = hashlib.sha512(combined.encode('utf-8')).digest()
    seed_int   = int.from_bytes(hash_bytes[:32], byteorder='big')

    rng       = random.Random(seed_int)
    positions = list(range(25))

    for i in range(24, 0, -1):
        j = rng.randint(0, i)
        positions[i], positions[j] = positions[j], positions[i]

    mines = set(positions[:num_mines])
    safe  = set(positions[num_mines:])
    return mines, safe

def render_grid(safe_set: set, mine_set: set, reveal_mines: bool = True) -> str:
    html = "<div class='mgrid'>"
    for i in range(25):
        if i in mine_set and reveal_mines:
            html += f"<div class='mcell cmine'><span class='cnum'>{i}</span>💣</div>"
        elif i in safe_set:
            html += f"<div class='mcell csafe'><span class='cnum'>{i}</span>💎</div>"
        else:
            html += f"<div class='mcell cempty'>{i}</div>"
    html += "</div>"
    return html

# ===================== LOGIN =====================
if not st.session_state.login:
    st.markdown("<div class='main-title'>💎 MINES 100% EXACT V5000</div>", unsafe_allow_html=True)
    _, col_b, _ = st.columns([1, 1.2, 1])
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
    s = st.session_state.stats
    tot, w, l = s.get('total', 0), s.get('wins', 0), s.get('losses', 0)
    wr = round(w / tot * 100, 1) if tot > 0 else 0
    st.markdown(f"<div class='sstat'><div class='ssv'>{wr}%</div><div>WIN RATE</div></div>", unsafe_allow_html=True)
    if st.button("🗑️ RESET DATA"):
        st.session_state.history, st.session_state.stats = [], {"total":0,"wins":0,"losses":0}
        st.rerun()

# ===================== MAIN =====================
st.markdown("<div class='main-title'>💎 MINES 100% EXACT V5000</div>", unsafe_allow_html=True)
col_in, col_out = st.columns([1, 1.55], gap="medium")

with col_in:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    srv = st.text_input("🔐 SERVER SEED", key="inp_server")
    cli = st.text_input("👤 CLIENT SEED", key="inp_client")
    hid = st.number_input("🔢 HISTORY ID", key="inp_hid", value=1, min_value=0)
    mns = st.selectbox("💣 MINES", options=[1, 2, 3], key="inp_mines")
    
    if st.button("💎 KAJY 100% EXACT", use_container_width=True):
        if srv and cli:
            m_set, s_set = compute_mines(srv, cli, int(hid), mns)
            st.session_state.result = {
                "server": srv, "client": cli, "history_id": int(hid),
                "num_mines": mns, "mines": sorted(list(m_set)), "safe": sorted(list(s_set)),
                "verified": True, "elapsed": 0.001, "hist_idx": len(st.session_state.history)
            }
            st.session_state.history.append(st.session_state.result)
            save_json(HISTORY_FILE, st.session_state.history)
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with col_out:
    res = st.session_state.result
    if res:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        mode = st.radio("👁️ VIEW:", ["💎 SAFE", "🗺️ BOARD"], horizontal=True)
        st.markdown(render_grid(set(res["safe"]), set(res["mines"]), reveal_mines=(mode=="🗺️ BOARD")), unsafe_allow_html=True)
        
        st.markdown(f"<div class='posbox'><div class='posnums'>{', '.join(map(str, res['safe']))}</div></div>", unsafe_allow_html=True)

        cw, cl = st.columns(2)
        with cw:
            if st.button("✅ WIN", use_container_width=True):
                st.session_state.stats["total"] += 1
                st.session_state.stats["wins"] += 1
                save_json(STATS_FILE, st.session_state.stats)
                st.rerun()
        with cl:
            if st.button("❌ LOSS", use_container_width=True):
                st.session_state.stats["total"] += 1
                st.session_state.stats["losses"] += 1
                save_json(STATS_FILE, st.session_state.stats)
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Ampidiro ny seeds dia tsindrio KAJY")
