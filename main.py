import streamlit as st
import hashlib, random, statistics, datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="TITAN V101 PREMIUM ULTRA FIABLE", layout="wide")

# --- STYLE ---
st.markdown("""
    <style>
    .stApp {background: linear-gradient(135deg,#0f0f0f,#1a1a1a);color:#00ffcc;font-family:'Courier New',monospace;}
    h1,h2,h3,h4 {color:#00ffcc;text-shadow:0 0 15px #00ffcc;}
    .stButton>button {background:linear-gradient(90deg,#00ffcc,#0066ff);color:#fff;border-radius:12px;
        padding:12px 24px;font-weight:bold;box-shadow:0 0 25px #00ffcc;}
    .stButton>button:hover {background:linear-gradient(90deg,#0066ff,#00ffcc);box-shadow:0 0 35px #0066ff;}
    </style>
""", unsafe_allow_html=True)

# --- DRAW MINES BOARD (stylé neon) ---
def draw_styled_board(schema, mines):
    fig, ax = plt.subplots(figsize=(6,6))
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#0E1117')
    for x in range(6):
        ax.axhline(x, color='#00ff00', lw=2)  # neon green grid
        ax.axvline(x, color='#00ff00', lw=2)
    for pos in schema:
        r,c = divmod(pos,5)
        ax.text(c+0.5,4.5-r,"💎",ha="center",va="center",fontsize=35,
                bbox=dict(facecolor='#00D4FF',alpha=0.3,edgecolor='none',boxstyle='round,pad=0.2'))
    for pos in mines:
        r,c = divmod(pos,5)
        ax.text(c+0.5,4.5-r,"💣",ha="center",va="center",fontsize=30,
                bbox=dict(facecolor='#FF0044',alpha=0.3,edgecolor='none',boxstyle='round,pad=0.2'))
    ax.set_xlim(0,5); ax.set_ylim(0,5); ax.axis('off')
    st.pyplot(fig)

# --- MINES ULTRA ENGINE ---
def mines_ultra_engine(server_seed, client_seeds, nb_mines, tour_actuel):
    heure = datetime.datetime.now().strftime("%H:%M:%S")
    combined = server_seed + ":" + ":".join(client_seeds) + f":{nb_mines}:{tour_actuel}:{heure}:MINES_ULTRA"
    h = hashlib.sha512(combined.encode()).digest()
    hash_int = int.from_bytes(h, "big")

    grid = list(range(25))
    for i in range(24,0,-1):
        j = hash_int % (i+1)
        grid[i],grid[j] = grid[j],grid[i]
        hash_int //= (i+1)

    random.seed(int.from_bytes(h[:16],"big") ^ nb_mines ^ tour_actuel)
    for _ in range(5):
        random.shuffle(grid)

    schema = grid[:5]  # diamants fixe 5
    mines = grid[5:5+nb_mines]
    safe_slots = [i for i in range(25) if i not in mines]

    probs = []
    for k in range(len(safe_slots)):
        p = round(((len(safe_slots)-k)/(25-k))*100,2)
        probs.append(p)

    return schema, mines, safe_slots, probs, heure

# --- COSMOS PREMIUM ENGINE ---
def cosmos_prediction(server_seed, client_seeds, tour_actuel):
    heure = datetime.datetime.now().strftime("%H:%M:%S")
    combined = server_seed + ":" + ":".join(client_seeds) + f":{tour_actuel}:{heure}:COSMOSX"
    h = hashlib.sha512(combined.encode()).hexdigest()

    # Calcul interne (tsy aseho amin'ny UI)
    hex_val = h[-8:]
    dec_val = int(hex_val,16)
    constante = 4294967295
    rtp = 0.97
    resultat = (constante * rtp) / dec_val
    if resultat < 1.0:
        resultat = 1.0

    # Dynamic jumps
    p_int = int(h[:16],16)
    heure_val = int(heure.replace(":",""))
    jump1 = (p_int % 12) + (heure_val % 5)
    jump2 = (p_int % 18) + (heure_val % 7)

    tour1 = tour_actuel + jump1
    tour2 = tour_actuel + jump2

    return tour1, tour2

# --- INTERFACE ---
st.title("🌌 TITAN V101 PREMIUM ULTRA FIABLE")

col1,col2 = st.columns(2)
with col1:
    s_seed = st.text_input("Server Seed","8763ac0c2e46896c640450c91894b7bb6c71d771766ba411e93499")
with col2:
    c_seeds = st.text_area("Client Seeds (separate by comma)","kaAfYhzp2OBQI8FPZkfg,BprqDhXFlmUcJYRXHnye,BOfwf4M0EXIFO5l4bj6t").split(",")

tab1,tab2 = st.tabs(["💎 MINES","📈 COSMOSX"])

with tab1:
    nb_mines = st.selectbox("Isan'ny Mines:",[1,2,3])
    tour_actuel = st.number_input("Tour Actuel:",min_value=1,value=8147979)
    if st.button("🚀 SCAN MINES"):
        schema,mines,safe_slots,probs,heure = mines_ultra_engine(s_seed,c_seeds,nb_mines,tour_actuel)
        draw_styled_board(schema,mines)
        st.success(f"Diamants (fixe 5): {schema}")
        st.warning(f"Mines ({nb_mines}): {mines}")
        st.info(f"Safe Slots: {safe_slots}")
        st.info(f"Probabilités dynamique: {probs}")
        st.info(f"Heure kajy: {heure}")

with tab2:
    tour_actuel = st.number_input("Tour Actuel Cosmos:",min_value=1,value=8147979)
    if st.button("🌠 ANALYZE COSMOS"):
        tour1, tour2 = cosmos_prediction(s_seed,c_seeds,tour_actuel)
        st.success(f"Tour Actuel: {tour_actuel}")
        st.info(f"Tour 1 → {tour1}")
        st.info(f"Tour 2 → {tour2}")
