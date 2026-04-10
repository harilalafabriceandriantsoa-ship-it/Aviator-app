import streamlit as st
import hashlib
import random
import numpy as np
import sqlite3
import json
from sklearn.ensemble import RandomForestClassifier

# ================= CONFIG =================
st.set_page_config(page_title="HUBRIS V1000 AI ENGINE", layout="wide")

# ================= DATABASE (V900 CORE) =================
conn = sqlite3.connect("hubris_ai.db", check_same_thread=False)
cursor = conn.cursor()

def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mine_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        server TEXT,
        client TEXT,
        nonce INTEGER,
        features TEXT,
        prediction INTEGER,
        label INTEGER
    )
    """)
    conn.commit()

init_db()

# ================= SESSION MEMORY =================
if "memory" not in st.session_state:
    st.session_state.memory = []

if "balance" not in st.session_state:
    st.session_state.balance = 1000

# ================= V800 COSMOS ENGINE =================
def crash(server, client, nonce):
    h = hashlib.sha512(f"{server}:{client}:{nonce}".encode()).hexdigest()
    dec = int(h[-8:], 16) or 1
    return round((4294967295 * 0.97) / dec, 2)

def cosmos_engine(server, client, nonce):
    series = [crash(server, client, nonce+i) for i in range(20)]
    avg = np.mean(series)

    streak = 0
    for r in reversed(series):
        if r < 2:
            streak += 1
        else:
            break

    signal = "SKIP"
    if streak >= 4 and avg > 1.8:
        signal = "PLAY"

    return series, avg, signal

# ================= V800 MINES CORE =================
def mines_core(server, client, nonce):
    h = hashlib.sha256(f"{server}:{client}:{nonce}".encode()).hexdigest()
    return [int(h[i:i+2], 16) for i in range(0, 20, 2)]

# ================= V900 FEATURE ENGINE =================
def features(server, client, nonce):
    h = hashlib.sha256(f"{server}:{client}:{nonce}".encode()).hexdigest()
    return [int(h[i:i+2], 16) for i in range(0, 20, 2)]

# ================= V900 ML TRAINING =================
def train_model():
    cursor.execute("SELECT features, label FROM mine_data")
    data = cursor.fetchall()

    if len(data) < 40:
        return None

    X = [json.loads(d[0]) for d in data]
    y = [d[1] for d in data]

    model = RandomForestClassifier(n_estimators=200)
    model.fit(X, y)
    return model

# ================= V1000 AI FUSION ENGINE =================
def mines_ai(server, client, nonce):
    risk = np.zeros(25)

    # Monte Carlo simulation
    for i in range(150):
        h = hashlib.sha256(f"{server}:{client}:{nonce+i}".encode()).hexdigest()
        idx = int(h[:2], 16) % 25
        risk[idx] += 1

    risk = risk / np.max(risk)

    model = train_model()

    ml_layer = np.zeros(25)

    if model:
        pred = model.predict([features(server, client, nonce)])[0]
        ml_layer[pred] = 1

    # V1000 fusion logic
    final_score = (1 - risk) * 0.6 + ml_layer * 0.2 + np.random.random(25) * 0.2

    rank = np.argsort(-final_score)

    safe = rank[:5]
    risky = rank[-5:]
    confidence = float(np.max(final_score) * 100)

    # learning memory (V900 self training)
    st.session_state.memory.append((features(server, client, nonce), safe[0]))

    return safe, risky, confidence

# ================= SAVE TRAINING DATA =================
def save_learning(server, client, nonce, pred):
    feat = features(server, client, nonce)

    cursor.execute("""
    INSERT INTO mine_data (server, client, nonce, features, prediction, label)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        server,
        client,
        nonce,
        json.dumps(feat),
        pred,
        pred  # simulation label
    ))

    conn.commit()

# ================= LOGIN =================
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 HUBRIS V1000 ACCESS")
    pwd = st.text_input("Password", type="password")

    if st.button("ENTER"):
        if pwd == "2026":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("WRONG PASSWORD")

    st.stop()

# ================= UI =================
st.title("🚀 HUBRIS V800 + V900 + V1000 AI SYSTEM")

tab1, tab2 = st.tabs(["🌌 COSMOS V800", "💎 MINES AI V1000"])

# ================= COSMOS =================
with tab1:
    s = st.text_input("Server Seed")
    c = st.text_input("Client Seed")
    n = st.number_input("Nonce", 1)

    if st.button("RUN COSMOS"):
        series, avg, signal = cosmos_engine(s, c, n)

        st.success(signal)
        st.write("AVG:", avg)
        st.write(series)

# ================= MINES AI =================
with tab2:
    s = st.text_input("Server M")
    c = st.text_input("Client M")
    n = st.number_input("Nonce M", 1)

    if st.button("RUN AI MINES"):
        safe, risky, conf = mines_ai(s, c, n)

        st.write("💎 SAFE:", list(safe))
        st.write("☠️ RISKY:", list(risky))
        st.success(f"CONFIDENCE: {conf:.2f}%")

        save_learning(s, c, n, safe[0])
