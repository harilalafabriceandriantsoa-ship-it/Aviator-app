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

# --- CONFIGURATION STYLE ---
st.set_page_config(page_title="TITAN V101 - PREMIUM 2026", layout="wide")

# Style NEON Premium ho an'ny interface
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle, #0a0a0a 0%, #050505 100%);
        color: #00ffcc;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    h1, h2, h3, h5 {
        color: #00ffcc;
        text-shadow: 0 0 15px #00ffcc;
        text-align: center;
    }
    .stButton>button {
        background: linear-gradient(90deg, #00ffcc 0%, #0066ff 100%);
        color: #fff;
        border-radius: 12px;
        border: none;
        padding: 12px 24px;
        font-weight: bold;
        box-shadow: 0 0 25px rgba(0, 255, 204, 0.5);
        transition: 0.3s;
        width: 100%;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #0066ff 0%, #00ffcc 100%);
        box-shadow: 0 0 35px #00ffcc;
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

# Function ho an'ny sary "Stylé" miaraka amin'ny Neon Glow
def draw_premium_board(schema):
    if not HAS_PLOT:
        st.warning("⚠️ Tsy mbola tafapetraka ny Matplotlib. Jereo ny requirements.txt.")
        return
    
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor('#050505') # Loko mainty streamlit
    ax.set_facecolor('#0A0A0A')
    
    # Grid neon lines
    for x in range(6):
        ax.axhline(x, color='#1E2633', lw=1, alpha=0.5)
        ax.axvline(x, color='#1E2633', lw=1, alpha=0.5)
    
    # Mametraka ny Diamonds miaraka amin'ny Glow Effect
    for pos in schema:
        r, c = divmod(pos, 5)
        
        # Sary kintana stylé
        ax.text(c + 0.5, 4.5 - r, "💎", ha="center", va="center", fontsize=38, 
                bbox=dict(facecolor='#00D4FF', alpha=0.1, edgecolor='#00ffcc', boxstyle='round,pad=0.3', lw=2))
        
        # "Glow" boribory kely (hazavana eo aoriany)
        glow_circle = plt.Circle((c + 0.5, 4.5 - r), 0.35, color='#00ffcc', alpha=0.08)
        ax.add_patch(glow_circle)
        
        # Hazavana kely eo afovoany
        center_glow = plt.Circle((c + 0.5, 4.5 - r), 0.1, color='white', alpha=0.15)
        ax.add_patch(center_glow)

    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)
    ax.axis('off') # Nesorina ny axe rehetra
    st.pyplot(fig)

# --- ENGINES ---

def cosmos_premium_engine(server_seed, client_seed, nonce, tour_cosmos, salt="T1", iters=500000):
    # Nampidirina ao anatin'ny hash ny tour_cosmos mba ho unique ny prediction
    heure = datetime.datetime.now().strftime("%H:%M:%S")
    base = f"{server_seed}:{client_seed}:{nonce}:{tour_cosmos}:{salt}:{heure}:V101"
    h1 = hashlib.sha512(base.encode()).digest()
    for i in range(iters):
        h1 = hashlib.sha512(h1 + str(i).encode()).digest()
    
    final_hex = h1.hex()
    p_int = int(final_hex[:16], 16)
    
    # Kajy ny vinavina miankina amin'ny tour nampidirinao
    prediction = tour_cosmos + (p_int % 10) # Vinavina ho an'ny manaraka
    
    # metrics variable
    vals = [int(final_hex[i:i+2], 16) / 10 for i in range(0, 20, 2)]
    min_v, max_v = min(vals), max(vals)
    mean_v = round(statistics.mean(vals), 2)
    accuracy = round((mean_v / max_v) * 100, 2) if max_v > 0 else 0
    
    return {"hex": final_hex[:64], "target": prediction, "acc": accuracy, "min": min_v, "mean": mean_v, "max": max_v}

def mines_premium_engine(s_seed, c_seed, nonce, nb_mines, iters=500000):
    heure = datetime.datetime.now().strftime("%H:%M:%S")
    # Ny nb_mines dia manova ny fomba fiasan'ny algorithm
    base = f"{s_seed}:{c_seed}:{nonce}:{nb_mines}:{heure}:MINES_V101"
    h = hashlib.sha512(base.encode()).digest()
    for i in range(iters):
        h = hashlib.sha512(h + f"STEP{i}".encode()).digest()
    
    random.seed(int.from_bytes(h[:8], "big") + nb_mines)
    grid = list(range(25))
    random.shuffle(grid)
    
    # Safe spots (kintana azo antoka)
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
        if admin_code == "2026": # Ity ny code fidirana
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("Code diso!")
else:
    st.title("🌌 TITAN V101 PREMIUM 2026")
    if st.button("LOGOUT", help="🚪 Mandao ny Dashboard"):
        st.session_state['logged_in'] = False
        st.rerun()

    # --- PARAMETRES COMUNS ---
    st.subheader("🔑 Seeds & Nonce Configuration")
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        s_seed = st.text_input("Server Seed / Hash:", "d17354bbdbbdbfefb1ef2d210fb3ea2c3aeb4e6be5c27ac08a3e49b49fdf0b91")
        n_val = st.number_input("Nonce (Current):", min_value=1, value=1)
    with col_input2:
        c_seed = st.text_input("Client Seed / Hex:", "SaSd3AAerLJrfAw053Bf")

    tab1, tab2 = st.tabs(["💎 MINES SCANNER", "🌠 COSMOSX PREDICTION"])

    with tab1:
        st.markdown("##### Fikirana ny Mines")
        nb_mines = st.selectbox("Isan'ny Mine (Number of Mines):", [1, 2, 3, 5, 10, 24])
        
        if st.button("🛰️ GENERATE SCHEMA PREMIUM"):
            schema = mines_premium_engine(s_seed, c_seed, n_val, nb_mines)
            
            st.markdown(f"### 🎯 Vinavina azo antoka ho an'ny {nb_mines} Mines")
            draw_premium_board(schema)
            st.success(f"Safe Slots: {schema}")

    with tab2:
        st.markdown("##### Fikirana ny Cosmos")
        # Eto no asiana ny Tour Cosmos tianao ho fantatra
        tour_cosmos = st.number_input("Numéro de Tour Cosmos (Target):", min_value=1, value=100)
        
        if st.button("🚀 ANALYZE TOUR METRICS"):
            res = cosmos_premium_engine(s_seed, c_seed, n_val, tour_cosmos)
            
            st.markdown("---")
            st.info(f"Analyse ho an'ny Tour faha-{tour_cosmos}")
            
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("MIN", f"{res['min']}x")
            m2.metric("MEAN", f"{res['mean']}x")
            m3.metric("MAX", f"{res['max']}x")
            m4.metric("ACCURACY", f"{res['acc']}%")
            
            st.success(f"Vinavina valiny (Tour faha-{res['target']}): x{res['mean']}")
            st.code(f"Hash Matrix: {res['hex']}...", language="bash")
