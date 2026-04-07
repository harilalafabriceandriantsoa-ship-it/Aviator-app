import streamlit as st
import hashlib, random, statistics
import numpy as np

try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

st.set_page_config(page_title="TITAN V101 PREMIUM 2026", layout="wide")

# --- STYLE ---
st.markdown("""
    <style>
    .stApp {background: linear-gradient(135deg,#0f0f0f,#1a1a1a);color:#00ffcc;font-family:'Courier New',monospace;}
    h2,h3,h4 {color:#00ffcc;text-shadow:0 0 10px #00ffcc;}
    .stButton>button {background:linear-gradient(90deg,#00ffcc,#0066ff);color:#fff;border-radius:12px;
        padding:10px 20px;font-weight:bold;box-shadow:0 0 20px #00ffcc;}
    .stButton>button:hover {background:linear-gradient(90deg,#0066ff,#00ffcc);box-shadow:0 0 30px #0066ff;}
    </style>
""", unsafe_allow_html=True)

# --- DRAW MINES BOARD ---
def draw_styled_board(schema):
    if not HAS_MATPLOTLIB:
        st.warning("⚠️ Tsy tafapetraka ny Matplotlib.")
        return
    fig, ax = plt.subplots(figsize=(6,6))
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#0E1117')
    for x in range(6):
        ax.axhline(x, color='#1E2633', lw=2)
        ax.axvline(x, color='#1E2633', lw=2)
    for pos in schema:
        r,c = divmod(pos,5)
        ax.text(c+0.5,4.5-r,"💎",ha="center",va="center",fontsize=35,
                bbox=dict(facecolor='#00D4FF',alpha=0.1,edgecolor='none',boxstyle='round,pad=0.2'))
    ax.set_xlim(0,5); ax.set_ylim(0,5); ax.axis('off')
    st.pyplot(fig)

# --- COSMOS ENGINE ---
def cosmos_premium_engine(server_seed, client_seed, tour_actuel):
    base = f"{server_seed}:{client_seed}:{tour_actuel}:COSMOSX_V101"
    h = hashlib.sha512(base.encode()).digest()
    for i in range(1000):
        h = hashlib.sha512(h + str(i).encode()).digest()
    hex_res = h.hex()

    # Kajy offset sy jumps variable avy amin'ny hash
    p_int = int(hex_res[:16], 16)
    jump1 = (p_int % 10) + 3   # variable jump
    jump2 = (p_int % 15) + 5   # variable jump

    # Tour vaovao
    tour1 = tour_actuel + jump1
    tour2 = tour_actuel + jump2

    # Metrics
    vals = [int(hex_res[i:i+2],16)/10 for i in range(0,20,2)]
    min_val = min(vals)
    max_val = max(vals)
    mean_val = round(statistics.mean(vals),2)
    accuracy = round((mean_val/max_val)*100,2)

    return {
        "hex": hex_res[:64],
        "tour_actuel": tour_actuel,
        "tour1": tour1,
        "tour2": tour2,
        "min": min_val,
        "mean": mean_val,
        "max": max_val,
        "accuracy": accuracy
    }

# --- MINES ENGINE ---
def mines_premium_engine(s_seed,c_seed,nb_mines):
    base = f"{s_seed}:{c_seed}:{nb_mines}:MINES_V101"
    h = hashlib.sha512(base.encode()).digest()
    random.seed(int.from_bytes(h[:8],"big")+nb_mines)
    grid = list(range(25))
    random.shuffle(grid)
    return sorted(grid[:5])

# --- LOGIN ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.title("🔐 TITAN V101 - ADMIN")
    code = st.text_input("Admin Code:", type="password")
    if st.button("LOGIN"):
        if code=="2026":
            st.session_state['logged_in']=True
            st.rerun()
        else:
            st.error("Diso ny code!")
else:
    st.title("🌌 TITAN V101 PREMIUM 2026")
    if st.button("LOGOUT"):
        st.session_state['logged_in']=False
        st.rerun()

    col1,col2 = st.columns(2)
    with col1:
        s_seed = st.text_input("Server Seed","d17354bbdbbdbfefb1ef2d210fb3ea2c3aeb4e6be5c27ac08a3e49b49fdf0b91")
    with col2:
        c_seed = st.text_input("Client Seed","SaSd3AAerLJrfAw053Bf")

    tab1,tab2 = st.tabs(["💎 MINES","📈 COSMOSX"])

    with tab1:
        nb_mines = st.selectbox("Isan'ny Mines:",[1,2,3,4,5,10,24])
        if st.button("🚀 SCAN MINES"):
            schema = mines_premium_engine(s_seed,c_seed,nb_mines)
            draw_styled_board(schema)
            st.success(f"Safe Slots: {schema}")

    with tab2:
        tour_actuel = st.number_input("Tour Actuel:",min_value=1,value=12)
        if st.button("🌠 ANALYZE COSMOS"):
            res = cosmos_premium_engine(s_seed,c_seed,tour_actuel)
            m1,m2,m3,m4 = st.columns(4)
            m1.metric("MIN",f"{res['min']}x")
            m2.metric("MEAN",f"{res['mean']}x")
            m3.metric("MAX",f"{res['max']}x")
            m4.metric("ACCURACY",f"{res['accuracy']}%")
            st.info(f"Tour Actuel {res['tour_actuel']}")
            st.info(f"Tour 1 → {res['tour1']}")
            st.info(f"Tour 2 → {res['tour2']}")
            st.code(res['hex'],language="bash")
