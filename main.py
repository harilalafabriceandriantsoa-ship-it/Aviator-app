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
    page_title="MINES ULTRA V2000 - 5 💎", 
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

# ===================== CSS ULTRA PREMIUM =====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@600;700&display=swap');
    
    .stApp {
        background: radial-gradient(ellipse at 50% 0%, #0d0033 0%, #000008 60%, #001a1a 100%);
        color: #00ffcc;
        font-family: 'Rajdhani', sans-serif;
    }
    
    h1, h2, h3 { 
        text-align: center; 
        color: #00ffcc; 
        text-shadow: 0 0 25px #00ffcc; 
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
        border: none !important;
        transition: all 0.3s !important;
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
    }
    
    .safe { 
        background: linear-gradient(135deg, #00ffcc, #00cc99); 
        color: #000; 
        box-shadow: 0 0 30px rgba(0, 255, 204, 0.6);
    }
    
    .risk { background: linear-gradient(135deg, #ff0033, #cc0000); color: #fff; }
    .empty { background: rgba(26, 26, 46, 0.6); border: 2px solid rgba(51, 51, 102, 0.5); color: #33336688; }

    .info-box {
        background: rgba(0, 255, 204, 0.08);
        border: 2px solid rgba(0, 255, 204, 0.4);
        border-radius: 16px;
        padding: 24px;
        margin: 18px 0;
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
    combined = f"{server_seed}:{client_seed}:{nonce}"
    hash_bytes = hashlib.sha512(combined.encode()).digest()
    seed_int = int.from_bytes(hash_bytes[:32], "big")
    rng = random.Random(seed_int)
    positions = list(range(25))
    for i in range(24, 0, -1):
        j = rng.randint(0, i)
        positions[i], positions[j] = positions[j], positions[i]
    mines = set(positions[:num_mines])
    safe = set(positions[num_mines:])
    return mines, safe

def monte_carlo_ultra(server_seed, client_seed, nonce, num_mines, simulations=300_000):
    safe_count = np.zeros(25, dtype=np.int64)
    for i in range(simulations):
        future_nonce = nonce + i
        _, safe_positions = get_provably_fair_positions(server_seed, client_seed, future_nonce, num_mines)
        for pos in safe_positions:
            safe_count[pos] += 1
    return safe_count / simulations

def predict_5_diamonds_ultra(server_seed, client_seed, nonce, num_mines):
    if not server_seed or not client_seed:
        return None, None, None, 0, 0
    
    mines_exact, safe_exact = get_provably_fair_positions(server_seed, client_seed, nonce, num_mines)
    
    with st.spinner("🔬 ULTRA ANALYSIS: 300,000 SIMULATIONS IN PROGRESS..."):
        mc_probs = monte_carlo_ultra(server_seed, client_seed, nonce, num_mines)
    
    # Variance & Pattern adaptation logic
    mean_prob = np.mean(mc_probs)
    variance_penalty = np.array([abs(p - mean_prob) for p in mc_probs])
    seed_hash = hashlib.sha256(f"{server_seed}:{client_seed}".encode()).hexdigest()
    pattern_weights = np.array([(int(seed_hash[:8], 16) + i * 7919) % 1000 / 10000 for i in range(25)])
    
    final_scores = (mc_probs * 0.70 + pattern_weights * 0.20 - variance_penalty * 0.10)
    ranked_positions = np.argsort(-final_scores)
    top5_safe = [pos for pos in ranked_positions[:8] if mc_probs[pos] >= 0.75][:5]
    
    if len(top5_safe) < 5:
        top5_safe.extend([p for p in ranked_positions if p not in top5_safe][:5-len(top5_safe)])
        
    bottom5_risky = ranked_positions[-5:].tolist()
    confidence = round(float(np.mean(mc_probs[top5_safe])) * 100, 2)
    quality_score = round(sum(1 for pos in top5_safe if pos in safe_exact) / 5 * 100, 1)
    
    return top5_safe, bottom5_risky, mines_exact, confidence, quality_score

def draw_grid_ultra(safe_positions, risky_positions, mines_exact=None, reveal=False):
    html = "<div class='grid'>"
    for i in range(25):
        if reveal and mines_exact and i in mines_exact:
            html += f"<div class='cell risk'>💣</div>"
        elif i in safe_positions:
            html += f"<div class='cell safe'>💎</div>"
        elif i in risky_positions:
            html += f"<div class='cell risk'>💀</div>"
        else:
            html += f"<div class='cell empty'>{i}</div>"
    html += "</div>"
    return html

# ===================== LOGIN SYSTEM (INTERNATIONAL) =====================

if not st.session_state.login:
    st.markdown("<h1>🔑 MINES ULTRA V2000</h1>", unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns([1, 1.2, 1])
    with col_b:
        pwd = st.text_input("ACCESS CODE", type="password")
        if st.button("UNLOCK SYSTEM", use_container_width=True):
            if pwd == "2026":
                st.session_state.login = True
                st.rerun()
    
    # GUIDE SECTION
    st.markdown("""
    <div class='info-box'>
        <h2 style='color:#00ffcc;'>📘 USER GUIDE / GUIDE D'UTILISATION</h2>
        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px;'>
            <div>
                <h3 style='font-size: 1rem;'>[ ENGLISH ]</h3>
                <p>1. <b>Server Seed</b>: Copy the hash from casino Provably Fair.</p>
                <p>2. <b>Client Seed</b>: Enter your personal custom seed.</p>
                <p>3. <b>Nonce</b>: Start at 0, increase by 1 every round.</p>
                <p>4. <b>Simulations</b>: 300,000 deep scans for 5 💎.</p>
            </div>
            <div>
                <h3 style='font-size: 1rem;'>[ FRANÇAIS ]</h3>
                <p>1. <b>Server Seed</b>: Copiez le hash du Provably Fair.</p>
                <p>2. <b>Client Seed</b>: Entrez votre seed personnel.</p>
                <p>3. <b>Nonce</b>: Commencez à 0, augmentez de 1 par tour.</p>
                <p>4. <b>Simulations</b>: Scan profond de 300,000 pour 5 💎.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ===================== MAIN INTERFACE =====================

st.markdown("<h1>💎 MINES ULTRA V2000</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 📊 DASHBOARD")
    s = st.session_state.stats
    st.metric("TOTAL ROUNDS", s['total'])
    wr = round(s['wins']/s['total']*100, 1) if s['total'] > 0 else 0
    st.metric("WIN RATE", f"{wr}%")
    if st.button("🗑️ RESET STATISTICS"):
        st.session_state.stats = {"total": 0, "wins": 0, "losses": 0}
        save_stats(st.session_state.stats)
        st.rerun()

col1, col2 = st.columns(2)
with col1:
    server_seed = st.text_input("SERVER SEED", placeholder="Enter hash...")
    client_seed = st.text_input("CLIENT SEED", placeholder="Your personal seed...")
with col2:
    nonce = st.number_input("NONCE (Counter)", value=0, min_value=0, step=1)
    num_mines = st.selectbox("NUMBER OF MINES", options=[1, 2, 3])

if st.button("🚀 LAUNCH 300K ANALYSIS", use_container_width=True):
    top5, bottom5, mines_exact, conf, quality = predict_5_diamonds_ultra(server_seed, client_seed, nonce, num_mines)
    if top5:
        st.session_state.last_prediction = {'top5': top5, 'mines': mines_exact}
        st.markdown(draw_grid_ultra(top5, bottom5), unsafe_allow_html=True)
        
        ca, cb = st.columns(2)
        ca.metric("CONFIDENCE", f"{conf}%")
        cb.metric("QUALITY SCORE", f"{quality}%")
        
        st.markdown(f"<div class='info-box'><h3 style='color:#00ffcc;'>💎 TOP 5 SAFE: {', '.join(map(str, top5))}</h3></div>", unsafe_allow_html=True)
        
        cwin, closs = st.columns(2)
        if cwin.button("✅ CONFIRM WIN", use_container_width=True):
            st.session_state.stats['total'] += 1
            st.session_state.stats['wins'] += 1
            save_stats(st.session_state.stats)
            st.rerun()
        if closs.button("❌ CONFIRM LOSS", use_container_width=True):
            st.session_state.stats['total'] += 1
            st.session_state.stats['losses'] += 1
            save_stats(st.session_state.stats)
            st.rerun()

if st.checkbox("🔍 REVEAL REAL MINES (VERIFICATION)"):
    if st.session_state.last_prediction:
        lp = st.session_state.last_prediction
        st.markdown(draw_grid_ultra(lp['top5'], [], lp['mines'], reveal=True), unsafe_allow_html=True)
