import streamlit as st
import hashlib
import random
import statistics
import time

# ---------------- CONFIG ----------------
st.set_page_config(page_title="TITAN V400 GOD MODE", layout="wide")
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

# -------- SMART JUMP --------
def smart_jump(decimals):
    weights = [d % 10 for d in decimals[:5]]
    base_jump = sum(weights) // len(weights)

    volatility = max(decimals[:5]) - min(decimals[:5])

    if volatility > 1_000_000:
        jump = base_jump + 3
    elif volatility > 100_000:
        jump = base_jump + 2
    else:
        jump = base_jump + 1

    return max(2, jump)

# -------- COSMOS ADVANCED --------
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

    # 🔥 SMART JUMP
    jump = smart_jump(decimals)

    next_tour1 = nonce + jump
    next_tour2 = nonce + jump + 2
    next_tour3 = nonce + jump + 4  # TOUR 4

    # 🔥 SIGNAL
    trend = results[-3:]
    if trend[0] < trend[1] < trend[2]:
        signal = "📈 HAUSSE FORTE"
    elif trend[0] > trend[1] > trend[2]:
        signal = "📉 CHUTE"
    else:
        signal = "⚖️ NEUTRE"

    return {
        "results": results,
        "min": round(min_v, 2),
        "max": round(max_v, 2),
        "mean": round(mean_v, 2),
        "accuracy": accuracy,
        "next1": next_tour1,
        "next2": next_tour2,
        "next3": next_tour3,
        "signal": signal
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

# -------- DIAMOND SAFE --------
def mines_diamond_safe(server, client, nonce, mines_count):
    runs = [mines_engine(server, client, nonce+i, mines_count) for i in range(15)]

    freq = {}
    for r in runs:
        for x in r:
            freq[x] = freq.get(x, 0) + 1

    safe_score = sorted(range(25), key=lambda x: freq.get(x, 0))
    safe5 = safe_score[:5]

    risky = [k for k, v in freq.items() if v >= 5]

    confidence = round(100 - sum(freq.get(x,0) for x in safe5), 2)

    return risky, safe5, confidence

# ---------------- LOGIN SYSTEM ----------------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>🔒 TITAN LOGIN</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        pwd = st.text_input("Code :", type="password")
        if st.button("LOGIN"):
            if pwd == "2026":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("❌ Code diso")
else:
    st.title("🚀 TITAN V400 GOD MODE")

    if st.button("Déconnexion"):
        st.session_state.logged_in = False
        st.rerun()

    tab1, tab2, tab3 = st.tabs(["🌌 COSMOS", "💣 MINES", "📘 GUIDE"])

    # ---------- COSMOS ----------
    with tab1:
        st.subheader("COSMOS PRO")

        server = st.text_input("Server Seed")
        client = st.text_input("Client Seed")
        nonce = st.number_input("Nonce", min_value=1, value=1)

        if st.button("SCAN COSMOS"):
            if not server or not client:
                st.error("Seed required")
            else:
                with st.spinner("Analyse..."):
                    time.sleep(0.5)
                    data = cosmos_advanced(server, client, nonce)

                if data["accuracy"] < 55:
                    st.error("❌ SIGNAL FAIBLE - SKIP")
                    st.stop()

                st.write("Résultats:", data["results"])
                st.success(f"MIN: {data['min']} | MEAN: {data['mean']} | MAX: {data['max']}")
                st.info(f"ACCURACY: {data['accuracy']}%")

                st.success(f"Signal: {data['signal']}")

                st.warning(f"🎯 Tour 1: {data['next1']}")
                st.warning(f"🎯 Tour 2: {data['next2']}")
                st.warning(f"🔥 Tour 4: {data['next3']}")

    # ---------- MINES ----------
    with tab2:
        st.subheader("MINES DIAMOND SAFE")

        server_m = st.text_input("Server Seed", key="m1")
        client_m = st.text_input("Client Seed", key="m2")
        nonce_m = st.number_input("Nonce", min_value=1, value=1, key="m3")
        mines_count = st.slider("Mines", 1, 7, 3)

        if st.button("SCAN MINES"):
            if not server_m or not client_m:
                st.error("Seed required")
            else:
                with st.spinner("Analyse mines..."):
                    time.sleep(0.5)
                    grid = mines_engine(server_m, client_m, nonce_m, mines_count)
                    risky, safe, confidence = mines_diamond_safe(server_m, client_m, nonce_m, mines_count)

                st.write("Mines:", grid)
                st.error(f"Risky: {risky}")
                st.success(f"💎 SAFE 5: {safe}")
                st.info(f"Confidence: {confidence}%")

    # ---------- GUIDE ----------
    with tab3:
        st.markdown("""
### 🌌 COSMOS
- Accuracy > 55%
- Signal HAUSSE = jouer
- Tour 1 ou Tour 4

### 💣 MINES
- SAFE 5 = zones fiables
- Jouer 2-3 cases max

### ⚠️ STRATEGY
- Bet 1%
- Stop après 3 pertes
""")

    # SESSION LIMIT
    if "plays" not in st.session_state:
        st.session_state.plays = 0

    st.session_state.plays += 1

    if st.session_state.plays > 30:
        st.error("STOP SESSION 🚫")
        st.stop()
