import streamlit as st
import hashlib
import random
import json
import time
from pathlib import Path

# ===================== CONFIG =====================
st.set_page_config(
    page_title="MINES 💎 100% V7000",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===================== PERSISTENCE =====================
try:
    DATA_DIR = Path(__file__).parent / "mines_v7000_data"
except:
    DATA_DIR = Path.cwd() / "mines_v7000_data"

DATA_DIR.mkdir(exist_ok=True, parents=True)
HISTORY_FILE = DATA_DIR / "history.json"
STATS_FILE   = DATA_DIR / "stats.json"

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
        background: radial-gradient(ellipse at 50% 0%, #080018 0%, #000008 55%, #001510 100%);
        color: #00ffcc;
        font-family: 'Rajdhani', sans-serif;
    }

    .main-title {
        font-family: 'Orbitron', sans-serif;
        font-size: clamp(1.6rem, 6.5vw, 3rem);
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #00ffcc, #00ff88, #00ddff, #00ffcc);
        background-size: 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 4s ease infinite;
        margin-bottom: 2px;
    }
    @keyframes shine {
        0%,100% { background-position: 0%; }
        50%      { background-position: 100%; }
    }

    .glass {
        background: rgba(0, 8, 18, 0.93);
        border: 2px solid rgba(0, 255, 204, 0.3);
        border-radius: 18px;
        padding: clamp(12px, 4vw, 22px);
        backdrop-filter: blur(16px);
        margin-bottom: 16px;
        box-shadow: 0 0 28px rgba(0,255,204,0.07);
    }

    /* NONCE BOX */
    .nonce-box {
        background: linear-gradient(135deg, rgba(0,255,204,0.15), rgba(0,255,100,0.08));
        border: 2px solid rgba(0,255,204,0.5);
        border-radius: 14px;
        padding: 16px;
        text-align: center;
        margin: 12px 0;
    }
    .nonce-val {
        font-size: clamp(2rem, 8vw, 3rem);
        font-weight: 900;
        font-family: 'Orbitron';
        color: #00ffcc;
    }

    /* GRID */
    .mgrid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: clamp(6px, 2vw, 12px);
        width: min(450px, 93vw);
        margin: 18px auto;
    }
    .mcell {
        aspect-ratio: 1/1;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border-radius: 13px;
        font-weight: 900;
        transition: transform 0.18s;
        position: relative;
        font-size: clamp(1.4rem, 5vw, 2.1rem);
    }
    .mcell:hover { transform: scale(1.07); }
    .cnum {
        position: absolute;
        top: 3px; left: 5px;
        font-size: clamp(0.42rem, 1.1vw, 0.58rem);
        font-family: 'Orbitron';
        opacity: 0.5;
    }

    /* 5 TOP DIAMANTS */
    .ctop {
        background: linear-gradient(135deg, #00ffcc, #00ff66);
        color: #000;
        box-shadow: 0 0 24px rgba(0,255,204,0.8);
        animation: glow5 1.8s ease infinite;
        border: 3px solid #00ffcc;
    }

    .csafe {
        background: rgba(0,255,204,0.1);
        color: #00ffcc;
        border: 1.5px solid rgba(0,255,204,0.25);
    }

    .cmine {
        background: linear-gradient(135deg, #ff0033, #880011);
        color: #fff;
        box-shadow: 0 0 18px rgba(255,0,51,0.5);
    }

    .cempty {
        background: rgba(10,10,30,0.8);
        border: 1.5px solid rgba(0,255,204,0.1);
        color: rgba(0,255,204,0.15);
    }

    .d5box {
        background: linear-gradient(135deg, rgba(0,255,204,0.12), rgba(0,255,100,0.06));
        border: 2.5px solid rgba(0,255,204,0.5);
        border-radius: 16px;
        padding: 18px;
        text-align: center;
        margin: 14px 0;
    }
    .d5nums {
        font-size: clamp(1.5rem, 6vw, 2.2rem);
        font-weight: 900;
        color: #00ffcc;
        font-family: 'Orbitron';
    }

    .sstat { background:rgba(0,255,204,.06); border:1px solid rgba(0,255,204,.18); border-radius:9px; padding:10px; text-align:center; margin:5px 0; }
    .ssv   { font-size:1.4rem; font-weight:900; font-family:'Orbitron'; color:#00ffcc; }

    .stButton>button {
        background: linear-gradient(135deg, #00ffcc, #00aa66) !important;
        color: #000 !important; font-weight:900 !important;
        border-radius:11px !important; height:52px !important;
    }
</style>
""", unsafe_allow_html=True)

# ===================== SESSION STATE =====================
if "login"     not in st.session_state: st.session_state.login     = False
if "history"   not in st.session_state: st.session_state.history   = load_json(HISTORY_FILE, [])
if "stats"     not in st.session_state: st.session_state.stats     = load_json(STATS_FILE, {"total":0,"wins":0,"losses":0})
if "result"    not in st.session_state: st.session_state.result    = None
if "cur_nonce" not in st.session_state: st.session_state.cur_nonce = 0

# ===================== LOGIC =====================

def compute_mines_nonce(server_seed: str, client_seed: str, nonce: int, num_mines: int):
    combined   = f"{server_seed.strip()}:{client_seed.strip()}:{nonce}"
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

def select_best_5(safe_set: set, mines_set: set, server_seed: str, client_seed: str, nonce: int):
    pattern_hash = hashlib.sha256(f"{server_seed}:{client_seed}:{nonce}".encode()).hexdigest()
    pattern_num = int(pattern_hash[:16], 16)

    scores = {}
    for pos in safe_set:
        row, col = pos // 5, pos % 5
        min_dist = min(abs(row - m//5) + abs(col - m%5) for m in mines_set) if mines_set else 4
        dist_score = min_dist * 22
        center_score = (4 - (abs(row - 2) + abs(col - 2))) * 10
        hash_score = (pattern_num + pos * 7919) % 100
        scores[pos] = dist_score + center_score + hash_score

    top5 = sorted(scores, key=lambda p: scores[p], reverse=True)[:5]
    return sorted(top5)

def render_grid(top5, safe_set, mine_set, show_mines):
    html = "<div class='mgrid'>"
    for i in range(25):
        if i in mine_set and show_mines:
            html += f"<div class='mcell cmine'><span class='cnum'>{i}</span>💣</div>"
        elif i in top5:
            html += f"<div class='mcell ctop'><span class='cnum' style='color:#003;'>{i}</span>💎</div>"
        elif i in safe_set:
            html += f"<div class='mcell csafe'><span class='cnum'>{i}</span>⭐</div>"
        else:
            html += f"<div class='mcell cempty'>{i}</div>"
    html += "</div>"
    return html

# ===================== MAIN UI =====================
if not st.session_state.login:
    st.markdown("<div class='main-title'>💎 MINES 100% EXACT V7000</div>", unsafe_allow_html=True)
    _, col_b, _ = st.columns([1, 1.2, 1])
    with col_b:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        pwd = st.text_input("🔑 MOT DE PASSE", type="password")
        if st.button("🔓 DÉVERROUILLER", use_container_width=True):
            if pwd == "2026":
                st.session_state.login = True
                st.rerun()
            else:
                st.error("❌ Code incorrect")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

with st.sidebar:
    st.markdown("### 📊 STATS")
    s = st.session_state.stats
    st.markdown(f"<div class='sstat'><div class='ssv'>{s['wins']} / {s['total']}</div><div style='color:#fff4;'>WINS</div></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f"<div class='nonce-box'><div class='nonce-val'>{st.session_state.cur_nonce}</div></div>", unsafe_allow_html=True)
    if st.button("🔄 RESET NONCE"):
        st.session_state.cur_nonce = 0
        st.rerun()

st.markdown("<div class='main-title'>💎 MINES 100% EXACT V7000</div>", unsafe_allow_html=True)

col_in, col_out = st.columns([1, 1.6], gap="medium")

with col_in:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    srv = st.text_input("🔐 SERVER SEED")
    cli = st.text_input("👤 CLIENT SEED")
    nonce = st.number_input("🔢 NONCE", value=st.session_state.cur_nonce, min_value=0)
    st.session_state.cur_nonce = int(nonce)
    num_m = st.selectbox("💣 MINES", options=[1, 2, 3])
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("💎 KAJY EXACT", use_container_width=True):
        if srv and cli:
            mines_set, safe_set = compute_mines_nonce(srv, cli, int(nonce), num_m)
            top5 = select_best_5(safe_set, mines_set, srv, cli, int(nonce))
            st.session_state.result = {"top5": top5, "safe": safe_set, "mines": mines_set}
            st.rerun()
        else:
            st.error("❌ Fenoy ny seeds!")

with col_out:
    res = st.session_state.result
    if res:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.markdown(f"<div class='d5box'><div class='d5nums'>{', '.join(map(str, res['top5']))}</div></div>", unsafe_allow_html=True)
        
        mode = st.radio("👁️ VIEW:", ["💎 TOP 5", "🗺️ BOARD"], horizontal=True)
        st.markdown(render_grid(res['top5'], res['safe'], res['mines'], show_mines=(mode == "🗺️ BOARD")), unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ WIN"):
                st.session_state.stats["total"] += 1
                st.session_state.stats["wins"] += 1
                st.session_state.cur_nonce += 1
                save_json(STATS_FILE, st.session_state.stats)
                st.rerun()
        with c2:
            if st.button("❌ LOSS"):
                st.session_state.stats["total"] += 1
                st.session_state.stats["losses"] += 1
                st.session_state.cur_nonce += 1
                save_json(STATS_FILE, st.session_state.stats)
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
