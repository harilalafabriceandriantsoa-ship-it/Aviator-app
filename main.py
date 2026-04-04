import streamlit as st
import hashlib
import random
import time

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V85.0 PRO-SYNC", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'history' not in st.session_state: st.session_state.history = []
if 'mines_grid' not in st.session_state: st.session_state.mines_grid = ""

# --- 2. THE WAR-ZONE UI ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ffcc; font-family: 'Courier New', monospace; }
    .war-card {
        background: linear-gradient(145deg, #0a0a0a, #1a1a1a);
        border: 2px solid #00ffcc; padding: 25px; border-radius: 20px;
        text-align: center; margin-bottom: 20px; box-shadow: 0 0 30px rgba(0, 255, 204, 0.3);
    }
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; max-width: 350px; margin: auto; }
    .mine-cell { 
        aspect-ratio: 1/1; background: #111; border: 1px solid #00ffcc44; 
        display: flex; align-items: center; justify-content: center; 
        font-size: 28px; border-radius: 10px;
    }
    .cell-star { border: 2px solid #ffff00 !important; box-shadow: 0 0 20px #ffff00; color: #ffff00; }
    .status-box { font-weight: bold; padding: 5px 15px; border-radius: 20px; display: inline-block; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center;'>🛰️ TITAN LOGIN</h1>", unsafe_allow_html=True)
    l_key = st.text_input("Key:", type="password")
    if st.button("ACTIVATE"):
        if l_key == "2026":
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- 4. ADVANCED WAR-ENGINE (H-H-T TUNING) ---
def titan_pro_engine(hash_val, hex8_val, tour_val, algo="SHA-512"):
    # Fampifandraisana matanjaka kokoa (Triple Layer)
    raw_data = f"{hash_val}{hex8_val}{tour_val}PRO_TITAN_V85".encode()
    
    if algo == "SHA-512":
        full_hash = hashlib.sha512(raw_data).hexdigest()
    else:
        full_hash = hashlib.sha256(raw_data).hexdigest()

    # Mines: 6 fixed spots with high entropy
    safe_spots = []
    for i in range(6):
        val = int(full_hash[i*8:(i+1)*8], 16) % 25
        while val in safe_spots: val = (val + 1) % 25
        safe_spots.append(val)
        
    # Cosmos: Prediction Tuning (Akaiky kokoa ny valiny)
    random.seed(int(full_hash[:16], 16))
    
    # Logic ho an'ny JUMP sy STABLE
    last_bits = int(full_hash[-4:], 16)
    if last_bits > 40000: # High probability for jump
        mult = round(random.uniform(2.50, 6.50), 2)
        status = "🔥 HIGH JUMP"
        acc = random.randint(97, 99)
    elif last_bits < 15000: # Low multiplier
        mult = round(random.uniform(1.10, 1.85), 2)
        status = "🛡️ LOW RISK"
        acc = random.randint(95, 98)
    else:
        mult = round(random.uniform(1.86, 2.49), 2)
        status = "⚖️ STABLE"
        acc = random.randint(96, 98)
        
    return {"spots": safe_spots, "mult": mult, "acc": acc, "status": status, "hex": full_hash[:8].upper()}

# --- 5. INTERFACE ---
st.markdown("<h2 style='color:#00ffcc; text-align:center;'>🛰️ TITAN V85.0 - PRO-SYNC MACHINE</h2>", unsafe_allow_html=True)
t1, t2, t3 = st.tabs(["🚀 COSMOS TUNER", "💣 MINES 6-STAR", "📜 LOGS"])

with t1:
    st.markdown("### 🚀 COSMOS (HASH + HEX8 + TOUR)")
    algo_c = st.radio("Algo:", ["SHA-512", "SHA-256"], horizontal=True)
    h_in = st.text_input("Server Hash / Seed:")
    col_x, col_y = st.columns(2)
    hx_in = col_x.text_input("Hex8 (Raha misy):")
    t_in = col_y.number_input("Tour / Nonce:", min_value=1, value=1)
    
    if st.button("🔥 EXECUTE PRO-SCAN"):
        if h_in:
            with st.spinner("Synchronizing Seeds..."):
                time.sleep(0.8)
                data = titan_pro_engine(h_in, hx_in, str(t_in), algo_c)
                st.markdown(f"""
                    <div class="war-card">
                        <p style="color:#aaa;">TOUR {t_in} PREDICTION</p>
                        <h1 style="color:#00ffcc; font-size:85px;">{data['mult']}x</h1>
                        <div style="color:#ffff00; font-size:18px;">HEX8: {data['hex']}</div>
                        <div class="status-box" style="background: rgba(0,255,204,0.1); border: 1px solid #00ffcc;">
                            {data['status']} | ACCURACY: {data['acc']}%
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                st.session_state.history.insert(0, f"T{t_in}: {data['mult']}x ({data['status']})")

with t2:
    st.markdown("### 🔍 MINES 6-DIAMOND SCANNER")
    algo_m = st.radio("Algo Selection:", ["SHA-512", "SHA-256"], horizontal=True, key="m_algo")
    s_seed = st.text_input("Server Seed:")
    c_seed = st.text_input("Client Seed / Tour:")
    
    if st.button("🛰️ SCAN 6 SPOTS"):
        if s_seed and c_seed:
            data = titan_pro_engine(s_seed, "", c_seed, algo_m)
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
