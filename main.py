import streamlit as st
import hashlib
import numpy as np
import pandas as pd
import json
from pathlib import Path
import time

# ============================================================
# CONFIGURATION & PERSISTENCE
# ============================================================
st.set_page_config(page_title="MINES ANDR V3", layout="wide", initial_sidebar_state="collapsed")

try:
    DATA_DIR = Path(__file__).parent / "mines_andr_v3"
except:
    DATA_DIR = Path.cwd() / "mines_andr_v3"
DATA_DIR.mkdir(exist_ok=True, parents=True)

HISTORY_FILE = DATA_DIR / "history.json"
STATS_FILE   = DATA_DIR / "stats.json"

def save_json(p, d):
    try:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2)
    except: pass

def load_json(p, d):
    try:
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
    except: pass
    return d

# ============================================================
# CSS CUSTOM DESIGN
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@600;700&display=swap');
.stApp{background:radial-gradient(ellipse at 50% 0%,#080018 0%,#000008 55%,#001510 100%);color:#00ffcc;font-family:'Rajdhani',sans-serif}
.ttl{font-family:'Orbitron';font-size:clamp(1.8rem,7vw,3rem);font-weight:900;text-align:center;background:linear-gradient(90deg,#00ffcc,#00ff88,#00ffcc);background-size:200%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:sh 3s ease infinite}
@keyframes sh{0%,100%{background-position:0%}50%{background-position:100%}}
.glass{background:rgba(0,8,18,.93);border:2px solid rgba(0,255,204,.3);border-radius:18px;padding:clamp(12px,4vw,22px);backdrop-filter:blur(16px);margin-bottom:16px}
.mgrid{display:grid;grid-template-columns:repeat(5,1fr);gap:clamp(5px,2vw,11px);width:min(440px,93vw);margin:16px auto}
.mcell{aspect-ratio:1/1;display:flex;flex-direction:column;align-items:center;justify-content:center;border-radius:13px;font-weight:900;transition:transform .18s;position:relative;font-size:clamp(1.3rem,4.5vw,2rem)}
.cnum{position:absolute;top:3px;left:5px;font-size:clamp(.4rem,1vw,.55rem);font-family:'Orbitron';opacity:.45}
.ctop{background:linear-gradient(135deg,#00ffcc,#00ff66);color:#000;box-shadow:0 0 22px rgba(0,255,204,.8);border:3px solid #00ffcc}
.cempty{background:rgba(10,10,30,.8);border:1.5px solid rgba(0,255,204,.1);color:rgba(0,255,204,.15)}
.risk-green{background:rgba(0,255,100,.1);border:2px solid rgba(0,255,100,.4);border-radius:12px;padding:14px;text-align:center;margin:10px 0}
.risk-yellow{background:rgba(255,200,0,.1);border:2px solid rgba(255,200,0,.4);border-radius:12px;padding:14px;text-align:center;margin:10px 0}
.risk-red{background:rgba(255,0,51,.12);border:2px solid rgba(255,0,51,.4);border-radius:12px;padding:14px;text-align:center;margin:10px 0}
.stButton>button{background:linear-gradient(135deg,#00ffcc,#00aa66)!important;color:#000!important;font-weight:900!important;border-radius:11px!important;height:52px!important;width:100%!important}
</style>
""", unsafe_allow_html=True)

# ============================================================
# APP STATE
# ============================================================
if "login" not in st.session_state: st.session_state.login = False
if "history" not in st.session_state: st.session_state.history = load_json(HISTORY_FILE, [])
if "stats" not in st.session_state: st.session_state.stats = load_json(STATS_FILE, {"total":0,"wins":0,"losses":0,"streak":0})
if "result" not in st.session_state: st.session_state.result = None
if "nonce" not in st.session_state: st.session_state.nonce = 0

# ============================================================
# CORE LOGIC (MONTE CARLO 300K)
# ============================================================
def analyze_mines(client_seed, nonce, num_mines, simulations=300000):
    seed_hash = hashlib.sha256(f"{client_seed}:{nonce}".encode()).hexdigest()
    seed_num = int(seed_hash[:16], 16)
    np.random.seed(seed_num % (2**32))
    
    safe_counts = np.zeros(25)
    for i in range(simulations):
        sim_seed = int(hashlib.sha256(f"{seed_hash}:{i}".encode()).hexdigest()[:8], 16)
        rng = np.random.default_rng(sim_seed)
        pos = list(range(25))
        rng.shuffle(pos)
        mines = set(pos[:num_mines])
        for p in range(25):
            if p not in mines: safe_counts[p] += 1
            
    probs = safe_counts / simulations
    top5 = sorted(range(25), key=lambda x: probs[x], reverse=True)[:5]
    confidence = (np.mean(probs[top5]) * 100)
    
    # Risk Assessment
    if confidence >= 85: rl, rm = "GO", "🟢 SIGNAL FORT — Milalao!"
    elif confidence >= 75: rl, rm = "CAUTION", "🟡 SIGNAL MODÉRÉ — Mitandrina"
    else: rl, rm = "SKIP", "🔴 SIGNAL AMBANY — Miandry"
    
    return top5, round(confidence, 1), rl, rm

# ============================================================
# LOGIN PAGE
# ============================================================
if not st.session_state.login:
    st.markdown("<div class='ttl'>💎 MINES ANDR V3</div>", unsafe_allow_html=True)
    _, cb, _ = st.columns([1,1.2,1])
    with cb:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        pw = st.text_input("🔑 PASSWORD", type="password")
        if st.button("🔓 DÉVERROUILLER"):
            if pw == "2026":
                st.session_state.login = True
                st.rerun()
            else: st.error("❌ Diso ny teny fanalahidy")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ============================================================
# MAIN INTERFACE
# ============================================================
st.markdown("<div class='ttl'>💎 MINES ANDR V3</div>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 📊 STATISTIQUES")
    s = st.session_state.stats
    st.write(f"Total: {s['total']} | Wins: {s['wins']} | Loss: {s['losses']}")
    st.write(f"Win Rate: {round(s['wins']/s['total']*100, 1) if s['total']>0 else 0}%")
    if st.button("🔄 Reset Nonce"): st.session_state.nonce = 0; st.rerun()

col_in, col_out = st.columns([1, 1.5])

with col_in:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    cli = st.text_input("👤 CLIENT SEED", placeholder="Ampidiro ny seed...")
    nv = st.number_input("🔢 NONCE", value=st.session_state.nonce, step=1)
    nm = st.selectbox("💣 MINES", [1, 2, 3], index=2)
    
    if st.button("💎 ANALYSER", use_container_width=True):
        if cli:
            with st.spinner("Mikajy (300k sims)..."):
                t5, conf, rl, rm = analyze_mines(cli, nv, nm)
                st.session_state.result = {
                    "top5": t5, "confidence": conf, 
                    "risk_level": rl, "risk_msg": rm,
                    "nonce": nv, "nm": nm
                }
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with col_out:
    res = st.session_state.result
    if res:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        # Fix for the KeyError: Ensure keys exist before accessing
        r_lvl = res.get("risk_level", "SKIP")
        r_msg = res.get("risk_msg", "Miandry...")
        
        r_class = "risk-green" if r_lvl == "GO" else "risk-yellow" if r_lvl == "CAUTION" else "risk-red"
        st.markdown(f"<div class='{r_class}'><b>{r_msg}</b></div>", unsafe_allow_html=True)
        
        # Grid Rendering
        html_grid = "<div class='mgrid'>"
        for i in range(25):
            if i in res["top5"]: html_grid += f"<div class='mcell ctop'><span class='cnum'>{i}</span>💎</div>"
            else: html_grid += f"<div class='mcell cempty'>{i}</div>"
        html_grid += "</div>"
        st.markdown(html_grid, unsafe_allow_html=True)
        
        st.markdown(f"<h2 style='text-align:center; color:#00ffcc;'>{' — '.join(map(str, res['top5']))}</h2>", unsafe_allow_html=True)
        
        # Feedback Buttons
        cw, cl = st.columns(2)
        if cw.button("✅ WIN"):
            st.session_state.stats["total"] += 1
            st.session_state.stats["wins"] += 1
            st.session_state.nonce += 1
            save_json(STATS_FILE, st.session_state.stats)
            st.rerun()
        if cl.button("❌ LOSS"):
            st.session_state.stats["total"] += 1
            st.session_state.stats["losses"] += 1
            st.session_state.nonce += 1
            save_json(STATS_FILE, st.session_state.stats)
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
