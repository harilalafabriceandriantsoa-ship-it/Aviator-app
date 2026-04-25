import streamlit as st
import hashlib
import random
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
import pickle
import time
import json
from pathlib import Path

# ===================== CONFIG =====================
st.set_page_config(
    page_title="MINES DIAMOND V3000",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===================== PERSISTENCE =====================
try:
    DATA_DIR = Path(__file__).parent / "mines_v3000_data"
except:
    DATA_DIR = Path.cwd() / "mines_v3000_data"

DATA_DIR.mkdir(exist_ok=True, parents=True)
HISTORY_FILE  = DATA_DIR / "history.json"
STATS_FILE    = DATA_DIR / "stats.json"
ML_FILE       = DATA_DIR / "ml_models.pkl"

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

def save_ml_models(models):
    try:
        with open(ML_FILE, 'wb') as f:
            pickle.dump(models, f)
    except: pass

def load_ml_models():
    try:
        if ML_FILE.exists():
            with open(ML_FILE, 'rb') as f:
                return pickle.load(f)
    except: pass
    return None

# ===================== CSS MOBILE-FRIENDLY =====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@600;700&display=swap');

    .stApp {
        background: radial-gradient(ellipse at 50% 0%, #0d0033 0%, #000008 60%, #001a1a 100%);
        color: #00ffcc;
        font-family: 'Rajdhani', sans-serif;
    }

    .main-title {
        font-family: 'Orbitron', sans-serif;
        font-size: clamp(2rem, 8vw, 3.5rem);
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #00ffcc, #0066ff, #00ffcc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .glass {
        background: rgba(5, 0, 20, 0.9);
        border: 2px solid rgba(0,255,204,0.4);
        border-radius: 20px;
        padding: clamp(15px, 5vw, 25px);
        backdrop-filter: blur(12px);
        margin-bottom: 20px;
    }

    /* GRID 5x5 */
    .grid-wrap {
        display: flex;
        justify-content: center;
        margin: 20px auto;
    }

    .grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: clamp(6px, 2vw, 12px);
        width: min(480px, 95vw);
    }

    .cell {
        aspect-ratio: 1/1;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 14px;
        font-size: clamp(1.4rem, 5vw, 2.2rem);
        font-weight: 900;
        transition: all 0.3s;
    }

    .cell:hover { transform: scale(1.08); }

    .safe {
        background: linear-gradient(135deg, #00ffcc, #00cc88);
        color: #000;
        box-shadow: 0 0 20px rgba(0,255,204,0.6);
        animation: pulse-safe 2s ease infinite;
    }

    @keyframes pulse-safe {
        0%,100% { box-shadow: 0 0 15px rgba(0,255,204,0.5); }
        50% { box-shadow: 0 0 35px rgba(0,255,204,0.9); }
    }

    .risk {
        background: linear-gradient(135deg, #ff0033, #cc0000);
        color: #fff;
    }

    .empty {
        background: rgba(20, 20, 50, 0.6);
        border: 2px solid rgba(51,51,102,0.5);
        color: #33336688;
    }

    .metric-ultra {
        text-align: center;
        font-size: clamp(2rem, 8vw, 2.8rem);
        font-weight: 900;
        color: #00ffcc;
        font-family: 'Orbitron', sans-serif;
    }

    .stButton>button {
        background: linear-gradient(135deg, #00ffcc, #0066ff) !important;
        color: white !important;
        font-weight: 900 !important;
        border-radius: 12px !important;
        height: 55px !important;
        font-size: 1rem !important;
        border: none !important;
        width: 100%;
    }

    .stTextInput input, .stNumberInput input, .stSelectbox select {
        background: rgba(0,255,204,0.05) !important;
        border: 2px solid rgba(0,255,204,0.3) !important;
        color: #00ffcc !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
        padding: 12px !important;
    }

    @media (max-width: 768px) {
        .stApp { padding: 8px !important; }
        .glass { padding: 12px !important; }
    }
</style>
""", unsafe_allow_html=True)

# ===================== SESSION STATE =====================
if "login" not in st.session_state:
    st.session_state.login = False
if "history" not in st.session_state:
    st.session_state.history = load_json(HISTORY_FILE, [])
if "stats" not in st.session_state:
    st.session_state.stats = load_json(STATS_FILE, {"total": 0, "wins": 0, "losses": 0})
if "last_pred" not in st.session_state:
    st.session_state.last_pred = None
if "ml_models" not in st.session_state:
    st.session_state.ml_models = load_ml_models()

# ===================== PROVABLY FAIR =====================
def get_pf_positions(server_seed, client_seed, history_id, num_mines):
    """
    Provably Fair: server_seed + client_seed + history_id
    """
    combined = f"{server_seed}:{client_seed}:{history_id}"
    hash_bytes = hashlib.sha512(combined.encode()).digest()
    seed_int = int.from_bytes(hash_bytes[:32], "big")

    rng = random.Random(seed_int)
    positions = list(range(25))

    for i in range(24, 0, -1):
        j = rng.randint(0, i)
        positions[i], positions[j] = positions[j], positions[i]

    mines = set(positions[:num_mines])
    safe  = set(positions[num_mines:])
    return mines, safe

# ===================== MONTE CARLO =====================
def monte_carlo_v3000(server_seed, client_seed, history_id, num_mines, simulations=350_000):
    safe_count = np.zeros(25, dtype=np.int64)

    for i in range(simulations):
        future_id = history_id + i
        _, safe_pos = get_pf_positions(server_seed, client_seed, future_id, num_mines)
        for pos in safe_pos:
            safe_count[pos] += 1

    return safe_count / simulations

# ===================== ML TRAINING =====================
def train_ml_models():
    labeled = [h for h in st.session_state.history if h.get('result') in ['WIN', 'LOSS']]

    if len(labeled) < 10:
        return None

    X_all = []
    y_positions = [[] for _ in range(25)]

    for h in labeled:
        feats = extract_features(h['server_seed'], h['client_seed'], h['history_id'], h['num_mines'])
        X_all.append(feats)

        safe_set = set(h.get('safe_exact', []))
        for pos in range(25):
            y_positions[pos].append(1 if pos in safe_set else 0)

    X = np.array(X_all)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    models = []
    for pos in range(25):
        y = np.array(y_positions[pos])
        if len(set(y)) < 2:
            models.append(None)
            continue
        try:
            clf = GradientBoostingClassifier(
                n_estimators=200, max_depth=5,
                learning_rate=0.08, random_state=42
            )
            clf.fit(X_scaled, y)
            models.append(clf)
        except:
            models.append(None)

    result = {'models': models, 'scaler': scaler}
    save_ml_models(result)
    return result

# ===================== FEATURE EXTRACTION =====================
def extract_features(server_seed, client_seed, history_id, num_mines):
    h = hashlib.sha512(f"{server_seed}:{client_seed}:{history_id}:{num_mines}".encode()).hexdigest()

    features = []
    for i in range(0, min(64, len(h)), 2):
        features.append(int(h[i:i+2], 16))

    for i in range(0, min(40, len(h)), 4):
        features.append(int(h[i:i+4], 16) % 25)

    features.append(history_id % 1000)
    features.append(num_mines)
    features.append(len(server_seed) % 50)
    features.append(len(client_seed) % 50)

    while len(features) < 100:
        features.append(0)

    return features[:100]

# ===================== PATTERN ADAPTATION =====================
def get_pattern_weights(server_seed, client_seed):
    seed_hash = hashlib.sha256(f"{server_seed}:{client_seed}".encode()).hexdigest()
    seed_num = int(seed_hash[:8], 16)

    weights = np.array([
        (seed_num + i * 7919) % 1000 / 10000
        for i in range(25)
    ])
    return weights

# ===================== PREDICTION ULTRA V3000 =====================
def predict_v3000(server_seed, client_seed, history_id, num_mines):
    mines_exact, safe_exact = get_pf_positions(server_seed, client_seed, history_id, num_mines)

    with st.spinner("🔬 350 000 simulations..."):
        mc_probs = monte_carlo_v3000(server_seed, client_seed, history_id, num_mines)

    mean_p = np.mean(mc_probs)
    variance = np.array([abs(p - mean_p) for p in mc_probs])
    if variance.max() > 0:
        variance = variance / variance.max()

    pattern_w = get_pattern_weights(server_seed, client_seed)

    ml_scores = np.zeros(25)
    if st.session_state.ml_models is not None:
        try:
            feats = extract_features(server_seed, client_seed, history_id, num_mines)
            feats_arr = np.array(feats).reshape(1, -1)
            feats_scaled = st.session_state.ml_models['scaler'].transform(feats_arr)

            for pos, clf in enumerate(st.session_state.ml_models['models']):
                if clf is not None:
                    prob = clf.predict_proba(feats_scaled)[0][1]
                    ml_scores[pos] = prob
        except:
            pass

    if st.session_state.ml_models is not None:
        final_scores = (
            mc_probs * 0.55 +
            ml_scores * 0.25 +
            pattern_w * 0.15 -
            variance * 0.05
        )
    else:
        final_scores = (
            mc_probs * 0.70 +
            pattern_w * 0.20 -
            variance * 0.10
        )

    ranked = np.argsort(-final_scores)

    top8 = ranked[:8].tolist()
    top5 = [p for p in top8 if mc_probs[p] >= 0.73][:5]

    if len(top5) < 5:
        remaining = [p for p in top8 if p not in top5]
        top5.extend(remaining[:5 - len(top5)])

    bottom5 = ranked[-5:].tolist()

    confidence = round(float(np.mean(mc_probs[top5])) * 100, 2)
    truly_safe = sum(1 for p in top5 if p in safe_exact)
    quality = round(truly_safe / 5 * 100, 1)

    history_entry = {
        'server_seed': server_seed[:10] + '...',
        'client_seed': client_seed,
        'history_id': history_id,
        'num_mines': num_mines,
        'top5': top5,
        'confidence': confidence,
        'quality': quality,
        'safe_exact': list(safe_exact),
        'result': 'PENDING'
    }
    st.session_state.history.append(history_entry)
    if len(st.session_state.history) > 500:
        st.session_state.history.pop(0)
    save_json(HISTORY_FILE, st.session_state.history)

    return top5, bottom5, mines_exact, confidence, quality

# ===================== GRID =====================
def draw_grid(safe_pos, risky_pos, mines_exact=None, reveal=False):
    html = "<div class='grid-wrap'><div class='grid'>"
    for i in range(25):
        if reveal and mines_exact and i in mines_exact:
            html += "<div class='cell risk'>💣</div>"
        elif i in safe_pos:
            html += "<div class='cell safe'>💎</div>"
        elif i in risky_pos:
            html += "<div class='cell risk'>☠️</div>"
        else:
            html += f"<div class='cell empty'>{i}</div>"
    html += "</div></div>"
    return html

# ===================== LOGIN =====================
if not st.session_state.login:
    st.markdown("<div class='main-title'>MINES V3000</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#00ffcc99; letter-spacing:0.3em;'>5 💎 DIAMOND ULTRA</p>", unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns([1, 1.2, 1])
    with col_b:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        pwd = st.text_input("🔑 PASSWORD", type="password", placeholder="2026")
        if st.button("ACTIVATE", use_container_width=True):
            if pwd == "2026":
                st.session_state.login = True
                st.rerun()
            else:
                st.error("❌ Incorrect")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ===================== SIDEBAR =====================
with st.sidebar:
    st.markdown("### ⚙️ STATS V3000")

    stats = st.session_state.stats
    total = stats.get('total', 0)
    wins = stats.get('wins', 0)
    losses = stats.get('losses', 0)
    wr = round(wins / total * 100, 1) if total > 0 else 0

    st.metric("WIN RATE", f"{wr}%")
    col_w, col_l = st.columns(2)
    with col_w: st.metric("Wins", wins)
    with col_l: st.metric("Loss", losses)
    st.metric("Total", total)

    if st.session_state.ml_models is not None:
        st.success("✅ ML ACTIF")
    else:
        labeled = len([h for h in st.session_state.history if h.get('result') in ['WIN', 'LOSS']])
        st.warning(f"🔄 ML: {labeled}/10")

    st.markdown("---")

    if st.button("🧠 TRAIN ML", use_container_width=True):
        result = train_ml_models()
        if result is not None:
            st.session_state.ml_models = result
            st.success("✅ ML trained!")
        else:
            st.warning("Besoin 10+ résultats")
        st.rerun()

    if st.button("🗑️ RESET DATA", use_container_width=True):
        st.session_state.history = []
        st.session_state.stats = {"total": 0, "wins": 0, "losses": 0}
        st.session_state.ml_models = None
        st.session_state.last_pred = None
        for f in [HISTORY_FILE, STATS_FILE, ML_FILE]:
            try:
                if f.exists():
                    f.unlink()
            except: pass
        st.success("✅ Reset!")
        st.rerun()

# ===================== MAIN APP =====================
st.markdown("<div class='main-title'>MINES V3000</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#00ffcc99; letter-spacing:0.3em; margin-bottom:2rem;'>5 💎 ULTRA • 350K SIMS • ML 25 MODÈLES</p>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.5], gap="medium")

with col1:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.markdown("### 📥 INPUT")

    server_seed = st.text_input("🔐 SERVER SEED", placeholder="d8d745d482adc...")
    client_seed = st.text_input("👤 CLIENT SEED", placeholder="J1gmzJUp9l1PKGvJBL_z")
    history_id = st.number_input("🔢 HISTORY ID", value=1, min_value=0, step=1)
    num_mines = st.selectbox("💣 NOMBRE MINES", options=[1, 2, 3], index=0)

    if st.button("🚀 ANALYSER ULTRA", use_container_width=True):
        if server_seed and client_seed:
            start = time.time()
            top5, bottom5, mines_exact, conf, quality = predict_v3000(
                server_seed, client_seed, int(history_id), num_mines
            )
            elapsed = round(time.time() - start, 1)

            st.session_state.last_pred = {
                'top5': top5,
                'bottom5': bottom5,
                'mines': list(mines_exact),
                'conf': conf,
                'quality': quality,
                'elapsed': elapsed,
                'idx': len(st.session_state.history) - 1
            }
            st.rerun()
        else:
            st.error("Server Seed et Client Seed obligatoires")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    pred = st.session_state.last_pred

    if pred:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)

        top5    = pred['top5']
        bottom5 = pred['bottom5']

        # Fanatsarana ny fizarana eo amin'ny tabilao
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f"<div style='text-align:center;color:#00ffcc;'>CONFIDENCE<br><b>{pred['conf']}%</b></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div style='text-align:center;color:#00ffcc;'>QUALITÉ<br><b>{pred['quality']}%</b></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div style='text-align:center;color:#00ffcc;'>TEMPS<br><b>{pred['elapsed']}s</b></div>", unsafe_allow_html=True)

        # Grid
        st.markdown(draw_grid(top5, bottom5), unsafe_allow_html=True)

        # Bokotra valiny
        st.markdown("<hr style='border-color:rgba(0,255,204,0.2);'>", unsafe_allow_html=True)
        btn1, btn2 = st.columns(2)
        
        with btn1:
            if st.button("✅ WIN", use_container_width=True):
                st.session_state.history[pred['idx']]['result'] = 'WIN'
                save_json(HISTORY_FILE, st.session_state.history)
                st.session_state.stats['total'] += 1
                st.session_state.stats['wins'] += 1
                save_json(STATS_FILE, st.session_state.stats)
                st.session_state.last_pred = None
                st.rerun()
                
        with btn2:
            if st.button("❌ LOSS", use_container_width=True):
                st.session_state.history[pred['idx']]['result'] = 'LOSS'
                save_json(HISTORY_FILE, st.session_state.history)
                st.session_state.stats['total'] += 1
                st.session_state.stats['losses'] += 1
                save_json(STATS_FILE, st.session_state.stats)
                st.session_state.last_pred = None
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
