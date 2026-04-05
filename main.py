import streamlit as st
import hashlib
import random
import time
import hmac

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V85.0 ULTRA-DYNAMIC", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'mines_grid' not in st.session_state: st.session_state.mines_grid = ""

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
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 4px; max-width: 280px; margin: 0 auto; }
    .mine-cell { aspect-ratio: 1/1; background: #111; border: 1px solid #00ffcc22; display: flex; align-items: center; justify-content: center; font-size: 20px; border-radius: 4px; }
    .cell-star { border: 2px solid #ffff00 !important; background: rgba(255, 255, 0, 0.1); color: #ffff00; }
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

# --- 4. CORE ENGINE (DYNAMIC & RECURSIVE) ---
def titan_engine(h, hx, t_val):
    # Fampiasana Hash sy Hex mba hamokarana multiplier tsy fixe
    raw_data = f"{h}{hx}{t_val}TITAN_V85_STRENGTH".encode()
    f_hash = hashlib.sha512(raw_data).hexdigest()
    
    # Entropy logic mampiasa ny toerana samy hafa amin'ny Hash
    random.seed(int(f_hash[:16], 16))
    # Ny multiplier dia miankina amin'ny bit farany sy ny hex8
    factor = int(f_hash[-2:], 16) / 255.0
    
    if factor > 0.85: m = round(random.uniform(3.50, 10.00), 2)
    elif factor > 0.40: m = round(random.uniform(1.80, 3.49), 2)
    else: m = round(random.uniform(1.05, 1.79), 2)
        
    return {"m": m, "hex": f_hash[:8].upper()}

# --- 5. INTERFACE ---
st.markdown("<h3 style='text-align:center; color:#00ffcc;'>🛰️ TITAN V85.0 - PRO DYNAMIC SCAN</h3>", unsafe_allow_html=True)
t1, t2 = st.tabs(["🚀 COSMOS SCAN", "💣 MINES SCAN"])

with t1:
    h_in = st.text_input("Hash / Server Seed:")
    c1, c2 = st.columns(2)
    hx_in = c1.text_input("Hex8 (Extra):")
    t_act = c2.number_input("Tour Actuel:", min_value=1, value=8132931)
    
    if st.button("🔥 EXECUTE DYNAMIC SCAN"):
        if h_in:
            with st.spinner("Analyzing Entropy..."):
                time.sleep(0.6)
                r1, r2 = st.columns(2)
                
                # PREDICTION TOUR 1 (Tour manaraka mivantana)
                p1_t = t_act + 1
                p1 = titan_engine(h_in, hx_in, p1_t)
                with r1:
                    st.markdown(f"""<div class="war-card">
                        <div class="tour-id">PREDICTION TOUR {p1_t}</div>
                        <p class="mult-val">{p1['m']}x</p>
                        <p style="color:#00ffcc; font-size:10px;">HEX8: {p1['hex']}</p>
                        <span style="font-size:11px; border:1px solid #00ffcc; padding:2px 5px;">STABLE SIGNAL</span>
                    </div>""", unsafe_allow_html=True)
                
                # PREDICTION TOUR 2 (Mikaroka ny JUMP voalohany hita)
                found = None
                for i in range(2, 15):
                    p2_t = t_act + i
                    p2 = titan_engine(h_in, hx_in, p2_t)
                    if p2['m'] >= 2.50: # Ny Jump dia mihoatra ny 2.50x foana
                        found = (p2_t, p2)
                        break
                
                with r2:
                    if found:
                        st.markdown(f"""<div class="war-card jump-card">
                            <div class="tour-id" style="color:#ff00ff;">PREDICTION TOUR {found[0]}</div>
                            <p class="mult-val" style="color:#ff00ff;">{found[1]['m']}x</p>
                            <p style="color:#ff00ff; font-size:10px;">HEX8: {found[1]['hex']}</p>
                            <span style="font-size:11px; border:1px solid #ff00ff; padding:2px 5px; color:#ff00ff;">JUMP DETECTED</span>
                        </div>""", unsafe_allow_html=True)

with t2:
    st.markdown("##### 🔍 MINES RECURSIVE SCAN (6-STAR FIXE)")
    n_m = st.select_slider("Mines ao amin'ny lalao:", options=[1, 2, 3], value=3)
    s_s = st.text_input("Server Seed:")
    c_s = st.text_input("Client Seed / Tour:")
    
    if st.button("🛰️ SCAN FOR SAFE SPOTS"):
        if s_s and c_s:
            # Recursive HMAC Algorithm ho fanamafisana ny Mine
            spots = []
            for j in range(6):
                # Isaky ny kintana dia misy Hash HMAC manokana mba ho "matanjaka" ny kajy
                key = f"MINE_RECURSIVE_{j}_{n_m}".encode()
                msg = f"{s_s}{c_s}{j}".encode()
                h_val = hmac.new(key, msg, hashlib.sha256).hexdigest()
                
                # Fakana ny toerana 0-24
                v = int(h_val[j:j+8], 16) % 25
                while v in spots:
                    v = (v + int(h_val[-1:], 16) + 1) % 25
                spots.append(v)
            
            grid_html = '<div class="mines-grid">'
            for i in range(25):
                is_star = i in spots
                grid_html += f'<div class="mine-cell {"cell-star" if is_star else ""}">{"⭐" if is_star else "⬛"}</div>'
            st.session_state.mines_grid = grid_html + '</div>'
            
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)
