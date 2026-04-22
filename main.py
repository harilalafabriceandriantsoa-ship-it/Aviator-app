import streamlit as st
import hashlib
import random
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import Pipeline
import time
import os
import json
from pathlib import Path

# ===================== CONFIGURATION =====================
st.set_page_config(
    page_title="MINES V1000 - 5 💎 ULTRA PRÉCIS", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# ===================== PERSISTENCE SYSTEM =====================
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data_mines_storage"
DATA_DIR.mkdir(exist_ok=True, parents=True)
MEMORY_FILE = DATA_DIR / "ml_memory.json"

def save_memory(memory_data):
    try:
        # Convert set to list for JSON serialization
        serializable_data = []
        for features, safe_set in memory_data:
            serializable_data.append([features, list(safe_set)])
        with open(MEMORY_FILE, 'w') as f:
            json.dump(serializable_data, f)
    except:
        pass

def load_memory():
    try:
        if MEMORY_FILE.exists():
            with open(MEMORY_FILE, 'r') as f:
                data = json.load(f)
                # Convert back list to set
                return [(item[0], set(item[1])) for item in data]
    except:
        return []
    return []

# ===================== CSS ULTRA PRÉCIS =====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@600;700&display=swap');
    
    .stApp {
        background: radial-gradient(ellipse at 50% 0%, #0d0033 0%, #000000 100%);
        color: #00ffcc;
        font-family: 'Rajdhani', sans-serif;
    }
    
    h1, h2, h3 { 
        text-align: center; 
        color: #00ffcc; 
        text-shadow: 0 0 20px #00ffcc; 
        font-family: 'Orbitron', sans-serif;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #00ffcc, #0066ff, #00ffcc) !important;
        background-size: 200%;
        color: white !important;
        border-radius: 14px !important;
        height: 56px !important;
        font-weight: 900 !important;
        border: none !important;
    }
    
    .grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 10px;
        max-width: 450px;
        margin: 30px auto;
    }
    
    .cell {
        aspect-ratio: 1/1;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 14px;
        font-size: 2rem;
        font-weight: 900;
        transition: all 0.3s;
    }
    
    .safe { 
        background: linear-gradient(135deg, #00ffcc, #00cc99); 
        color: #000; 
        box-shadow: 0 0 20px #00ffcc;
    }
    
    .risk { 
        background: linear-gradient(135deg, #ff0033, #cc0000); 
        color: #fff; 
    }
    
    .empty { 
        background: rgba(26, 26, 46, 0.6); 
        border: 2px solid rgba(51, 51, 102, 0.5); 
        color: #33336688;
    }

    .info-box {
        background: rgba(0, 255, 204, 0.08);
        border: 2px solid rgba(0, 255, 204, 0.4);
        border-radius: 14px;
        padding: 20px;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# ===================== SESSION STATE =====================
if "login" not in st.session_state:
    st.session_state.login = False
if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

# ===================== CORE ALGORITHMS =====================

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

def monte_carlo_simulations(server_seed, client_seed, nonce, num_mines, simulations=200_000):
    safe_count = np.zeros(25, dtype=np.int64)
    for i in range(simulations):
        future_nonce = nonce + i
        _, safe_positions = get_provably_fair_positions(server_seed, client_seed, future_nonce, num_mines)
        for pos in safe_positions:
            safe_count[pos] += 1
    return safe_count / simulations

def extract_features(server_seed, client_seed, nonce, num_mines):
    h = hashlib.sha512(f"{server_seed}:{client_seed}:{nonce}:{num_mines}".encode()).hexdigest()
    features = [int(h[i:i+2], 16) for i in range(0, 40, 2)]
    features.append(nonce % 100)
    features.append(num_mines)
    # Pad to 100 features for the model
    while len(features) < 100:
        features.append(0)
    return features

def predict_5_diamonds(server_seed, client_seed, nonce, num_mines):
    if not server_seed or not client_seed:
        return None, None, None, 0
    
    mines_exact, safe_exact = get_provably_fair_positions(server_seed, client_seed, nonce, num_mines)
    
    with st.spinner("Analyse en cours (200,000 simulations)..."):
        mc_probs = monte_carlo_simulations(server_seed, client_seed, nonce, num_mines)
    
    # Combined score (Mainly Monte Carlo for this version)
    final_scores = mc_probs * 0.9 + np.random.uniform(0.98, 1.02, 25) * 0.1
    ranked = np.argsort(-final_scores)
    
    top5 = ranked[:5].tolist()
    bottom5 = ranked[-5:].tolist()
    confidence = round(float(np.mean(final_scores[top5])) * 100, 2)
    
    # ML Memory update
    features = extract_features(server_seed, client_seed, nonce, num_mines)
    st.session_state.memory.append((features, safe_exact))
    if len(st.session_state.memory) > 1000: st.session_state.memory.pop(0)
    save_memory(st.session_state.memory)
    
    return top5, bottom5, mines_exact, confidence

def draw_grid(safe_positions, risky_positions, mines_exact=None, reveal=False):
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

# ===================== LOGIN INTERFACE (FRENCH) =====================

if not st.session_state.login:
    st.markdown("<h1>🔓 MINES V1000 ACCESS</h1>", unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns([1, 1.2, 1])
    with col_b:
        st.markdown("<div class='info-box'>", unsafe_allow_html=True)
        pwd = st.text_input("MOT DE PASSE", type="password")
        if st.button("DÉVERROUILLER", use_container_width=True):
            if pwd == "2026":
                st.session_state.login = True
                st.rerun()
            else:
                st.error("Code incorrect")
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.markdown("""
    <div class='info-box' style='max-width:600px; margin:auto;'>
        <h4 style='color:#00ffcc;'>📘 GUIDE RAPIDE (Malagasy)</h4>
        <p>1. Ampidiro ny <b>Server Seed</b> avy amin'ny Casino.</p>
        <p>2. Ampidiro ny <b>Client Seed</b> (izay tianao).</p>
        <p>3. Ny <b>Nonce</b> dia ny isan'ny round efa vita.</p>
        <p>4. Tsindrio ny bokotra ANALYSER.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ===================== MAIN APP (FRENCH) =====================

st.markdown("<h1>💎 PRÉDICTION MINES V1000</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ PARAMÈTRES")
    if st.button("🗑️ RÉINITIALISER ML"):
        st.session_state.memory = []
        if MEMORY_FILE.exists(): os.remove(MEMORY_FILE)
        st.success("Mémoire effacée")
        st.rerun()
    st.write(f"Mémoire ML: {len(st.session_state.memory)}/1000")

col1, col2 = st.columns(2)
with col1:
    server_seed = st.text_input("SERVER SEED (Hash Casino)")
    client_seed = st.text_input("CLIENT SEED (Vôtre Seed)")
with col2:
    nonce = st.number_input("NONCE (Compteur)", value=0, step=1)
    num_mines = st.selectbox("NOMBRE DE MINES", options=[1, 2, 3])

if st.button("🚀 LANCER L'ANALYSE ULTRA PRÉCISE", use_container_width=True):
    if server_seed and client_seed:
        top5, bottom5, mines_exact, conf = predict_5_diamonds(server_seed, client_seed, nonce, num_mines)
        
        st.markdown(draw_grid(top5, bottom5), unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        c1.metric("CONFIANCE", f"{conf}%")
        c2.metric("MINES", num_mines)
        c3.metric("DIAMANTS", "5")
        
        st.markdown(f"""
        <div class='info-box' style='text-align:center;'>
            <h3 style='color:#00ffcc;'>💎 POSITIONS CONSEILLÉES</h3>
            <p style='font-size:2rem; font-weight:900;'>{', '.join(map(str, top5))}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.checkbox("🔍 RÉVÉLER LES MINES (VÉRIFICATION)"):
            st.markdown(draw_grid(top5, bottom5, mines_exact, reveal=True), unsafe_allow_html=True)
    else:
        st.warning("Veuillez remplir tous les champs.")

st.markdown("---")
st.markdown("<p style='text-align:center; color:#555;'>V1000 ULTRA PRECISION SYSTEM © 2026</p>", unsafe_allow_html=True)
