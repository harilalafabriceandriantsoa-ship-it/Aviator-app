import streamlit as st
import hashlib
import random
import numpy as np
import sqlite3
import json
from sklearn.ensemble import RandomForestClassifier

# ================= CONFIG =================
st.set_page_config(page_title="HUBRIS V800 AI ML", layout="wide")

# ================= DATABASE =================
conn = sqlite3.connect("hubris_v800.db", check_same_thread=False)
cursor = conn.cursor()

def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mine_memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        features TEXT,
        prediction INTEGER,
        label INTEGER
    )
    """)
    conn.commit()

init_db()

# ================= SESSION =================
if "memory" not in st.session_state:
    st.session_state.memory = []

# ================= COSMOS ENGINE =================
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

# ================= FEATURES =================
def extract_features(server, client, nonce):
    h = hashlib.sha256(f"{server}:{client}:{nonce}".encode()).hexdigest()
    return [int(h[i:i+2], 16) for i in range(0, 20, 2)]

# ================= ML MODEL =================
def train_model():
    cursor.execute("SELECT features, label FROM mine_memory")
    data = cursor.fetchall()

    if len(data) < 30:
        return None

    X = [json.loads(d[0]) for d in data]
    y = [d[1] for d in data]

    model = RandomForestClassifier(n_estimators=150)
    model.fit(X, y)
    return model

# ================= MINES AI ENGINE =================
def mines_ai(server, client, nonce):
    # Monte Carlo risk simulation
    risk = np.zeros(25)
    for i in range(150):
        h = hashlib.sha256(f"{server}:{client}:{nonce+i}".encode()).hexdigest()
        idx = int(h[:2], 16) % 25
        risk[idx] += 1

    risk = risk / np.max(risk)

    # ML prediction
    model = train_model()
    ml_layer = np.zeros(25)

    features = extract_features(server, client, nonce)

    if model:
        try:
            pred = model.predict([features])[0]
            ml_layer[pred] = 1
        except:
            pass

    # AI fusion (final brain)
    final_score = (1 - risk) * 0.7 + ml_layer * 0.3

    ranking = np.argsort(-final_score)

    safe = ranking[:5]
    risky = ranking[-5:]

    confidence = float(np.max(final_score) * 100)

    # learning memory
    label = safe[0]

    cursor.execute("""
        INSERT INTO mine_memory (features, prediction, label)
        VALUES (?, ?, ?)
    """, (
        json.dumps(features),
        safe[0],
        label
    ))
    conn.commit()

    return safe, risky, confidence

# ================= LOGIN =================
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 HUBRIS V800 ACCESS")
    pwd = st.text_input("Password", type="password")

    if st.button("ENTER"):
        if pwd == "2026":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("WRONG PASSWORD")

    st.stop()

# ================= UI =================
st.title("🚀 HUBRIS V800 AI + ML ENGINE")

tab1, tab2 = st.tabs(["🌌 COSMOS", "💎 MINES AI"])

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

# ================= MINES =================
with tab2:
    s = st.text_input("Server")
    c = st.text_input("Client")
    n = st.number_input("Nonce", 1)

    if st.button("RUN MINES AI"):
        safe, risky, conf = mines_ai(s, c, n)

        st.write("💎 SAFE ZONES:", list(safe))
        st.write("☠️ RISK ZONES:", list(risky))
        st.success(f"CONFIDENCE: {conf:.2f}%")
