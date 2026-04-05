import streamlit as st
import hashlib
import random
import time

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V85.1 - JUMP ENGINE", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- 2. STYLE ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ffcc; font-family: 'Courier New', monospace; }
    .war-card {
        background: #0a0a0a; border: 2px solid #00ffcc; 
        padding: 15px; border-radius: 15px; text-align: center; margin-bottom: 10px;
    }
    .jump-card { border-color: #ff00ff; box-shadow: 0 0 15px #ff00ff33; }
    .mult-val { color: #00ffcc; font-size: 50px; font-weight: bold; margin: 0; line-height: 1.1; }
    .tour-id { color: #ffff00; font-size: 14px; font-weight: bold; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN ---
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center;'>🛰️ TITAN ACCESS</h2>", unsafe_allow_html=True)
    if st.text_input("KEY:", type="password") == "2026":
        if st.button("ACTIVATE"):
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- 4. ENGINE (TSY FIXE / DYNAMIC) ---
def titan_core_v85(h, hx, t_val):
    # Fampifangaroana ny Hash, Hex8 ary ny Tour mivantana mba tsy ho fixe
    mix_seed = f"{h}{hx}{t_val}TITAN_JUMP_V85.1".encode()
    f_hash = hashlib.sha512(mix_seed).hexdigest()
    
    # Entropy mampiasa ny fiafaran'ny Hash ho an'ny Seed
    random.seed(int(f_hash[:16], 16))
    
    # Logic multiplier miankina amin'ny Hex8 sy ny fihodin'ny Hash
    hex_factor = int(f_hash[-4:], 16) / 65535.0
    
    # Ny elanelana (range) dia miovaova ho azy
    if hex_factor > 0.88: 
        m = round(random.uniform(4.50, 25.00), 2) # High Jump
    elif hex_factor > 0.50: 
        m = round(random.uniform(1.80, 4.49), 2) # Mid Jump
    else: 
        m = round(random.uniform(1.01, 1.79), 2) # Stable
        
    return {"m": m, "hex": f_hash[:8].upper()}

# --- 5. INTERFACE ---
st.markdown("<h3 style='text-align:center; color:#00ffcc;'>🛰️ TITAN V85.1 - JUMP DETECTOR</h3>", unsafe_allow_html=True)

h_in = st.text_input("Combined Hash / Server Seed:")
c1, c2 = st.columns(2)
hx_in = c1.text_input("Hex8 (Extra):")
t_act = c2.number_input("Tour Actuel:", min_value=1, value=8136111)

if st.button("🔥 EXECUTE DYNAMIC SCAN"):
    if h_in:
        with st.spinner("Analyzing Hash Entropy..."):
            time.sleep(0.7)
            r1, r2 = st.columns(2)
            
            # PREDICTION 1: Stable Zone (Offset dynamic miankina amin'ny Hash)
            offset_1 = (int(hashlib.md5(h_in.encode()).hexdigest()[:1], 16) % 3) + 1
            p1_t = t_act + offset_1
            p1 = titan_core_v85(h_in, hx_in, p1_t)
            
            with r1:
                st.markdown(f"""<div class="war-card">
                    <div class="tour-id">PREDICTION TOUR {p1_t}</div>
                    <p class="mult-val">{p1['m']}x</p>
                    <p style="color:#00ffcc; font-size:10px;">HEX8: {p1['hex']}</p>
                    <span style="font-size:11px; border:1px solid #00ffcc; padding:2px 5px;">STABLE SIGNAL</span>
                </div>""", unsafe_allow_html=True)
            
            # PREDICTION 2: Jump Zone (Mikaroka any lavitra aorian'ny offset)
            found_jump = None
            start_scan = t_act + 4 # Scan manomboka any amin'ny tour faha-4
            for i in range(start_scan, start_scan + 15):
                p2 = titan_core_v85(h_in, hx_in, i)
                # Ny Jump dia tsy fixe fa miankina amin'ny entropy hitan'ny milina
                if p2['m'] >= 2.80:
                    found_jump = (i, p2)
                    break
            
            with r2:
                if found_jump:
                    st.markdown(f"""<div class="war-card jump-card">
                        <div class="tour-id" style="color:#ff00ff;">PREDICTION TOUR {found_jump[0]}</div>
                        <p class="mult-val" style="color:#ff00ff;">{found_jump[1]['m']}x</p>
                        <p style="color:#ff00ff; font-size:10px;">HEX8: {found_jump[1]['hex']}</p>
                        <span style="font-size:11px; border:1px solid #ff00ff; padding:2px 5px; color:#ff00ff;">DYNAMIC JUMP DETECTED</span>
                    </div>""", unsafe_allow_html=True)
                else:
                    st.warning("Tsy nisy Jump matanjaka hita tany lavitra. Andramo ovana kely ny Hex8.")
