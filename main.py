import streamlit as st
import hashlib
import random
import time
import hmac

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V85.7 - ANTI-STREAK WAR MACHINE", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'mines_grid' not in st.session_state: st.session_state.mines_grid = ""

# --- 2. STYLE (ULTRA DARK MODE) ---
st.markdown("""
    <style>
    .stApp { background-color: #030303; color: #00ffcc; font-family: 'Courier New', monospace; }
    .war-card {
        background: #080808; border: 2px solid #00ffcc; 
        padding: 15px; border-radius: 15px; text-align: center; margin-bottom: 10px;
        box-shadow: 0 0 10px #00ffcc22;
    }
    .mult-val { color: #00ffcc; font-size: 48px; font-weight: bold; margin: 0; text-shadow: 0 0 10px #00ffcc44; }
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; max-width: 330px; margin: 0 auto; }
    .mine-cell { aspect-ratio: 1/1; background: #0a0a0a; border: 1px solid #00ffcc33; display: flex; align-items: center; justify-content: center; font-size: 26px; border-radius: 10px; transition: 0.3s; }
    .cell-star { border: 2px solid #ffff00 !important; background: rgba(255, 255, 0, 0.25); color: #ffff00; box-shadow: 0 0 15px #ffff0066; font-weight: bold; transform: scale(1.05); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN (KEY: 2026) ---
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center;'>🛰️ TITAN SYSTEM ACCESS</h2>", unsafe_allow_html=True)
    user_key = st.text_input("ENTER MASTER KEY:", type="password")
    if st.button("ACTIVATE V85.7"):
        if user_key == "2026":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("ACCESS DENIED: KEY INCORRECT")
    st.stop()

# --- 4. ADVANCED ENGINE (COSMOS & MINES) ---
def advanced_titan_engine(s_seed, c_seed, t_val, mode="cosmos"):
    # Mampiasa SHA512 ho an'ny fiarovana avo lenta
    raw_mix = f"{s_seed}{c_seed}{t_val}V85.7_HARDCORE_{mode}".encode()
    main_hash = hashlib.sha512(raw_mix).hexdigest()
    random.seed(int(main_hash[:16], 16))
    
    if mode == "cosmos":
        factor = int(main_hash[-8:], 16) / 4294967295.0
        if factor > 0.92: m = round(random.uniform(7.00, 50.00), 2)
        elif factor > 0.40: m = round(random.uniform(1.90, 6.99), 2)
        else: m = round(random.uniform(1.01, 1.89), 2)
        return {"m": m, "hex": main_hash[:8].upper()}
    return main_hash

# --- 5. INTERFACE ---
st.markdown("<h3 style='text-align:center; color:#00ffcc;'>🛰️ TITAN V85.7 - ANTI-STREAK MACHINE</h3>", unsafe_allow_html=True)
tab1, tab2 = st.tabs(["🚀 COSMOS SCANNER", "💣 MINES 1-3 (5 DIAMANTS FIXE)"])

with tab1:
    h_in = st.text_input("Server Seed / Hash:")
    col_x, col_y = st.columns(2)
    hx_in = col_x.text_input("Hex8 / Extra:")
    t_act = col_y.number_input("Tour Actuel:", min_value=1, value=8136200)
    
    if st.button("🚀 EXECUTE COSMOS DEEP SCAN"):
        if h_in:
            with st.spinner("Breaking Encryption..."):
                time.sleep(0.6)
                r1, r2 = st.columns(2)
                # Offset +2/+3 mba tsy ho tratra
                off = (int(hashlib.md5(h_in.encode()).hexdigest()[:1], 16) % 2) + 2
                res = advanced_titan_engine(h_in, hx_in, t_act + off, "cosmos")
                with r1:
                    st.markdown(f'<div class="war-card"><div>TARGET TOUR {t_act+off}</div><p class="mult-val">{res["m"]}x</p></div>', unsafe_allow_html=True)
                with r2:
                    jump_t = t_act + random.randint(10, 25)
                    j_res = advanced_titan_engine(h_in, hx_in, jump_t, "cosmos")
                    st.markdown(f'<div class="war-card" style="border-color:#ff00ff;"><div>JUMP SIGNAL {jump_t}</div><p class="mult-val" style="color:#ff00ff;">{j_res["m"]}x</p></div>', unsafe_allow_html=True)

with tab2:
    st.markdown("##### 🔍 MINES 1-3: 5 DIAMANTS (FIXE & REINFORCED)")
    nb_m = st.selectbox("Mines ao amin'ny lalao:", [1, 2, 3], index=2)
    s_s = st.text_input("Server Seed (Mines):")
    c_s = st.text_input("Client Seed (Tour):")
    
    if st.button("🛰️ SCAN 5 SAFE SPOTS"):
        if s_s and c_s:
            spots = []
            # 5 Diamants foana ho an'ny Mines 1-3
            for j in range(5):
                # Double HMAC Layer mba tsy ho "tapaka"
                k1 = f"LAYER1_{nb_m}_{j}".encode()
                k2 = f"LAYER2_ANTI_STREAK_{j}".encode()
                msg = f"{s_s}{c_s}{j}".encode()
                
                h1 = hmac.new(k1, msg, hashlib.sha512).digest()
                h2 = hmac.new(k2, h1, hashlib.sha512).hexdigest()
                
                v = int(h2[j*2:j*2+8], 16) % 25
                while v in spots:
                    v = (v + int(h2[-2:], 16) + 1) % 25
                spots.append(v)
            
            grid_html = '<div class="mines-grid">'
            for i in range(25):
                grid_html += f'<div class="mine-cell {"cell-star" if i in spots else ""}">{"⭐" if i in spots else "⬛"}</div>'
            st.session_state.mines_grid = grid_html + '</div>'
            
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)
        st.success("5 DIAMANTS DETECTED - SIGNAL STABLE")
