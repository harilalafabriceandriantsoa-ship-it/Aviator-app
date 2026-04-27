import streamlit as st
import hashlib
import hmac
import numpy as np
import pandas as pd
import json
from pathlib import Path
import time

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
# CSS
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
.mcell:hover{transform:scale(1.06)}
.cnum{position:absolute;top:3px;left:5px;font-size:clamp(.4rem,1vw,.55rem);font-family:'Orbitron';opacity:.45}
.ctop{background:linear-gradient(135deg,#00ffcc,#00ff66);color:#000;box-shadow:0 0 22px rgba(0,255,204,.8);animation:g5 1.8s ease infinite;border:3px solid #00ffcc}
@keyframes g5{0%,100%{box-shadow:0 0 15px rgba(0,255,204,.7)}50%{box-shadow:0 0 38px rgba(0,255,204,1)}}
.csafe{background:rgba(0,255,204,.1);color:#00ffcc;border:1.5px solid rgba(0,255,204,.25)}
.cmine{background:linear-gradient(135deg,#ff0033,#880011);color:#fff;box-shadow:0 0 16px rgba(255,0,51,.5)}
.cempty{background:rgba(10,10,30,.8);border:1.5px solid rgba(0,255,204,.1);color:rgba(0,255,204,.15);font-size:clamp(.6rem,1.8vw,.8rem)}
.d5box{background:linear-gradient(135deg,rgba(0,255,204,.12),rgba(0,255,100,.06));border:2.5px solid rgba(0,255,204,.5);border-radius:16px;padding:18px;text-align:center;margin:14px 0;box-shadow:0 0 28px rgba(0,255,204,.14)}
.d5nums{font-size:clamp(1.4rem,5.5vw,2rem);font-weight:900;color:#00ffcc;font-family:'Orbitron';letter-spacing:.06em;margin:8px 0}
.nbox{background:linear-gradient(135deg,rgba(0,255,204,.12),rgba(0,255,100,.06));border:2px solid rgba(0,255,204,.45);border-radius:14px;padding:13px;text-align:center;margin:10px 0}
.nval{font-size:clamp(1.8rem,7vw,2.6rem);font-weight:900;font-family:'Orbitron';color:#00ffcc}
.mbox2{background:rgba(0,255,204,.06);border:1px solid rgba(0,255,204,.2);border-radius:11px;padding:11px;text-align:center}
.mv{font-size:clamp(1.2rem,4.5vw,1.8rem);font-weight:900;font-family:'Orbitron';color:#00ffcc}
.ml{font-size:.6rem;color:rgba(255,255,255,.35);letter-spacing:.12em;text-transform:uppercase;margin-top:3px}
.ss{background:rgba(0,255,204,.06);border:1px solid rgba(0,255,204,.18);border-radius:9px;padding:10px;text-align:center;margin:5px 0}
.sv{font-size:1.4rem;font-weight:900;font-family:'Orbitron';color:#00ffcc}
.risk-green{background:rgba(0,255,100,.1);border:2px solid rgba(0,255,100,.4);border-radius:12px;padding:14px;text-align:center;margin:10px 0}
.risk-yellow{background:rgba(255,200,0,.1);border:2px solid rgba(255,200,0,.4);border-radius:12px;padding:14px;text-align:center;margin:10px 0}
.risk-red{background:rgba(255,0,51,.12);border:2px solid rgba(255,0,51,.4);border-radius:12px;padding:14px;text-align:center;margin:10px 0}
.stButton>button{background:linear-gradient(135deg,#00ffcc,#00aa66)!important;color:#000!important;font-weight:900!important;border-radius:11px!important;height:52px!important;font-size:.95rem!important;border:none!important;width:100%!important;transition:all .2s!important}
.stButton>button:hover{transform:scale(1.02);box-shadow:0 0 22px rgba(0,255,204,.5)!important}
</style>
""", unsafe_allow_html=True)

# ============================================================
# STATE
# ============================================================
for k,v in [
    ("login",False),
    ("history",load_json(HISTORY_FILE,[])),
    ("stats",load_json(STATS_FILE,{"total":0,"wins":0,"losses":0,"streak":0,"best_streak":0})),
    ("result",None),("ck",0),("nonce",0)
]:
    if k not in st.session_state: st.session_state[k] = v

# ============================================================
# ALGORITHM
# ============================================================

def analyze_client_seed(client_seed: str, nonce: int, num_mines: int, simulations=300_000):
    seed_hash = hashlib.sha256(f"{client_seed}:{nonce}".encode()).hexdigest()
    seed_num  = int(seed_hash[:16], 16)
    np.random.seed(seed_num % (2**32))
    safe_count = np.zeros(25, dtype=np.int64)
    for i in range(simulations):
        sim_hash = hashlib.sha256(f"{seed_hash}:{i}".encode()).digest()
        sim_seed = int.from_bytes(sim_hash[:4], "big")
        rng = np.random.default_rng(sim_seed)
        positions = list(range(25))
        for j in range(24, 0, -1):
            k2 = int(rng.random() * (j+1))
            positions[j], positions[k2] = positions[k2], positions[j]
        mines_sim = set(positions[:num_mines])
        for pos in range(25):
            if pos not in mines_sim: safe_count[pos] += 1
    return safe_count / simulations

def get_hot_cold_pattern(history, num_mines):
    if len(history) < 3: return None
    recent = history[-10:]
    pos_wins, pos_losses = np.zeros(25), np.zeros(25)
    for h in recent:
        if h.get("res") == "WIN ✅":
            for p in h.get("top5", []): pos_wins[p] += 1
        elif h.get("res") == "LOSS ❌":
            for p in h.get("mines", []): pos_losses[p] += 1
    return pos_wins * 1.5 - pos_losses * 2.0

def select_best_5_smart(probabilities, pattern_score, client_seed, nonce):
    pn = int(hashlib.sha256(f"{client_seed}:{nonce}".encode()).hexdigest()[:16], 16)
    final_scores = probabilities.copy()
    if pattern_score is not None:
        norm = (pattern_score - pattern_score.min())
        if norm.max() > 0: norm = norm / norm.max()
        final_scores = final_scores * 0.75 + norm * 0.25
    for p in range(25):
        final_scores[p] += ((pn + p * 7919) % 100) / 2000
    top5 = sorted(range(25), key=lambda p: final_scores[p], reverse=True)[:5]
    return sorted(top5), final_scores

def compute_confidence(probabilities, top5, num_mines):
    avg_prob = float(np.mean(probabilities[top5]))
    baseline = (25 - num_mines) / 25
    boost = (avg_prob - baseline) / baseline if baseline > 0 else 0
    return round(min(95, max(50, 50 + boost * 200 + (85 - num_mines * 10))), 1)

def get_risk_level(confidence, streak):
    if streak <= -3: return "STOP", "🛑 STOP LOSS — Miandry kely!"
    if confidence >= 82: return "GO", "🟢 SIGNAL FORT — Milalao!"
    if confidence >= 72: return "CAUTION", "🟡 SIGNAL MODÉRÉ — Mitandrina"
    return "SKIP", "🔴 SIGNAL AMBANY — Skip ity"

def render_grid(top5):
    html = "<div class='mgrid'>"
    for i in range(25):
        if i in top5: html += f"<div class='mcell ctop'><span class='cnum' style='color:#003'>{i}</span>💎</div>"
        else: html += f"<div class='mcell cempty'>{i}</div>"
    html += "</div>"
    return html

# ============================================================
# LOGIN
# ============================================================
if not st.session_state.login:
    st.markdown("<div class='ttl'>💎 MINES ANDR V3</div>", unsafe_allow_html=True)
    _, cb, _ = st.columns([1,1.2,1])
    with cb:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        pw = st.text_input("🔑 PASSWORD", type="password", placeholder="2026")
        if st.button("🔓 DÉVERROUILLER"):
            if pw == "2026":
                st.session_state.login = True
                st.rerun()
            else: st.error("Diso")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ============================================================
# MAIN UI
# ============================================================
st.markdown("<div class='ttl'>💎 MINES ANDR V3</div>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 📊 STATS")
    s = st.session_state.stats
    st.metric("WIN RATE", f"{round(s['wins']/s['total']*100,1) if s['total']>0 else 0}%")
    st.write(f"Wins: {s['wins']} | Loss: {s['losses']}")
    if st.button("🔄 RESET ALL"):
        st.session_state.clear()
        st.rerun()

col_in, col_out = st.columns([1,1.6])

with col_in:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    cli = st.text_input("👤 CLIENT SEED", placeholder="Ampidiro ny seed...")
    nv = st.number_input("🔢 NONCE", value=st.session_state.nonce, min_value=0)
    nm = st.selectbox("💣 MINES", [1,2,3], index=2)
    
    if st.button("💎 ANALYSER", use_container_width=True):
        if cli:
            with st.spinner("Simulations..."):
                probs = analyze_client_seed(cli, nv, nm)
                pattern = get_hot_cold_pattern(st.session_state.history, nm)
                top5, _ = select_best_5_smart(probs, pattern, cli, nv)
                conf = compute_confidence(probs, top5, nm)
                rl, rm = get_risk_level(conf, st.session_state.stats["streak"])
                
                st.session_state.result = {
                    "top5": top5, "confidence": conf, "risk_level": rl, 
                    "risk_msg": rm, "nonce": nv, "nm": nm
                }
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with col_out:
    res = st.session_state.result
    if res:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        # Fix Syntax Error point: ensure string literal is closed
        risk_color = "risk-green" if res["risk_level"] == "GO" else "risk-yellow" if res["risk_level"] == "CAUTION" else "risk-red"
        st.markdown(f"<div class='{risk_color}'><b>{res['risk_msg']}</b></div>", unsafe_allow_html=True)
        
        st.markdown(render_grid(res["top5"]), unsafe_allow_html=True)
        st.markdown(f"<div class='d5box'><div class='d5nums'>{' — '.join(map(str, res['top5']))}</div></div>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        if c1.button("✅ WIN"):
            st.session_state.stats["total"] += 1
            st.session_state.stats["wins"] += 1
            st.session_state.stats["streak"] = max(0, st.session_state.stats["streak"]) + 1
            st.session_state.nonce += 1
            st.rerun()
        if c2.button("❌ LOSS"):
            st.session_state.stats["total"] += 1
            st.session_state.stats["losses"] += 1
            st.session_state.stats["streak"] = min(0, st.session_state.stats["streak"]) - 1
            st.session_state.nonce += 1
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center;color:#fff2;font-size:.6rem;'>MINES ANDR V3 • 2026</p>", unsafe_allow_html=True)
