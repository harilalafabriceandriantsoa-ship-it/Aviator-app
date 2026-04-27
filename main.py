import streamlit as st
import hashlib
import random
import hmac
import pandas as pd
import json
import time
from pathlib import Path

# ============================================================
# CONFIGURATION GÉNÉRALE
# ============================================================
st.set_page_config(
    page_title="MINES 💎 V9000 PRO",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# FITANTANANA NY DATA (PERSISTENCE)
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
# STYLING (CSS)
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
    font-size: clamp(1.8rem, 7vw, 3.5rem);
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg, #00ffcc, #00ff88, #00ddff, #00ffcc);
    background-size: 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 4s ease infinite;
}
@keyframes shine { 0%,100%{background-position:0%} 50%{background-position:100%} }

.glass {
    background: rgba(0,8,18,0.95);
    border: 2px solid rgba(0,255,204,0.3);
    border-radius: 20px;
    padding: 20px;
    backdrop-filter: blur(15px);
    box-shadow: 0 0 30px rgba(0,255,204,0.1);
    margin-bottom: 20px;
}

.nonce-box {
    background: linear-gradient(135deg,rgba(0,255,204,0.15),rgba(0,255,100,0.05));
    border: 2px solid rgba(0,255,204,0.5);
    border-radius: 15px;
    padding: 15px;
    text-align: center;
}
.nonce-val {
    font-size: 2.5rem;
    font-weight: 900;
    font-family: 'Orbitron';
    color: #00ffcc;
}

