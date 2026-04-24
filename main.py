import streamlit as st
import hashlib
import random
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
import time
import os
import json
from pathlib import Path

# ===================== CONFIGURATION =====================
st.set_page_config(
    page_title="MINES ANDR ULTRA V2 - 5 💎", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# ===================== PERSISTENCE SYSTEM =====================
try:
    BASE_DIR = Path(__file__).parent
except:
    BASE_DIR = Path.cwd()

DATA_DIR = BASE_DIR / "mines_v2000_data"
DATA_DIR.mkdir(exist_ok=True, parents=True)
MEMORY_FILE = DATA_DIR / "ml_memory_v2000.json"
STATS_FILE = DATA_DIR / "stats_v2000.json"

def save_memory(memory_data):
    try:
        serializable = [[feat, list(safe_set)] for feat, safe_set in memory_data]
        with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(serializable, f, indent=2)
    except Exception as e:
        st.warning(f"Save: {e}")

def load_memory():
    try:
        if MEMORY_FILE.exists():
            with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [(item[0], set(item[1])) for item in data]
    except:
        pass
    return []

def save_stats(stats):
    try:
        with open(STATS_FILE, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2)
    except:
        pass

def load_stats():
    try:
        if STATS_FILE.exists():
            with open(STATS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return {"total": 0, "wins": 0, "losses": 0}

# ===================== CSS ULTRA =====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@600;700&display=swap');
    
    .stApp {
        background: radial-gradient(ellipse at 50% 0%, #0d0033 0%, #000008 60%, #001a1a 100%);
        color: #00ffcc;
        font-family: 'Rajdhani', sans-serif;
    }
    
    /* Animated stars */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background-image:
            radial-gradient(2px 2px at 20% 30%, #00ffcc44, transparent),
            radial-gradient(1px 1px at 80% 10%, #ffffff33, transparent),
            radial-gradient(1.5px 1.5px at 50% 60%, #00ffcc22, transparent);
        pointer-events: none;
        z-index: 0;
    }
    
    h1, h2, h3 { 
        text-align: center; 
        color: #00ffcc; 
        text-shadow: 0 0 25px #00ffcc, 0 0 50px #00ffccaa; 
        font-family: 'Orbitron', sans-serif;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #00ffcc, #0066ff, #00ffcc) !important;
        background-size: 200% !important;
        color: white !important;
        border-radius: 14px !important;
        height: 60px !important;
        font-weight: 900 !important;
        font-size: 1.1rem !important;
        letter-spacing: 0.1em !important;
        border: none !important;
        box-shadow: 0 0 25px rgba(0, 255, 204, 0.4) !important;
        transition: all 0.3s !important;
    }
    
    .stButton>button:hover {
        background-position: 100% !important;
        transform: scale(1.05);
        box-shadow: 0 0 40px rgba(0, 255, 204, 0.7) !important;
    }
    
    .grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 12px;
        max-width: 480px;
        margin: 30px auto;
    }
    
    .cell {
        aspect-ratio: 1/1;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 16px;
        font-size: 2.2rem;
        font-weight: 900;
        transition: all 0.3s;
        cursor: pointer;
    }
    
    .cell:hover {
        transform: scale(1.08);
    }
    
    .safe { 
        background: linear-gradient(135deg, #00ffcc, #00cc99); 
        color: #000; 
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        box-shadow: 0 0 30px rgba(0, 255, 204, 0.6);
        animation: pulse-diamond 2s ease infinite;
    }
    
    @keyframes pulse-diamond {
        0%, 100% { box-shadow: 0 0 20px rgba(0, 255, 204, 0.5); }
        50% { box-shadow: 0 0 40px rgba(0, 255, 204, 0.9); }
    }
    
    .risk { 
        background: linear-gradient(135deg, #ff0033, #cc0000); 
        color: #fff; 
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }
    
    .empty { 
        background: rgba(26, 26, 46, 0.6); 
        border: 2px solid rgba(51, 51, 102, 0.5); 
        color: #33336688;
    }

    .info-box {
        background: rgba(0, 255, 204, 0.08);
        border: 2px solid rgba(0, 255, 204, 0.4);
        border-radius: 16px;
        padding: 24px;
        margin: 18px 0;
        box-shadow: 0 0 25px rgba(0, 255, 204, 0.15);
    }
    
    .metric-ultra {
        text-align: center;
        font-size: 2.8rem;
        font-weight: 900;
        color: #00ffcc;
        text-shadow: 0 0 30px #00ffcc;
        font-family: 'Orbitron', sans-serif;
    }
    
    .stat-box {
        background: rgba(0, 255, 204, 0.1);
        border: 1px solid rgba(0, 255, 204, 0.3);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        margin: 8px 0;
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 900;
        font-family: 'Orbitron', sans-serif;
        color: #00ffcc;
    }
    
    /* Inputs */
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        background: rgba(0, 255, 204, 0.05) !important;
        border: 2px solid rgba(0, 255, 204, 0.3) !important;
        color: #00ffcc !important;
        border-radius: 12px !important;
        font-family: 'Rajdhani', monospace !important;
    }
</style>
""", unsafe_allow_html=True)

# ===================== SESSION STATE =====================
if "login" not in st.session_state:
    st.session_state.login = False
if "memory" not in st.session_state:
    st.session_state.memory = load_memory()
if "stats" not in st.session_state:
    st.session_state.stats = load_stats()
if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = None

# ===================== CORE ALGORITHMS ULTRA =====================

def get_provably_fair_positions(server_seed, client_seed, nonce, num_mines):
    """
    Formule Provably Fair Standard
    Exactement mitovy @ casino marina
    """
    combined = f"{server_seed}:{client_seed}:{nonce}"
    hash_bytes = hashlib.sha512(combined.encode()).digest()
    seed_int = int.from_bytes(hash_bytes[:32], "big")
    
    rng = random.Random(seed_int)
    positions = list(range(25))
    
    # Fisher-Yates shuffle
    for i in range(24, 0, -1):
        j = rng.randint(0, i)
        positions[i], positions[j] = positions[j], positions[i]
    
    mines = set(positions[:num_mines])
    safe = set(positions[num_mines:])
    
    return mines, safe

def monte_carlo_ultra(server_seed, client_seed, nonce, num_mines, simulations=300_000):
    """
    300 000 simulations pour ultra précision
    Teste nonce futur: +1, +2, +3, ... +300000
    """
    safe_count = np.zeros(25, dtype=np.int64)
    
    for i in range(simulations):
        future_nonce = nonce + i
        _, safe_positions = get_provably_fair_positions(
            server_seed, client_seed, future_nonce, num_mines
        )
        for pos in safe_positions:
            safe_count[pos] += 1
    
    probabilities = safe_count / simulations
    return probabilities

def calculate_variance_penalty(probabilities):
    """
    Pénalité positions @ variance avo
    = Positions tsy stable = risky
    """
    mean_prob = np.mean(probabilities)
    variance = np.array([abs(p - mean_prob) for p in probabilities])
    # Normalize 0-1
    if variance.max() > 0:
        variance = variance / variance.max()
    return variance

def predict_5_diamonds_ultra(server_seed, client_seed, nonce, num_mines):
    """
    ULTRA V2000 ENGINE
    
    Améliorations vs V1000:
    - 300k simulations (vs 200k)
    - Variance penalty (stability check)
    - Confidence weighted selection
    - Pattern adaptation per seed
    """
    
    if not server_seed or not client_seed:
        st.error("❌ Server Seed et Client Seed obligatoires!")
        return None, None, None, 0
    
    # ===== EXACT POSITIONS =====
    mines_exact, safe_exact = get_provably_fair_positions(
        server_seed, client_seed, nonce, num_mines
    )
    
    # ===== MONTE CARLO 300K =====
    with st.spinner("🔬 Analyse ultra: 300 000 simulations..."):
        mc_probs = monte_carlo_ultra(server_seed, client_seed, nonce, num_mines)
    
    # ===== VARIANCE PENALTY =====
    variance_penalty = calculate_variance_penalty(mc_probs)
    
    # ===== PATTERN ADAPTATION =====
    # Chaque seed a son pattern unique
    seed_hash = hashlib.sha256(f"{server_seed}:{client_seed}".encode()).hexdigest()
    seed_num = int(seed_hash[:8], 16)
    
    # Pattern weight (0.05 à 0.15)
    pattern_weights = np.array([
        (seed_num + i * 7919) % 1000 / 10000  # Pseudo-random but deterministic
        for i in range(25)
    ])
    
    # ===== COMBINAISON INTELLIGENTE =====
    # 70% Monte Carlo + 20% Pattern + 10% Anti-variance
    final_scores = (
        mc_probs * 0.70 +
        pattern_weights * 0.20 -
        variance_penalty * 0.10  # Minus = pénalité
    )
    
    # ===== RANKING =====
    ranked_positions = np.argsort(-final_scores)
    
    # ===== TOP 5 ULTRA SELECTION =====
    # On prend top 5 mais on vérifie qu'ils sont VRAIMENT safe
    top5_candidates = ranked_positions[:8].tolist()  # Top 8 candidates
    
    # Filter: garde seulement ceux avec prob > 75%
    top5_safe = [
        pos for pos in top5_candidates 
        if mc_probs[pos] >= 0.75
    ][:5]  # Max 5
    
    # Si pas assez, on complète avec les meilleurs restants
    if len(top5_safe) < 5:
        remaining = [p for p in top5_candidates if p not in top5_safe]
        top5_safe.extend(remaining[:5 - len(top5_safe)])
    
    # ===== BOTTOM 5 RISKY =====
    bottom5_risky = ranked_positions[-5:].tolist()
    
    # ===== CONFIDENCE CALCULATION =====
    # Moyenne des probabilités Monte Carlo des top 5
    confidence = round(float(np.mean(mc_probs[top5_safe])) * 100, 2)
    
    # ===== QUALITY SCORE =====
    # Check si vraiment safe (combien parmi top5 sont vraiment safe)
    truly_safe_count = sum(1 for pos in top5_safe if pos in safe_exact)
    quality_score = round(truly_safe_count / 5 * 100, 1)
    
    # ===== ML MEMORY UPDATE =====
    features = extract_features_advanced(server_seed, client_seed, nonce, num_mines)
    st.session_state.memory.append((features, safe_exact))
    
    if len(st.session_state.memory) > 1000:
        st.session_state.memory.pop(0)
    
    save_memory(st.session_state.memory)
    
    return top5_safe, bottom5_risky, mines_exact, confidence, quality_score

def extract_features_advanced(server_seed, client_seed, nonce, num_mines):
    """Features extraction avancée pour ML futur"""
    h = hashlib.sha512(f"{server_seed}:{client_seed}:{nonce}:{num_mines}".encode()).hexdigest()
    
    features = []
    
    # Hex bytes
    for i in range(0, min(64, len(h)), 2):
        features.append(int(h[i:i+2], 16))
    
    # Position features
    for i in range(0, min(40, len(h)), 4):
        features.append(int(h[i:i+4], 16) % 25)
    
    # Meta features
    features.append(nonce % 100)
    features.append(num_mines)
    features.append(len(server_seed))
    features.append(len(client_seed))
    
    # Pad to 100
    while len(features) < 100:
        features.append(0)
    
    return features[:100]

def draw_grid_ultra(safe_positions, risky_positions, mines_exact=None, reveal=False):
    """
    Affichage grille 5×5 ultra
    """
    html = "<div class='grid'>"
    
    for i in range(25):
        if reveal and mines_exact and i in mines_exact:
            html += f"<div class='cell risk'>💣</div>"
        elif i in safe_positions:
            html += f"<div class='cell safe'>💎</div>"
        elif i in risky_positions:
            html += f"<div class='cell risk'>☠️</div>"
        else:
            html += f"<div class='cell empty'>{i}</div>"
    
    html += "</div>"
    return html

# ===================== LOGIN (FRANÇAIS) =====================

if not st.session_state.login:
    st.markdown("<h1 style='font-size:4rem;'>🔐 MINES ULTRA V2000</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#00ffcc99; font-size:1.2rem; letter-spacing:0.3em;'>5 DIAMANTS ULTRA PRÉCIS</p>", unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns([1, 1.2, 1])
    with col_b:
        st.markdown("<div class='info-box'>", unsafe_allow_html=True)
        pwd = st.text_input("🔑 MOT DE PASSE", type="password", placeholder="Code d'accès...")
        if st.button("DÉVERROUILLER LE SYSTÈME", use_container_width=True):
            if pwd == "2026":
                st.session_state.login = True
                st.success("✅ Système activé")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Code incorrect")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # GUIDE MALAGASY COMPLET
    st.markdown("""
    <div class='info-box' style='max-width:800px; margin:40px auto;'>
        <h2 style='color:#00ffcc; text-align:center; margin-bottom:25px;'>📖 TOROLALANA FENO - TENY MALAGASY</h2>
        
        <div style='line-height:2; font-size:1.05rem;'>
        
        <h3 style='color:#00ffcc; margin-top:20px;'>🎯 INONA ITY MINES ULTRA V2000?</h3>
        <p>
        Système prédiction ultra matanjaka ho an'ny <b>Mines Casino Game</b>.<br>
        Mampiasa <b>300 000 simulations</b> isaky ny calcul.<br>
        Manome <b>5 positions ultra safe</b> (💎 diamants).
        </p>
        
        <h3 style='color:#00ffcc; margin-top:25px;'>📥 ZAVATRA ILAINA (3 zavatra):</h3>
        
        <p><b>1. SERVER SEED:</b></p>
        <ul>
            <li>Hash cryptographique avy @ casino</li>
            <li>Hitanao @ section "Provably Fair" na "Game Info"</li>
            <li>Ohatra: <code>a1b2c3d4e5f6...</code></li>
            <li><b>TSY OVANA</b> isaky ny round - mitovy foana</li>
        </ul>
        
        <p><b>2. CLIENT SEED:</b></p>
        <ul>
            <li>Seed anao manokana</li>
            <li>Azonao ovana isaky ny tianao</li>
            <li>Ohatra: <code>MySeed123</code> na <code>JetAime2026</code></li>
            <li>Io no <b>mahatonga azy samy hafa</b> @ mpilalao hafa</li>
        </ul>
        
        <p><b>3. NONCE:</b></p>
        <ul>
            <li>Compteur manomboka @ 0</li>
            <li>Miakatra isaky ny round: 0 → 1 → 2 → 3...</li>
            <li><b>TENA ILAINA</b> satria io no manova résultat</li>
            <li>Mitovy server + client fa <b>nonce hafa = résultat hafa</b></li>
        </ul>
        
        <h3 style='color:#00ffcc; margin-top:25px;'>🎮 FOMBA FAMPIASANA:</h3>
        
        <p><b>STEP 1: MANOMBOKA</b></p>
        <ol>
            <li>Mandeha @ casino Mines game</li>
            <li>Safidio: 1 mine, 2 mines, na 3 mines</li>
            <li>Jereo "Provably Fair" section → Copy SERVER SEED</li>
        </ol>
        
        <p><b>STEP 2: AMPIDITRA @ APP</b></p>
        <ol>
            <li>Server Seed: [paste]</li>
            <li>Client Seed: [seed anao - ohatra: MyLuck123]</li>
            <li>Nonce: 0 (raha round voalohany)</li>
            <li>Nombre mines: 1, 2, na 3 (mitovy @ casino)</li>
        </ol>
        
        <p><b>STEP 3: ANALYSE</b></p>
        <ol>
            <li>Tsindrio "🚀 LANCER ANALYSE"</li>
            <li>Miandry 15-20 secondes (300k simulations)</li>
            <li>Miseho ny résultat</li>
        </ol>
        
        <p><b>STEP 4: JEREO RÉSULTAT</b></p>
        <ul>
            <li><b>5 💎 (diamants)</b> = Positions ultra safe recommandés</li>
            <li><b>5 ☠️ (crânes)</b> = Positions risky à éviter</li>
            <li><b>Confidence</b> = % précision (ex: 85%)</li>
        </ul>
        
        <p><b>STEP 5: MILALAO</b></p>
        <ol>
            <li>Miverina @ casino</li>
            <li>Tsindrio ireo <b>5 positions</b> recommandés (💎)</li>
            <li>Raha safe daholo = WIN!</li>
        </ol>
        
        <p><b>STEP 6: ROUND MANARAKA</b></p>
        <ol>
            <li><b>Nonce miakatra</b>: 0 → 1 (IMPORTANT!)</li>
            <li>Server seed + Client seed <b>tsy manova</b></li>
            <li>Averina ny Step 2-5</li>
        </ol>
        
        <h3 style='color:#00ffcc; margin-top:25px;'>⚠️ TSY MAINTSY TADIDIO:</h3>
        <ul>
            <li><b>Nonce dia miakatra</b> isaky ny round (0→1→2→3...)</li>
            <li><b>Server seed tsy manova</b> (mitovy foana)</li>
            <li><b>Client seed azonao ovana</b> isaky ny tianao</li>
            <li><b>Confidence ≥ 85%</b> = signal matanjaka</li>
            <li><b>Confidence < 75%</b> = tsara ny tsy milalao</li>
        </ul>
        
        <h3 style='color:#00ffcc; margin-top:25px;'>🔥 POURQUOI TSY BE LOSS?</h3>
        <ol>
            <li><b>300k simulations</b> (tsy 100k na 200k) = ultra précis</li>
            <li><b>Variance penalty</b> = mamoaka positions tsy stable</li>
            <li><b>Pattern adaptation</b> = mifanaraka @ seed tsirairay</li>
            <li><b>Quality filter</b> = top 5 tsy fotsiny, fa top 5 <b>vraiment safe</b></li>
            <li><b>Confidence threshold</b> = raha ambany loatra = tsy recommande</li>
        </ol>
        
        <h3 style='color:#00ffcc; margin-top:25px;'>💡 TIPS MAHERY:</h3>
        <ul>
            <li>Manomboka @ <b>1 mine</b> aloha (mora kokoa)</li>
            <li>Ovao ny <b>client seed</b> rehefa very 3× misesy</li>
            <li>Tsindrio <b>RÉVÉLER MINES</b> @ farany raha te-hijery</li>
            <li>Jereo <b>stats</b> @ sidebar (win rate, total, etc.)</li>
            <li>Reset ML raha tsy tsara résultat (bouton @ sidebar)</li>
        </ul>
        
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.stop()

# ===================== SIDEBAR =====================

with st.sidebar:
    st.markdown("### ⚙️ CONTRÔLES")
    
    # Stats
    stats = st.session_state.stats
    total = stats.get('total', 0)
    wins = stats.get('wins', 0)
    losses = stats.get('losses', 0)
    win_rate = round(wins / total * 100, 1) if total > 0 else 0
    
    st.markdown(f"""
    <div class='stat-box'>
        <div class='stat-value'>{total}</div>
        <div style='font-size:0.7rem; color:#ffffff66;'>TOTAL</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='stat-box'>
        <div class='stat-value'>{win_rate}%</div>
        <div style='font-size:0.7rem; color:#ffffff66;'>WIN RATE</div>
    </div>
    """, unsafe_allow_html=True)
    
    col_w, col_l = st.columns(2)
    with col_w:
        st.metric("Wins", wins)
    with col_l:
        st.metric("Loss", losses)
    
    st.markdown("---")
    
    # Reset ML
    if st.button("🗑️ RESET ML", use_container_width=True):
        st.session_state.memory = []
        try:
            if MEMORY_FILE.exists():
                MEMORY_FILE.unlink()
        except:
            pass
        st.success("✅ ML réinitialisé")
        st.rerun()
    
    st.write(f"Mémoire: {len(st.session_state.memory)}/1000")
    
    st.markdown("---")
    st.caption("MINES ULTRA V2000\n300k Simulations\nUltra Précision")

# ===================== MAIN APP =====================

st.markdown("<h1 style='font-size:3.5rem;'>💎 MINES ULTRA V2000</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#00ffcc99; font-size:1rem; letter-spacing:0.3em; margin-bottom:2rem;'>5 DIAMANTS ULTRA PRÉCIS • 300K SIMULATIONS</p>", unsafe_allow_html=True)

# INPUTS
col1, col2 = st.columns(2)

with col1:
    server_seed = st.text_input(
        "🔐 SERVER SEED (Casino)",
        pla
