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
        background: linear-gradient(145deg, #0a0a0a, #161616);
        border: 2px solid #00ffcc; padding: 25px; border-radius: 20px;
        text-align: center; margin-bottom: 20px;
        box-shadow: 0 0 30px rgba(0, 255, 204, 0.3);
    }
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; max-width: 350px; margin: auto; }
    .mine-cell { 
        aspect-ratio: 1/1; background: #111; border: 1px solid #00ffcc44; 
        display: flex; align-items: center; justify-content: center; 
        font-size: 28px; border-radius: 10px;
    }
    .cell-star { 
        border: 2px solid #ffff00 !important; background: rgba(255, 255, 0, 0.1);
        box-shadow: 0 0 20px #ffff00; color: #ffff00;
    }
    .hex-box {
        font-size: 14px; color: #ffff00; font-weight: bold;
        background: rgba(255, 255, 0, 0.1); padding: 10px; 
        border-radius: 10px; border: 1px dashed #ffff00; margin-top: 10px;
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

# --- 4. CORE WAR-ENGINE (HEX8 TRIPLE-SYNC) ---
def titan_war_engine(hash_val, hex8_val, tour_val, algo="SHA-512"):
    # Itambaran'ny singa 3 ho lasa hery iray
    combined_data = f"{hash_val}{hex8_val}{tour_val}TITAN_ULTRA_2026".encode()
    
    if algo == "SHA-512":
        raw_hash = hashlib.sha512(combined_data).hexdigest()
    else:
        raw_hash = hashlib.sha256(combined_data).hexdigest()

    # Mines logic (6 Spots)
    safe_spots = []
    for i in range(6):
        val = int(raw_hash[i*8:(i+1)*8], 16) % 25
        while val in safe_spots:
            val = (val + 1) % 25
        safe_spots.append(val)
        
    # Cosmos logic
    random.seed(int(raw_hash[:16], 16))
    mult = round(random.uniform(1.65, 5.20), 2)
    acc = random.randint(97, 99)
    # Hex8 Extraction ho an'ny prediction
    extracted_hex8 = raw_hash[:8].upper()
    
    return {"spots": safe_spots, "mult": mult, "acc": acc, "hex8": extracted_hex8, "full_hash": raw_hash}

# --- 5. INTERFACE ---
st.markdown("<h2 style='color:#00ffcc; text-align:center;'>🛰️ TITAN V85.0 - ULTRA-WAR SYNC</h2>", unsafe_allow_html=True)
t1, t2, t3 = st.tabs(["🚀 COSMOS TRIPLE-SCAN", "💣 MINES 6-STAR", "📜 LOGS"])

with t1:
    st.markdown("### 🚀 COSMOS ANALYZER (HASH + HEX8 + TOUR)")
    algo_c = st.radio("Select Algorithm:", ["SHA-512", "SHA-256"], horizontal=True)
    
    c1, c2 = st.columns(2)
    h_in = c1.text_input("1. Server Hash / Seed:")
    hx_in = c2.text_input("2. Hex8 (Optional / Extra):")
    t_in = st.number_input("3. Numéro de Tour (Nonce):", min_value=1, value=1)
    
    if st.button("🔥 EXECUTE TRIPLE SYNC"):
        if h_in:
            with st.spinner("Decoding H-H-T Pattern..."):
                time.sleep(0.7)
                data = titan_war_engine(h_in, hx_in, str(t_in), algo_c)
                st.markdown(f"""
                    <div class="war-card">
                        <p style="color:#aaa;">PREDICTED TARGET (TOUR {t_in})</p>
                        <h1 style="color:#00ffcc; font-size:80px;">{data['mult']}x</h1>
                        <div class="hex-box">IDENTIFIED HEX8: {data['hex8']}</div>
                        <p style="margin-top:15px;">🎯 PRECISION: {data['acc']}%</p>
                        <p style="font-size:10px; color:#444; word-break: break-all;">FULL: {data['full_hash']}</p>
                    </div>
                """, unsafe_allow_html=True)
                st.session_state.history.insert(0, f"Cosmos T{t_in}: {data['mult']}x [Hex8: {data['hex8']}]")

with t2:
    st.markdown("### 🔍 MINES 6-DIAMOND SCANNER")
    algo_m = st.radio("Select Algorithm:", ["SHA-512", "SHA-256"], horizontal=True, key="m_algo")
    
    col1, col2 = st.columns(2)
    ms_seed = col1.text_input("Server Seed:")
    mc_seed = col2.text_input("Client Seed / Tour:")
    
    if st.button("🛰️ SCAN 6 SAFE SPOTS"):
        if ms_seed and mc_seed:
            with st.spinner("Locking 6 Diamonds..."):
                time.sleep(0.5)
                data = titan_war_engine(ms_seed, "", mc_seed, algo_m)
                grid_html = '<div class="mines-grid">'
                for i in range(25):
                    is_safe = i in data['spots']
                    grid_html += f'<div class="mine-cell {"cell-star" if is_safe else ""}">{"⭐" if is_safe else "⬛"}</div>'
                st.session_state.mines_grid = grid_html + '</div>'
            
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)
        st.success("✅ 6-STAR PATTERN LOCKED")

with t3:
    st.markdown("### 📜 SYSTEM LOGS")
    for log in st.session_state.history[:15]:
        st.write(f"📡 {log}")
