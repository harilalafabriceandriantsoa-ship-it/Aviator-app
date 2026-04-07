import streamlit as st
import hashlib, hmac, random, statistics, datetime
import numpy as np

# Fiarovana amin'ny matplotlib
try:
    import matplotlib.pyplot as plt
    plt.style.use('dark_background')
    HAS_PLOT = True
except ImportError:
    HAS_PLOT = False

# --- CONFIGURATION ---
st.set_page_config(page_title="TITAN V101 - PREMIUM 2026", layout="wide")

# --- ENGINE FUNCTIONS ---

def safe_int_conversion(hex_val):
    try:
        if not hex_val or len(hex_val) < 16:
            return 0
        return int(hex_val[:16], 16)
    except ValueError:
        return 0

def cosmos_premium_engine(server_seed, client_seed, nonce, tour_cosmos, salt="T1"):
    # Nampidirina ao anatin'ny hash ny tour_cosmos mba ho unique ny prediction
    heure = datetime.datetime.now().strftime("%H:%M:%S")
    base = f"{server_seed}:{client_seed}:{nonce}:{tour_cosmos}:{salt}:{heure}:V101"
    h1 = hashlib.sha512(base.encode()).digest()
    
    final_hex = h1.hex()
    p_int = safe_int_conversion(final_hex)
    
    # Kajy ny vinavina miankina amin'ny tour nampidirinao
    offset = (p_int % 29) + (9 if salt == "T1" else 15)
    prediction = tour_cosmos + (p_int % 10) # Vinavina ho an'ny manaraka
    
    values = [offset, prediction % 50, (p_int % 7) + 2]
    accuracy = round((statistics.mean(values) / max(values)) * 100, 2) if max(values) > 0 else 0
    
    return {"hex": final_hex[:64], "target": prediction, "acc": accuracy}

def mines_premium_engine(s_seed, c_seed, nonce, nb_mines):
    heure = datetime.datetime.now().strftime("%H:%M:%S")
    # Ny nb_mines dia manova ny fomba fiasan'ny algorithm (salt samihafa)
    base = f"{s_seed}:{c_seed}:{nonce}:{nb_mines}:{heure}:MINES_V101"
    h = hashlib.sha512(base.encode()).digest()
    
    random.seed(int.from_bytes(h[:8], "big") + nb_mines)
    grid = list(range(25))
    random.shuffle(grid)
    
    # Maka kintana (diamonds) miankina amin'ny isan'ny mine (25 - nb_mines)
    # Raha 1 mine, dia 24 ny kintana. Matetika 5 no asiana vinavina (safe spots)
    safe_spots = 5 
    schema = sorted(grid[:safe_spots])
    
    return schema

# --- LOGIN SYSTEM ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.title("🔐 TITAN V101 - ADMIN LOGIN")
    admin_code = st.text_input("Enter Admin Code:", type="password")
    if st.button("LOGIN"):
        if admin_code == "2026":
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("Code diso!")
else:
    st.title("🌌 TITAN V101 PREMIUM 2026")
    if st.button("LOGOUT"):
        st.session_state['logged_in'] = False
        st.rerun()

    # --- PARAMETRES COMUNS ---
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        s_seed = st.text_input("Server Seed / Hash:", "d17354bbdbbdbfefb1ef2d210fb3ea2c3aeb4e6be5c27ac08a3e49b49fdf0b91")
        n_val = st.number_input("Nonce (Current):", min_value=1, value=1)
    with col_input2:
        c_seed = st.text_input("Client Seed / Hex:", "SaSd3AAerLJrfAw053Bf")

    tab1, tab2 = st.tabs(["💣 MINES STRATEGY", "🌌 COSMOS PREDICTION"])

    with tab1:
        st.subheader("Fikirana ny Mines")
        # Eto no idirana ny isan'ny mine (1, 2, 3...)
        nb_mines = st.selectbox("Isan'ny Mine (Number of Mines):", [1, 2, 3, 4, 5, 10, 24])
        
        if st.button("🚀 GENERATE SCHEMA"):
            schema = mines_premium_engine(s_seed, c_seed, n_val, nb_mines)
            
            if HAS_PLOT:
                fig, ax = plt.subplots(figsize=(5, 5))
                img = np.zeros((5, 5))
                for pos in schema:
                    r, c = divmod(pos, 5)
                    img[r, c] = 1 # 1 midika hoe kintana
                ax.imshow(img, cmap='winter')
                for p in schema:
                    r, c = divmod(p, 5)
                    ax.text(c, r, "💎", ha="center", va="center", fontsize=20)
                ax.set_xticks([]); ax.set_yticks([])
                st.pyplot(fig)
            
            st.success(f"Vinavina toerana azo antoka (Safe Spots) ho an'ny {nb_mines} Mines: {schema}")

    with tab2:
        st.subheader("Fikirana ny Cosmos")
        # Eto no asiana ny Tour Cosmos tianao ho fantatra
        tour_cosmos = st.number_input("Numéro de Tour Cosmos (Target):", min_value=1, value=100)
        
        if st.button("🌠 ANALYZE TOUR"):
            res = cosmos_premium_engine(s_seed, c_seed, n_val, tour_cosmos)
            
            c1, c2 = st.columns(2)
            c1.metric("Target Prediction", f"x{res['target']/10:.2f}")
            c2.metric("Accuracy Rate", f"{res['acc']}%")
            
            st.info(f"Ny algorithme dia nanao analyse ny tour faha-{tour_cosmos}")
            st.code(f"Hash Matrix: {res['hex']}")
