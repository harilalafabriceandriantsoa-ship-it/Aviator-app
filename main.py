import streamlit as st
import hashlib
import random
import hmac
import json
from pathlib import Path

# ===================== CONFIG =====================
st.set_page_config(
    page_title="MINES 💎 V8000 SHA256",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===================== PERSISTENCE =====================
try:
    DATA_DIR = Path(__file__).parent / "mines_v8000_data"
except:
    DATA_DIR = Path.cwd() / "mines_v8000_data"

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

    /* GRID */
    .mgrid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: clamp(6px, 2vw, 12px);
        width: min(450px, 93vw);
        margin: 16px auto;
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
        font-size: clamp(1.3rem, 4.5vw, 2rem);
    }
    .cnum {
        position: absolute;
        top: 3px; left: 5px;
        font-size: 0.6rem;
        opacity: 0.5;
    }
    .ctop {
        background: linear-gradient(135deg, #00ffcc, #00ff66);
        color: #000;
        box-shadow: 0 0 22px rgba(0,255,204,0.8);
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
    }
    .cempty {
        background: rgba(10,10,30,0.8);
        border: 1.5px solid rgba(0,255,204,0.1);
        color: rgba(255,255,255,0.1);
    }

    .badge {
        background: linear-gradient(135deg, #00ffcc, #00ff88);
        color: #000;
        font-family: 'Orbitron';
        font-weight: 900;
        padding: 8px 18px;
        border-radius: 50px;
        display: inline-block;
    }

    .d5box {
        background: linear-gradient(135deg, rgba(0,255,204,0.12), rgba(0,255,100,0.06));
        border: 2px solid rgba(0,255,204,0.5);
        border-radius: 16px;
        padding: 15px;
        text-align: center;
        margin: 10px 0;
    }
    .d5nums {
        font-size: 1.8rem;
        font-weight: 900;
        color: #00ffcc;
        font-family: 'Orbitron';
    }

    .stButton>button {
        background: linear-gradient(135deg, #00ffcc, #00aa66) !important;
        color: #000 !important; font-weight:900 !important;
        border-radius:11px !important; height:52px !important;
        width:100% !important;
    }
</style>
""", unsafe_allow_html=True)

# ===================== SESSION STATE =====================
if "login"     not in st.session_state: st.session_state.login     = False
if "stats"     not in st.session_state: st.session_state.stats     = load_json(STATS_FILE, {"total":0,"wins":0,"losses":0})
if "result"    not in st.session_state: st.session_state.result    = None
if "cur_nonce" not in st.session_state: st.session_state.cur_nonce = 0

# ===================== ALGORITHMS =====================

def get_positions(server_seed, client_seed, nonce, num_mines, method_type):
    if method_type == "HMAC":
        msg = f"{client_seed}:{nonce}".encode()
        h = hmac.new(server_seed.encode(), msg, hashlib.sha256).digest()
    elif method_type == "CONCAT":
        h = hashlib.sha256(f"{server_seed}:{client_seed}:{nonce}".encode()).digest()
    elif method_type == "CHAIN":
        srv_h = hashlib.sha256(server_seed.encode()).hexdigest()
        h = hashlib.sha256(f"{srv_h}:{client_seed}:{nonce}".encode()).digest()
    else: # SHA512
        h = hashlib.sha512(f"{server_seed}:{client_seed}:{nonce}".encode()).digest()

    seed_int = int.from_bytes(h[:16], byteorder='big')
    rng = random.Random(seed_int)
    positions = list(range(25))
    for i in range(24, 0, -1):
        j = rng.randint(0, i)
        positions[i], positions[j] = positions[j], positions[i]
    
    return set(positions[:num_mines]), set(positions[num_mines:])

def run_all_methods(server_seed, client_seed, nonce, num_mines):
    m1, s1 = get_positions(server_seed, client_seed, nonce, num_mines, "HMAC")
    m2, s2 = get_positions(server_seed, client_seed, nonce, num_mines, "CONCAT")
    m3, s3 = get_positions(server_seed, client_seed, nonce, num_mines, "CHAIN")
    m4, s4 = get_positions(server_seed, client_seed, nonce, num_mines, "SHA512")

    all_mines = [m1, m2, m3, m4]
    consensus_mine = max(all_mines, key=lambda x: sum(1 for m in all_mines if m == x))
    match_count = sum(1 for m in all_mines if m == consensus_mine)
    consensus_safe = set(range(25)) - consensus_mine
    
    return list(consensus_mine), consensus_safe, match_count

# ===================== UI HELPERS =====================

def render_grid(top5, safe_set, mine_set):
    html = "<div class='mgrid'>"
    for i in range(25):
        if i in top5:
            html += f"<div class='mcell ctop'><span class='cnum'>{i}</span>💎</div>"
        elif i in mine_set:
            html += f"<div class='mcell cmine'><span class='cnum'>{i}</span>💣</div>"
        elif i in safe_set:
            html += f"<div class='mcell csafe'><span class='cnum'>{i}</span>⭐</div>"
        else:
            html += f"<div class='mcell cempty'>{i}</div>"
    html += "</div>"
    return html

# ===================== MAIN APP =====================

if not st.session_state.login:
    st.markdown("<div class='main-title'>💎 MINES V8000</div>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        pwd = st.text_input("🔑 MOT DE PASSE", type="password")
        if st.button("🔓 DÉVERROUILLER"):
            if pwd == "2026":
                st.session_state.login = True
                st.rerun()
            else: st.error("Diso ny teny fanindry")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

st.markdown("<div class='main-title'>💎 MINES V8000 SHA256</div>", unsafe_allow_html=True)

col_in, col_out = st.columns([1, 1.6], gap="medium")

with col_in:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    srv = st.text_input("🔐 SERVER SEED SHA256", placeholder="b682668...")
    cli = st.text_input("👤 CLIENT SEED", placeholder="y4FU1V8...")
    non = st.number_input("🔢 NONCE", min_value=0, value=st.session_state.cur_nonce)
    min_count = st.selectbox("💣 MINES", options=[1, 3, 5, 24], index=1)
    
    if st.button("💎 KAJY EXACT"):
        if srv and cli:
            m_list, s_set, count = run_all_methods(srv, cli, non, min_count)
            # Fidio ny 5 diamants
            top5 = sorted(list(s_set))[:5] 
            st.session_state.result = {"top5": top5, "safe": s_set, "mines": m_list, "count": count}
            st.session_state.cur_nonce = non + 1
        else:
            st.warning("Fenoy ny banga")
    st.markdown("</div>", unsafe_allow_html=True)

with col_out:
    if st.session_state.result:
        res = st.session_state.result
        st.markdown(f"<div style='text-align:center'><span class='badge'>CONSENSUS: {res['count']}/4</span></div>", unsafe_allow_html=True)
        st.markdown(render_grid(res['top5'], res['safe'], res['mines']), unsafe_allow_html=True)
        st.markdown(f"<div class='d5box'><div class='d5nums'>{' - '.join(map(str, res['top5']))}</div></div>", unsafe_allow_html=True)
    else:
        st.info("Miandry ny kajy...")
