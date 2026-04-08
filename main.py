import streamlit as st
import hashlib, random, statistics, datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="TITAN V101 PREMIUM", layout="wide")

# --- STYLE ---
st.markdown("""
    <style>
    .stApp {background: linear-gradient(135deg,#0f0f0f,#1a1a1a);color:#00ffcc;font-family:'Courier New',monospace;}
    h1,h2,h3,h4 {color:#00ffcc;text-shadow:0 0 10px #00ffcc;}
    .stButton>button {background:linear-gradient(90deg,#00ffcc,#0066ff);color:#fff;border-radius:12px;
        padding:10px 20px;font-weight:bold;box-shadow:0 0 20px #00ffcc;}
    .stButton>button:hover {background:linear-gradient(90deg,#0066ff,#00ffcc);box-shadow:0 0 30px #0066ff;}
    </style>
""", unsafe_allow_html=True)

# --- LOGIN KATHY ---
st.sidebar.title("🔐 Login Kathy")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
if username and password:
    st.sidebar.success(f"Bienvenue {username} !")

# --- DRAW MINES BOARD ---
def draw_styled_board(schema, mines):
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
    for pos in mines:
        r,c = divmod(pos,5)
        ax.text(c+0.5,4.5-r,"💣",ha="center",va="center",fontsize=25,
                bbox=dict(facecolor='#FF0044',alpha=0.1,edgecolor='none',boxstyle='round,pad=0.2'))
    ax.set_xlim(0,5); ax.set_ylim(0,5); ax.axis('off')
    st.pyplot(fig)

# --- MINES ULTRA ENGINE ---
def mines_ultra_engine(server_seed, client_seed, nb_mines, tour_actuel):
    heure = datetime.datetime.now().strftime("%H:%M:%S")
    base = f"{server_seed}:{client_seed}:{nb_mines}:{tour_actuel}:{heure}:MINES_ULTRA"
    h = hashlib.sha512(base.encode()).digest()
    hash_int = int.from_bytes(h, "big")

    grid = list(range(25))
    for i in range(24,0,-1):
        j = hash_int % (i+1)
        grid[i],grid[j] = grid[j],grid[i]
        hash_int //= (i+1)

    random.seed(int.from_bytes(h[:16],"big") ^ nb_mines ^ tour_actuel)
    for _ in range(5):
        random.shuffle(grid)

    # Fixe 5 diamants
    schema = grid[:5]
    mines = grid[5:5+nb_mines]
    safe_slots = [i for i in range(25) if i not in mines]

    probs = []
    for k in range(len(safe_slots)):
        p = round(((len(safe_slots)-k)/(25-k))*100,2)
        probs.append(p)

    return schema, mines, safe_slots, probs, heure

# --- COSMOS PREMIUM ENGINE ---
def cosmos_premium_engine(server_seed, client_seed, tour_actuel):
    heure = datetime.datetime.now().strftime("%H:%M:%S")
    base = f"{server_seed}:{client_seed}:{tour_actuel}:{heure}:COSMOSX"
    h = hashlib.sha512(base.encode()).hexdigest()

    hex_val = h[-8:]
    dec_val = int(hex_val,16)
    constante = 4294967295
    rtp = 0.97
    resultat = (constante * rtp) / dec_val
    if resultat < 1.0:
        resultat = 1.0

    # Dynamic jumps (not fixed)
    p_int = int(h[:16],16)
    jump1 = (p_int % 12) + (int(heure.replace(":","")) % 5)
    jump2 = (p_int % 18) + (int(heure.replace(":","")) % 7)
    tour1 = tour_actuel + jump1
    tour2 = tour_actuel + jump2

    vals = [int(h[i:i+2],16)/10 for i in range(0,20,2)]
    min_val = min(vals)
    max_val = max(vals)
    mean_val = round(statistics.mean(vals),2)
    accuracy = round((mean_val/max_val)*100,2)

    return {
        "hash": h,
        "hex": hex_val,
        "decimal": dec_val,
        "constante": constante,
        "rtp": rtp,
        "resultat": round(resultat,2),
        "tour_actuel": tour_actuel,
        "heure": heure,
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
    s_seed = st.text_input("Server Seed","ea147a04df73500c6a2d8bc508e47bd5452de266f1d82abed77335f")
with col2:
    c_seed = st.text_input("Client Seed","VVysLnEDMZEEC6Givsrv")

tab1,tab2 = st.tabs(["💎 MINES","📈 COSMOSX"])

with tab1:
    nb_mines = st.selectbox("Isan'ny Mines:",[1,2,3])
    tour_actuel = st.number_input("Tour Actuel:",min_value=1,value=8147129)
    if st.button("🚀 SCAN MINES"):
        schema,mines,safe_slots,probs,heure = mines_ultra_engine(s_seed,c_seed,nb_mines,tour_actuel)
        draw_styled_board(schema,mines)
        st.success(f"Diamants (fixe 5): {schema}")
        st.warning(f"Mines ({nb_mines}): {mines}")
        st.info(f"Safe Slots: {safe_slots}")
        st.info(f"Probabilités dynamique: {probs}")
        st.info(f"Heure kajy: {heure}")

with tab2:
    tour_actuel = st.number_input("Tour Actuel Cosmos:",min_value=1,value=8147129)
    if st.button("🌠 ANALYZE COSMOS"):
        res = cosmos_premium_engine(s_seed,c_seed,tour_actuel)
        m1,m2,m3,m4 = st.columns(4)
        m1.metric("MIN",f"{res['min']}x")
        m2.metric("MEAN",f"{res['mean']}x")
        m3.metric("MAX",f"{res['max']}x")
        m4.metric("ACCURACY",f"{res['accuracy']}%")
        st.success(f"Résultat: {res['resultat']}x")
        st.info(f"Tour Actuel {res['tour_actuel']} @ {res['heure']}")
        st.info(f"Tour 1 → {res['tour1']}")
        st.info(f"Tour 2 → {res['tour2']}")
        st.code(f"Hash: {res['hash']}\nHEX: {res['hex']}\nDecimal: {res['decimal']}\nConstante: {res['constante']}\nRTP: {res['rtp']}",language="bash")
