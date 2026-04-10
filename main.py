import streamlit as st
import hashlib
import random
import statistics
import numpy as np
import sqlite3
from sklearn.ensemble import RandomForestClassifier
from streamlit_autorefresh import st_autorefresh

# ================= CONFIG =================
st.set_page_config(page_title="HUBRIS AI CORE SYSTEM", layout="wide")

# ================= DATABASE (ONLY HISTORY SAFE) =================
conn = sqlite3.connect("hubris.db", check_same_thread=False)
cursor = conn.cursor()

def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        input TEXT,
        output TEXT
    )
    """)
    conn.commit()

init_db()

# ================= SESSION =================
if "memory" not in st.session_state:
    st.session_state.memory = []

if "balance" not in st.session_state:
    st.session_state.balance = 1000

if "login" not in st.session_state:
    st.session_state.login = False

if "role" not in st.session_state:
    st.session_state.role = "user"

# ================= LOGIN =================
def login(password):
    if password == "2026":
        st.session_state.login = True
        st.session_state.role = "admin"
    else:
        st.session_state.role = "user"

# ================= COSMOS ENGINE =================
def crash(server, client, nonce):
    h = hashlib.sha512(f"{server}:{client}:{nonce}".encode()).hexdigest()
    dec = int(h[-8:], 16) or 1
    return round((4294967295 * 0.97) / dec, 2)

def cosmos(server, client, nonce):
    results = [crash(server, client, nonce+i) for i in range(20)]
    avg = np.mean(results)

    streak = 0
    for r in reversed(results):
        if r < 2:
            streak += 1
        else:
            break

    signal = "SKIP"
    if streak >= 4 and avg > 1.8:
        signal = "PLAY"

    return results, avg, signal

def cosmos_signals(series):
    return ["🟢" if sum(x < 2 for x in series[i:i+5]) > 2 else "🔴"
            for i in range(0,15,5)]

# ================= MINES CORE =================
def mines_core(server, client, nonce):
    h = hashlib.sha512(f"{server}:{client}:{nonce}".encode()).digest()
    seed = int.from_bytes(h[:16], "big")
    rng = random.Random(seed)
    grid = list(range(25))
    rng.shuffle(grid)
    return grid

# ================= MONTE CARLO =================
def monte_carlo(server, client, nonce):
    scores = np.zeros(25)
    for i in range(200):
        h = hashlib.sha256(f"{server}:{client}:{nonce+i}".encode()).digest()
        idx = int.from_bytes(h[:2], "big") % 25
        scores[idx] += 1
    return scores / 200

# ================= FEATURES =================
def features(s, c, n):
    h = hashlib.sha256(f"{s}:{c}:{n}".encode()).hexdigest()
    return [int(h[i:i+2], 16) for i in range(0, 20, 2)]

# ================= TRAIN ML =================
def train_model():
    if len(st.session_state.memory) < 30:
        return None

    X = [m[0] for m in st.session_state.memory]
    y = [m[1] for m in st.session_state.memory]

    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)
    return model

# ================= MINES AI =================
def mines_ai(server, client, nonce):
    risk = monte_carlo(server, client, nonce)
    model = train_model()

    ml = np.zeros(25)

    if model:
        pred = model.predict([features(server, client, nonce)])[0]
        ml[pred] = 1

    final = (1 - risk) * 0.7 + ml * 0.3
    rank = np.argsort(-final)

    safe = rank[:5]
    risky = rank[-5:]
    conf = float(np.max(final) * 100)

    # learning memory
    st.session_state.memory.append((features(server, client, nonce), int(safe[0])))

    return safe, risky, conf

# ================= AUTO BET =================
def auto_bet(conf):
    bet = st.session_state.balance * 0.01

    if conf > 70:
        if random.random() > 0.5:
            st.session_state.balance += bet
            return "WIN"
        else:
            st.session_state.balance -= bet
            return "LOSE"
    return "SKIP"

# ================= LOGIN UI =================
if not st.session_state.login:
    st.title("🔐 HUBRIS ACCESS SYSTEM")
    pwd = st.text_input("Password", type="password")

    if st.button("ENTER"):
        login(pwd)
        st.rerun()

    st.stop()

# ================= MAIN UI =================
st.title("🚀 HUBRIS FULL AI ENGINE (CLEAN CORE)")

tab1, tab2, tab3 = st.tabs(["🌌 COSMOS", "💎 MINES", "🤖 AI"])

# ================= COSMOS =================
with tab1:
    s = st.text_input("Server")
    c = st.text_input("Client")
    n = st.number_input("Nonce", 1)

    if st.button("RUN COSMOS"):
        series, avg, signal = cosmos(s, c, n)
        st.success(signal)
        st.write(series)
        st.write("AVG:", avg)
        st.write("SIGNALS:", cosmos_signals(series))

# ================= MINES =================
with tab2:
    s = st.text_input("Server M")
    c = st.text_input("Client M")
    n = st.number_input("Nonce M", 1)

    if st.button("RUN MINES"):
        safe, risky, conf = mines_ai(s, c, n)
        st.write("SAFE 💎:", list(safe))
        st.write("RISKY ☠️:", list(risky))
        st.success(f"CONFIDENCE: {conf:.2f}%")

# ================= AI AUTO =================
with tab3:
    conf = st.slider("Confidence", 0, 100, 50)
    st.write("RESULT:", auto_bet(conf))
    st.write("BALANCE:", st.session_state.balance)

st_autorefresh(interval=10000)
