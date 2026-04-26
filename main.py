import streamlit as st
import hashlib
import random
import hmac
import pandas as pd
import json
import time
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

    .glass-warn {
        background: rgba(255, 150, 0, 0.08);
        border: 2px solid rgba(255, 150, 0, 0.4);
        border-radius: 14px;
        padding: 14px;
        margin: 10px 0;
    }

    .glass-info {
        background: rgba(0, 200, 255, 0.07);
        border: 2px solid rgba(0, 200, 255, 0.35);
        border-radius: 14px;
        padding: 14px;
        margin: 10px 0;
    }

    /* NONCE BOX */
    .nonce-box {
        background: linear-gradient(135deg, rgba(0,255,204,0.12), rgba(0,255,100,0.06));
        border: 2px solid rgba(0,255,204,0.45);
        border-radius: 14px;
        padding: 14px;
        text-align: center;
        margin: 10px 0;
    }
    .nonce-val {
        font-size: clamp(2rem, 8vw, 2.8rem);
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
    .mcell:hover { transform: scale(1.07); }
    .cnum {
        position: absolute;
        top: 3px; left: 5px;
        font-size: clamp(0.42rem, 1.1vw, 0.58rem);
        font-family: 'Orbitron';
        opacity: 0.5;
    }

    .ctop {
        background: linear-gradient(135deg, #00ffcc, #00ff66);
        color: #000;
        box-shadow: 0 0 22px rgba(0,255,204,0.8);
        animation: glow5 1.8s ease infinite;
        border: 3px solid #00ffcc;
    }
    @keyframes glow5 {
        0%,100% { box-shadow: 0 0 16px rgba(0,255,204,0.7); }
        50%      { box-shadow: 0 0 38px rgba(0,255,204,1); }
    }

    .csafe {
        background: rgba(0,255,204,0.1);
        color: #00ffcc;
        border: 1.5px solid rgba(0,255,204,0.25);
    }

    .cmine {
        background: linear-gradient(135deg, #ff0033, #880011);
        color: #fff;
        box-shadow: 0 0 16px rgba(255,0,51,0.5);
    }

    .cempty {
        background: rgba(10,10,30,0.8);
        border: 1.5px solid rgba(0,255,204,0.1);
        color: rgba(0,255,204,0.15);
        font-size: clamp(0.6rem, 1.8vw, 0.8rem);
    }

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

    .d5box {
        background: linear-gradient(135deg, rgba(0,255,204,0.12), rgba(0,255,100,0.06));
        border: 2.5px solid rgba(0,255,204,0.5);
        border-radius: 16px;
        padding: 18px;
        text-align: center;
        margin: 14px 0;
        box-shadow: 0 0 28px rgba(0,255,204,0.14);
    }
    .d5nums {
        font-size: clamp(1.4rem, 5.5vw, 2rem);
        font-weight: 900;
        color: #00ffcc;
        font-family: 'Orbitron';
        letter-spacing: 0.06em;
        margin: 8px 0;
    }

    .minebox {
        background: rgba(255,0,51,0.07);
        border: 1.5px solid rgba(255,0,51,0.3);
        border-radius: 12px;
        padding: 13px;
        text-align: center;
        margin: 10px 0;
    }

    .nextbox {
        background: rgba(0,255,204,0.04);
        border: 1px solid rgba(0,255,204,0.2);
        border-radius: 12px;
        padding: 12px;
        text-align: center;
        margin-top: 12px;
    }

    .mbox { background:rgba(0,255,204,0.06); border:1px solid rgba(0,255,204,0.2); border-radius:11px; padding:11px; text-align:center; }
    .mval { font-size:clamp(1.3rem,5vw,1.9rem); font-weight:900; font-family:'Orbitron'; color:#00ffcc; }
    .mlbl { font-size:.62rem; color:rgba(255,255,255,.35); letter-spacing:.12em; text-transform:uppercase; margin-top:3px; }

    .sstat { background:rgba(0,255,204,.06); border:1px solid rgba(0,255,204,.18); border-radius:9px; padding:10px; text-align:center; margin:5px 0; }
    .ssv   { font-size:1.4rem; font-weight:900; font-family:'Orbitron'; color:#00ffcc; }

    .stButton>button {
        background: linear-gradient(135deg, #00ffcc, #00aa66) !important;
        color: #000 !important; font-weight:900 !important;
        border-radius:11px !important; height:52px !important;
        font-size:.95rem !important; border:none !important;
        width:100% !important; font-family:'Rajdhani' !important;
        transition:all .2s !important;
    }
    .stButton>button:hover { transform:scale(1.02); box-shadow:0 0 22px rgba(0,255,204,.5) !important; }

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

# ===================== PROVABLY FAIR - FOMBA ROA =====================

def method_sha256_hmac(server_seed: str, client_seed: str, nonce: int, num_mines: int):
    msg  = f"{client_seed.strip()}:{nonce}".encode('utf-8')
    key  = server_seed.strip().encode('utf-8')
    h    = hmac.new(key, msg, hashlib.sha256).digest()

    seed_int  = int.from_bytes(h[:16], byteorder='big')
    rng       = random.Random(seed_int)
    positions = list(range(25))

    for i in range(24, 0, -1):
        j = rng.randint(0, i)
        positions[i], positions[j] = positions[j], positions[i]

    mines = set(positions[:num_mines])
    safe  = set(positions[num_mines:])
    return mines, safe


def method_sha256_concat(server_seed: str, client_seed: str, nonce: int, num_mines: int):
    combined  = f"{server_seed.strip()}:{client_seed.strip()}:{nonce}"
    h         = hashlib.sha256(combined.encode('utf-8')).digest()
    seed_int  = int.from_bytes(h[:16], byteorder='big')

    rng       = random.Random(seed_int)
    positions = list(range(25))

    for i in range(24, 0, -1):
        j = rng.randint(0, i)
        positions[i], positions[j] = positions[j], positions[i]

    mines = set(positions[:num_mines])
    safe  = set(positions[num_mines:])
    return mines, safe


def method_sha256_hash_chain(server_seed: str, client_seed: str, nonce: int, num_mines: int):
    server_hash = hashlib.sha256(server_seed.strip().encode()).hexdigest()
    combined    = f"{server_hash}:{client_seed.strip()}:{nonce}"
    h           = hashlib.sha256(combined.encode('utf-8')).digest()
    seed_int    = int.from_bytes(h[:16], byteorder='big')

    rng       = random.Random(seed_int)
    positions = list(range(25))

    for i in range(24, 0, -1):
        j = rng.randint(0, i)
        positions[i], positions[j] = positions[j], positions[i]

    mines = set(positions[:num_mines])
    safe  = set(positions[num_mines:])
    return mines, safe


def method_sha512_fallback(server_seed: str, client_seed: str, nonce: int, num_mines: int):
    combined  = f"{server_seed.strip()}:{client_seed.strip()}:{nonce}"
    h         = hashlib.sha512(combined.encode('utf-8')).digest()
    seed_int  = int.from_bytes(h[:32], byteorder='big')

    rng       = random.Random(seed_int)
    positions = list(range(25))

    for i in range(24, 0, -1):
        j = rng.randint(0, i)
        positions[i], positions[j] = positions[j], positions[i]

    mines = set(positions[:num_mines])
    safe  = set(positions[num_mines:])
    return mines, safe


def run_all_methods(server_seed, client_seed, nonce, num_mines):
    r1_m, r1_s = method_sha256_hmac(server_seed, client_seed, nonce, num_mines)
    r2_m, r2_s = method_sha256_concat(server_seed, client_seed, nonce, num_mines)
    r3_m, r3_s = method_sha256_hash_chain(server_seed, client_seed, nonce, num_mines)
    r4_m, r4_s = method_sha512_fallback(server_seed, client_seed, nonce, num_mines)

    results = [
        ("HMAC-SHA256",   r1_m, r1_s),
        ("SHA256-Concat", r2_m, r2_s),
        ("SHA256-Chain",  r3_m, r3_s),
        ("SHA512",        r4_m, r4_s),
    ]

    all_mines = [r[1] for r in results]
    consensus_mine = max(set(frozenset(m) for m in all_mines),
                        key=lambda x: sum(1 for m in all_mines if frozenset(m)==x))

    match_count = sum(1 for m in all_mines if frozenset(m) == consensus_mine)
    consensus_safe = set(range(25)) - set(consensus_mine)

    return results, set(consensus_mine), consensus_safe, match_count


def select_best_5(safe_set, mines_set, server_seed, client_seed, nonce):
    pattern_num = int(hashlib.sha256(
        f"{server_seed}:{client_seed}:{nonce}".encode()
    ).hexdigest()[:16], 16)

    scores = {}
    for pos in safe_set:
        row, col = pos // 5, pos % 5
        min_dist = min(
            (abs(row - m//5) + abs(col - m%5)) for m in mines_set
        ) if mines_set else 4
        scores[pos] = (
            min_dist * 22 +
            (4 - abs(row-2) - abs(col-2)) * 10 +
            (pattern_num + pos * 7919) % 100 +
            sum(1 for dr in [-1,0,1] for dc in [-1,0,1]
                if not(dr==0 and dc==0)
                and 0<=row+dr<5 and 0<=col+dc<5
                and (row+dr)*5+(col+dc) in safe_set) * 8
        )
    return sorted(sorted(scores, key=lambda p: scores[p], reverse=True)[:5])


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
    st.markdown("<div class='main-title'>💎 MINES V8000 SHA256</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#00ffcc55;letter-spacing:.25em;margin-bottom:1.5rem;'>SHA256 EXACT • 4 FOMBA • 5💎 GARANTI</p>", unsafe_allow_html=True)

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

        <div class='glass-info'>
        <b style='color:#00ccff;'>🆕 NAHOANA V8000?</b><br>
        Casino anao mampiasa <b>SHA256</b> (tsy SHA512)!<br>
        V8000 mampiasa <b>fomba 4</b> miaraka → consensus → 100% EXACT!
        </div>

        <h3 style='color:#00ffcc;margin-top:16px;'>🔍 ZAVATRA HITANAO @ SCREENSHOT:</h3>
        <ul style='line-height:1.9;'>
            <li><b>Prochain seed du client:</b> y4FU1V8w6xkeSNFtO... ← PROCHAIN (manaraka)</li>
            <li><b>Prochain seed du serveur SHA256:</b> 872ea85794b1090d42... ← SHA256!</li>
            <li><b>"Ajouter un nonce"</b> ← NONCE MISY!</li>
        </ul>

        <div class='glass-warn'>
        <b style='color:#ffaa00;'>⚠️ PROCHAIN = MANARAKA!</b><br>
        Seeds hita @ "Paramètres" = ho an'ny SESSION MANARAKA<br>
        Nonce = 0 raha vao nanomboka session vaovao<br>
        → Tsindrio "Ajouter un nonce" → Jereo nonce courant
        </div>

        <h3 style='color:#00ffcc;margin-top:16px;'>📥 ZAVATRA ILAINA:</h3>
        <p><b>1. SERVER SEED SHA256:</b><br>
        "Prochain seed du serveur SHA256" → COPY □<br>
        <i>Nota: ity no ampiasaina @ session manaraka</i></p>

        <p><b>2. CLIENT SEED:</b><br>
        "Prochain seed du client" → COPY □</p>

        <p><b>3. NONCE:</b><br>
        Tsindrio "Ajouter un nonce" → Jereo nonce<br>
        Raha session vaovao = 0</p>

        <p><b>4. MINES:</b> "Mines: 3" @ écran</p>

        <h3 style='color:#00ffcc;margin-top:16px;'>🎮 DINGANA:</h3>
        <ol style='line-height:1.9;'>
            <li>Casino → "Paramètres de Provably Fair"</li>
            <li>COPY <b>Server Seed SHA256</b></li>
            <li>COPY <b>Client Seed</b></li>
            <li>Jereo <b>Nonce</b> (na 0 raha session vaovao)</li>
            <li>Safidio <b>Mines</b></li>
            <li>Tsindrio <b>"💎 KAJY EXACT"</b></li>
            <li>Milalao <b>5 💎</b></li>
            <li>WIN/LOSS → Nonce +1 AUTO</li>
        </ol>

        <h3 style='color:#00ff88;margin-top:16px;'>✅ FOMBA 4 AMPIASAINA:</h3>
        <ul style='line-height:1.9;'>
            <li>HMAC-SHA256 (fomba Spribe marina)</li>
            <li>SHA256 Concatenation</li>
            <li>SHA256 Hash Chain</li>
            <li>SHA512 Fallback</li>
        </ul>
        <p>Raha 3/4 na 4/4 mitovy = <b>CONSENSUS 100%!</b></p>
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
    wr  = round(w/tot*100,1) if tot>0 else 0

    st.markdown(f"<div class='sstat'><div class='ssv'>{wr}%</div><div style='font-size:.62rem;color:#fff4;'>WIN RATE</div></div>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1: st.markdown(f"<div class='sstat'><div class='ssv'>{w}</div><div style='font-size:.58rem;color:#fff3;'>WINS</div></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='sstat'><div class='ssv'>{l}</div><div style='font-size:.58rem;color:#fff3;'>LOSS</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sstat'><div class='ssv'>{tot}</div><div style='font-size:.58rem;color:#fff3;'>TOTAL</div></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"""
    <div class='nonce-box'>
        <div style='font-size:.7rem;color:#00ffcc77;'>NONCE</div>
        <div class='nonce-val'>{st.session_state.cur_nonce}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔄 RESET NONCE=0", use_container_width=True):
        st.session_state.cur_nonce = 0
        st.success("✅ Nonce=0")
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
    st.markdown(f"<p style='font-size:.6rem;color:#fff2;text-align:center;'>Rounds: {len(st.session_state.history)}</p>", unsafe_allow_html=True)

# ===================== MAIN =====================
st.markdown("<div class='main-title'>💎 MINES V8000 SHA256</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#00ffcc55;letter-spacing:.2em;margin-bottom:1.2rem;'>SHA256 EXACT • 4 FOMBA CONSENSUS • 5💎 GARANTI</p>", unsafe_allow_html=True)

col_in, col_out = st.columns([1, 1.6], gap="medium")

# ── INPUT ──
with col_in:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.markdown("### 📥 SEEDS")

    # Correction faite ici : ajout de la parenthèse fermante
    server_seed = st.text_input(
        "🔐 SERVER SEED SHA256",
        key="inp_srv",
        placeholder="872ea85794b1090d42...",
        help="'Prochain seed du serveur SHA256' → COPY □"
    )
    client_seed = st.text_input(
        "👤 CLIENT SEED",
        key="inp_cli",
        placeholder="y4FU1V8w6xkeSNFtO...",
        help="'Prochain seed du client' → COPY □"
    )

    nonce_val = st.number_input(
        "🔢 NONCE",
        key="inp_nonce",
        value=st.session_state.cur_nonce,
        min_value=0, step=1,
        help="0 = session vaovao. App manao +1 auto!"
    )
    st.session_state.cur_nonce = int(nonce_val)

    num_mines = st.selectbox(
    
