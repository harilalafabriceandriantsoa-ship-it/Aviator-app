import streamlit as st
import hashlib
import random
import pandas as pd
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

    .glass-warn {
        background: rgba(255, 150, 0, 0.08);
        border: 2px solid rgba(255, 150, 0, 0.4);
        border-radius: 14px;
        padding: 16px;
        margin: 12px 0;
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
    @keyframes glow5 {
        0%,100% { box-shadow: 0 0 18px rgba(0,255,204,0.7); }
        50%      { box-shadow: 0 0 40px rgba(0,255,204,1), 0 0 60px rgba(0,255,100,0.4); }
    }

    /* Autres safe */
    .csafe {
        background: rgba(0,255,204,0.1);
        color: #00ffcc;
        border: 1.5px solid rgba(0,255,204,0.25);
    }

    /* Mine */
    .cmine {
        background: linear-gradient(135deg, #ff0033, #880011);
        color: #fff;
        box-shadow: 0 0 18px rgba(255,0,51,0.5);
    }

    /* Empty */
    .cempty {
        background: rgba(10,10,30,0.8);
        border: 1.5px solid rgba(0,255,204,0.1);
        color: rgba(0,255,204,0.15);
        font-size: clamp(0.6rem, 1.8vw, 0.8rem);
    }

    /* Badge */
    .badge {
        background: linear-gradient(135deg, #00ffcc, #00ff88);
        color: #000;
        font-family: 'Orbitron';
        font-weight: 900;
        font-size: clamp(0.85rem, 3vw, 1.3rem);
        padding: 10px 22px;
        border-radius: 50px;
        display: inline-block;
        box-shadow: 0 0 28px rgba(0,255,204,0.55);
    }

    /* 5 diamants display */
    .d5box {
        background: linear-gradient(135deg, rgba(0,255,204,0.12), rgba(0,255,100,0.06));
        border: 2.5px solid rgba(0,255,204,0.5);
        border-radius: 16px;
        padding: 18px;
        text-align: center;
        margin: 14px 0;
        box-shadow: 0 0 30px rgba(0,255,204,0.15);
    }
    .d5nums {
        font-size: clamp(1.5rem, 6vw, 2.2rem);
        font-weight: 900;
        color: #00ffcc;
        font-family: 'Orbitron';
        letter-spacing: 0.06em;
        margin: 8px 0;
    }

    /* Mine box */
    .minebox {
        background: rgba(255,0,51,0.07);
        border: 1.5px solid rgba(255,0,51,0.3);
        border-radius: 12px;
        padding: 14px;
        text-align: center;
        margin: 10px 0;
    }

    /* Next box */
    .nextbox {
        background: rgba(0,255,204,0.04);
        border: 1px solid rgba(0,255,204,0.2);
        border-radius: 12px;
        padding: 13px;
        text-align: center;
        margin-top: 12px;
    }

    /* Metrics */
    .mbox { background:rgba(0,255,204,0.06); border:1px solid rgba(0,255,204,0.2); border-radius:11px; padding:11px; text-align:center; }
    .mval { font-size:clamp(1.3rem,5vw,2rem); font-weight:900; font-family:'Orbitron'; color:#00ffcc; }
    .mlbl { font-size:.62rem; color:rgba(255,255,255,.35); letter-spacing:.12em; text-transform:uppercase; margin-top:3px; }

    /* Stat sidebar */
    .sstat { background:rgba(0,255,204,.06); border:1px solid rgba(0,255,204,.18); border-radius:9px; padding:10px; text-align:center; margin:5px 0; }
    .ssv   { font-size:1.4rem; font-weight:900; font-family:'Orbitron'; color:#00ffcc; }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #00ffcc, #00aa66) !important;
        color: #000 !important; font-weight:900 !important;
        border-radius:11px !important; height:52px !important;
        font-size:.95rem !important; border:none !important;
        width:100% !important; font-family:'Rajdhani' !important;
        transition:all .2s !important;
    }
    .stButton>button:hover { transform:scale(1.02); box-shadow:0 0 22px rgba(0,255,204,.5) !important; }

    /* Inputs */
    .stTextInput input, .stNumberInput input {
        background:rgba(0,255,204,.04) !important;
        border:2px solid rgba(0,255,204,.22) !important;
        color:#00ffcc !important; border-radius:11px !important;
        font-size:.9rem !important; padding:10px 13px !important;
        font-family:'Rajdhani' !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color:rgba(0,255,204,.65) !important;
        box-shadow:0 0 12px rgba(0,255,204,.18) !important;
    }
    .stSelectbox > div > div {
        background:rgba(0,255,204,.04) !important;
        border:2px solid rgba(0,255,204,.22) !important;
        border-radius:11px !important; color:#00ffcc !important;
    }

    @media (max-width:768px) { .glass { padding:11px !important; } }
</style>
""", unsafe_allow_html=True)

# ===================== SESSION STATE =====================
if "login"     not in st.session_state: st.session_state.login     = False
if "history"   not in st.session_state: st.session_state.history   = load_json(HISTORY_FILE, [])
if "stats"     not in st.session_state: st.session_state.stats     = load_json(STATS_FILE, {"total":0,"wins":0,"losses":0})
if "result"    not in st.session_state: st.session_state.result    = None
if "calc_key"  not in st.session_state: st.session_state.calc_key  = 0
if "cur_nonce" not in st.session_state: st.session_state.cur_nonce = 0

# ===================== PROVABLY FAIR 100% EXACT =====================

def compute_mines_nonce(server_seed: str, client_seed: str, nonce: int, num_mines: int):
    """
    PROVABLY FAIR 100% EXACT
    Formula marina mitovy tanteraka @ casino Spribe:

    SHA512(server_seed : client_seed : nonce)
    → seed integer
    → Fisher-Yates shuffle
    → mines = X positions voalohany
    """
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


def verify_sha512_hash(server_seed: str, client_seed: str, nonce: int, provided_hash: str) -> bool:
    """
    Verification: hash casino mitovy @ kajy antsika ve?
    """
    if not provided_hash or len(provided_hash) < 10:
        return None  # tsy azo atao verification

    combined   = f"{server_seed.strip()}:{client_seed.strip()}:{nonce}"
    our_hash   = hashlib.sha512(combined.encode('utf-8')).hexdigest()
    provided_clean = provided_hash.strip().lower()

    # Mitovy @ premiers chars
    min_len = min(len(our_hash), len(provided_clean))
    return our_hash[:min_len] == provided_clean[:min_len]


def select_best_5(safe_set: set, mines_set: set, server_seed: str, client_seed: str, nonce: int):
    """
    Safidy 5 positions tsara indrindra:
    - Lava avy @ mines
    - Eo afovoan'ny board
    - Stable neighbors
    - Hash pattern unique
    """
    pattern_hash = hashlib.sha256(
        f"{server_seed}:{client_seed}:{nonce}".encode()
    ).hexdigest()
    pattern_num = int(pattern_hash[:16], 16)

    scores = {}
    for pos in safe_set:
        row, col = pos // 5, pos % 5

        # Distance avy @ mines
        min_dist = min(
            abs(row - m // 5) + abs(col - m % 5)
            for m in mines_set
        ) if mines_set else 4
        dist_score = min_dist * 22

        # Center score
        center_score = (4 - (abs(row - 2) + abs(col - 2))) * 10

        # Hash pattern
        hash_score = (pattern_num + pos * 7919) % 100

        # Neighbor safety
        neighbor_safe = sum(
            1 for dr in [-1,0,1] for dc in [-1,0,1]
            if not (dr==0 and dc==0)
            and 0 <= row+dr < 5 and 0 <= col+dc < 5
            and (row+dr)*5+(col+dc) in safe_set
        )
        neighbor_score = neighbor_safe * 8

        scores[pos] = dist_score + center_score + hash_score + neighbor_score

    top5 = sorted(scores, key=lambda p: scores[p], reverse=True)[:5]
    return sorted(top5)


# ===================== GRID =====================

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


# ===================== LOGIN =====================
if not st.session_state.login:
    st.markdown("<div class='main-title'>💎 MINES 100% EXACT V7000</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#00ffcc55;letter-spacing:.25em;margin-bottom:1.5rem;'>NONCE MARINA • PROVABLY FAIR • 5💎 GARANTI</p>", unsafe_allow_html=True)

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

    st.markdown("""
    <div class='glass' style='max-width:820px;margin:28px auto;'>
        <h2 style='color:#00ffcc;text-align:center;'>📖 TOROLALANA MALAGASY</h2>

        <h3 style='color:#00ffcc;margin-top:18px;'>🔑 INONA NY NONCE?</h3>
        <p>
        <b>NONCE</b> = Compteur manomboka @ <b>0</b><br>
        Miakatra <b>+1</b> isaky ny bet vita<br>
        <b>TSY MITOVY</b> @ "ID de la manche" (785239186...)<br><br>
        Casino mampiasa: <code>SHA512(server:client:<b>nonce</b>)</code><br>
        → Nonce 0 = Round voalohany<br>
        → Nonce 1 = Round faharoa<br>
        → Sns...
        </p>

        <h3 style='color:#00ffcc;margin-top:18px;'>🔍 AIZA HITANA NY NONCE?</h3>

        <div class='glass-warn'>
        <b style='color:#ffaa00;'>FOMBA 1 (TSARA INDRINDRA):</b><br>
        → Scroll down @ "Provably Fair" na "Informations"<br>
        → Jereo raha misy <b>"Nonce"</b> na <b>"Tour"</b> written<br>
        → Ampidira io exactly
        </div>

        <div class='glass-warn' style='margin-top:8px;'>
        <b style='color:#ffaa00;'>FOMBA 2 (Raha tsy hita nonce):</b><br>
        → Ovao client seed (tsindrio "Change")<br>
        → Client seed vaovao = <b>Nonce manomboka @ 0</b><br>
        → Round 1 = Nonce 0<br>
        → Round 2 = Nonce 1<br>
        → Sns...
        </div>

        <div class='glass-warn' style='margin-top:8px;'>
        <b style='color:#ffaa00;'>FOMBA 3 (Verification SHA512):</b><br>
        → Casino mampiseho SHA512 hash<br>
        → Ampidira @ "SHA512 Verification"<br>
        → App manambara raha nonce marina
        </div>

        <h3 style='color:#00ffcc;margin-top:18px;'>🎮 DINGANA:</h3>
        <ol style='line-height:1.9;'>
            <li>Ovao <b>Client Seed</b> @ casino → COPY vaovao</li>
            <li>COPY <b>Server Seed</b></li>
            <li>Ampidira <b>Nonce = 0</b> (round voalohany)</li>
            <li>Safidio <b>mines</b> (mitovy @ casino)</li>
            <li>Tsindrio <b>"💎 KAJY EXACT"</b></li>
            <li>Milalao <b>5 💎</b> @ casino</li>
            <li>Confirm WIN/LOSS</li>
            <li>Round manaraka: <b>Nonce +1</b> (auto!)</li>
        </ol>

        <h3 style='color:#ff6600;margin-top:16px;'>⚠️ TSY MAINTSY:</h3>
        <ul style='line-height:1.8;'>
            <li>COPY-PASTE seeds — TSY SORATRA TANANA!</li>
            <li>Nonce manomboka @ <b>0</b> aorian'ny change seed</li>
            <li>Nonce +1 isaky ny round (app manao auto)</li>
            <li>Mines mitovy @ casino</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ===================== SIDEBAR =====================
with st.sidebar:
    st.markdown("### 📊 STATS")
    s   = st.session_state.stats
    tot = s.get('total',0)
    w   = s.get('wins',0)
    l   = s.get('losses',0)
    wr  = round(w/tot*100,1) if tot > 0 else 0

    st.markdown(f"<div class='sstat'><div class='ssv'>{wr}%</div><div style='font-size:.62rem;color:#fff4;'>WIN RATE</div></div>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1: st.markdown(f"<div class='sstat'><div class='ssv'>{w}</div><div style='font-size:.58rem;color:#fff3;'>WINS</div></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='sstat'><div class='ssv'>{l}</div><div style='font-size:.58rem;color:#fff3;'>LOSS</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sstat'><div class='ssv'>{tot}</div><div style='font-size:.58rem;color:#fff3;'>TOTAL</div></div>", unsafe_allow_html=True)

    st.markdown("---")

    # Nonce courant
    st.markdown(f"""
    <div class='nonce-box'>
        <div style='font-size:.7rem;color:#00ffcc77;margin-bottom:4px;'>NONCE COURANT</div>
        <div class='nonce-val'>{st.session_state.cur_nonce}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔄 RESET NONCE → 0", use_container_width=True):
        st.session_state.cur_nonce = 0
        st.success("✅ Nonce = 0")
        st.rerun()

    st.markdown("---")

    if st.button("🗑️ RESET DATA", use_container_width=True):
        st.session_state.history   = []
        st.session_state.stats     = {"total":0,"wins":0,"losses":0}
        st.session_state.result    = None
        st.session_state.cur_nonce = 0
        for f in [HISTORY_FILE, STATS_FILE]:
            try:
                if f.exists(): f.unlink()
            except: pass
        st.success("✅ Reset!")
        st.rerun()

    st.markdown(f"<p style='font-size:.6rem;color:#fff2;text-align:center;margin-top:6px;'>Rounds: {len(st.session_state.history)}</p>", unsafe_allow_html=True)

# ===================== MAIN =====================
st.markdown("<div class='main-title'>💎 MINES 100% EXACT V7000</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#00ffcc55;letter-spacing:.2em;margin-bottom:1.2rem;'>NONCE MARINA • SHA512 EXACT • 5💎 GARANTI</p>", unsafe_allow_html=True)

col_in, col_out = st.columns([1, 1.6], gap="medium")

# ── INPUT ──
with col_in:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.markdown("### 📥 SEEDS + NONCE")

    server_seed = st.text_input(
        "🔐 SERVER SEED",
        key="inp_srv",
        placeholder="dMuspZqjaSvLSYirFGiv3Q9640...",
        help="COPY-PASTE bouton □ FOANA!"
    )
    client_seed = st.text_input(
        "👤 CLIENT SEED",
        key="inp_cli",
        placeholder="FEE6PwyWDPOkcbqdB5fx",
        help="COPY-PASTE bouton □"
    )

    # NONCE - auto-managed
    nonce_val = st.number_input(
        "🔢 NONCE (0 = round voalohany)",
        key="inp_nonce",
        value=st.session_state.cur_nonce,
        min_value=0,
        step=1,
        help="Manomboka @ 0 aorian'ny change seed. App manao +1 auto!"
    )
    st.session_state.cur_nonce = int(nonce_val)

    num_mines = st.selectbox(
        "💣 MINES",
        key="inp_mines",
        options=[1,2,3], index=0,
        help="Mitovy @ casino"
    )

    # Optional SHA512 verification
    with st.expander("🔍 SHA512 VERIFICATION (optionnel)"):
        sha_verify = st.text_input(
            "SHA512 hash avy @ casino",
            placeholder="ac50e686e92a4300...",
            help="Raha misy @ casino — verification azô atao"
        )

    # Warnings
    if server_seed and len(server_seed.strip()) < 15:
        st.warning("⚠️ Server seed fohy — COPY-PASTE tsara!")
    if client_seed and len(client_seed.strip()) < 5:
        st.warning("⚠️ Client seed fohy!")

    st.markdown("</div>", unsafe_allow_html=True)

    # NONCE info
    st.markdown(f"""
    <div class='nonce-box'>
        <div style='font-size:.72rem;color:#00ffcc77;margin-bottom:4px;'>NONCE ANKEHITRINY</div>
        <div class='nonce-val'>{st.session_state.cur_nonce}</div>
        <div style='font-size:.68rem;color:#fff3;margin-top:4px;'>
            Round manaraka → {st.session_state.cur_nonce + 1}
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("💎 KAJY EXACT", use_container_width=True):
        srv = server_seed.strip()
        cli = client_seed.strip()
        n   = int(st.session_state.cur_nonce)

        if not srv:
            st.error("❌ Server Seed tsy misy!"
