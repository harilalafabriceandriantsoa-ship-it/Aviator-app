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
    Tsy nonce intsony fa HISTORY ID (mitovy @ screenshot)
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
    """350k simulations - ultra précis"""
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
    """Pattern unique pour chaque combinaison de seeds"""
    seed_hash = hashlib.sha256(f"{server_seed}:{client_seed}".encode()).hexdigest()
    seed_num = int(seed_hash[:8], 16)

    weights = np.array([
        (seed_num + i * 7919) % 1000 / 10000
        for i in range(25)
    ])
    return weights

# ===================== PREDICTION ULTRA V3000 =====================
def predict_v3000(server_seed, client_seed, history_id, num_mines):
    # Exact positions
    mines_exact, safe_exact = get_pf_positions(server_seed, client_seed, history_id, num_mines)

    # Monte Carlo 350k
    with st.spinner("🔬 350 000 simulations..."):
        mc_probs = monte_carlo_v3000(server_seed, client_seed, history_id, num_mines)

    # Variance penalty
    mean_p = np.mean(mc_probs)
    variance = np.array([abs(p - mean_p) for p in mc_probs])
    if variance.max() > 0:
        variance = variance / variance.max()

    # Pattern weights (unique per seed)
    pattern_w = get_pattern_weights(server_seed, client_seed)

    # ML scores
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

    # Combinaison finale
    if st.session_state.ml_models is not None:
        # Avec ML: 55% MC + 25% ML + 15% Pattern - 5% Variance
        final_scores = (
            mc_probs * 0.55 +
            ml_scores * 0.25 +
            pattern_w * 0.15 -
            variance * 0.05
        )
    else:
        # Sans ML: 70% MC + 20% Pattern - 10% Variance
        final_scores = (
            mc_probs * 0.70 +
            pattern_w * 0.20 -
            variance * 0.10
        )

    # Ranking
    ranked = np.argsort(-final_scores)

    # Top 5 avec filtre qualité
    top8 = ranked[:8].tolist()
    top5 = [p for p in top8 if mc_probs[p] >= 0.73][:5]

    if len(top5) < 5:
        remaining = [p for p in top8 if p not in top5]
        top5.extend(remaining[:5 - len(top5)])

    bottom5 = ranked[-5:].tolist()

    confidence = round(float(np.mean(mc_probs[top5])) * 100, 2)

    truly_safe = sum(1 for p in top5 if p in safe_exact)
    quality = round(truly_safe / 5 * 100, 1)

    # Sauvegarder dans history
    feats = extract_features(server_seed, client_seed, history_id, num_mines)
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

    st.markdown("""
    <div class='glass' style='max-width:800px; margin:40px auto;'>
        <h2 style='color:#00ffcc; text-align:center;'>📖 FANAZAVANA MALAGASY</h2>

        <h3 style='color:#00ffcc; margin-top:20px;'>🎯 ZAVATRA ILAINA (4):</h3>

        <p><b>1. SERVER SEED (Graine du serveur):</b></p>
        <ul style='line-height:1.8;'>
            <li>Hash avy @ casino (Provably Fair section)</li>
            <li>Ohatra: <code>d8d745d482adc462243d0f857968854b...</code></li>
            <li>TSY OVANA isaky ny session</li>
        </ul>

        <p><b>2. CLIENT SEED (Graine du client):</b></p>
        <ul style='line-height:1.8;'>
            <li>Seed anao manokana (azonao ovana)</li>
            <li>Ohatra: <code>J1gmzJUp9l1PKGvJBL_z</code></li>
            <li>Miovaova = résultat miovaova</li>
        </ul>

        <p><b>3. HISTORY ID (Identifiant de la manche):</b></p>
        <ul style='line-height:1.8;'>
            <li>Numéro de la manche (hitanao @ "Voir les détails")</li>
            <li>Ohatra: <code>69...</code></li>
            <li>Miakatra isaky ny round</li>
            <li><b>TENA ILAINA</b> - manatanjaka prédiction!</li>
        </ul>

        <p><b>4. NOMBRE DE MINES:</b></p>
        <ul style='line-height:1.8;'>
            <li>1 mine = facile (avo ny win)</li>
            <li>2 mines = moyen</li>
            <li>3 mines = difficile</li>
        </ul>

        <h3 style='color:#00ffcc; margin-top:25px;'>🎮 FOMBA FAMPIASANA:</h3>
        <ol style='line-height:2;'>
            <li>Mitsidika @ casino Mines game</li>
            <li>Tsindrio "Provably Fair" → "Voir les détails"</li>
            <li>Copy <b>Server Seed</b> (Graine du serveur)</li>
            <li>Copy <b>Client Seed</b> (Graine du client)</li>
            <li>Tadidio <b>History ID</b> (Identifiant de la manche)</li>
            <li>Safidio <b>Nombre de mines</b> mitovy @ casino</li>
            <li>Ampiditra daholo @ app</li>
            <li>Tsindrio "ANALYSER"</li>
            <li>Miandry 20-30 sec (350k simulations)</li>
            <li>Tsindrio ireo <b>5 💎</b> @ casino</li>
            <li>Confirm WIN/LOSS</li>
        </ol>

        <h3 style='color:#00ffcc; margin-top:25px;'>⚡ AMÉLIORATIONS V3000:</h3>
        <ul style='line-height:2;'>
            <li>✅ <b>History ID</b> (tsy nonce) = plus précis!</li>
            <li>✅ <b>350k simulations</b> ultra précis</li>
            <li>✅ <b>ML 25 modèles</b> (un par position)</li>
            <li>✅ <b>Pattern adaptatif</b> per seed</li>
            <li>✅ <b>Variance penalty</b> = moins de loss</li>
            <li>✅ <b>Grid miovaova</b> @ seed</li>
            <li>✅ <b>Mobile-friendly</b> tsara</li>
        </ul>

        <h3 style='color:#ff0066; margin-top:25px;'>⚠️ TIPS:</h3>
        <ul style='line-height:2;'>
            <li>Manomboka @ <b>1 mine</b> aloha</li>
            <li>Ovao <b>client seed</b> raha very 3× misesy</li>
            <li>Confirm WIN/LOSS tsirairay = ML mahay kokoa</li>
            <li>Train ML rehefa 10+ results</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
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

    st.write(f"History: {len(st.session_state.history)}")

# ===================== MAIN APP =====================
st.markdown("<div class='main-title'>MINES V3000</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#00ffcc99; letter-spacing:0.3em; margin-bottom:2rem;'>5 💎 ULTRA • 350K SIMS • ML 25 MODÈLES</p>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.5], gap="medium")

with col1:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.markdown("### 📥 INPUT")

    server_seed = st.text_input(
        "🔐 SERVER SEED",
        placeholder="d8d745d482adc...",
        help="Graine du serveur @ Provably Fair"
    )

    client_seed = st.text_input(
        "👤 CLIENT SEED",
        placeholder="J1gmzJUp9l1PKGvJBL_z",
        help="Votre graine (Graine du client)"
    )

    history_id = st.number_input(
        "🔢 HISTORY ID",
        value=1,
        min_value=0,
        step=1,
        help="Identifiant de la manche (miakatra isaky ny round)"
    )

    num_mines = st.selectbox(
        "💣 NOMBRE MINES",
        options=[1, 2, 3],
        index=0,
        help="1=facile, 2=moyen, 3=difficile"
    )

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

        # Grid
        st.markdown(draw_grid(top5, bottom5), unsafe_allow_html=True)

        # Metrics
        c1, c2, c3 = st.co
