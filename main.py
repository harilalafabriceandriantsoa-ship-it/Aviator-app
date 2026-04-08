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
        ax.axhline(x, color='#00ff00', lw=2)
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

    schema = grid[:5]  # fixe 5 diamants
    mines = grid[5:5+nb_mines]
    safe_slots = [i for i in range(25) if i not in mines]

    # Résultat samihafa arakaraka ny nb_mines
    base_result = (4294967295 * 0.97) / (int.from_bytes(h[:8],"big") % 999999999)
    resultat = round(base_result / (nb_mines + 0.5), 2)
    if resultat < 1.0:
        resultat = 1.0

    probs = []
    for k in range(len(safe_slots)):
        p = round(((len(safe_slots)-k)/(25-k))*100,2)
        probs.append(p)

    return schema, mines, safe_slots, probs, heure, resultat

# --- COSMOS PREMIUM ENGINE ---
def cosmos_prediction(server_seed, client_seeds, tour_actuel):
    heure = datetime.datetime.now().strftime("%H:%M:%S")
    combined = server_seed + ":" + ":".join(client_seeds) + f":{tour_actuel}:{heure}:COSMOSX"
    h = hashlib.sha512(combined.encode()).hexdigest()

    hex_val = h[-8:]
    dec_val = int(hex_val,16)
    constante = 4294967295
    rtp = 0.97
    resultat = (constante * rtp) / dec_val
    if resultat < 1.0:
        resultat = 1.0

    p_int = int(h[:16],16)
    heure_val = int(heure.replace(":",""))
    jump1 = (p_int % 12) + (heure_val % 5)
    jump2 = (p_int % 18) + (heure_val % 7)

    tour1 = tour_actuel + jump1
    tour2 = tour_actuel + jump2

    vals = [int(h[i:i+2],16)/10 for i in range(0,20,2)]
    min_val = min(vals)
    max_val = max(vals)
    mean_val = round(statistics.mean(vals),2)
    accuracy = round((mean_val/max_val)*100,2)

    return {
        "tour_actuel": tour_actuel,
        "tour1": tour1,
        "tour2": tour2,
        "min": min_val,
        "mean": mean_val,
        "max": max_val,
        "accuracy": accuracy
    }

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
        schema,mines,safe_slots,probs,heure,resultat = mines_ultra_engine(s_seed,c_seeds,nb_mines,tour_actuel)
        draw_styled_board(schema,mines)
        st.success(f"Diamants (fixe 5): {schema}")
        st.warning(f"Mines ({nb_mines}): {mines}")
        st.info(f"Safe Slots: {safe_slots}")
        st.info(f"Probabilités dynamique: {probs}")
        st.info(f"Heure kajy: {heure}")
        st.metric("Résultat",f"{resultat}x")

with tab2:
    tour_actuel = st.number_input("Tour Actuel Cosmos:",min_value=1,value=8147979)
    if st.button("🌠 ANALYZE COSMOS"):
        res = cosmos_prediction(s_seed,c_seeds,tour_actuel)
        st.success(f"Tour Actuel: {res['tour_actuel']}")
        st.info(f"Tour 1 → {res['tour1']}")
        st.info(f"Tour 2 → {res['tour2']}")
        m1,m2,m3,m4 = st.columns(4)
        m1.metric("MIN",f"{res['min']}x")
        m2.metric("MEAN",f"{res['mean']}x")
        m3.metric("MAX",f"{res['max']}x")
        m4.metric("ACCURACY",f"{res['accuracy']}%")
