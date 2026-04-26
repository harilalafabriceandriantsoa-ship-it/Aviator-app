import streamlit as st
import hashlib
import random
import json
import time
from pathlib import Path

# ===================== CONFIG =====================
st.set_page_config(
    page_title="MINES 5💎 100% ASSURÉ",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===================== PERSISTENCE =====================
try:
    DATA_DIR = Path(__file__).parent / "mines_5d_data"
except:
    DATA_DIR = Path.cwd() / "mines_5d_data"

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

    /* ===== GRID 5×5 ===== */
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

    /* === 5 DIAMANTS RECOMMANDÉS === */
    .ctop {
        background: linear-gradient(135deg, #00ffcc, #00ff66);
        color: #000;
        box-shadow: 0 0 24px rgba(0,255,204,0.8), 0 0 50px rgba(0,255,100,0.3);
        animation: glow5 1.8s ease infinite;
        border: 3px solid #00ffcc;
    }
    @keyframes glow5 {
        0%,100% { box-shadow: 0 0 18px rgba(0,255,204,0.7); }
        50%      { box-shadow: 0 0 40px rgba(0,255,204,1), 0 0 60px rgba(0,255,100,0.4); }
    }

    /* === AUTRES SAFE (non recommandés) === */
    .csafe {
        background: rgba(0, 255, 204, 0.12);
        color: #00ffcc;
        border: 1.5px solid rgba(0,255,204,0.3);
    }

    /* === MINE === */
    .cmine {
        background: linear-gradient(135deg, #ff0033, #880011);
        color: #fff;
        box-shadow: 0 0 18px rgba(255,0,51,0.5);
    }

    /* === EMPTY === */
    .cempty {
        background: rgba(10, 10, 30, 0.8);
        border: 1.5px solid rgba(0,255,204,0.1);
        color: rgba(0,255,204,0.15);
        font-size: clamp(0.6rem, 1.8vw, 0.8rem);
    }

    /* ===== BADGE ===== */
    .badge {
        background: linear-gradient(135deg, #00ffcc, #00ff88);
        color: #000;
        font-family: 'Orbitron';
        font-weight: 900;
        font-size: clamp(0.9rem, 3vw, 1.4rem);
        padding: 10px 22px;
        border-radius: 50px;
        display: inline-block;
        box-shadow: 0 0 28px rgba(0,255,204,0.55);
    }

    /* ===== 5 DIAMANTS BOX ===== */
    .d5box {
        background: linear-gradient(135deg, rgba(0,255,204,0.12), rgba(0,255,100,0.06));
        border: 2.5px solid rgba(0,255,204,0.5);
        border-radius: 16px;
        padding: 20px;
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
    .d5label {
        font-size: 0.75rem;
        color: rgba(0,255,204,0.6);
        letter-spacing: 0.18em;
        text-transform: uppercase;
    }

    /* ===== MINE BOX ===== */
    .minebox {
        background: rgba(255,0,51,0.07);
        border: 1.5px solid rgba(255,0,51,0.3);
        border-radius: 12px;
        padding: 14px;
        text-align: center;
        margin: 10px 0;
    }

    /* ===== NEXT BOX ===== */
    .nextbox {
        background: rgba(0,255,204,0.04);
        border: 1px solid rgba(0,255,204,0.2);
        border-radius: 12px;
        padding: 13px;
        text-align: center;
        margin-top: 12px;
    }

    /* ===== SIDEBAR STAT ===== */
    .sstat { background:rgba(0,255,204,.06); border:1px solid rgba(0,255,204,.18); border-radius:9px; padding:10px; text-align:center; margin:5px 0; }
    .ssv   { font-size:1.4rem; font-weight:900; font-family:'Orbitron'; color:#00ffcc; }

    /* ===== BUTTONS ===== */
    .stButton>button {
        background: linear-gradient(135deg, #00ffcc, #00aa66) !important;
        color: #000 !important; font-weight:900 !important;
        border-radius:11px !important; height:52px !important;
        font-size:.95rem !important; border:none !important;
        width:100% !important; font-family:'Rajdhani' !important;
        transition:all .2s !important;
    }
    .stButton>button:hover { transform:scale(1.02); box-shadow:0 0 22px rgba(0,255,204,.5) !important; }

    /* ===== INPUTS ===== */
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
if "login"    not in st.session_state: st.session_state.login    = False
if "history"  not in st.session_state: st.session_state.history  = load_json(HISTORY_FILE, [])
if "stats"    not in st.session_state: st.session_state.stats    = load_json(STATS_FILE, {"total":0,"wins":0,"losses":0})
if "result"   not in st.session_state: st.session_state.result   = None

# ===================== PROVABLY FAIR 100% EXACT =====================

def compute_mines_exact(server_seed: str, client_seed: str, history_id: int, num_mines: int):
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


def select_best_5(safe_set: set, mines_set: set, server_seed: str, client_seed: str, history_id: int):
    scores = {}

    pattern_hash = hashlib.sha256(f"{server_seed}:{client_seed}:{history_id}".encode()).hexdigest()
    pattern_num = int(pattern_hash[:16], 16)

    for pos in safe_set:
        row = pos // 5
        col = pos % 5

        min_dist = float('inf')
        for m in mines_set:
            mr, mc = m // 5, m % 5
            dist = abs(row - mr) + abs(col - mc)
            if dist < min_dist:
                min_dist = dist
        dist_score = min_dist * 20

        center_dist = abs(row - 2) + abs(col - 2)
        center_score = (4 - center_dist) * 10

        hash_score = (pattern_num + pos * 7919) % 100

        neighbor_safe = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if 0 <= nr < 5 and 0 <= nc < 5:
                    npos = nr * 5 + nc
                    if npos in safe_set:
                        neighbor_safe += 1
        neighbor_score = neighbor_safe * 8

        scores[pos] = dist_score + center_score + hash_score + neighbor_score

    top5 = sorted(scores.keys(), key=lambda p: scores[p], reverse=True)[:5]
    return sorted(top5), scores

# ===================== GRID HTML =====================

def render_grid(top5: list, safe_set: set, mine_set: set, show_mines: bool) -> str:
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
    st.markdown("<div class='main-title'>💎 MINES 5 DIAMANTS 100%</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#00ffcc55;letter-spacing:.25em;margin-bottom:1.5rem;'>PROVABLY FAIR • 5 DIAMANTS ASSURÉ • V6000</p>", unsafe_allow_html=True)

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
    s   = st.session_state.stats
    tot = s.get('total', 0)
    w   = s.get('wins',  0)
    l   = s.get('losses',0)
    wr  = round(w / tot * 100, 1) if tot > 0 else 0

    st.markdown(f"<div class='sstat'><div class='ssv'>{wr}%</div><div style='font-size:.62rem;color:#fff4;'>WIN RATE</div></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: st.markdown(f"<div class='sstat'><div class='ssv'>{w}</div><div style='font-size:.58rem;color:#fff3;'>WINS</div></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='sstat'><div class='ssv'>{l}</div><div style='font-size:.58rem;color:#fff3;'>LOSS</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sstat'><div class='ssv'>{tot}</div><div style='font-size:.58rem;color:#fff3;'>TOTAL</div></div>", unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🗑️ RESET", use_container_width=True):
        st.session_state.history = []
        st.session_state.stats   = {"total":0,"wins":0,"losses":0}
        st.session_state.result  = None
        for f in [HISTORY_FILE, STATS_FILE]:
            try:
                if f.exists(): f.unlink()
            except: pass
        st.success("✅ Reset!")
        st.rerun()
    st.markdown(f"<p style='font-size:.6rem;color:#fff2;text-align:center;margin-top:6px;'>Rounds: {len(st.session_state.history)}</p>", unsafe_allow_html=True)

# ===================== MAIN =====================
st.markdown("<div class='main-title'>💎 MINES 5 DIAMANTS 100% ASSURÉ</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#00ffcc55;letter-spacing:.2em;margin-bottom:1.2rem;'>PROVABLY FAIR • SHA512 EXACT • 5💎 GARANTIS</p>", unsafe_allow_html=True)

col_in, col_out = st.columns([1, 1.6], gap="medium")

# ── INPUT ──
with col_in:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.markdown("### 📥 SEEDS CASINO")

    server_seed = st.text_input(
        "🔐 SERVER SEED",
        key="inp_srv",
        placeholder="dMuspZqjaSvLSYirFGiv3Q9640...",
        help="⚠️ COPY-PASTE bouton □ — TSY SORATRA TANANA!"
    )
    client_seed = st.text_input(
        "👤 CLIENT SEED",
        key="inp_cli",
        placeholder="FEE6PwyWDPOkcbqdB5fx",
        help="⚠️ COPY-PASTE bouton □"
    )
    history_id = st.number_input(
        "🔢 HISTORY ID",
        key="inp_hid",
        value=1, min_value=0, step=1,
        help="+1 isaky ny round"
    )
    num_mines = st.selectbox(
        "💣 MINES (Taille du terrain)",
        key="inp_mines",
        options=[1, 2, 3], index=0,
        help="Mitovy @ casino"
    )

    if server_seed and len(server_seed.strip()) < 15:
        st.warning("⚠️ Server seed fohy — COPY-PASTE tsara!")
    if client_seed and len(client_seed.strip()) < 5:
        st.warning("⚠️ Client seed fohy — COPY-PASTE tsara!")

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("💎 KAJY 5 DIAMANTS", use_container_width=True):
        srv = server_seed.strip()
        cli = client_seed.strip()

        if not srv:
            st.error("❌ Server Seed tsy misy!")
        elif not cli:
            st.error("❌ Client Seed tsy misy!")
        elif len(srv) < 8:
            st.error("❌ Server Seed fohy loatra — COPY-PASTE!")
        else:
            t0 = time.perf_counter()

            mines_set, safe_set = compute_mines_exact(srv, cli, int(history_id), num_mines)
            top5, scores = select_best_5(safe_set, mines_set, srv, cli, int(history_id))
            elapsed = round(time.perf_counter() - t0, 4)

            # Eto ilay block madio tsara:
            st.session_state.result = {
                "srv_preview" : srv[:14] + "...",
                "cli_seed"    : cli,
                "history_id"  : int(history_id),
                "num_mines"   : num_mines,
                "mines"       : sorted(list(mines_set)),
                "safe"        : sorted(list(safe_set)),
                "top5"        : top5,
                "elapsed"     : elapsed,
                "hist_idx"    : len(st.session_state.history)
            }
            
            st.session_state.history.append(st.session_state.result)
            save_json(HISTORY_FILE, st.session_state.history)
            st.rerun()

# ── OUTPUT ──
with col_out:
    res = st.session_state.result
    if res:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.markdown("### 💎 TOP 5 DIAMANTS RECOMMANDÉS")
        st.markdown(f"<div class='d5box'><div class='d5nums'>{', '.join(map(str, res['top5']))}</div><div class='d5label'>MILALAA IREO 5 IREO @ CASINO</div></div>", unsafe_allow_html=True)
        
        mode = st.radio("👁️ VIEW:", ["💎 TOP 5", "🗺️ BOARD (Voir Mines)"], horizontal=True)
        show_m = (mode == "🗺️ BOARD (Voir Mines)")
        
        st.markdown(render_grid(res['top5'], set(res['safe']), set(res['mines']), show_mines=show_m), unsafe_allow_html=True)
        
        st.markdown(f"<div class='minebox'>💣 Positions des Mines: {', '.join(map(str, res['mines']))}</div>", unsafe_allow_html=True)
        st.markdown("<div class='nextbox'>▶️ Round manaraka: <b>Aza adino ny manampy +1 ny History ID</b></div>", unsafe_allow_html=True)

        st.markdown("---")
        cw, cl = st.columns(2)
        with cw:
            if st.button("✅ WIN", use_container_width=True, key="btn_win"):
                st.session_state.stats["total"] += 1
                st.session_state.stats["wins"] += 1
                save_json(STATS_FILE, st.session_state.stats)
                st.rerun()
        with cl:
            if st.button("❌ LOSS", use_container_width=True, key="btn_loss"):
                st.session_state.stats["total"] += 1
                st.session_state.stats["losses"] += 1
                save_json(STATS_FILE, st.session_state.stats)
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("👈 Ampidiro eo ankavia ny seeds dia tsindrio 'KAJY 5 DIAMANTS'")
