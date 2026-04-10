import streamlit as st
import hashlib
import random
import statistics
import time
from streamlit_autorefresh import st_autorefresh

# ---------------- CONFIG ----------------
st.set_page_config(page_title="HUBRIS V600 AI REAL LEARNING", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
.stApp {background: linear-gradient(135deg,#0f0f0f,#1c1c1c);color:#00ffcc;}
h1,h2,h3{text-align:center;color:#00ffcc;}

.stButton>button {
    background: linear-gradient(90deg,#00ffcc,#0066ff);
    color:white;border-radius:10px;height:45px;
}

.grid {
    display:grid;
    grid-template-columns:repeat(5,60px);
    gap:10px;justify-content:center;margin-top:20px;
}
.cell {
    width:60px;height:60px;
    display:flex;align-items:center;justify-content:center;
    border-radius:10px;font-size:22px;
}
.safe {background:#00ffcc;color:#000;box-shadow:0 0 15px #00ffcc;}
.risk {background:#ff0033;color:#fff;}
.empty {background:#222;border:1px solid #444;}
</style>
""", unsafe_allow_html=True)

# ---------------- MEMORY (AI LEARNING) ----------------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- HASH VERIFY ----------------
def verify_hash(server, client, nonce):
    h = hashlib.sha512(f"{server}:{client}:{nonce}".encode()).hexdigest()
    return h

# ---------------- CRASH ----------------
def crash(server, client, nonce):
    h = verify_hash(server, client, nonce)
    dec = int(h[-8:], 16) or 1
    return round((4294967295 * 0.97) / dec, 2)

# ---------------- COSMOS AI ----------------
def analyse_crash_series(server, client, nonce):
    results = [crash(server, client, nonce+i) for i in range(20)]
    
    avg = round(statistics.mean(results),2)
    variance = round(statistics.pvariance(results),2)

    # streak low
    streak_low = 0
    for r in reversed(results):
        if r < 2:
            streak_low += 1
        else:
            break

    signal = "🔴 SKIP"
    if streak_low >= 4 and avg > 1.8:
        signal = "🟢 PLAY"

    return results, avg, variance, streak_low, signal

# ---------------- DETECT ENTRY ----------------
def detect_best_entry(series):
    low = sum(1 for x in series if x < 2)
    high = sum(1 for x in series if x >= 2)

    if low > high:
        return "🔴 WAIT"
    return "🟢 ENTER"

# ---------------- MINES CORE ----------------
def mines_core(server, client, nonce):
    h = hashlib.sha512(f"{server}:{client}:{nonce}".encode()).digest()
    seed = int.from_bytes(h[:16], "big")
    rng = random.Random(seed)
    grid = list(range(25))
    rng.shuffle(grid)
    return grid

# ---------------- MINES AI ----------------
def mines_ai(server, client, nonce, mines_count):
    freq = {}
    history_maps = []

    for i in range(30):
        grid = mines_core(server, client, nonce+i)
        mines = grid[:mines_count]
        history_maps.append(mines)

        for m in mines:
            freq[m] = freq.get(m,0)+1

    ranking = sorted(range(25), key=lambda x: freq.get(x,0))
    
    safe5 = ranking[:5]
    best2 = ranking[:2]
    risky = ranking[-5:]

    confidence = round(100 - sum(freq.get(x,0) for x in safe5),2)

    return safe5, best2, risky, confidence, freq

# ---------------- DRAW GRID ----------------
def draw_grid(safe, risky):
    html = "<div class='grid'>"
    for i in range(25):
        if i in safe:
            html += "<div class='cell safe'>💎</div>"
        elif i in risky:
            html += "<div class='cell risk'>☠️</div>"
        else:
            html += "<div class='cell empty'></div>"
    html += "</div>"
    return html

# ---------------- LOGIN ----------------
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 HUBRIS ACCESS")
    pwd = st.text_input("Code", type="password")
    if st.button("ENTER"):
        if pwd == "2026":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Code diso")

else:
    st.title("🔥 HUBRIS V600 AI REAL LEARNING")

    tab1, tab2, tab3 = st.tabs(["🌌 COSMOS AI", "💎 MINES AI", "📘 GUIDE"])

    # ---------------- COSMOS ----------------
    with tab1:
        server = st.text_input("Server Seed")
        client = st.text_input("Client Seed")
        nonce = st.number_input("Nonce", min_value=1, value=1)

        if st.button("SCAN COSMOS"):
            if not server or not client:
                st.error("Seed required")
            else:
                series, avg, var, streak, signal = analyse_crash_series(server, client, nonce)
                entry = detect_best_entry(series)

                st.success(signal)
                st.info(entry)

                st.write("📊 Série Crash:", series)
                st.write(f"AVG: {avg} | VAR: {var} | STREAK LOW: {streak}")

                # learning
                st.session_state.history.append(avg)

    # ---------------- MINES ----------------
    with tab2:
        server_m = st.text_input("Server Seed", key="m1")
        client_m = st.text_input("Client Seed", key="m2")
        nonce_m = st.number_input("Nonce", min_value=1, value=1, key="m3")
        mines_count = st.slider("Nombre de mines", 1, 3, 3)

        if st.button("SCAN MINES"):
            if not server_m or not client_m:
                st.error("Seed required")
            else:
                safe, best2, risky, conf, freq = mines_ai(server_m, client_m, nonce_m, mines_count)

                st.markdown(draw_grid(safe, risky), unsafe_allow_html=True)

                st.success(f"💎 SAFE 5: {safe}")
                st.warning(f"🔥 BEST 2: {best2}")
                st.error(f"☠️ RISKY: {risky}")
                st.info(f"CONFIDENCE: {conf}%")

    # ---------------- GUIDE ----------------
    with tab3:
        st.markdown("""
### 📘 CONSIGNE CLIENT

### 🌌 COSMOS
- Miditra raha 🟢 PLAY
- Streak low ≥ 4
- AVG > 1.8

### 💎 MINES
- Mifidiana 2 amin'ny BEST 2 🔥
- SAFE 5 = support
- Aza misafidy risky ☠️

### 🎯 STRATEGY
- Bet = 1% bankroll
- Stop après 2 pertes
- Reset nonce

### ⚠️
- Tsy misy 100%
- AI = manampy décision
""")

    st_autorefresh(interval=10000, limit=None, key="refresh")
