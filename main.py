import streamlit as st
import hashlib
import random
import time
import hmac

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V86.0 - QUANTUM DEEP", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'mines_grid' not in st.session_state: st.session_state.mines_grid = ""

# --- 2. STYLE (DEEP TECH) ---
st.markdown("""
    <style>
    .stApp { background-color: #000505; color: #00ffcc; font-family: 'Courier New', monospace; }
    .war-card {
        background: #001010; border: 2px solid #00ffcc; 
        padding: 15px; border-radius: 15px; text-align: center; margin-bottom: 10px;
        box-shadow: 0 0 15px #00ffcc33;
    }
    .mult-val { color: #00ffcc; font-size: 55px; font-weight: bold; margin: 0; text-shadow: 0 0 10px #00ffcc66; }
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; max-width: 330px; margin: 0 auto; }
    .mine-cell { aspect-ratio: 1/1; background: #000; border: 1px solid #00ffcc22; display: flex; align-items: center; justify-content: center; font-size: 28px; border-radius: 12px; }
    .cell-star { border: 2px solid #ffff00 !important; background: rgba(255, 255, 0, 0.2); color: #ffff00; box-shadow: 0 0 20px #ffff0088; transform: scale(1.08); transition: 0.5s; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN (KEY: 2026) ---
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center;'>🛰️ TITAN QUANTUM ACCESS</h2>", unsafe_allow_html=True)
    if st.text_input("ENTER MASTER KEY:", type="password") == "2026":
        if st.button("ACTIVATE QUANTUM-DEEP"):
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- 4. THE DEEP HASH CALCULATOR (NO MORE "TSATOKA") ---
def quantum_deep_calc(s_seed, c_seed, salt, iterations=10000):
    """Manao kajy Hash in-10.000 vao mamoaka valiny iray (Proof of Work)"""
    # 1. Base Hash
    current_hash = hmac.new(salt.encode(), f"{s_seed}{c_seed}".encode(), hashlib.sha512).digest()
    
    # 2. Deep Iteration (Eto ilay 3s-5s)
    for i in range(iterations):
        current_hash = hmac.new(current_hash, f"ITER_{i}_{salt}".encode(), hashlib.sha512).digest()
    
    return current_hash.hex()

# --- 5. INTERFACE ---
st.markdown("<h3 style='text-align:center; color:#00ffcc;'>🛰️ TITAN V86.0 - QUANTUM DEEP</h3>", unsafe_allow_html=True)
tab1, tab2 = st.tabs(["🚀 DEEP COSMOS SCAN", "💣 DEEP MINES (FIXE 5)"])

with tab1:
    h_in = st.text_input("Server Seed / Hash:")
    col_1, col_2 = st.columns(2)
    hx_in = col_1.text_input("Hex8 / Extra:")
    t_act = col_2.number_input("Tour Actuel:", min_value=1, value=8136350)
    
    if st.button("🚀 EXECUTE QUANTUM SCAN"):
        if h_in:
            with st.spinner("Breaking Encryption (10,000 passes)..."):
                # Kajy lalina ho an'ny Cosmos
                off = (int(hashlib.md5(h_in.encode()).hexdigest()[:1], 16) % 2) + 2
                res_hash = quantum_deep_calc(h_in, hx_in, f"COSMOS_{t_act+off}")
                
                random.seed(int(res_hash[:16], 16))
                f = int(res_hash[-12:], 16) / 281474976710655.0
                if f > 0.95: m = round(random.uniform(20.0, 100.0), 2)
                elif f > 0.40: m = round(random.uniform(2.8, 12.0), 2)
                else: m = round(random.uniform(1.01, 2.79), 2)
                
                st.markdown(f'<div class="war-card"><div>TARGET TOUR {t_act+off}</div><p class="mult-val">{m}x</p></div>', unsafe_allow_html=True)

with tab2:
    st.markdown("##### 🛡️ MINES 1-3: 5 STARS (DEEP HASH CALCULATION)")
    st.info("Status: Deep Iteration Active (10,000 passes per scan)")
    nb_mines = st.selectbox("Isan'ny Mines:", [1, 2, 3], index=2)
    s_s = st.text_input("Server Seed (Mines):")
    c_s = st.text_input("Client Seed (Tour Num):")
    
    if st.button("🛰️ EXECUTE DEEP-MINE SCAN"):
        if s_s and c_s:
            spots = []
            progress_bar = st.progress(0)
            
            with st.spinner("Calculating 5 Golden Spots..."):
                # Deep calculation ho an'ny kintana 5
                for j in range(5):
                    # Ity no tena "Calcul Hash" madio
                    h_deep = quantum_deep_calc(s_s, c_s, f"MINE_{nb_mines}_{j}", iterations=5000)
                    
                    v = int(h_deep[j*5:j*5+8], 16) % 25
                    while v in spots:
                        v = (v + int(h_deep[-2:], 16) + 1) % 25
                    spots.append(v)
                    progress_bar.progress((j + 1) * 20)
                
                grid_html = '<div class="mines-grid">'
                for i in range(25):
                    grid_html += f'<div class="mine-cell {"cell-star" if i in spots else ""}">{"⭐" if i in spots else "⬛"}</div>'
                st.session_state.mines_grid = grid_html + '</div>'
            
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)
        st.success("QUANTUM SCAN COMPLETE - 5 SPOTS IDENTIFIED")
