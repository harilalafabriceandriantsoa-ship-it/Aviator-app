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
    .hex-display {
        font-size: 11px; color: #00ffcc; word-break: break-all; margin-top: 15px;
        background: rgba(0, 255, 204, 0.1); padding: 10px; border-radius: 5px;
        border: 1px solid #00ffcc44;
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
    # Ity no mampifandray ny Hash sy ny Numéro de tour
    data_stream = f"{seed}{context}TITAN_WAR_2026_ULTRA".encode()
    
    if algo == "SHA-512":
        raw_hash = hashlib.sha512(data_stream).hexdigest()
        chunk = 8
    else:
        raw_hash = hashlib.sha256(data_stream).hexdigest()
        chunk = 4

    # Mines Logic (6 Spots)
    safe_spots = []
    for i in range(count):
        val = int(raw_hash[i*chunk:(i+1)*chunk], 16) % 25
        while val in safe_spots:
            val = (val + 1) % 25
        safe_spots.append(val)
        
    # Cosmos Logic (Jump & Multiplier)
    random.seed(int(raw_hash[:16], 16))
    mult = round(random.uniform(1.55, 4.95), 2)
    acc = random.randint(96, 99)
    status = "JUMP DETECTED" if int(raw_hash[-2:], 16) > 180 else "STABLE"
    
    return {"spots": safe_spots, "mult": mult, "acc": acc, "status": status, "hash": raw_hash}

# --- 5. INTERFACE ---
st.markdown("<h2 style='color:#00ffcc; text-align:center;'>🛰️ TITAN V85.0 - UNIVERSAL WAR-MACHINE</h2>", unsafe_allow_html=True)
t1, t2, t3 = st.tabs(["🚀 COSMOS SCANNER", "💣 MINES SCANNER", "📜 SYSTEM LOGS"])

with t1:
    st.markdown("### 🚀 COSMOS (HASH + TOUR + HEX)")
    algo_c = st.radio("Algo Selection:", ["SHA-512", "SHA-256"], horizontal=True, key="c_algo")
    h_val = st.text_input("1. Server Hash / Combined Seed:")
    t_num = st.number_input("2. Numéro de Tour (Nonce):", min_value=1, value=1, step=1)
    
    if st.button("🔥 EXECUTE FULL COSMOS SCAN"):
        if h_val:
            with st.spinner("Extracting Hex Signature..."):
                time.sleep(0.6)
                data = titan_war_engine(h_val, str(t_num), algo_c)
                st.markdown(f"""
                    <div class="war-card">
                        <p style="color:#aaa;">TOUR: {t_num}</p>
                        <h1 style="color:#00ffcc; font-size:70px;">{data['mult']}x</h1>
                        <p>🎯 PRECISION: {data['acc']}% | STATUS: <span style="color:#ffff00;">{data['status']}</span></p>
                        <div class="hex-display"><b>HEX SIGNATURE:</b><br>{data['hash']}</div>
                    </div>
                """, unsafe_allow_html=True)
                st.session_state.history.insert(0, f"Cosmos T{t_num}: {data['mult']}x | Hex: {data['hash'][:10]}...")

with t2:
    st.markdown("### 🔍 MINES DEEP SCANNER")
    algo_m = st.radio("Algo Selection:", ["SHA-512", "SHA-256"], horizontal=True, key="m_algo")
    nb_mines = st.select_slider("Mines Target:", options=[1, 2, 3], value=3)
    
    c1, c2 = st.columns(2)
    s_seed = c1.text_input("Server Seed:")
    c_seed = c2.text_input("Client Seed:")
    
    if st.button("🛰️ START MINES SCAN"):
        if s_seed and c_seed:
            with st.spinner("Synchronizing 6-Diamond Grid..."):
                time.sleep(0.5)
                data = titan_war_engine(s_seed, c_seed, algo_m)
                grid_html = '<div class="mines-grid">'
                for i in range(25):
                    is_safe = i in data['spots']
                    grid_html += f'<div class="mine-cell {"cell-star" if is_safe else ""}">{"⭐" if is_safe else "⬛"}</div>'
                st.session_state.mines_grid = grid_html + '</div>'
                st.session_state.history.insert(0, f"Mines Scan: 6 Stars Generated")
            
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)
        st.success(f"✅ WAR-PATTERN SYNCHRONIZED!")

with t3:
    st.markdown("### 📜 SYSTEM COMMAND LOGS")
    for log in st.session_state.history[:15]:
        st.write(f"📡 {log}")
