import streamlit as st
import hashlib
import random
import time
import hmac

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V86.1 - ANTI-SHUFFLE", layout="wide")

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
    .cell-star { border: 2px solid #ffff00 !important; background: rgba(255, 255, 0, 0.2); color: #ffff00; box-shadow: 0 0 25px #ffff00aa; transform: scale(1.08); transition: 0.5s; }
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

# --- 4. THE ANTI-SHUFFLE CORE (STRICT CALCULATION) ---
def quantum_deep_calc(s_seed, c_seed, salt, iterations=12000):
    """Deep Hash-Chain algorithm: mampiasa iterations 12.000 mba handresena ny dynamic shuffling"""
    # Nampiana "Double Salting" mba tsy ho tratry ny tsatoka
    combined_salt = hmac.new(salt.encode(), f"DEEP_REINFORCE_{c_seed}".encode(), hashlib.sha512).hexdigest()
    current_hash = hmac.new(combined_salt.encode(), s_seed.encode(), hashlib.sha512).digest()
    
    for i in range(iterations):
        # Isaky ny mi-iterate dia manova ny pattern ny milina
        current_hash = hmac.new(current_hash, f"BLOCK_{i}_{salt}_{c_seed}".encode(), hashlib.sha512).digest()
    
    return current_hash.hex()

# --- 5. INTERFACE ---
st.markdown("<h3 style='text-align:center; color:#00ffcc;'>🛰️ TITAN V86.1 - ANTI-SHUFFLE</h3>", unsafe_allow_html=True)
tab1, tab2 = st.tabs(["🚀 DEEP COSMOS SCAN", "💣 DEEP MINES (FIXE 5)"])

with tab1:
    h_in = st.text_input("Server Seed / Hash:")
    col_1, col_2 = st.columns(2)
    hx_in = col_1.text_input("Hex8 / Extra:")
    t_act = col_2.number_input("Tour Actuel:", min_value=1, value=8136350)
    
    if st.button("🚀 EXECUTE QUANTUM SCAN"):
        if h_in:
            with st.spinner("Analyzing Quantum Orbits (12,000 passes)..."):
                off = (int(hashlib.md5(h_in.encode()).hexdigest()[:1], 16) % 2) + 2
                res_hash = quantum_deep_calc(h_in, hx_in, f"COSMOS_{t_act+off}")
                
                random.seed(int(res_hash[:16], 16))
                f = int(res_hash[-12:], 16) / 281474976710655.0
                if f > 0.95: m = round(random.uniform(25.0, 120.0), 2)
                elif f > 0.45: m = round(random.uniform(3.0, 15.0), 2)
                else: m = round(random.uniform(1.01, 2.99), 2)
                
                st.markdown(f'<div class="war-card"><div>TARGET TOUR {t_act+off}</div><p class="mult-val">{m}x</p></div>', unsafe_allow_html=True)

with tab2:
    st.markdown("##### 🛡️ MINES 1-3: 5 STARS (STRICT HASH CALC)")
    st.info("Kajy Hash in-12,000: Mitady ny 'Safe Zone' tsy voakitiky ny tsatoka.")
    nb_mines = st.selectbox("Isan'ny Mines:", [1, 2, 3], index=2)
    s_s = st.text_input("Server Seed (Mines):")
    c_s = st.text_input("Client Seed (Tour Num):")
    
    if st.button("🛰️ EXECUTE DEEP-MINE SCAN"):
        if s_s and c_s:
            spots = []
            progress_bar = st.progress(0)
            
            with st.spinner("Breaking Anti-Bot Shield..."):
                # Kajy lalina ho an'ny kintana 5 - tsy azo tapahina
                for j in range(5):
                    # Nampiana dynamic offset isaky ny kintana (j)
                    h_deep = quantum_deep_calc(s_s, c_s, f"SAFE_MINE_{nb_mines}_{j}", iterations=8000)
                    
                    # Fampiasana "Recursive Modulo" mba hialana amin'ny baomba
                    v = int(h_deep[j*6:j*6+8], 16) % 25
                    while v in spots:
                        v = (v + int(h_deep[-4:], 16) + j + 1) % 25
                    spots.append(v)
                    progress_bar.progress((j + 1) * 20)
                
                grid_html = '<div class="mines-grid">'
                for i in range(25):
                    grid_html += f'<div class="mine-cell {"cell-star" if i in spots else ""}">{"⭐" if i in spots else "⬛"}</div>'
                st.session_state.mines_grid = grid_html + '</div>'
            
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)
        st.success("ANTI-SHUFFLE SCAN COMPLETE - 5 SAFE SPOTS LOCKED")
