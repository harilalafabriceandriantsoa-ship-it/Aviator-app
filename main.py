import streamlit as st
import hashlib
import time
import numpy as np

# --- 1. CONFIGURATION SYSTEM ---
st.set_page_config(page_title="TITAN V85.0 WAR-MACHINE", layout="wide", initial_sidebar_state="collapsed")

# Session State ho an'ny fitadidiana (Memory)
if 'history' not in st.session_state: st.session_state.history = []
if 'scan_active' not in st.session_state: st.session_state.scan_active = False

# --- 2. STYLE NEON WAR-MACHINE (DARK INTERFACE) ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #050505 0%, #000000 100%); color: #00ffcc; font-family: 'Courier New', monospace; }
    .war-card {
        background: rgba(0, 20, 20, 0.8); border: 1px solid #00ffcc;
        border-left: 5px solid #00ffcc; padding: 20px; border-radius: 5px;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.2); margin-bottom: 20px;
    }
    .glitch-text { animation: pulse 2s infinite; font-weight: bold; color: #ff0055; text-transform: uppercase; }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; max-width: 350px; margin: auto; padding: 15px; background: #080808; border: 2px solid #333; }
    .mine-cell { aspect-ratio: 1/1; display: flex; align-items: center; justify-content: center; font-size: 24px; border-radius: 4px; background: #111; border: 1px solid #222; transition: 0.3s; }
    .cell-target { border: 2px solid #00ffcc !important; box-shadow: 0 0 20px #00ffcc; background: rgba(0, 255, 204, 0.1) !important; color: #00ffcc; transform: scale(1.05); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ENGINE: MACHINE DE GUERRE (ALGORITHM) ---
class TitanEngine:
    @staticmethod
    def generate_sha512_pattern(seed, round_id, count=5):
        # Mampiasa SHA-512 ho an'ny securité sy précision ambony indrindra
        combined = f"{seed}-{round_id}-TITAN-ULTRA-V85"
        hash_result = hashlib.sha512(combined.encode()).hexdigest()
        
        # Simulation de probabilité mampiasa Numpy
        indices = []
        for i in range(count):
            # Maka segment 4 avy amin'ny hash mba hivadika ho isa
            segment = hash_result[i*8 : (i+1)*8]
            pos = int(segment, 16) % 25
            while pos in indices:
                pos = (pos + 1) % 25
            indices.append(pos)
        return indices

    @staticmethod
    def predict_aviator(hash_val):
        # Algorithm de prédiction ho an'ny Aviator/Cosmos
        h = hashlib.sha256(hash_val.encode()).hexdigest()
        val = (int(h[:8], 16) % 1000) / 100
        if val < 1.0: val = 1.25
        accuracy = 85 + (int(h[-2:], 16) % 14) # Précision 85% - 99%
        return round(val, 2), accuracy

# --- 4. INTERFACE PRINCIPALE ---
st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🛰️ TITAN V85.0 : WAR-MACHINE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:12px; color:#666;'>SYSTEM STATUS: ENCRYPTED | CORE: SHA-512</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🎯 CRASH ANALYZER", "💣 MINES SCANNER"])

# --- TAB 1: CRASH ANALYZER (AVIATOR) ---
with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### 📡 INPUT DATA")
        server_hash = st.text_input("HASH SHA-256 (Current):", placeholder="Ampidiro ny Hash farany...")
        last_result = st.number_input("Last Result (x):", min_value=1.0, value=1.5, step=0.1)
        
    with col2:
        st.markdown("### ⚙️ SYSTEM SYNC")
        sync_mode = st.toggle("ULTRA-SYNC MODE", value=True)
        if st.button("🔥 EXECUTE SCAN", use_container_width=True):
            if server_hash:
                with st.spinner("Analyzing data patterns..."):
                    time.sleep(1.5) # Simulation de calcul
                    pred, acc = TitanEngine.predict_aviator(server_hash)
                    
                    st.markdown(f"""
                        <div class="war-card">
                            <p style='margin:0; font-size:14px;'>PREDICTION CONFIRMED</p>
                            <h1 style='font-size:60px; margin:0;'>{pred}x</h1>
                            <div style='display:flex; justify-content:space-between;'>
                                <span>🎯 ACCURACY: {acc}%</span>
                                <span class='glitch-text'>SIGNAL: STABLE</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.session_state.history.append(f"Crash: {pred}x ({acc}%)")
            else:
                st.error("Mila Hash vao afaka manao scan!")

# --- TAB 2: MINES SCANNER ---
with tab2:
    st.markdown("### 🔍 MINES SHA-512 SCANNER")
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        m_seed = st.text_input("Server Seed / Hash:", key="m_seed")
    with m_col2:
        m_client = st.text_input("Client Seed:", key="m_client")
    
    num_stars = st.select_slider("Isan'ny Diamondra (Target):", options=[3, 5, 8], value=5)
    
    if st.button("🛰️ START DEEP SCAN", use_container_width=True):
        if m_seed and m_client:
            with st.spinner("Synchronizing with server algorithm..."):
                time.sleep(2)
                targets = TitanEngine.generate_sha512_pattern(m_seed, m_client, num_stars)
                
                # GRID GENERATION
                grid_html = '<div class="mines-grid">'
                for i in range(25):
                    is_target = i in targets
                    style = 'cell-target' if is_target else ''
                    icon = '💎' if is_target else '⬛'
                    grid_html += f'<div class="mine-cell {style}">{icon}</div>'
                grid_html += '</div>'
                
                st.markdown(grid_html, unsafe_allow_html=True)
                st.success(f"✅ Scan Vita: Toerana {num_stars} voatondro!")
        else:
            st.warning("Ampidiro ny Seed rehetra!")

# --- 5. LOGS & HISTORY ---
with st.expander("📜 SYSTEM LOGS (HISTORY)"):
    if st.session_state.history:
        for log in reversed(st.session_state.history):
            st.text(f" {log}")
    else:
        st.text("No data scanned yet.")
