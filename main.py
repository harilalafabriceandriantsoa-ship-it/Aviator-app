import streamlit as st
import hashlib
import random
import time
import hmac

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V85.3 - WAR MACHINE", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'mines_grid' not in st.session_state: st.session_state.mines_grid = ""

# --- 2. STYLE ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ffcc; font-family: 'Courier New', monospace; }
    .war-card {
        background: #0a0a0a; border: 2px solid #00ffcc; 
        padding: 15px; border-radius: 15px; text-align: center; margin-bottom: 10px;
    }
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; max-width: 320px; margin: 0 auto; }
    .mine-cell { aspect-ratio: 1/1; background: #111; border: 1px solid #00ffcc44; display: flex; align-items: center; justify-content: center; font-size: 24px; border-radius: 8px; }
    .cell-star { border: 2px solid #ffff00 !important; background: rgba(255, 255, 0, 0.2); color: #ffff00; box-shadow: 0 0 15px #ffff0044; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN ---
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center;'>🛰️ TITAN ACCESS</h2>", unsafe_allow_html=True)
    if st.text_input("KEY:", type="password") == "2026":
        if st.button("ACTIVATE MACHINE"):
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- 4. ENGINE CORE ---
def titan_core_v85(h, hx, t_val):
    mix_seed = f"{h}{hx}{t_val}TITAN_WAR_V85.3".encode()
    f_hash = hashlib.sha512(mix_seed).hexdigest()
    random.seed(int(f_hash[:16], 16))
    hex_factor = int(f_hash[-4:], 16) / 65535.0
    if hex_factor > 0.86: m = round(random.uniform(4.50, 25.00), 2)
    elif hex_factor > 0.48: m = round(random.uniform(1.85, 4.49), 2)
    else: m = round(random.uniform(1.01, 1.84), 2)
    return {"m": m, "hex": f_hash[:8].upper()}

# --- 5. INTERFACE ---
st.markdown("<h3 style='text-align:center; color:#00ffcc;'>🛰️ TITAN V85.3 - FULL WAR MACHINE</h3>", unsafe_allow_html=True)
tab1, tab2 = st.tabs(["🚀 COSMOS SCANNER", "💣 MINES 1-3 (ULTRA SUR)"])

with tab1:
    h_in = st.text_input("Combined Hash / Server Seed:")
    col_a, col_b = st.columns(2)
    hx_in = col_a.text_input("Hex8 (Extra):")
    t_act = col_b.number_input("Tour Actuel:", min_value=1, value=8136111)
    
    if st.button("🚀 EXECUTE COSMOS SCAN"):
        if h_in:
            with st.spinner("Analyzing Orbits..."):
                time.sleep(0.7)
                r1, r2 = st.columns(2)
                offset_1 = (int(hashlib.md5(h_in.encode()).hexdigest()[:1], 16) % 3) + 1
                p1_t = t_act + offset_1
                p1 = titan_core_v85(h_in, hx_in, p1_t)
                with r1:
                    st.markdown(f'<div class="war-card"><div class="tour-id">PREDICTION TOUR {p1_t}</div><p class="mult-val">{p1["m"]}x</p></div>', unsafe_allow_html=True)
                
                possible_jumps = []
                for i in range(t_act + 4, t_act + 20):
                    res = titan_core_v85(h_in, hx_in, i)
                    if res['m'] >= 2.90: possible_jumps.append((i, res))
                with r2:
                    if possible_jumps:
                        random.seed(int(hashlib.sha256(h_in.encode()).hexdigest()[:8], 16))
                        final_j = random.choice(possible_jumps)
                        st.markdown(f'<div class="war-card" style="border-color:#ff00ff;"><div class="tour-id" style="color:#ff00ff;">JUMP TOUR {final_j[0]}</div><p class="mult-val" style="color:#ff00ff;">{final_j[1]["m"]}x</p></div>', unsafe_allow_html=True)

with tab2:
    st.markdown("##### 🔍 SCAN ULTRA-SUR (MINES 1, 2, 3)")
    # Nampiana slider hifidianana ny isan'ny Mines
    nb_mines = st.select_slider("Nombre de Mines ao amin'ny lalao:", options=[1, 2, 3])
    
    s_seed = st.text_input("Server Seed (Kopiavo avy ao amin'ny Bet261):")
    c_seed = st.text_input("Client Seed (Laharana tour na anaranao):")
    
    if st.button("🛰️ SCAN SAFE SPOTS"):
        if s_seed and c_seed:
            spots = []
            # Raha mines 1-3 dia mamoaka kintana 4-7 tena azo antoka
            num_stars = 7 if nb_mines == 1 else (5 if nb_mines == 2 else 4)
            
            for j in range(num_stars):
                # Triple-Hash Logic (HMAC + SHA256 + MD5) ho an'ny fiarovana
                key = f"TITAN_SAFE_{nb_mines}_{j}".encode()
                msg = f"{s_seed}{c_seed}{j}{time.time()}".encode()
                h_val = hmac.new(key, msg, hashlib.sha256).hexdigest()
                v = int(h_val[j:j+8], 16) % 25
                while v in spots:
                    v = (v + 7) % 25
                spots.append(v)
            
            grid_html = '<div class="mines-grid">'
            for i in range(25):
                is_star = i in spots
                grid_html += f'<div class="mine-cell {"cell-star" if is_star else ""}">{"⭐" if is_star else "⬛"}</div>'
            st.session_state.mines_grid = grid_html + '</div>'
            
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)
        st.success(f"SCAN VITA: Toerana {len(spots)} no azo antoka ho an'ny Mines {nb_mines}")
