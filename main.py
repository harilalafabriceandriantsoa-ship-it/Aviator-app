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
    width:100%!important;transition:all .2s!important;
}
.stButton>button:hover{transform:scale(1.02);box-shadow:0 0 22px rgba(0,255,204,.5)!important}

.stTextInput input,.stNumberInput input{
    background:rgba(0,255,204,.04)!important;
    border:2px solid rgba(0,255,204,.22)!important;
    color:#00ffcc!important;border-radius:11px!important;
}
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
# CORE LOGIC
# ============================================================
def _fisher_yates(seed_bytes, num_mines):
    seed_int = int.from_bytes(seed_bytes[:16], "big")
    rng = random.Random(seed_int)
    pos = list(range(25))
    for i in range(24, 0, -1):
        j = rng.randint(0, i)
        pos[i], pos[j] = pos[j], pos[i]
    return set(pos[:num_mines]), set(pos[num_mines:])

def m1_hmac_sha256(srv, cli, nonce, nm):
    h = hmac.new(srv.encode(), f"{cli}:{nonce}".encode(), hashlib.sha256).digest()
    return _fisher_yates(h, nm)

def m2_sha256_concat(srv, cli, nonce, nm):
    h = hashlib.sha256(f"{srv}:{cli}:{nonce}".encode()).digest()
    return _fisher_yates(h, nm)

def m3_sha256_chain(srv, cli, nonce, nm):
    srv_h = hashlib.sha256(srv.encode()).hexdigest()
    h = hashlib.sha256(f"{srv_h}:{cli}:{nonce}".encode()).digest()
    return _fisher_yates(h, nm)

def m4_sha256_rev(srv, cli, nonce, nm):
    h = hashlib.sha256(f"{nonce}:{cli}:{srv}".encode()).digest()
    return _fisher_yates(h, nm)

def run_consensus(srv, cli, nonce, nm):
    methods = [
        ("HMAC", m1_hmac_sha256(srv, cli, nonce, nm)),
        ("Concat", m2_sha256_concat(srv, cli, nonce, nm)),
        ("Chain", m3_sha256_chain(srv, cli, nonce, nm)),
        ("Rev", m4_sha256_rev(srv, cli, nonce, nm))
    ]
    all_mines = [frozenset(m[1][0]) for m in methods]
    best_mines = max(set(all_mines), key=all_mines.count)
    match_count = all_mines.count(best_mines)
    safe = set(range(25)) - set(best_mines)
    detail = [(m[0], sorted(list(m[1][0])), frozenset(m[1][0])==best_mines) for m in methods]
    return set(best_mines), safe, match_count, detail

