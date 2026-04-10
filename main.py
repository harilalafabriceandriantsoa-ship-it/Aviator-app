import streamlit as st
import hashlib
import random
import numpy as np
import sqlite3
import json
from sklearn.ensemble import RandomForestClassifier

# ================= CONFIG =================
st.set_page_config(page_title="HUBRIS V800 AI", layout="wide")

# ================= DATABASE SAFE =================
conn = sqlite3.connect("hubris_v800.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS mine_memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    features TEXT,
    prediction INTEGER,
    label INTEGER
)
""")
conn.commit()

# ================= SESSION =================
if "memory" not in st.session_state:
    st.session_state.memory = []

# ================= FEATURES =================
def features(server, client, nonce):
    h = hashlib.sha256(f"{server}:{client}:{nonce}".encode()).hexdigest()
    return [int(h[i:i+2], 16) for i in range(0, 20, 2)]

# ================= ML TRAIN =================
def train_model():
    cursor.execute("SELECT features, label FROM mine_memory")
    data = cursor.fetchall()

    if len(data) < 25:
        return None

    X = [json.loads(d[0]) for d in data]
    y = [d[1] for d in data]

    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)
    return model

# ================= IA ENGINE (V800 STRONG) =================
def mines_ai(server, client, nonce):
    feat = features(server, client, nonce)

    # Monte Carlo risk map
    risk = np.zeros(25)

    for i in range(120):
        h = hashlib.sha256(f"{server}:{client}:{nonce+i}".encode()).hexdigest()
        idx = int(h[:2], 16) % 25
        risk[idx] += 1

    risk = risk / (np.max(risk) + 1e-9)

    model = train_model()

    ml = np.zeros(25)

    if model is not None:
        try:
            pred = model.predict([feat])[0]
            ml[pred] = 1
        except:
            pass

    # AI fusion (INTELLIGENT SCORE)
    final = (1 - risk) * 0.7 + ml * 0.3

    rank = np.argsort(-final)

    safe = rank[:5]
    risky = rank[-5:]

    confidence = float(np.max(final) * 100)

    # ================= LEARNING =================
    label = safe[0]

    cursor.execute("""
        INSERT INTO mine_memory (features, prediction, label)
        VALUES (?, ?, ?)
    """, (
        json.dumps(feat),
        safe[0],
        label
    ))
    conn.commit()

    return safe, risky, confidence

# ================= COSMOS =================
def crash(server, client, nonce):
    h = hashlib.sha512(f"{server}:{client}:{nonce}".encode()).hexdigest()
    dec = int(h[-8:], 16) or 1
    return round((4294967295 * 0.97) / dec, 2)

def cosmos(server, client, nonce):
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

# ================= LOGIN (FIXED SAFE) =================
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
st.title("🚀 HUBRIS V800 AI ENGINE (STABLE ML)")

tab1, tab2 = st.tabs(["🌌 COSMOS", "💎 MINES AI"])

# ================= COSMOS =================
with tab1:
    s = st.text_input("Server Seed")
    c = st.text_input("Client Seed")
    n = st.number_input("Nonce", 1)

    if st.button("RUN COSMOS"):
        series, avg, signal = cosmos(s, c, n)

        st.success(signal)
        st.write("AVERAGE:", avg)
        st.write(series)

# ================= MINES =================
with tab2:
    s = st.text_input("Server")
    c = st.text_input("Client")
    n = st.number_input("Nonce", 1)

    if st.button("RUN MINES AI"):
        safe, risky, conf = mines_ai(s, c, n)

        st.write("💎 SAFE:", list(safe))
        st.write("☠️ RISK:", list(risky))
        st.success(f"CONFIDENCE: {conf:.2f}%")
