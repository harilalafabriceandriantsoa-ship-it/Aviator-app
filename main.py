import streamlit as st
import hashlib, hmac, random, datetime, statistics

# --- CONFIGURATION ---
LOGIN_KEY = "2026"
st.set_page_config(page_title="TITAN V100 ULTRA STYLÉ", layout="wide")

# --- STYLE ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f0f0f, #1a1a1a);
        color: #00ffcc;
        font-family: 'Courier New', monospace;
    }
    h2, h3, h4 {
        color: #00ffcc;
        text-shadow: 0 0 10px #00ffcc;
    }
    .stButton>button {
        background: linear-gradient(90deg, #00ffcc, #0066ff);
        color: #fff;
        border-radius: 12px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        box-shadow: 0 0 20px #00ffcc;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #0066ff, #00ffcc);
        box-shadow: 0 0 30px #0066ff;
    }
    .mines-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 10px;
        max-width: 330px;
        margin: auto;
        padding: 20px;
    }
    .mine-cell {
        aspect-ratio: 1/1;
        background: #111;
        border: 1px solid #00ffcc44;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        border-radius: 12px;
        transition: 0.3s;
        color: #333;
    }
    .mine-cell:hover {
        transform: scale(1.1);
        box-shadow: 0 0 15px #00ffcc;
    }
    .cell-diamond {
        border: 2px solid #00d4ff !important;
        background: rgba(0, 212, 255, 0.3);
        color: #00d4ff;
        box-shadow: 0 0 30px #00d4ff;
    }
    .cell-mine {
        border: 2px solid #ff0044 !important;
        background: rgba(255, 0, 68, 0.3);
        color: #ff0044;
        box-shadow: 0 0 30px #ff0044;
    }
    </style>
""", unsafe_allow_html=True)

# --- COSMOS ENGINE ---
def cosmos_ultra_engine(hash_val, hex_val, tour_id, salt, heure=None, iters=200000):
    if heure is None:
        heure = datetime.datetime.now().strftime("%H:%M:%S")
    base = f"{hash_val}:{hex_val}:{tour_id}:{salt}:{heure}:COSMOSX_V100"
    h1 = hmac.new(b"COSMOS_CORE", base.encode(), hashlib.sha512).digest()
    for i in range(iters):
        h1 = hmac.new(h1, f"STEP_{i}".encode(), hashlib.sha512).digest()
    blake = hashlib.blake2b(h1).digest()
    sha3 = hashlib.sha3_256(blake).digest()
    sha384 = hashlib.sha384(sha3).digest()
    sha256 = hashlib.sha256(sha384).digest()
    final = bytes(a ^ b ^ c ^ d for a, b, c, d in zip(h1, blake, sha3, sha256))
    hex_out = final.hex()

    p_int = int(hex_out[:16], 16)
    offset = (p_int % 29) + (9 if salt == "T1" else 15)

    # Côte de prédiction
    constante = 4294967295
    rtp = 0.97
    dec_val = int(hex_out[-8:], 16)
    resultat = (constante * rtp) / dec_val
    if resultat < 1.0:
        resultat = 1.0
    resultat = round(resultat, 2)

    # Metrics (raikitra amin'ny seed)
    vals = [int(hex_out[i:i+4], 16)/10000 for i in range(0,20,4)]
    min_val = round(min(vals),2)
    max_val = round(max(vals),2)
    mean_val = round(statistics.mean(vals),2)
    accuracy = round((mean_val/max_val)*100,2)

    return {
        "tour": tour_id + offset,
        "cote": resultat,
        "min": min_val,
        "mean": mean_val,
        "max": max_val,
        "accuracy": accuracy,
        "salt": salt
    }

# --- MINES ENGINE (fixe 5 diamants foana, Résultat multiplier fotsiny) ---
def mines_ultra_engine(server_seed, client_seed, nonce, nb_mines, heure=None, iters=200000):
    if heure is None:
        heure = datetime.datetime.now().strftime("%H:%M:%S")
    base = f"{server_seed}:{client_seed}:{nonce}:{heure}:MINES_V100"
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
    for i in range(24, 0, -1):
        j = hash_int % (i + 1)
        grid[i], grid[j] = grid[j], grid[i]
        hash_int //= (i + 1)

    random.seed(int.from_bytes(h3[:16], "big") ^ nb_mines)
    random.shuffle(grid); random.shuffle(grid); random.shuffle(grid)

    schema = grid[:5]  # fixe 5 diamants
    mines = grid[5:5+nb_mines]

    # Résultat multiplier fotsiny
    base_result = (4294967295 * 0.97) / (int.from_bytes(h1[:8], "big") % 999999999)
    resultat = round(base_result / (nb_mines + 0.5), 2)
    if resultat < 1.0:
        resultat = 1.0

    return schema, mines, resultat

# --- LOGIN ---
st.markdown("<h2 style='text-align:center;'>🔐 TITAN V100 ULTRA STYLÉ</h2>", unsafe_allow_html=True)
admin_input = st.text_input("Enter Admin Code:", type="password", key="main_auth")

if admin_input == LOGIN_KEY:
    st.success("✅ TITAN V100 Activated.")
    tab1, tab2 = st.tabs(["🌌 COSMOSX", "💣 MINES ULTRA"])

    with tab1:
        st.markdown("##### 🌌 COSMOSX Prediction")
        h_v = st.text_input("Hash Value:", key="c_hash")
        x_v = st.text_input("Hex Value:", key="c_hex")
        t_v = st.number_input("Tour Actuel:", min_value=1, value=8147979, key="c_tour")
        c_h = st.text_input("Heure (HH:mm:ss):", value=datetime.datetime.now().strftime("%H:%M:%S"), key="c_time")
        if st.button("🚀 ANALYZE COSMOS"):
            if h_v and x_v:
                res1 = cosmos_ultra_engine(h_v, x_v, t_v, "T1", c_h)
                res2 = cosmos_ultra_engine(h_v, x_v, t_v, "T2", c_h)
                st.write(f"**T1 → Tour: {res1['tour']} | Côte: {res1['cote']}x | Min: {res1['min']}x | Moyen: {res1['mean']}x | Max: {res1['max']}x | Accuracy: {res1['accuracy']}%**")
                st.write(f"**T2 → Tour: {res2['tour']} | Côte: {res2['cote']}x | Min: {res2['min']}x | Moyen: {res2['mean']}
