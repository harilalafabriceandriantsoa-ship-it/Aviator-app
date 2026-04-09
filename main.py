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

/* GRID 24 */
.grid-container {
    display: grid;
    grid-template-columns: repeat(6, 60px);
    gap: 10px;
    justify-content: center;
    margin-top: 20px;
}

.grid-item {
    width: 60px;
    height: 60px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
}

.safe {
    background: #00ffcc;
    color: black;
    box-shadow: 0 0 15px #00ffcc;
}

.risky {
    background: #ff4d4d;
    color: white;
    box-shadow: 0 0 15px red;
}

.neutral {
    background: #222;
    border: 1px solid #444;
}
</style>
""", unsafe_allow_html=True)

# ---------------- COSMOS ----------------
def crash_result(server_seed, client_seed, nonce):
    base = f"{server_seed}:{client_seed}:{nonce}"
    h = hashlib.sha512(base.encode()).hexdigest()

    hex_part = h[-8:]
    decimal = int(hex_part, 16)

    if decimal == 0:
        decimal = 1

    result = (4294967295 * 0.97) / decimal
    return float(round(max(result, 1.0), 2)), decimal


def generate_real_tours(decimals, base_nonce):
    tours = []

    for i in range(6):
        d = decimals[i]
        jump = ((d % 13) + (d % 7) + (d % 5)) // 2
        jump += (i * (d % 3 + 1))
        tours.append(base_nonce + jump)

    return list(set(tours))[:4]


def analyze_single_tour(server, client, nonce):
    results = []

    for i in range(6):
        r, _ = crash_result(server, client, nonce + i)
        results.append(r)

    mean_v = statistics.mean(results)
    variance = statistics.pvariance(results)

    accuracy = round(max(0, 100 - variance), 2)

    if mean_v > 2 and accuracy > 60:
        signal = "🟢 BON"
    elif mean_v > 1.5:
        signal = "🟡 MOYEN"
    else:
        signal = "🔴 DANGER"

    return {
        "nonce": nonce,
        "min": round(min(results), 2),
        "mean": round(mean_v, 2),
        "max": round(max(results), 2),
        "accuracy": accuracy,
        "signal": signal
    }


def cosmos_advanced(server, client, nonce):
    decimals = []

    for i in range(10):
        _, d = crash_result(server, client, nonce + i)
        decimals.append(d)

    tours = generate_real_tours(decimals, nonce)

    analyses = []
    for t in tours:
        analyses.append(analyze_single_tour(server, client, t))

    return analyses


# ---------------- MINES ----------------
def mines_engine(server, client, nonce, mines_count=3):
    base = f"{server}:{client}:{nonce}"
    h = hashlib.sha512(base.encode()).digest()

    seed_int = int.from_bytes(h[:16], "big", signed=False)
    rng = random.Random(seed_int)

    grid = list(range(24))  # 🔥 24 CASES
    rng.shuffle(grid)

    return sorted(grid[:mines_count])


def mines_diamond_safe(server, client, nonce, mines_count):
    runs = [mines_engine(server, client, nonce+i, mines_count) for i in range(12)]

    freq = {}
    for r in runs:
        for x in r:
            freq[x] = freq.get(x, 0) + 1

    safe_sorted = sorted(range(24), key=lambda x: freq.get(x, 0))
    safe5 = safe_sorted[:5]

    risky = [k for k, v in freq.items() if v >= 4]

    confidence = round(100 - sum(freq.get(x, 0) for x in safe5), 2)

    return risky, safe5, confidence


def draw_grid(safe, risky):
    html = "<div class='grid-container'>"

    for i in range(24):
        if i in safe:
            html += "<div class='grid-item safe'>💎</div>"
        elif i in risky:
            html += "<div class='grid-item risky'>💣</div>"
        else:
            html += "<div class='grid-item neutral'></div>"

    html += "</div>"
    return html


# ---------------- LOGIN ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h3>🔒 LOGIN</h3>", unsafe_allow_html=True)
    pwd = st.text_input("Code", type="password")

    if st.button("LOGIN"):
        if pwd == "2026":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("❌ Diso code")

else:
    st.title("🚀 TITAN V400 GOD MODE")

    if st.button("LOGOUT"):
        st.session_state.logged_in = False
        st.rerun()

    tab1, tab2, tab3 = st.tabs(["🌌 COSMOS", "💣 MINES", "📘 GUIDE"])

    # -------- COSMOS --------
    with tab1:
        server = st.text_input("Server Seed")
        client = st.text_input("Client Seed")
        nonce = st.number_input("Nonce", min_value=1, value=1)

        if st.button("SCAN COSMOS"):
            if not server or not client:
                st.error("Seed required")
            else:
                data = cosmos_advanced(server, client, nonce)

                for d in data:
                    st.markdown(f"### 🎯 TOUR → {d['nonce']}")
                    st.success(f"MIN: {d['min']} | MEAN: {d['mean']} | MAX: {d['max']}")
                    st.info(f"ACCURACY: {d['accuracy']}%")
                    st.warning(f"SIGNAL: {d['signal']}")

    # -------- MINES --------
    with tab2:
        server_m = st.text_input("Server Seed", key="m1")
        client_m = st.text_input("Client Seed", key="m2")
        nonce_m = st.number_input("Nonce", min_value=1, value=1, key="m3")
        m_count = st.slider("Mines", 1, 7, 3)

        if st.button("SCAN MINES"):
            if not server_m or not client_m:
                st.error("Seed required")
            else:
                risky, safe, conf = mines_diamond_safe(server_m, client_m, nonce_m, m_count)

                st.markdown(draw_grid(safe, risky), unsafe_allow_html=True)

                col1, col2, col3 = st.columns(3)
                col1.success(f"💎 SAFE: {len(safe)}")
                col2.error(f"💣 RISKY: {len(risky)}")
                col3.info(f"📊 CONF: {conf}%")

                if conf > 70:
                    st.success("🟢 SAFE ZONE")
                elif conf > 50:
                    st.warning("🟡 MOYEN")
                else:
                    st.error("🔴 DANGER")

    # -------- GUIDE --------
    with tab3:
        st.markdown("""
### 📘 GUIDE
- COSMOS: jouer si accuracy > 60%
- MINES: jouer SAFE uniquement
- 2 cases max
- STOP après 3 pertes
""")

    # -------- SESSION LIMIT --------
    if "plays" not in st.session_state:
        st.session_state.plays = 0

    st.session_state.plays += 1

    if st.session_state.plays > 30:
        st.error("STOP SESSION 🚫")
        st.stop()