def select_best_5(safe_set, mines_set, srv, cli, nonce):
    pn = int(hashlib.sha256(f"{srv}:{cli}:{nonce}".encode()).hexdigest()[:8], 16)
    scores = {}
    for p in safe_set:
        r, c = p//5, p%5
        dist = min((abs(r-m//5)+abs(c-m%5)) for m in mines_set) if mines_set else 2
        scores[p] = dist * 20 + (pn + p) % 100
    return sorted(scores, key=scores.get, reverse=True)[:5]

def render_grid(top5, safe_s, mine_s, show_mines):
    html = "<div class='mgrid'>"
    for i in range(25):
        if i in mine_s and show_mines:
            html += f"<div class='mcell cmine'><span class='cnum'>{i}</span>💣</div>"
        elif i in top5:
            html += f"<div class='mcell ctop'><span class='cnum'>{i}</span>💎</div>"
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
    _, cb, _ = st.columns([1,1.2,1])
    with cb:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        pw = st.text_input("🔑 PASSWORD", type="password", placeholder="2026")
        if st.button("🔓 DÉVERROUILLER", use_container_width=True):
            if pw == "2026":
                st.session_state.login = True
                st.rerun()
            else: st.error("❌ Diso")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ============================================================
# MAIN INTERFACE
# ============================================================
with st.sidebar:
    st.markdown("### 📊 STATS")
    s = st.session_state.stats
    wr = round(s['wins']/s['total']*100, 1) if s['total']>0 else 0
    st.markdown(f"<div class='sstat'><div class='ssv'>{wr}%</div><div>WIN RATE</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='nonce-box'><div>NONCE</div><div class='nonce-val'>{st.session_state.cur_nonce}</div></div>", unsafe_allow_html=True)
    if st.button("🔄 RESET NONCE"):
        st.session_state.cur_nonce = 0
        st.rerun()

st.markdown("<div class='main-title'>💎 MINES V9000</div>", unsafe_allow_html=True)
col_in, col_out = st.columns([1, 1.6], gap="medium")

with col_in:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    srv_in = st.text_input("🔐 SERVER SEED SHA256", placeholder="Copy-Paste avy ao @ casino...")
    cli_in = st.text_input("👤 CLIENT SEED", placeholder="Copy-Paste avy ao @ casino...")
    non_in = st.number_input("🔢 NONCE", value=st.session_state.cur_nonce, step=1)
    min_in = st.selectbox("💣 MINES", options=[1,2,3], index=2)
    st.session_state.cur_nonce = int(non_in)
    
    if st.button("💎 KAJY EXACT", use_container_width=True):
        if srv_in and cli_in:
            t0 = time.perf_counter()
            m_s, s_s, mc, det = run_consensus(srv_in.strip(), cli_in.strip(), int(non_in), min_in)
            t5 = select_best_5(s_s, m_s, srv_in.strip(), cli_in.strip(), int(non_in))
            st.session_state.result = {
                "mines": list(m_s), "safe": list(s_s), "top5": t5, "mc": mc,
                "nonce": int(non_in), "nm": min_in, "elapsed": round(time.perf_counter()-t0, 3)
            }
            st.session_state.history.append({"nonce": int(non_in), "top5": t5, "res": "PENDING"})
            st.session_state.calc_key += 1
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with col_out:
    res = st.session_state.result
    if res:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        # FIX: The badge part that caused the error is now on one line or properly quoted
        badge_txt = "✅ 100% CONFIRMED" if res["mc"] >= 3 else "⚠️ CHECK SEEDS"
        st.markdown(f"<div style='text-align:center;margin-bottom:10px;'><span class='badge'>{badge_txt} — {res['mc']}/4</span></div>", unsafe_allow_html=True)
        
        mode = st.radio("👁️ JEREHO:", ["💎 5 DIAMANTS", "🗺️ BOARD FENO"], horizontal=True, key=f"v_{st.session_state.calc_key}")
        st.markdown(render_grid(res["top5"], set(res["safe"]), set(res["mines"]), mode=="🗺️ BOARD FENO"), unsafe_allow_html=True)
        
        st.markdown(f"<div class='d5box'><div class='d5nums'>{' — '.join(map(str,res['top5']))}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='minebox'>💣 MINES: {' — '.join(map(str,res['mines']))}</div>", unsafe_allow_html=True)

        cw, cl = st.columns(2)
        with cw:
            if st.button("✅ WIN", use_container_width=True):
                st.session_state.stats["total"] += 1
                st.session_state.stats["wins"] += 1
                st.session_state.cur_nonce += 1
                save_json(STATS_FILE, st.session_state.stats)
                st.rerun()
        with cl:
            if st.button("❌ LOSS", use_container_width=True):
                st.session_state.stats["total"] += 1
                st.session_state.stats["losses"] += 1
                st.session_state.cur_nonce += 1
                save_json(STATS_FILE, st.session_state.stats)
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='glass' style='height:350px;display:flex;align-items:center;justify-content:center;opacity:0.3;'>AMPIDIRO SEEDS DIA TSINDRIO KAJY</div>", unsafe_allow_html=True)

# ============================================================
# HISTORY
# ============================================================
st.markdown("### 📜 HISTORIQUE")
if st.session_state.history:
    st.dataframe(pd.DataFrame(st.session_state.history).tail(10), use_container_width=True)
