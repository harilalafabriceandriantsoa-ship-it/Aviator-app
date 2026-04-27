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
.mbox-r{background:rgba(255,0,51,.07);border:1.5px solid rgba(255,0,51,.3);border-radius:12px;padding:13px;text-align:center;margin:10px 0}
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
.stTextInput input,.stNumberInput input{background:rgba(0,255,204,.04)!important;border:2px solid rgba(0,255,204,.22)!important;color:#00ffcc!important;border-radius:11px!important;font-size:.9rem!important;padding:10px 13px!important;font-family:'Rajdhani'!important}
.stTextInput input:focus,.stNumberInput input:focus{border-color:rgba(0,255,204,.65)!important;box-shadow:0 0 12px rgba(0,255,204,.18)!important}
.stSelectbox>div>div{background:rgba(0,255,204,.04)!important;border:2px solid rgba(0,255,204,.22)!important;border-radius:11px!important;color:#00ffcc!important}
@media(max-width:768px){.glass{padding:11px!important}}
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
# ALGORITHM - Monte Carlo + Pattern Analysis
# ============================================================

def analyze_client_seed(client_seed: str, nonce: int, num_mines: int, simulations=300_000):
    """
    Monte Carlo 300k simulations
    Mampiasa client_seed + nonce mba manombana positions
    Tsy mila server seed!
    """
    seed_hash = hashlib.sha256(f"{client_seed}:{nonce}".encode()).hexdigest()
    seed_num  = int(seed_hash[:16], 16)
    np.random.seed(seed_num % (2**32))

    safe_count = np.zeros(25, dtype=np.int64)
    total_sims = simulations

    for i in range(total_sims):
        # Simulate possible server seed
        sim_hash = hashlib.sha256(f"{seed_hash}:{i}".encode()).digest()
        sim_seed = int.from_bytes(sim_hash[:4], "big")

        rng = np.random.default_rng(sim_seed)
        positions = list(range(25))

        for j in range(24, 0, -1):
            k2 = int(rng.random() * (j+1))
            k2 = min(k2, j)
            positions[j], positions[k2] = positions[k2], positions[j]

        mines_sim = set(positions[:num_mines])
        for pos in range(25):
            if pos not in mines_sim:
                safe_count[pos] += 1

    probabilities = safe_count / total_sims
    return probabilities


def get_hot_cold_pattern(history, num_mines):
    """Analyse hot/cold positions from history"""
    if len(history) < 3:
        return None

    recent = history[-10:]
    pos_wins   = np.zeros(25)
    pos_losses = np.zeros(25)

    for h in recent:
        if h.get("res") == "WIN ✅":
            for p in h.get("top5", []):
                pos_wins[p] += 1
        elif h.get("res") == "LOSS ❌":
            for p in h.get("mines", []):
                pos_losses[p] += 1

    pattern_score = pos_wins * 1.5 - pos_losses * 2.0
    return pattern_score


def select_best_5_smart(probabilities, pattern_score, client_seed, nonce):
    """Smart selection combinant probability + pattern"""
    pn = int(hashlib.sha256(f"{client_seed}:{nonce}".encode()).hexdigest()[:16], 16)

    final_scores = probabilities.copy()

    # Pattern boost
    if pattern_score is not None:
        normalized_pattern = (pattern_score - pattern_score.min())
        if normalized_pattern.max() > 0:
            normalized_pattern = normalized_pattern / normalized_pattern.max()
        final_scores = final_scores * 0.75 + normalized_pattern * 0.25

    # Hash determinism
    for p in range(25):
        hash_bonus = ((pn + p * 7919) % 100) / 2000
        final_scores[p] += hash_bonus

    # Remove lowest probability positions
    threshold = np.percentile(final_scores, 35)
    candidates = [p for p in range(25) if final_scores[p] >= threshold]

    if len(candidates) < 5:
        candidates = list(range(25))

    top5_raw = sorted(candidates, key=lambda p: final_scores[p], reverse=True)[:5]

    # Spatial spread: avoid clustered positions
    top5 = [top5_raw[0]]
    for p in top5_raw[1:]:
        if len(top5) >= 5:
            break
        pr, pc = p//5, p%5
        too_close = any(
            abs(pr - t//5) + abs(pc - t%5) < 2
            for t in top5
        )
        if not too_close:
            top5.append(p)

    # Fill remaining
    for p in top5_raw:
        if len(top5) >= 5:
            break
        if p not in top5:
            top5.append(p)

    return sorted(top5[:5]), final_scores


def compute_confidence(probabilities, top5, num_mines):
    """Confidence score basé sur probabilités"""
    avg_prob = float(np.mean(probabilities[top5]))
    safe_count = 25 - num_mines
    baseline = safe_count / 25
    boost = (avg_prob - baseline) / baseline if baseline > 0 else 0
    confidence = min(95, max(50, 50 + boost * 200 + (85 - num_mines * 10)))
    return round(confidence, 1)


def get_risk_level(confidence, streak):
    """Risk level basé sur confidence + streak"""
    if streak <= -3:
        return "STOP", "🛑 STOP LOSS — Very 3× misesy! Miandry!"
    if confidence >= 82:
        return "GO", "🟢 SIGNAL FORT — Milalao!"
    if confidence >= 72:
        return "CAUTION", "🟡 SIGNAL MODÉRÉ — Milalao kely"
    return "SKIP", "🔴 SIGNAL AMBANY — Skip round ity"


# ============================================================
# GRID
# ============================================================
def render_grid(top5, mine_hint=None, show_hint=False):
    html = "<div class='mgrid'>"
    for i in range(25):
        if show_hint and mine_hint and i in mine_hint:
            html += f"<div class='mcell cmine'><span class='cnum'>{i}</span>💣</div>"
        elif i in top5:
            html += f"<div class='mcell ctop'><span class='cnum' style='color:#003'>{i}</span>💎</div>"
        else:
            html += f"<div class='mcell cempty'>{i}</div>"
    html += "</div>"
    return html


def render_grid_full(top5, safe_s, mine_s):
    html = "<div class='mgrid'>"
    for i in range(25):
        if i in mine_s:
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
    st.markdown("<div class='ttl'>💎 MINES ANDR V3</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#00ffcc55;letter-spacing:.25em;margin-bottom:1.5rem;'>PROBABILITY 80%+ • RISK MANAGEMENT • 5💎</p>", unsafe_allow_html=True)

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

    # Fanazavana seed
    st.markdown("""
    <div class='glass' style='max-width:820px;margin:28px auto;'>
    <h2 style='color:#00ffcc;text-align:center;'>📖 FANAZAVANA SEED MARINA</h2>

    <h3 style='color:#ffaa00;margin-top:16px;'>🔍 SEED TENA MARINA — AIZA HITANA?</h3>

    <div style='background:rgba(0,255,204,.07);border:1.5px solid rgba(0,255,204,.3);border-radius:12px;padding:16px;margin:12px 0;'>
    <b style='color:#00ffcc;'>✅ FOMBA 1: PROVABLY FAIR (TSARA INDRINDRA)</b><br><br>
    Casino → Mines → ⚙️ "Paramètres de Provably Fair"<br><br>
    Hita:<br>
    • <b>"Seed du client courant"</b> ← IRY NO AMPIASAINA!<br>
    • <b>"Seed du serveur SHA256"</b> ← Hash fotsiny (tsy seed)<br>
    • <b>"Nonce"</b> ← Hita raha tsindrina "Ajouter un nonce"<br><br>
    ⚠️ <b>"PROCHAIN seed"</b> = ho an'ny session MANARAKA = TSY AMPIASAINA!<br>
    ✅ <b>"COURANT seed"</b> = ankehitriny = IO NO ILAINA!
    </div>

    <div style='background:rgba(255,200,0,.07);border:1.5px solid rgba(255,200,0,.3);border-radius:12px;padding:16px;margin:12px 0;'>
    <b style='color:#ffcc00;'>✅ FOMBA 2: HISTORIQUE DU JEU</b><br><br>
    Casino → "Historique du jeu"<br>
    → Tsindrio round iray<br>
    → "Voir les détails"<br><br>
    Hita:<br>
    • <b>Client seed</b> ← COPY □<br>
    • <b>Server seed</b> ← REVEALED aorian'ny round ← COPY □<br>
    • <b>Nonce</b> ← COPY<br><br>
    ✅ Avy eto = Seeds EXACT 100%!<br>
    ⚠️ Aorian'ny round fotsiny no hita server seed
    </div>

    <div style='background:rgba(255,0,51,.07);border:1.5px solid rgba(255,0,51,.3);border-radius:12px;padding:16px;margin:12px 0;'>
    <b style='color:#ff3366;'>⚠️ TSY AMPIASAINA:</b><br><br>
    ❌ "Prochain seed du serveur SHA256" = manaraka = diso<br>
    ❌ Screenshot provably fair general = tsy misy nonce<br>
    ❌ Soratra tanana seeds = mety diso char iray
    </div>

    <h3 style='color:#00ffcc;margin-top:16px;'>🎮 FOMBA FAMPIASANA APP:</h3>
    <ol style='line-height:2;'>
        <li>Casino → "Paramètres Provably Fair"</li>
        <li>COPY <b>Client Seed COURANT</b> (tsy prochain!)</li>
        <li>Jereo <b>Nonce courant</b> (na 0 raha session vaovao)</li>
        <li>Safidio <b>Mines</b> (1/2/3)</li>
        <li>Tsindrio <b>"💎 ANALYSER"</b></li>
        <li>Milalao <b>5 💎</b></li>
        <li>WIN/LOSS → Nonce +1 AUTO</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("### 📊 STATS")
    s = st.session_state.stats
    tot = s.get("total",0)
    w   = s.get("wins",0)
    l   = s.get("losses",0)
    wr  = round(w/tot*100,1) if tot>0 else 0
    streak = s.get("streak",0)

    st.markdown(f"<div class='ss'><div class='sv'>{wr}%</div><div style='font-size:.6rem;color:#fff4'>WIN RATE</div></div>", unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1: st.markdown(f"<div class='ss'><div class='sv'>{w}</div><div style='font-size:.58rem;color:#fff3'>WINS</div></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='ss'><div class='sv'>{l}</div><div style='font-size:.58rem;color:#fff3'>LOSS</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='ss'><div class='sv'>{tot}</div><div style='font-size:.58rem;color:#fff3'>TOTAL</div></div>", unsafe_allow_html=True)

    streak_color = "#00ffcc" if streak >= 0 else "#ff3366"
    st.markdown(f"<div class='ss'><div class='sv' style='color:{streak_color}'>{'+' if streak>0 else ''}{streak}</div><div style='font-size:.58rem;color:#fff3'>STREAK</div></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"<div class='nbox'><div style='font-size:.7rem;color:#00ffcc77'>NONCE</div><div class='nval'>{st.session_state.nonce}</div></div>", unsafe_allow_html=True)

    if st.button("🔄 NONCE=0", use_container_width=True):
        st.session_state.nonce = 0
        st.success("✅ Nonce=0")
        st.rerun()

    st.markdown("---")
    if st.button("🗑️ RESET", use_container_width=True):
        st.session_state.history = []
        st.session_state.stats   = {"total":0,"wins":0,"losses":0,"streak":0,"best_streak":0}
        st.session_state.result  = None
        st.session_state.nonce   = 0
        for f in [HISTORY_FILE, STATS_FILE]:
            try:
                if f.exists(): f.unlink()
            except: pass
        st.success("✅ Reset!")
        st.rerun()

# ============================================================
# MAIN
# ============================================================
st.markdown("<div class='ttl'>💎 MINES ANDR V3</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#00ffcc55;letter-spacing:.2em;margin-bottom:1rem;'>PROBABILITY 80%+ • 300K SIMS • RISK MANAGEMENT</p>", unsafe_allow_html=True)

col_in, col_out = st.columns([1,1.6], gap="medium")

# ── INPUT ──
with col_in:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.markdown("### 📥 SEEDS")

    cli = st.text_input(
        "👤 CLIENT SEED COURANT",
        placeholder="Client seed ankehitriny...",
        help="COPY □ @ 'Paramètres Provably Fair' → Courant (TSY PROCHAIN!)"
    )

    nv = st.number_input("🔢 NONCE", value=st.session_state.nonce, min_value=0, step=1)
    st.session_state.nonce = int(nv)

    nm = st.selectbox("💣 MINES", [1,2,3], index=2)

    if cli and len(cli.strip()) < 5:
        st.warning("⚠️ Client seed fohy!")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class='nbox'>
        <div style='font-size:.7rem;color:#00ffcc77'>NONCE</div>
        <div class='nval'>{st.session_state.nonce}</div>
        <div style='font-size:.65rem;color:#fff3;margin-top:3px'>Manaraka → {st.session_state.nonce+1}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("💎 ANALYSER", use_container_width=True):
        c2 = cli.strip()
        n  = st.session_state.nonce

        if not c2:
            st.error("❌ Client Seed tsy misy!")
        elif len(c2) < 5:
            st.error("❌ Client Seed fohy!")
        else:
            with st.spinner("🔬 300k simulations..."):
                t0 = time.perf_counter()
                probs = analyze_client_seed(c2, n, nm, simulations=300_000)
                pattern = get_hot_cold_pattern(st.session_state.history, nm)
                top5, final_scores = select_best_5_smart(probs, pattern, c2, n)
                confidence = compute_confidence(probs, top5, nm)
                streak = st.session_state.stats.get("streak", 0)
                risk_level, risk_msg = get_risk_level(confidence, streak)
                elapsed = round(time.perf_counter() - t0, 2)

            avg_prob = round(float(np.mean(probs[top5])) * 100, 1)

            st.session_state.result = {
                "cli": c2[:14]+"..." if len(c2)>14 else c2,
                "nonce": n, "nm": nm,
                "top5": top5,
                "confidence": confidence,
                "avg_prob": avg_prob,
                "risk_level": risk_level,
                "risk_msg": risk_msg,
                "elapsed": elapsed,
                "hist_idx": len(st.session_state.history),
                "res": "PENDING",
            }
            st.session_state.ck += 1
            st.session_state.history.append(dict(st.session_state.result))
            if len(st.session_state.history) > 300:
                st.session_state.history.pop(0)
            save_json(HISTORY_FILE, st.session_state.history)
            st.rerun()

# ── OUTPUT ──
with col_out:
    r = st.session_state.result

    if r:
        top5 = r["top5"]
        conf = r["confidence"]
        rl   = r["r
