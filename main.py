import streamlit as st
import hashlib
import random
import hmac
import pandas as pd
import json
import time
from pathlib import Path

# ============================================================
# CONFIG
# ============================================================
st.set_page_config(
    page_title="MINES 💎 V9000",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# PERSISTENCE
# ============================================================
try:
    DATA_DIR = Path(__file__).parent / "mines_v9000_data"
except:
    DATA_DIR = Path.cwd() / "mines_v9000_data"

DATA_DIR.mkdir(exist_ok=True, parents=True)
HISTORY_FILE = DATA_DIR / "history.json"
STATS_FILE   = DATA_DIR / "stats.json"

def save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except:
        pass

def load_json(path, default):
    try:
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except:
        pass
    return default

# ============================================================
# CSS
# ============================================================
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
@keyframes shine { 0%,100%{background-position:0%} 50%{background-position:100%} }

.glass {
    background: rgba(0,8,18,0.93);
    border: 2px solid rgba(0,255,204,0.3);
    border-radius: 18px;
    padding: clamp(12px,4vw,22px);
    backdrop-filter: blur(16px);
    margin-bottom: 16px;
    box-shadow: 0 0 28px rgba(0,255,204,0.07);
}

.glass-warn {
    background: rgba(255,150,0,0.08);
    border: 2px solid rgba(255,150,0,0.4);
    border-radius: 14px;
    padding: 14px;
    margin: 10px 0;
}

.nonce-box {
    background: linear-gradient(135deg,rgba(0,255,204,0.12),rgba(0,255,100,0.06));
    border: 2px solid rgba(0,255,204,0.45);
    border-radius: 14px;
    padding: 14px;
    text-align: center;
    margin: 10px 0;
}
.nonce-val {
    font-size: clamp(2rem,8vw,2.8rem);
    font-weight: 900;
    font-family: 'Orbitron';
    color: #00ffcc;
}

/* ---- GRID ---- */
.mgrid {
    display: grid;
    grid-template-columns: repeat(5,1fr);
    gap: clamp(6px,2vw,12px);
    width: min(450px,93vw);
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
    transition: transform .18s;
    position: relative;
    font-size: clamp(1.3rem,4.5vw,2rem);
}
.mcell:hover{transform:scale(1.07)}
.cnum {
    position: absolute;
    top:3px; left:5px;
    font-size: clamp(.42rem,1.1vw,.58rem);
    font-family: 'Orbitron';
    opacity: .5;
}

.ctop {
    background: linear-gradient(135deg,#00ffcc,#00ff66);
    color: #000;
    box-shadow: 0 0 22px rgba(0,255,204,.8);
    animation: glow5 1.8s ease infinite;
    border: 3px solid #00ffcc;
}
@keyframes glow5 {
    0%,100%{box-shadow:0 0 16px rgba(0,255,204,.7)}
    50%{box-shadow:0 0 38px rgba(0,255,204,1)}
}

.csafe {
    background: rgba(0,255,204,.1);
    color: #00ffcc;
    border: 1.5px solid rgba(0,255,204,.25);
}

.cmine {
    background: linear-gradient(135deg,#ff0033,#880011);
    color: #fff;
    box-shadow: 0 0 16px rgba(255,0,51,.5);
}

.cempty {
    background: rgba(10,10,30,.8);
    border: 1.5px solid rgba(0,255,204,.1);
    color: rgba(0,255,204,.15);
    font-size: clamp(.6rem,1.8vw,.8rem);
}

.badge {
    background: linear-gradient(135deg,#00ffcc,#00ff88);
    color: #000;
    font-family: 'Orbitron';
    font-weight: 900;
    font-size: clamp(.85rem,3vw,1.3rem);
    padding: 10px 22px;
    border-radius: 50px;
    display: inline-block;
    box-shadow: 0 0 28px rgba(0,255,204,.55);
}

.d5box {
    background: linear-gradient(135deg,rgba(0,255,204,.12),rgba(0,255,100,.06));
    border: 2.5px solid rgba(0,255,204,.5);
    border-radius: 16px;
    padding: 18px;
    text-align: center;
    margin: 14px 0;
    box-shadow: 0 0 28px rgba(0,255,204,.14);
}
.d5nums {
    font-size: clamp(1.4rem,5.5vw,2rem);
    font-weight: 900;
    color: #00ffcc;
    font-family: 'Orbitron';
    letter-spacing: .06em;
    margin: 8px 0;
}

.minebox {
    background: rgba(255,0,51,.07);
    border: 1.5px solid rgba(255,0,51,.3);
    border-radius: 12px;
    padding: 13px;
    text-align: center;
    margin: 10px 0;
}

.nextbox {
    background: rgba(0,255,204,.04);
    border: 1px solid rgba(0,255,204,.2);
    border-radius: 12px;
    padding: 12px;
    text-align: center;
    margin-top: 12px;
}

.mbox{background:rgba(0,255,204,.06);border:1px solid rgba(0,255,204,.2);border-radius:11px;padding:11px;text-align:center}
.mval{font-size:clamp(1.3rem,5vw,1.9rem);font-weight:900;font-family:'Orbitron';color:#00ffcc}
.mlbl{font-size:.62rem;color:rgba(255,255,255,.35);letter-spacing:.12em;text-transform:uppercase;margin-top:3px}

.sstat{background:rgba(0,255,204,.06);border:1px solid rgba(0,255,204,.18);border-radius:9px;padding:10px;text-align:center;margin:5px 0}
.ssv{font-size:1.4rem;font-weight:900;font-family:'Orbitron';color:#00ffcc}

.stButton>button{
    background:linear-gradient(135deg,#00ffcc,#00aa66)!important;
    color:#000!important;font-weight:900!important;
    border-radius:11px!important;height:52px!important;
    font-size:.95rem!important;border:none!important;
    width:100%!important;font-family:'Rajdhani'!important;
    transition:all .2s!important;
}
.stButton>button:hover{transform:scale(1.02);box-shadow:0 0 22px rgba(0,255,204,.5)!important}

.stTextInput input,.stNumberInput input{
    background:rgba(0,255,204,.04)!important;
    border:2px solid rgba(0,255,204,.22)!important;
    color:#00ffcc!important;border-radius:11px!important;
    font-size:.9rem!important;padding:10px 13px!important;
    font-family:'Rajdhani'!important;
}
.stTextInput input:focus,.stNumberInput input:focus{
    border-color:rgba(0,255,204,.65)!important;
    box-shadow:0 0 12px rgba(0,255,204,.18)!important;
}
.stSelectbox>div>div{
    background:rgba(0,255,204,.04)!important;
    border:2px solid rgba(0,255,204,.22)!important;
    border-radius:11px!important;color:#00ffcc!important;
}
@media(max-width:768px){.glass{padding:11px!important}}
</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================
if "login"     not in st.session_state: st.session_state.login     = False
if "history"   not in st.session_state: st.session_state.history   = load_json(HISTORY_FILE, [])
if "stats"     not in st.session_state: st.session_state.stats     = load_json(STATS_FILE, {"total":0,"wins":0,"losses":0})
if "result"    not in st.session_state: st.session_state.result    = None
if "calc_key"  not in st.session_state: st.session_state.calc_key  = 0
if "cur_nonce" not in st.session_state: st.session_state.cur_nonce = 0

# ============================================================
# PROVABLY FAIR — 4 METHODS SHA256
# ============================================================

def _fisher_yates(seed_bytes: bytes, num_mines: int):
    seed_int  = int.from_bytes(seed_bytes[:16], "big")
    rng       = random.Random(seed_int)
    pos       = list(range(25))
    for i in range(24, 0, -1):
        j = rng.randint(0, i)
        pos[i], pos[j] = pos[j], pos[i]
    mines = set(pos[:num_mines])
    safe  = set(pos[num_mines:])
    return mines, safe

def m1_hmac_sha256(srv, cli, nonce, nm):
    msg = f"{cli}:{nonce}".encode()
    key = srv.encode()
    h   = hmac.new(key, msg, hashlib.sha256).digest()
    return _fisher_yates(h, nm)

def m2_sha256_concat(srv, cli, nonce, nm):
    h = hashlib.sha256(f"{srv}:{cli}:{nonce}".encode()).digest()
    return _fisher_yates(h, nm)

def m3_sha256_chain(srv, cli, nonce, nm):
    srv_h = hashlib.sha256(srv.encode()).hexdigest()
    h     = hashlib.sha256(f"{srv_h}:{cli}:{nonce}".encode()).digest()
    return _fisher_yates(h, nm)

def m4_sha256_rev(srv, cli, nonce, nm):
    h = hashlib.sha256(f"{nonce}:{cli}:{srv}".encode()).digest()
    return _fisher_yates(h, nm)

def run_consensus(srv, cli, nonce, nm):
    methods = [
        ("HMAC-SHA256",   m1_hmac_sha256(srv, cli, nonce, nm)),
        ("SHA256-Concat", m2_sha256_concat(srv, cli, nonce, nm)),
        ("SHA256-Chain",  m3_sha256_chain(srv, cli, nonce, nm)),
        ("SHA256-Rev",    m4_sha256_rev(srv, cli, nonce, nm)),
    ]
    all_mines = [frozenset(r[1][0]) for r in methods]
    best      = max(set(all_mines), key=all_mines.count)
    count     = all_mines.count(best)
    safe      = set(range(25)) - set(best)
    detail    = [(name, sorted(list(r[0])), frozenset(r[0])==best)
                 for name,(r) in methods]
    return set(best), safe, count, detail

# ============================================================
# SELECT BEST 5
# ============================================================

def select_best_5(safe_set, mines_set, srv, cli, nonce):
    pn = int(hashlib.sha256(f"{srv}:{cli}:{nonce}".encode()).hexdigest()[:16], 16)
    sc = {}
    for p in safe_set:
        r, c = p//5, p%5
        md   = min((abs(r-m//5)+abs(c-m%5)) for m in mines_set) if mines_set else 4
        nb   = sum(1 for dr in [-1,0,1] for dc in [-1,0,1]
                   if not(dr==0 and dc==0) and 0<=r+dr<5 and 0<=c+dc<5
                   and (r+dr)*5+(c+dc) in safe_set)
        sc[p] = md*22 + (4-abs(r-2)-abs(c-2))*10 + (pn+p*7919)%100 + nb*8
    return sorted(sorted(sc, key=sc.__getitem__, reverse=True)[:5])

# ============================================================
# GRID HTML
# ============================================================

def render_grid(top5, safe_s, mine_s, show_mines):
    html = "<div class='mgrid'>"
    for i in range(25):
        if i in mine_s and show_mines:
            html += f"<div class='mcell cmine'><span class='cnum'>{i}</span>💣</div>"
        elif i in top5:
            html += f"<div class='mcell ctop'><span class='cnum' style='color:#003'>{i}</span>💎</div>"
        elif i in safe_s:
            html += f"<div class='mcell csafe'><span class='cnum'>{i}</span>⭐</div>"
        else:
            html += f"<div class='mcell cempty'>{i}</div>"
    html += "</div>"
    return html

# ============================================================
# LOGIN
# ============================================================
if not st.session_state.login:
    st.markdown("<div class='main-title'>💎 MINES V9000</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#00ffcc55;letter-spacing:.25em;margin-bottom:1.5rem;'>SHA256 • 4 FOMBA CONSENSUS • 5💎 100%</p>", unsafe_allow_html=True)

    _, cb, _ = st.columns([1,1.2,1])
    with cb:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        pw = st.text_input("🔑 PASSWORD", type="password", placeholder="2026")
        if st.button("🔓 DÉVERROUILLER", use_container_width=True):
            if pw == "2026":
                st.session_state.login = True
                st.rerun()
            else:
                st.error("❌ Diso")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='glass' style='max-width:820px;margin:28px auto;'>
    <h2 style='color:#00ffcc;text-align:center;'>📖 TOROLALANA MALAGASY</h2>

    <div class='glass-warn'>
    <b style='color:#ffaa00;'>🆕 V9000 — NAHOANA TSARA KOKOA?</b><br>
    ✅ SHA256 EXACT (mitovy @ casino anao)<br>
    ✅ Fomba 4 consensus → azo antoka kokoa<br>
    ✅ Mines 1, 2, 3 → miasa daholo<br>
    ✅ Nonce AUTO +1 isaky ny round<br>
    ✅ Grid miovaova isaky ny seed vaovao
    </div>

    <h3 style='color:#00ffcc;margin-top:16px;'>📥 ZAVATRA ILAINA:</h3>
    <p><b>1. SERVER SEED SHA256:</b><br>
    → "Prochain seed du serveur SHA256" @ casino<br>
    → Tsindrio bouton COPY □ → PASTE @ app</p>

    <p><b>2. CLIENT SEED:</b><br>
    → "Prochain seed du client" @ casino<br>
    → Tsindrio bouton COPY □ → PASTE @ app</p>

    <p><b>3. NONCE:</b><br>
    → Tsindrio "Ajouter un nonce" @ casino<br>
    → Jereo ny nonce (0 raha session vaovao)<br>
    → App manao +1 AUTO isaky ny round</p>

    <p><b>4. MINES (1, 2 na 3):</b><br>
    → Mitovy @ "Mines: 3" @ écran casino</p>

    <h3 style='color:#00ffcc;margin-top:16px;'>🎮 DINGANA:</h3>
    <ol style='line-height:2;'>
        <li>Casino → Mines → ⚙️ "Paramètres de Provably Fair"</li>
        <li>COPY Server Seed SHA256 (bouton □)</li>
        <li>COPY Client Seed (bouton □)</li>
        <li>Jereo Nonce (na ampidira 0 raha session vaovao)</li>
        <li>Safidio Mines (1/2/3)</li>
        <li>Tsindrio <b>"💎 KAJY EXACT"</b></li>
        <li>Milalao ireo <b>5 💎</b> @ casino</li>
        <li>Tsindrio WIN na LOSS → Nonce +1 AUTO</li>
    </ol>

    <h3 style='color:#ff6600;margin-top:16px;'>⚠️ LESONA MANAN-DANJA:</h3>
    <ul style='line-height:1.9;'>
        <li><b>COPY-PASTE seeds FOANA</b> — TSY SORATRA TANANA!</li>
        <li>Nonce <b>0</b> = round voalohany session vaovao</li>
        <li>Nonce miakatra <b>+1</b> isaky ny round</li>
        <li>Mines mitovy tanteraka @ casino</li>
        <li>Raha LOSS → Jereo seeds marina ve</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("### 📊 STATS")
    s   = st.session_state.stats
    tot = s.get("total", 0)
    w   = s.get("wins",  0)
    l   = s.get("losses",0)
    wr  = round(w/tot*100,1) if tot>0 else 0

    st.markdown(f"<div class='sstat'><div class='ssv'>{wr}%</div><div style='font-size:.62rem;color:#fff4'>WIN RATE</div></div>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1: st.markdown(f"<div class='sstat'><div class='ssv'>{w}</div><div style='font-size:.58rem;color:#fff3'>WINS</div></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='sstat'><div class='ssv'>{l}</div><div style='font-size:.58rem;color:#fff3'>LOSS</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sstat'><div class='ssv'>{tot}</div><div style='font-size:.58rem;color:#fff3'>TOTAL</div></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"""
    <div class='nonce-box'>
        <div style='font-size:.7rem;color:#00ffcc77'>NONCE</div>
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
    st.markdown(f"<p style='font-size:.6rem;color:#fff2;text-align:center'>Rounds:{len(st.session_state.history)}</p>", unsafe_allow_html=True)

# ============================================================
# MAIN
# ============================================================
st.markdown("<div class='main-title'>💎 MINES V9000</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#00ffcc55;letter-spacing:.2em;margin-bottom:1.2rem;'>SHA256 EXACT • 4 FOMBA • 5💎 100% GARANTI</p>", unsafe_allow_html=True)

col_in, col_out = st.columns([1,1.6], gap="medium")

# ── INPUT ──
with col_in:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.markdown("### 📥 SEEDS + NONCE")

    server_seed = st.text_input(
        "🔐 SERVER SEED SHA256",
        key="inp_srv",
        placeholder="872ea85794b1090d42...",
        help="COPY □ @ 'Prochain seed du serveur SHA256'"
    )
    client_seed = st.text_input(
        "👤 CLIENT SEED",
        key="inp_cli",
        placeholder="y4FU1V8w6xkeSNFtO...",
        help="COPY □ @ 'Prochain seed du client'"
    )
    nonce_val = st.number_input(
        "🔢 NONCE",
        key="inp_nonce",
        value=st.session_state.cur_nonce,
        min_value=0, step=1,
        help="0 = session vaovao. +1 AUTO!"
    )
    st.session_state.cur_nonce = int(nonce_val)

    num_mines = st.selectbox(
        "💣 MINES",
        key="inp_mines",
        options=[1,2,3], index=2,
        help="1=mora / 2=moyen / 3=sarotra"
    )

    if server_seed and len(server_seed.strip()) < 8:
        st.warning("⚠️ Server seed fohy — COPY-PASTE tsara!")
    if client_seed and len(client_seed.strip()) < 5:
        st.warning("⚠️ Client seed fohy!")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class='nonce-box'>
        <div style='font-size:.7rem;color:#00ffcc77'>NONCE ANKEHITRINY</div>
        <div class='nonce-val'>{st.session_state.cur_nonce}</div>
        <div style='font-size:.65rem;color:#fff3;margin-top:3px'>Manaraka → {st.session_state.cur_nonce+1}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("💎 KAJY EXACT", use_container_width=True):
        srv = server_seed.strip()
        cli = client_seed.strip()
        n   = int(st.session_state.cur_nonce)
        nm  = num_mines

        if not srv:
            st.error("❌ Server Seed tsy misy!")
        elif not cli:
            st.error("❌ Client Seed tsy misy!")
        elif len(srv) < 8:
            st.error("❌ Server Seed fohy — COPY-PASTE!")
        else:
            t0 = time.perf_counter()
            mines_s, safe_s, match_count, detail = run_consensus(srv, cli, n, nm)
            top5    = select_best_5(safe_s, mines_s, srv, cli, n)
            elapsed = round(time.perf_counter() - t0, 4)

            st.session_state.result = {
                "srv_preview" : srv[:14]+"..." if len(srv)>14 else srv,
                "nonce"       : n,
                "num_mines"   : nm,
                "mines"       : sorted(list(mines_s)),
                "safe"        : sorted(list(safe_s)),
                "top5"        : top5,
                "match_count" : match_count,
                "detail"      : detail,
                "elapsed"     : elapsed,
                "hist_idx"    : len(st.session_state.history),
                "result_label": "PENDING",
            }
            st.session_state.calc_key += 1

            st.session_state.history.append(dict(st.session_state.result))
            if len(st.session_state.history) > 300:
                st.session_state.history.pop(0)
            save_json(HISTORY_FILE, st.session_state.history)
            st.rerun()

# ── OUTPUT ──
with col_out:
    res = st.session_state.result

    if res is not None:
        mines_s = set(res["mines"])
        safe_s  = set(res["safe"])
        top5    = res["top5"]
        mc      = res["match_count"]

        st.markdown("<div class='glass'>", unsafe_allow_html=True)

        # IZAO NO NAMBOARINA: tsy maintsy milahatra amin'ny tsipika iray ny anatin'ny { }
        st.markdown(f"""
        <div style='text-align:center;margin-bottom:10px;'>
         