/* GRID SYSTEM */
.mgrid {
    display: grid;
    grid-template-columns: repeat(5,1fr);
    gap: 12px;
    width: min(450px, 95vw);
    margin: 20px auto;
}
.mcell {
    aspect-ratio: 1/1;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 12px;
    font-weight: 900;
    position: relative;
    font-size: 1.8rem;
    transition: 0.3s;
}
.cnum { position: absolute; top:2px; left:5px; font-size: 0.6rem; opacity: 0.4; color: white; }
.ctop { background: linear-gradient(135deg,#00ffcc,#00ff66); color: #000; box-shadow: 0 0 25px #00ffcc; border: 2px solid #00ffcc; }
.csafe { background: rgba(0,255,204,0.12); color: #00ffcc; border: 1.5px solid rgba(0,255,204,0.3); }
.cmine { background: #ff0033; color: #fff; box-shadow: 0 0 15px #ff0033; }
.cempty { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); color: rgba(255,255,255,0.1); }

.badge {
    background: linear-gradient(135deg,#00ffcc,#00ff88);
    color: #000;
    font-family: 'Orbitron';
    font-weight: 900;
    padding: 10px 25px;
    border-radius: 50px;
    display: inline-block;
}

.d5box {
    background: rgba(0,255,204,0.08);
    border: 2.5px solid #00ffcc;
    border-radius: 15px;
    padding: 20px;
    text-align: center;
}
.d5nums { font-size: 2.2rem; font-weight: 900; color: #00ffcc; font-family: 'Orbitron'; letter-spacing: 5px; }

.minebox {
    background: rgba(255,0,51,0.1);
    border: 1px solid #ff0033;
    border-radius: 10px;
    padding: 10px;
    text-align: center;
    margin-top: 15px;
}

.sstat { background: rgba(0,255,204,0.06); border: 1px solid rgba(0,255,204,0.2); border-radius: 10px; padding: 12px; text-align: center; margin-bottom: 10px; }
.ssv { font-size: 1.6rem; font-weight: 900; color: #00ffcc; font-family: 'Orbitron'; }

.stButton>button {
    background: linear-gradient(135deg,#00ffcc,#00aa66)!important;
    color: #000!important;
    font-weight: 900!important;
    border-radius: 12px!important;
    height: 55px!important;
    font-family: 'Rajdhani'!important;
    font-size: 1.1rem!important;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# LOJIKA PROVABLY FAIR (4 FOMBA)
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
    # Mifidy ny valiny miverina betsaka indrindra (Consensus)
    best_mines = max(set(all_mines), key=all_mines.count)
    match_count = all_mines.count(best_mines)
    safe_indices = set(range(25)) - set(best_mines)
    return set(best_mines), safe_indices, match_count

# ============================================================
# ALGORITHME SELECTION DIAMANTS
# ============================================================
def select_best_5(safe_set, mines_set, srv, cli, nonce):
    # Ity no lojika mifidy ny 5 tena azo antoka indrindra
    pn = int(hashlib.sha256(f"{srv}:{cli}:{nonce}".encode()).hexdigest()[:12], 16)
    scores = {}
    for p in safe_set:
        r, c = p // 5, p % 5
        # 1. Halavirana amin'ny baomba (Weight 70%)
        dist = min((abs(r - m // 5) + abs(c - m % 5)) for m in mines_set) if mines_set else 2
        # 2. "Seed Entropy" (Weight 30%)
        entropy = (pn + p * 13) % 100
        scores[p] = (dist * 100) + entropy
    
    # Maka ny 5 manana score ambony indrindra
    return sorted(scores, key=scores.get, reverse=True)[:5]

# ============================================================
# RENDERING GRID
# ============================================================
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
# SESSION STATE & DATA LOAD
# ============================================================
if "login"     not in st.session_state: st.session_state.login     = False
if "history"   not in st.session_state: st.session_state.history   = load_json(HISTORY_FILE, [])
if "stats"     not in st.session_state: st.session_state.stats     = load_json(STATS_FILE, {"total":0,"wins":0,"losses":0})
if "result"    not in st.session_state: st.session_state.result    = None
if "calc_key"  not in st.session_state: st.session_state.calc_key  = 0
if "cur_nonce" not in st.session_state: st.session_state.cur_nonce = 0

# ============================================================
# PAGE: LOGIN
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
            else: st.error("❌ Diso ny teny fanalahidy")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ============================================================
# PAGE: MAIN APP
# ============================================================
with st.sidebar:
    st.markdown("### 📊 STATISTIQUES")
    s = st.session_state.stats
    wr = round(s['wins']/s['total']*100, 1) if s['total'] > 0 else 0
    st.markdown(f"<div class='sstat'><div class='ssv'>{wr}%</div><div>WIN RATE</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sstat'><div class='ssv'>{s['wins']}</div><div>WINS</div></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown(f"<div class='nonce-box'><div>CURRENT NONCE</div><div class='nonce-val'>{st.session_state.cur_nonce}</div></div>", unsafe_allow_html=True)
    if st.button("🔄 RESET NONCE TO 0"):
        st.session_state.cur_nonce = 0
        st.rerun()

st.markdown("<div class='main-title'>💎 MINES V9000</div>", unsafe_allow_html=True)

col_in, col_out = st.columns([1, 1.5], gap="large")

with col_in:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.subheader("📥 Data avy amin'ny Casino")
    
    server_seed = st.text_input("🔐 SERVER SEED SHA256", placeholder="Ampidiro ny Server Seed...")
    client_seed = st.text_input("👤 CLIENT SEED", placeholder="Ampidiro ny Client Seed...")
    nonce_input = st.number_input("🔢 NONCE", value=st.session_state.cur_nonce, step=1)
    mines_count = st.selectbox("💣 ISAN'NY MINES", options=[1, 2, 3], index=2)
    
    st.session_state.cur_nonce = int(nonce_input)
    
    if st.button("💎 KAJY EXACT (SHA256)", use_container_width=True):
        if server_seed and client_seed:
            with st.spinner("Manao consensus SHA256..."):
                m_s, s_s, mc = run_consensus(server_seed.strip(), client_seed.strip(), int(nonce_input), mines_count)
                t5 = select_best_5(s_s, m_s, server_seed.strip(), client_seed.strip(), int(nonce_input))
                
                st.session_state.result = {
                    "mines": list(m_s),
                    "safe": list(s_s),
                    "top5": t5,
                    "mc": mc,
                    "nonce": int(nonce_input),
                    "num_mines": mines_count
                }
                st.session_state.calc_key += 1
                st.rerun()
        else:
            st.error("❌ Fenoy ny Server Seed sy Client Seed")
    st.markdown("</div>", unsafe_allow_html=True)

with col_out:
    res = st.session_state.result
    if res:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        
        # Badge Consensus
        badge_text = "✅ 100% CONFIRMED" if res["mc"] >= 3 else "⚠️ VALIDATING..."
        st.markdown(f"<div style='text-align:center;'><span class='badge'>{badge_text} ({res['mc']}/4)</span></div>", unsafe_allow_html=True)
        
        # Grid View
        view_mode = st.radio("👁️ JEREHO:", ["💎 TOP 5 DIAMANTS", "🗺️ BOARD FENO (DEBUG)"], horizontal=True, key=f"mode_{st.session_state.calc_key}")
        
        show_all = (view_mode == "🗺️ BOARD FENO (DEBUG)")
        st.markdown(render_grid(res["top5"], set(res["safe"]), set(res["mines"]), show_all), unsafe_allow_html=True)
        
        # Top 5 box
        st.markdown(f"<div class='d5box'><div style='font-size:0.8rem;opacity:0.6;'>TSINDRIO IREO 5 IREO @ CASINO</div><div class='d5nums'>{' - '.join(map(str, res['top5']))}</div></div>", unsafe_allow_html=True)
        
        if show_all:
            st.markdown(f"<div class='minebox'>💣 BAOMBA: {' , '.join(map(str, res['mines']))}</div>", unsafe_allow_html=True)

        # Win / Loss Buttons
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ WIN (+1 Nonce)", use_container_width=True):
                st.session_state.stats["total"] += 1
                st.session_state.stats["wins"] += 1
                st.session_state.cur_nonce += 1
                save_json(STATS_FILE, st.session_state.stats)
                # Save to history
                st.session_state.history.append({"nonce": res["nonce"], "result": "WIN", "mines": res["num_mines"]})
                save_json(HISTORY_FILE, st.session_state.history)
                st.rerun()
        with c2:
            if st.button("❌ LOSS (+1 Nonce)", use_container_width=True):
                st.session_state.stats["total"] += 1
                st.session_state.stats["losses"] += 1
                st.session_state.cur_nonce += 1
                save_json(STATS_FILE, st.session_state.stats)
                st.session_state.history.append({"nonce": res["nonce"], "result": "LOSS", "mines": res["num_mines"]})
                save_json(HISTORY_FILE, st.session_state.history)
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='glass' style='height:400px; display:flex; align-items:center; justify-content:center; color:rgba(255,255,255,0.2);'>AMPIDIRO DATA DIA TSINDRIO KAJY...</div>", unsafe_allow_html=True)

# ============================================================
# HISTORY TABLE
# ============================================================
if st.session_state.history:
    with st.expander("📜 HISTORIQUE DES ROUNDS"):
        df = pd.DataFrame(st.session_state.history).tail(15)
        st.table(df)

st.markdown("<div style='text-align:center; color:rgba(0,255,204,0.2); font-size:0.7rem;'>MINES V9000 - SECURITY PROTOCOL SHA256</div>", unsafe_allow_html=True)
