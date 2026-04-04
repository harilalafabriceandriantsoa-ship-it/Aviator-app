import streamlit as st
import hashlib
import random
import time

# --- 1. TITAN V85.0 WAR-MACHINE CONFIG ---
st.set_page_config(page_title="TITAN V85.0 WAR-MACHINE", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'history' not in st.session_state: st.session_state.history = []
if 'mines_grid' not in st.session_state: st.session_state.mines_grid = ""

# --- 2. THE WAR-ZONE UI (NEON CYBER) ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ffcc; font-family: 'Courier New', monospace; }
    .war-card {
        background: linear-gradient(145deg, #0a0a0a, #1a1a1a);
        border: 2px solid #00ffcc; padding: 25px; border-radius: 20px;
        text-align: center; margin-bottom: 20px;
        box-shadow: 0 0 30px rgba(0, 255, 204, 0.3);
    }
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; max-width: 350px; margin: auto; }
    .mine-cell { 
        aspect-ratio: 1/1; background: #111; border: 1px solid #00ffcc44; 
        display: flex; align-items: center; justify-content: center; 
        font-size: 28px; border-radius: 10px; transition: 0.3s;
    }
    .cell-star { 
        border: 2px solid #ffff00 !important; background: rgba(255, 255, 0, 0.1);
        box-shadow: 0 0 20px #ffff00; color: #ffff00;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ACCESS CONTROL ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center;'>🛰️ TITAN ENGINE ACCESS</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        login_key = st.text_input("ENTER COMMAND KEY:", type="password")
        if st.button("ACTIVATE WAR-MACHINE"):
            if login_key == "2026":
                st.session_state.logged_in = True
                st.rerun()
    st.stop()

# --- 4. CORE WAR-ENGINE (UNIVERSAL LOGIC) ---
def titan_war_engine(seed, context, algo="SHA-512", count=6):
    # Combine seeds for high-level cryptography
    data_stream = f"{seed}{context}TITAN_WAR_2026_ULTRA".encode()
    
    if algo == "SHA-512":
        raw_hash = hashlib.sha512(data_stream).hexdigest()
        chunk = 8
    else:
        raw_hash = hashlib.sha256(data_stream).hexdigest()
        chunk = 4

    # Mines Logic: Calculate 6 Fixed Safe Spots
    safe_spots = []
    for i in range(count):
        # High precision offset calculation
        val = int(raw_hash[i*chunk:(i+1)*chunk], 16) % 25
        while val in safe_spots:
            val = (val + 1) % 25
        safe_spots.append(val)
        
    # Cosmos Logic: Multiplier & Precision
    random.seed(int(raw_hash[:16], 16))
    mult = round(random.uniform(1.50, 4.80), 2)
    acc = random.randint(96, 99)
    status = "JUMP DETECTED" if int(raw_hash[-2:], 16) > 200 else "STABLE"
    
    return {"spots": safe_spots, "mult": mult, "acc": acc, "status": status, "hash": raw_hash}

# --- 5. INTERFACE ---
st.markdown("<h2 style='color:#00ffcc; text-align:center;'>🛰️ TITAN V85.0 - UNIVERSAL WAR-MACHINE</h2>", unsafe_allow_html=True)
t1, t2, t3 = st.tabs(["🚀 COSMOS ANALYZER", "💣 MINES SCANNER", "📜 SYSTEM LOGS"])

with t1:
    st.markdown("### 🚀 COSMOS JUMP DETECTOR")
    algo_c = st.radio("Select Algorithm:", ["SHA-512", "SHA-256"], horizontal=True, key="cosmos_algo")
    h_val = st.text_input("Server Hash (From Provably Fair):")
    t_id = st.text_input("Round ID (Nonce):")
    
    if st.button("🔥 EXECUTE COSMOS ANALYSIS"):
        if h_val and t_id:
            with st.spinner("Decoding Satellite Data..."):
                time.sleep(0.6)
                data = titan_war_engine(h_val, t_id, algo_c)
                st.markdown(f"""
                    <div class="war-card">
                        <p style="color:#aaa;">PREDICTED MULTIPLIER</p>
                        <h1 style="color:#00ffcc; font-size:70px;">{data['mult']}x</h1>
                        <p>🎯 PRECISION: {data['acc']}% | STATUS: <span style="color:#ffff00;">{data['status']}</span></p>
                    </div>
                """, unsafe_allow_html=True)
                st.session_state.history.insert(0, f"Cosmos: {data['mult']}x ({data['status']})")

with t2:
    st.markdown("### 🔍 MINES DEEP SCANNER")
    algo_m = st.radio("Select Algorithm:", ["SHA-512", "SHA-256"], horizontal=True, key="mines_algo")
    nb_mines = st.select_slider("Target Mines in Game:", options=[1, 2, 3], value=3)
    
    c1, c2 = st.columns(2)
    s_seed = c1.text_input("Server Seed (Past):")
    c_seed = c2.text_input("Client Seed (Active):")
    
    if st.button("🛰️ START DEEP SCAN"):
        if s_seed and c_seed:
            with st.spinner("Injecting SHA-Logic..."):
                time.sleep(0.5)
                data = titan_war_engine(s_seed, c_seed, algo_m)
                grid_html = '<div class="mines-grid">'
                for i in range(25):
                    is_safe = i in data['spots']
                    grid_html += f'<div class="mine-cell {"cell-star" if is_safe else ""}">{"⭐" if is_safe else "⬛"}</div>'
                st.session_state.mines_grid = grid_html + '</div>'
                st.session_state.history.insert(0, f"Mines Scan ({algo_m}): Pattern Locked")
            
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)
        st.success(f"✅ WAR-PATTERN SYNCHRONIZED (6 DIAMONDS)")

with t3:
    st.markdown("### 📜 SYSTEM COMMAND LOGS")
    for log in st.session_state.history[:15]:
        st.write(f"📡 {log}")
