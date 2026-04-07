import streamlit as st
import hashlib, random, statistics
import numpy as np

try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

st.set_page_config(page_title="TITAN V101 PREMIUM", layout="wide")

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

    # Jump variable avy amin'ny hash
    p_int = int(hex_res[:16], 16)
    jump1 = (p_int % 10) + 3
    jump2 = (p_int % 15) + 5

    tour1 = tour_actuel + jump1
    tour2 = tour_actuel + jump2

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

# --- MINES ULTRA ENGINE ---
def mines_ultra_engine(server_seed, client_seed, nb_mines, iters=100000):
    base = f"{server_seed}:{client_seed}:{nb_mines}:ULTRA_V102"
    h1 = hashlib.sha512(base.encode()).digest()
    h2 = hashlib.blake2b(h1).digest()
    h3 = hashlib.sha3_256(h2).digest()
    h4 = hashlib.sha384(h3).digest()
    h5 = hashlib.sha256(h4).digest()
    h_mut = h1
    for i in range(iters):
        h_mut = hashlib.sha512(h_mut + f"STEP{i}".encode()).digest()
    combined = h1 + h2 + h3 + h4 + h5 + h_mut
    hash_int = int.from_bytes(combined, "big")

    grid = list(range(25))
    for i in range(24,0,-1):
        j = hash_int % (i+1)
        grid[i],grid[j] = grid[j],grid[i]
        hash_int //= (i+1)

    random.seed(int.from_bytes(h3[:16],"big") ^ nb_mines)
    for _ in range(5):
        random.shuffle(grid)

    schema = grid[:5]
    if len(set(schema))<5 or max(schema)-min(schema)<3:
        random.shuffle(grid)
        schema = grid[:5]

    probs = []
    for k in range(5):
        p = round(((5-k)/(25-k))*100,2)
        probs.append(p)

    return schema, probs

# --- INTERFACE ---
st.title("🌌 TITAN V101 PREMIUM")

col1,col2 = st.columns(2)
with col1:
    s_seed = st.text_input("Server Seed","d17354bbdbbdbfefb1ef2d210fb3ea2c3aeb4e6be5c27ac08a3e49b49fdf0b91")
with col2:
    c_seed = st.text_input("Client Seed","SaSd3AAerLJrfAw053Bf")

tab1,tab2 = st.tabs(["💎 MINES","📈 COSMOSX"])

with tab1:
    nb_mines = st.selectbox("Isan'ny Mines:",[1,2,3,4,5,10,24])
    if st.button("🚀 SCAN MINES"):
        schema,probs = mines_ultra_engine(s_seed,c_seed,nb_mines)
        draw_styled_board(schema)
        st.success(f"Safe Slots: {schema}")
        st.info(f"Probabilités dynamique: {probs}")

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
