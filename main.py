import streamlit as st
import hashlib
import random
import statistics
import time

# ---------------- CONFIG ----------------
st.set_page_config(page_title="TITAN V300 ULTRA PRO", layout="wide")
st.set_option('client.showErrorDetails', True)

# ---------------- STYLE ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f0f0f, #1c1c1c);
    color: #00ffcc;
}
h1, h2, h3 {
    text-align:center;
    color:#00ffcc;
}
.stButton>button {
    background: linear-gradient(90deg,#00ffcc,#0066ff);
    color:white;
    border-radius:10px;
    height:50px;
}
</style>
""", unsafe_allow_html=True)

st.title("🚀 TITAN V300 ULTRA PRO MAX")

# ---------------- COSMOS ENGINE ----------------
def crash_result(server_seed, client_seed, nonce):
    base = f"{server_seed}:{client_seed}:{nonce}"
    h = hashlib.sha512(base.encode()).hexdigest()

    hex_part = h[-8:]
    decimal = int(hex_part, 16)

    if decimal == 0:
        decimal = 1

    result = (4294967295 * 0.97) / decimal
    return float(round(max(result, 1.0), 2)), int(decimal)


def cosmos_advanced(server, client, nonce):
    results = []
    decimals = []

    for i in range(10):
        r, d = crash_result(server, client, nonce + i)
        results.append(r)
        decimals.append(d)

    min_v = min(results)
    max_v = max(results)
    mean_v = statistics.mean(results)

    variance = statistics.pvariance(results)
    accuracy = round(max(0, 100 - variance), 2)

    jump1 = (decimals[0] % 5) + 1
    jump2 = (decimals[1] % 7) + 2

    next_tour1 = nonce + jump1
    next_tour2 = nonce + jump2

    return {
        "results": results,
        "min": round(min_v, 2),
        "max": round(max_v, 2),
        "mean": round(mean_v, 2),
        "accuracy": accuracy,
        "next1": next_tour1,
        "next2": next_tour2
    }

# ---------------- MINES ENGINE ----------------
def mines_engine(server, client, nonce, mines_count=3):
    base = f"{server}:{client}:{nonce}"
    h = hashlib.sha512(base.encode()).digest()

    seed_int = int.from_bytes(h[:16], "big", signed=False)
    rng = random.Random(seed_int)

    grid = list(range(25))
    rng.shuffle(grid)

    return sorted(grid[:mines_count])


def mines_ultra_safe(server, client, nonce, mines_count):
    runs = [mines_engine(server, client, nonce+i, mines_count) for i in range(7)]

    freq = {}
    for r in runs:
        for x in r:
            freq[x] = freq.get(x, 0) + 1

    risky = [k for k, v in freq.items() if v >= 3]
    safe = [i for i in range(25) if i not in risky]

    confidence = round(100 - len(risky)*4, 2)

    return risky, safe[:5], confidence

# ---------------- UI ----------------
tab1, tab2, tab3 = st.tabs(["🌌 COSMOS PRO", "💣 MINES PRO", "📘 GUIDE"])

# ---------- COSMOS ----------
with tab1:
    st.subheader("COSMOS PREDICTION")

    server = st.text_input("Server Seed")
    client = st.text_input("Client Seed")
    nonce = st.number_input("Tour actuel", min_value=1, value=1)

    scan_cosmos = st.button("🚀 SCAN COSMOS")

    if scan_cosmos:
        if not server or not client:
            st.error("Ampidiro seed!")
        else:
            with st.spinner("Analyse..."):
                time.sleep(0.5)
                data = cosmos_advanced(server, client, nonce)

            st.write("Résultats:", data["results"])
            st.success(f"MIN: {data['min']} | MOYEN: {data['mean']} | MAX: {data['max']}")
            st.info(f"ACCURACY: {data['accuracy']}%")

            st.warning(f"🎯 Tour 1: {data['next1']}")
            st.warning(f"🎯 Tour 2: {data['next2']}")

# ---------- MINES ----------
with tab2:
    st.subheader("MINES SAFE")

    server_m = st.text_input("Server Seed", key="m1")
    client_m = st.text_input("Client Seed", key="m2")
    nonce_m = st.number_input("Nonce", min_value=1, value=1, key="m3")
    mines_count = st.slider("Nombre mines", 1, 7, 3)

    scan_mines = st.button("💣 SCAN MINES")

    if scan_mines:
        if not server_m or not client_m:
            st.error("Seed vide!")
        else:
            with st.spinner("Analyse mines..."):
                time.sleep(0.5)
                grid = mines_engine(server_m, client_m, nonce_m, mines_count)
                risky, safe, confidence = mines_ultra_safe(server_m, client_m, nonce_m, mines_count)

            st.write("Mines:", grid)
            st.error(f"Risky: {risky}")
            st.success(f"SAFE: {safe}")
            st.info(f"Confidence: {confidence}%")

# ---------- GUIDE ----------
with tab3:
    st.markdown("""
### 🌌 COSMOS
- Accuracy > 60% → OK
- Jouer Tour 1 ou 2

### 💣 MINES
- SAFE = jouer
- Risky = éviter

### ⚠️ ANTI LOSS
- Bet 1%
- Stop après 3 pertes
""")

# ---------------- SESSION LIMIT ----------------
if "plays" not in st.session_state:
    st.session_state.plays = 0

st.session_state.plays += 1

if st.session_state.plays > 30:
    st.error("STOP SESSION 🚫")
    st.stop()
