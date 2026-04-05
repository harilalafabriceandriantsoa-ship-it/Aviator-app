import streamlit as st
import hashlib
import random
import time

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V85.0 ULTRA-DYNAMIC", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- 2. THE WAR-ZONE UI ---
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

# --- 4. ULTRA-DYNAMIC ENGINE ---
def titan_ultra_engine(h, hx, t_val):
    # Fampiasana entropy lalina mba tsy ho fixe
    raw_data = f"{h}{hx}{t_val}TITAN_ULTRA_2026".encode()
    f_hash = hashlib.sha512(raw_data).hexdigest()
    
    # Miovaova ho azy ny multiplier araka ny hash tanteraka
    random.seed(int(f_hash[:16], 16))
    
    # Logic ho an'ny multiplier (tsy fixe)
    val = int(f_hash[-4:], 16) / 65535.0
    if val > 0.90: m = round(random.uniform(5.00, 15.00), 2)
    elif val > 0.60: m = round(random.uniform(2.50, 4.99), 2)
    else: m = round(random.uniform(1.01, 2.49), 2)
        
    return {"m": m, "hex": f_hash[:8].upper()}

# --- 5. INTERFACE ---
st.markdown("<h3 style='text-align:center; color:#00ffcc;'>🛰️ TITAN V85.0 - ULTRA-DYNAMIC SCANNER</h3>", unsafe_allow_html=True)

h_in = st.text_input("Hash / Server Seed:")
c1, c2 = st.columns(2)
hx_in = c1.text_input("Hex8 (Extra):")
t_act = c2.number_input("Tour Actuel:", min_value=1, value=8136036)

if st.button("🔥 EXECUTE DEEP SCAN"):
    if h_in:
        with st.spinner("Scanning for Far Jumps..."):
            time.sleep(0.8)
            r1, r2 = st.columns(2)
            
            # PREDICTION 1: Namboarina hitady tour "Stable" (tsy voatery ho +1)
            # Mampiasa offset dynamic avy amin'ny Hash
            offset_1 = (int(hashlib.md5(h_in.encode()).hexdigest()[:2], 16) % 3) + 1
            p1_t = t_act + offset_1
            p1 = titan_ultra_engine(h_in, hx_in, p1_t)
            
            with r1:
                st.markdown(f"""<div class="war-card">
                    <div class="tour-id">PREDICTION TOUR {p1_t}</div>
                    <p class="mult-val">{p1['m']}x</p>
                    <p style="color:#00ffcc; font-size:10px;">HEX8: {p1['hex']}</p>
                    <span style="font-size:11px; border:1px solid #00ffcc; padding:2px 5px;">DYNAMIC PREDICTION</span>
                </div>""", unsafe_allow_html=True)
            
            # PREDICTION 2: Mikaroka JUMP any lavitra (offset > 4)
            # Tsy mamoaka JUMP raha akaiky loatra
            found = None
            start_scan = t_act + 4 # Manomboka scan 4 tours aorian'ny tour actuel
            for i in range(start_scan, start_scan + 20):
                p2 = titan_ultra_engine(h_in, hx_in, i)
                if p2['m'] >= 3.00: # Mitady multiplier matanjaka
                    found = (i, p2)
                    break
            
            with r2:
                if found:
                    st.markdown(f"""<div class="war-card jump-card">
                        <div class="tour-id" style="color:#ff00ff;">PREDICTION TOUR {found[0]}</div>
                        <p class="mult-val" style="color:#ff00ff;">{found[1]['m']}x</p>
                        <p style="color:#ff00ff; font-size:10px;">HEX8: {found[1]['hex']}</p>
                        <span style="font-size:11px; border:1px solid #ff00ff; padding:2px 5px; color:#ff00ff;">FAR JUMP DETECTED</span>
                    </div>""", unsafe_allow_html=True)
                else:
                    st.warning("Tsy nisy Jump matanjaka hita tany lavitra. Andramo ovana kely ny Hex8.")
